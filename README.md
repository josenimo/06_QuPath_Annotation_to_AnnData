# QuPath_Annotation_to_AnnData
Annotate cells whether they are inside a QuPath annotation. 

Inputs:
QuPath geojson export of annotations.
Anndata object to annotate.

Output:
New column in adata.obs, called ROI, where the name of the QuPath Annotation will be, as a string.


Potential issues:
1. What about a cell being inside two ROIs? 
