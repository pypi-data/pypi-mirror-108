# CorePytools package

CorePytools (CorePy) is a machine learning python package applied to data collected from geological samples of core. The primary focus of CorePy is to classify high resolution 
X-ray fluoresence data into chemofacies using unsupervised and supervised clustering tools. CorePy establishes a folder structure for input and output data. Visualizations are used to validate clustering results.

Corebox photographs can be cropped and used to visualized chemofacies results. Wireline log data can be upsampled and data integrated to chemofacies for upscaling  

# Installation
pip install corepytools

# Examples and data
The authors Github account has examples and datapackages that apply corepytools.


## About the authors

CorePy is being developed by Toti Larson at the University of Texas at Austin, Bureau of Economic Geology, Mudrocks Systems Research Laboratory (MSRL) research consortium.

1. **Toti E. Larson, Ph.D.** - Research Associate at the University of Texas at Austin. PI MSRL research consortium

2. **Esben Pedersen, M.S.** - Graduate student (graduated 2020) at the University of Texas at Austin. 

3. **Priyanka Periwal, Ph.D.** - Research Science Associate at the University of Texas at Austin. 

4. **J. Evan Sivil** - Research Science Associate at the University of Texas at Austin. 

5. **Ana Letícia Batista** - Undergraduate at Jackson State University (graduated 2020). 2020 Jackson School of Geosciences GeoForce Student

## Package Inventory
 
corepytools.py


## Package Dependencies

- os
- numpy
- pandas
- seaborn
- pickle
- glob
- matplotlib.pyplot
- seaborn as sns
- sklearn.preprocessing import StandardScaler
- sklearn.decomposition import PCA
- sklearn.cluster import KMeans
- matplotlib.patheffects
- from PIL import Image

# Notes

Install corepytools using **pip install corepytools**
Follow over to the authors Github account to download example Python scripts that use corepytools


# Folder structure
corepytools

    |-LICENSE.txt         **MIT**

    |-README.md           **edited in markdown**

    |-setup.py            **name=corepy-tools, package=src, python module=corepytools**

    |-src

        |-corepytools    **contains functions**
    
        |-__init__.py     ** empty**


