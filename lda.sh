#!/bin/sh
set -e

MALLET=$HOME/src/mallet-2.0.8
INPDIR=.
OUTDIR=lda

mkdir $OUTDIR

time $MALLET/bin/mallet import-file \
    --input $INPDIR/chunkedcorpus.txt \
        --label 1 \
        --name 2 \
        --keep-sequence \
        --output $OUTDIR/corpus.mallet

time $MALLET/bin/mallet train-topics \
        --input $OUTDIR/corpus.mallet \
        --num-topics 100 \
        --num-threads 10 \
        --num-iterations 5000 \
        --num-top-docs 10000 \
        --optimize-interval 50 \
        --output-state $OUTDIR/topics.state.gz \
        --output-model $OUTDIR/model.mallet \
        --inferencer-filename $OUTDIR/inferencer.mallet \
        --evaluator-filename $OUTDIR/evaluator.mallet \
        --output-topic-docs $OUTDIR/topicdocs.txt \
        --output-doc-topics $OUTDIR/doctopics.txt \
        --output-topic-keys $OUTDIR/topickeys.txt \
        --xml-topic-phrase-report $OUTDIR/topicphrase.xml \
        --xml-topic-report $OUTDIR/topicreport.xml \
        --diagnostics-file $OUTDIR/diagnostics.xml \
        --word-topic-counts-file $OUTDIR/wordtopiccounts.txt \
        --topic-word-weights-file $OUTDIR/topicwordweights.txt

