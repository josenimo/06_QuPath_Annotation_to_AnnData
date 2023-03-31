#!/bin/bash -ue
shopt -s nullglob
python /app/CommandSingleCellExtraction.py --image Exemplar001_subset--unmicst.ome.tif      --masks cell*.tif --output . --channel_names markers.csv
