#!/bin/bash

python bootstrap.sh
#conda-build -c conda-forge carnapy --python=3.7
conda-build -c conda-forge carnapy --python=3.8
#conda-build -c conda-forge carnapy --python=3.9

