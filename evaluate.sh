#!/usr/bin/env bash

# Taken from https://github.com/wikilinks/neleval/blob/master/scripts/run_tac15_evaluation.sh

set -e

usage="Usage: $0 GOLD_FILE SYSTEMS_FILE OUT_DIR NUM_JOBS [-x EXCLUDED_SPANS]"

if [ "$#" -lt 4 ]; then
    echo $usage
    exit 1
fi

cleanup_cmd='OFS="\t" {} $6 == "TTL/NAM" {$6 = "PER/NOM"} ($6 ~ /NAM$/ || ($6 ~ /PER.NOM$/ && $1 ~ /^ENG/)) && $1 != "CMN_NW_001331_20150702_F00100023"'

gtab=$1; shift # gold standard link annotations (tab-separated)
sysfile=$1; shift # file containing output from systems
outdir=$1; shift # directory to which results are written
jobs=$1; shift # number of jobs for parallel mode

SCR=`dirname $0`


# CONVERT GOLD TO EVALUATION FORMAT
echo "INFO Converting gold to evaluation format.."
# XXX: "combined" is a misnomer in tac15. Should be neleval? But existing scripts depend on this extension.
gold=$outdir/gold.combined.tsv
options=$@
python -m neleval prepare-tac15 $gtab $options | awk -F'\t' "$cleanup_cmd" > $gold

# convert systems to evaluation format
echo "INFO converting systems to evaluation format.."
sys_file_name=$(basename -- "$sysfile")
my_results=$outdir/$sys_file_name.combined.tsv
python -m neleval prepare-tac15 $sysfile $options | awk -F'\t' "$cleanup_cmd" > $my_results

# EVALUATE
echo "INFO Evaluating systems.."
python -m neleval evaluate -m all -f tab -g $gold $my_results > $outdir/results.evaluation


echo "INFO Creating summary of results"
echo -e "right\twrong\tright\texpcted\t" > $outdir/summary.evaluation
grep -e 'measure'  $outdir/results.evaluation >> $outdir/summary.evaluation

filter="$(grep -e strong_mention_match $outdir/results.evaluation)"
echo -e "$filter\tDetected mentions with right span" >> $outdir/summary.evaluation

filter="$(grep -e strong_link_match $outdir/results.evaluation)"
echo -e "$filter\tRight linked mentions only" >> $outdir/summary.evaluation

filter="$(grep -e strong_nil_match $outdir/results.evaluation)"
echo -e "$filter\tRight NIL detection only" >> $outdir/summary.evaluation

filter="$(grep -e strong_all_match $outdir/results.evaluation)"
echo -e "$filter\tRight linked mentions and NIL detections" >> $outdir/summary.evaluation

filter="$(grep -e entity_match $outdir/results.evaluation)"
echo -e "$filter\tRight Micro-averaged document-level set-of-links (repeated links count only once)" >> $outdir/summary.evaluation
