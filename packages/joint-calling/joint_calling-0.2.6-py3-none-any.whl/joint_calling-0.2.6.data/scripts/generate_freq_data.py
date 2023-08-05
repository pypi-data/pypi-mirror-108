#!python

"""
Generates input for random_forest.py:
- frequencies.ht
"""

import logging
from typing import Dict, List
import click
import hail as hl

from gnomad.resources.grch38.gnomad import (
    DOWNSAMPLINGS,
    POPS,
    POPS_TO_REMOVE_FOR_POPMAX,
    SEXES,
    SUBSETS,
)
from gnomad.sample_qc.sex import adjusted_sex_ploidy_expr
from gnomad.utils.annotations import (
    age_hists_expr,
    annotate_freq,
    bi_allelic_site_inbreeding_expr,
    faf_expr,
    get_adj_expr,
    pop_max_expr,
    qual_hist_expr,
)
from gnomad.utils.file_utils import file_exists
from gnomad.utils.vcf import index_globals

from joint_calling import utils, _version


logger = logging.getLogger('generate_freq_data')
logger.setLevel(logging.INFO)


@click.command()
@click.version_option(_version.__version__)
@click.option(
    '--out-ht',
    'out_ht_path',
    required=True,
    help='',
)
@click.option(
    '--mt',
    'mt_path',
    required=True,
    callback=utils.get_validation_callback(ext='mt', must_exist=True),
    help='path to the input MatrixTable',
)
@click.option(
    '--hard-filtered-samples-ht',
    'hard_filtered_samples_ht',
    required=True,
    help='Path to a table with only samples that passed filters '
    '(it\'s generated by sample QC)',
)
@click.option(
    '--meta-ht',
    'meta_ht',
    required=True,
    help='',
)
@click.option(
    '--existing-frequencies',
    'existing_frequencies_ht_path',
    help='Load allele frequencies from the previous version '
    'to avoid an extra frequency calculation',
)
@click.option(
    '--test',
    help='Runs a test on two partitions of chr20',
    is_flag=True,
)
@click.option(
    '--subset',
    help='Name of subset for which to generate frequency data',
    type=click.Choice(SUBSETS),
)
@click.option(
    '--bucket',
    'work_bucket',
    required=True,
    help='path to write intermediate output and checkpoints. '
    'Can be a Google Storage URL (i.e. start with `gs://`).',
)
@click.option(
    '--local-tmp-dir',
    'local_tmp_dir',
    help='local directory for temporary files and Hail logs (must be local).',
)
@click.option(
    '--overwrite/--reuse',
    'overwrite',
    is_flag=True,
    help='if an intermediate or a final file exists, skip running the code '
    'that generates it.',
)
def main(  # pylint: disable=too-many-arguments,too-many-locals,missing-function-docstring
    out_ht_path: str,
    mt_path: str,
    hard_filtered_samples_ht: str,
    meta_ht: str,
    existing_frequencies_ht_path: str,
    test: bool,
    subset: str,
    work_bucket: str,  # pylint: disable=unused-argument
    local_tmp_dir: str,
    overwrite: bool,
):
    local_tmp_dir = utils.init_hail(
        f'generate_frequency_data {("for " + subset) if subset else ""}', local_tmp_dir
    )

    if not overwrite and file_exists(out_ht_path):
        logger.info(f'{out_ht_path} exists, reusing')

    logger.info('Reading full sparse MT and metadata table...')
    mt = utils.get_mt(
        mt_path,
        hard_filtered_samples_to_remove_ht=hl.read_table(hard_filtered_samples_ht),
        meta_ht=hl.read_table(meta_ht),
        add_meta=True,
        release_only=True,
    )

    if test:
        logger.info('Filtering to two partitions on chr20')
        mt = hl.filter_intervals(mt, [hl.parse_locus_interval('chr20:1-1000000')])
        mt = mt._filter_partitions(range(2))  # pylint: disable=protected-access

    mt = hl.experimental.sparse_split_multi(mt, filter_changed_loci=True)

    if subset:
        mt = mt.filter_cols(mt.meta.subsets[subset])
        logger.info(
            f'Running frequency generation pipeline on {mt.count_cols()} '
            f'samples in {subset} subset...'
        )
    else:
        logger.info(
            f'Running frequency generation pipeline on {mt.count_cols()} samples...'
        )

    logger.info('Computing adj and sex adjusted genotypes...')
    mt = mt.annotate_entries(
        GT=adjusted_sex_ploidy_expr(mt.locus, mt.GT, mt.meta.sex_karyotype),
        adj=get_adj_expr(mt.GT, mt.GQ, mt.DP, mt.AD),
    )

    logger.info('Densify-ing...')
    mt = hl.experimental.densify(mt)
    mt = mt.filter_rows(hl.len(mt.alleles) > 1)

    # Temporary hotfix for depletion of homozygous alternate genotypes
    logger.info(
        'Setting het genotypes at sites with >1% AF (using v3.0 frequencies) '
        'and > 0.9 AB to homalt...'
    )
    if existing_frequencies_ht_path:
        freq_ht = hl.read_table(existing_frequencies_ht_path)
        freq_ht = freq_ht.select(AF=freq_ht.freq[0].AF)
        mt = mt.annotate_entries(
            GT=hl.cond(
                (freq_ht[mt.row_key].AF > 0.01)
                & mt.GT.is_het()
                & (mt.AD[1] / mt.DP > 0.9),
                hl.call(1, 1),
                mt.GT,
            )
        )

    logger.info('Generating frequency data...')
    if subset:
        mt = annotate_freq(
            mt,
            sex_expr=mt.meta.sex_karyotype,
            pop_expr=mt.meta.pop,
        )

        # NOTE: no FAFs or popmax needed for subsets
        mt = mt.select_rows('freq')

        logger.info(f'Writing out frequency data for {subset} subset...')
        mt.rows().write(out_ht_path, overwrite=True)

    else:
        mt = _compute_age_hists(mt)

        mt = annotate_freq(
            mt,
            sex_expr=mt.meta.sex_karyotype,
            pop_expr=mt.meta.pop,
            downsamplings=DOWNSAMPLINGS,
        )
        # Remove all loci with raw AC=0
        mt = mt.filter_rows(mt.freq[1].AC > 0)

        mt = _calc_inbreeding_coeff(mt)

        mt = _compute_filtering_af_and_popmax(mt)

        ht = _annotate_quality_merics_hist(mt)

        logger.info('Writing out frequency data...')
        ht.write(out_ht_path, overwrite=True)


def _compute_age_hists(mt: hl.MatrixTable) -> hl.Table:
    logger.info('Computing age histograms for each variant...')
    try:
        mt = mt.annotate_cols(age=hl.float64(mt.meta.age))
    except AttributeError:
        pass
    else:
        mt = mt.annotate_rows(
            **age_hists_expr(
                mt.adj,
                mt.GT,
                mt.age,
            )
        )
        # Compute callset-wide age histogram global
        mt = mt.annotate_globals(
            age_distribution=mt.aggregate_cols(
                hl.agg.hist(
                    mt.age,
                    30,
                    80,
                    10,
                )
            )
        )
    return mt


def _calc_inbreeding_coeff(mt: hl.MatrixTable) -> hl.MatrixTable:
    logger.info('Calculating InbreedingCoeff...')
    # NOTE: This is not the ideal location to calculate this, but added here
    # to avoid another densify
    mt = mt.annotate_rows(InbreedingCoeff=bi_allelic_site_inbreeding_expr(mt.GT))
    return mt


def _compute_filtering_af_and_popmax(mt: hl.MatrixTable) -> hl.Table:
    logger.info('Computing filtering allele frequencies and popmax...')
    faf, faf_meta = faf_expr(mt.freq, mt.freq_meta, mt.locus, POPS_TO_REMOVE_FOR_POPMAX)
    mt = mt.select_rows(
        'InbreedingCoeff',
        'freq',
        faf=faf,
        popmax=pop_max_expr(mt.freq, mt.freq_meta, POPS_TO_REMOVE_FOR_POPMAX),
    )
    mt = mt.annotate_globals(
        faf_meta=faf_meta, faf_index_dict=make_faf_index_dict(faf_meta)
    )
    mt = mt.annotate_rows(
        popmax=mt.popmax.annotate(
            faf95=mt.faf[
                mt.faf_meta.index(lambda x: x.values() == ['adj', mt.popmax.pop])
            ].faf95
        )
    )
    return mt


def _annotate_quality_merics_hist(mt: hl.MatrixTable) -> hl.Table:
    logger.info('Annotating quality metrics histograms...')
    # NOTE: these are performed here as the quality metrics histograms
    # also require densifying
    mt = mt.annotate_rows(qual_hists=qual_hist_expr(mt.GT, mt.GQ, mt.DP, mt.AD, mt.adj))
    ht = mt.rows()
    ht = ht.annotate(
        qual_hists=hl.Struct(
            **{
                i.replace('_adj', ''): ht.qual_hists[i]
                for i in ht.qual_hists
                if '_adj' in i
            }
        ),
        raw_qual_hists=hl.Struct(
            **{i: ht.qual_hists[i] for i in ht.qual_hists if '_adj' not in i}
        ),
    )
    return ht


def make_faf_index_dict(faf_meta: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Create a look-up Dictionary for entries contained in the filter allele frequency annotation array
    :param List of Dict faf_meta: Global annotation containing the set of groupings for each element of the faf array (e.g., [{'group': 'adj'}, {'group': 'adj', 'pop': 'nfe'}])
    :return: Dictionary of faf annotation population groupings, where values are the corresponding 0-based indices for the
        groupings in the faf_meta array
    :rtype: Dict of str: int
    """

    index_dict = index_globals(faf_meta, dict(group=['adj']))
    index_dict.update(index_globals(faf_meta, dict(group=['adj'], pop=POPS)))
    index_dict.update(index_globals(faf_meta, dict(group=['adj'], sex=SEXES)))
    index_dict.update(index_globals(faf_meta, dict(group=['adj'], pop=POPS, sex=SEXES)))

    return index_dict


if __name__ == '__main__':
    main()  # pylint: disable=E1120
