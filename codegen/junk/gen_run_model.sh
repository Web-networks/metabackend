#!/bin/bash

source ~/dev/neurogen/codegen/venv/bin/activate

if [ "$@" = "ALL" ]; then
  set -e
  set -x

  for CASE in sample_*; do
    python3 gen_model.py --case=$CASE
  done

  exit 0
fi

set -e
set -x

CASE="$1"
shift

python3 gen_model.py --case=$CASE
cd $CASE/generated
nice python3 cli.py "$@"
