"""
This is the entry point of the app MatToPy tool written by Teodor Ticu. Make sure all modules needed are in the same directory before running
and make sure all necessary python packages are installed, otherwise the app might crash. The Readme on GitHub specifies all necessary packages.
This is an, as of yet, unoptimized version.
"""

import h5py
import numpy as np
import scipy.io
import matplotlib
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem
import sys

# from show_data import show_data, this is used mostly for testing and debugging the import
from MatToPy import MatToPy_Base, MatToPyHDF5, MatToPySTD
from GUI import MatplotlibViewer

app = QApplication(sys.argv)

viewer = MatplotlibViewer()

sys.exit(app.exec_())
