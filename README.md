# QuPath_Annotation_to_AnnData
Annotate cells whether they are inside a QuPath annotation. 

Inputs:
QuPath geojson export of annotations.
Anndata object to annotate.

Output:
New column in adata.obs, called ROI, where the name of the QuPath Annotation will be, as a string.


Potential issues:
1. What about a cell being inside two ROIs? 


# QuPath_Annotation_to_Quantification_file
Running with Docker:
* inputs:
    * quantification file (csv) with columns: X_centroid, Y_centroid
    * geojson file with annotations
* outputs:
    * quantification file with new column: ROI
    * optional qc png files for each ROI
```
docker run \
    -v /path/to/inputs:/data \
    -v /path/to/outputs:/output \
    kbestak/ann_to_quant:0.1.0 \
    python run_annotation.py \
    --in-quantification ../data/quantification.csv \
    --in-geojson ../data/annotations.geojson \
    --out ../output/quantification.csv \
    --qc ../output/qc
```
Provided Dockerfile (replace CRLF with LF) is for building the image locally from the environment.yml file (replace CRLF with LF).
