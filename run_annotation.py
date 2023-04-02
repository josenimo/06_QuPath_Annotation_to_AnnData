import geopandas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from os.path import abspath
from argparse import ArgumentParser as AP
import sys
import copy
import argparse
import os
from shapely.geometry import Point, LineString

# arg parser
def get_args():
    # Script description
    description="""Adds annotation column to quantification file from geojson file (QuPath export)."""

    # Add parser
    parser = AP(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

    # Sections
    inputs = parser.add_argument_group(title="Required Input", description="Path to required input file (quantification, geojson)")
    inputs.add_argument("--in-quantification", "-q", dest="quantification", action="store", required=True, help="File path to quantification file.")
    inputs.add_argument("--in-annotation", "-a", dest="annotation", action="store", required=True, help="File path to annotation geojson file")
    inputs.add_argument("--version", action="version", version="0.1.0")
    
    outputs = parser.add_argument_group(title="Output", description="Path to output file")
    outputs.add_argument("-o", "--out", dest="output", action="store", required=True, help="Path to output file")
    outputs.add_argument("--qc", dest="qc", action="store", required=False, help="Path to qc folder")

    arg = parser.parse_args()

    # Standardize paths
    arg.root = abspath(arg.quantification)
    arg.markers = abspath(arg.annotation)
    arg.output = abspath(arg.output)
    if arg.qc:
        arg.qc = abspath(arg.qc)
        if not os.path.exists(arg.qc):
            os.makedirs(arg.qc)
    return arg

def get_contour_type(df):
    df['Name'] = np.nan
    for i in df.index:
        tmp = df.classification[i].get('name')
        df.at[i, 'Name'] = tmp
    return df

def main(args):
    # Read in files
    annotation = geopandas.read_file(args.annotation)
    quantification = pd.read_csv(args.quantification)

    get_contour_type(annotation)
    print(annotation['Name'].unique())

    # initilize ROI column as unclassified
    quantification['ROI']="Unclassified"
    
    # get all cell points from quantification dataframe
    cellpoints = geopandas.points_from_xy(quantification.X_centroid, quantification.Y_centroid)
    
    #for each cell in the quantification file
    for cell_in_quantification in quantification.index: 
        #for each row in the ROI table
        for Qupath_Annotation in annotation.index:
            #if the cell is in the ROI
            if annotation.geometry[Qupath_Annotation].contains(cellpoints[cell_in_quantification]):
                #add the ROI name to the quantification file
                quantification.at[cell_in_quantification,'ROI'] = annotation.Name[Qupath_Annotation]   
    #save the quantification file
    quantification.to_csv(args.output, index=False)

    # QC
    if args.qc:
        for i in quantification.ROI.unique():
            tmp = quantification[quantification.ROI == i]
            plt.scatter(tmp.X_centroid, tmp.Y_centroid, label=i)
            plt.legend()
            plt.savefig(args.qc + f"/qc{i}.png")
            plt.close()

if __name__ == '__main__':
    # Read in arguments
    args = get_args()

    # Run script
    st = time.time()
    main(args)
    rt = time.time() - st
    print(f"Script finished in {rt // 60:.0f}m {rt % 60:.0f}s")