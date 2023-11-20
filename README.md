# PythonMatlabScript

The MatToPy tool is written and maintained by Teodor Ticu, Bachelor student at the University of Heidelberg in support of the Heidelberg Center for Motion Research.

This is a tool that handles imports of Matlab data in python. It is still a work in progress, since for now the data can't be interacted with. In order to make the data visualization easier, a GUI appears. In this GUI you can load the data from your machine and you will be able to see what you imported. The console prints both messages and the data as-is in the background, in order to be able to check if the import worked successfully.
As of right now, only standard .mat files work seamlessly for this, since HDF5 is a little odd and requires more tailoring (this is a TODO). There is a method in the MatToPy module which helps you check whether the Matlab file you are working with is HDF5 or Standard Matlab. 
