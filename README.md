# PythonMatlabScript

The MatToPy tool is written and maintained by Teodor Ticu, a student assistant at the University of Heidelberg for the Heidelberg Center for Motion Research, HeiAGE project.

This is a tool that handles imports of Matlab data (a so-called .MAT structure) into Python to support further analysis in Python. 
The code is created in the context of and tested with data from "van Criekinge, A full-body motion capture gait dataset of 138 able-bodied adults across the life span and 50 stroke survivors. Nature Data (2023)". These datasets are the standard .mat files (not HDF5). if you use this script for other datasets, you can use a method in MatToPy module to check whether the Matlab file you are working with is HDF5. This type is not yet supported.

While .MAT structures are easy to work and interact with in Matlab, they are not created or support in Python. To support those people who prefer to perform their analysis of the dataset in Python, this script help reading in the MAT data in Python and gives examples of how to interact with the data. 

In order to make the data visualization easier, a GUI appears. In this GUI you can load the data from your machine and you will be able to see what you imported. The console prints both messages and the data as-is in the background, in order to be able to check if the import worked successfully.
