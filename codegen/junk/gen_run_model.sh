#!/bin/bash

source ~/dev/neurogen/codegen/venv/bin/activate

set -e
set -x

# CASE=sample_vgg
CASE=sample_few_layers

python3 gen_model.py --case=$CASE
cd $CASE/generated
nice python3 cli.py "$@"
