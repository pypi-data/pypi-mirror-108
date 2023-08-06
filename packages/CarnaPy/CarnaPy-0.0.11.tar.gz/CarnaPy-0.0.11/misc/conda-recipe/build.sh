#!/bin/bash

python bootstrap.py
conda-build -c conda-forge carnapy

