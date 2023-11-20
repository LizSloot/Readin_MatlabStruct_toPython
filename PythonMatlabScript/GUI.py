from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem, QComboBox
import sys
import numpy as np
import scipy.io

from MatToPy import MatToPyHDF5, MatToPySTD, MatToPy_Base

"""
This class handles the creation and data visualization in a GUI, similar to how Matlab represents the data. Implementation in progress,
HDF5 is not available yet, because of the way HDF5 is formatted
"""


class MatplotlibViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.load_button = QPushButton('Load MATLAB Data')
        self.load_button.clicked.connect(self.load_matlab_data)

        self.group_selector_label = QLabel('Select Group:')
        self.group_selector = QComboBox()

        self.data_label = QLabel('')

        self.table = QTableWidget()

        self.data = None

        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.group_selector_label)
        self.layout.addWidget(self.group_selector)
        self.layout.addWidget(self.data_label)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.show()
    
    def display_mat_data(self, data_dict):
        #Clear previous table contents
        self.table.clear()

        if data_dict is not None:
            #Iterate over the keys and values in data_dict
            for key, value in data_dict.items():
                #Create a new row in the table for each key-value pair
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)

                #Set the key in the first column
                key_item = QTableWidgetItem(str(key))
                self.table.setItem(row_position, 0, key_item)

                #Set the value in the second column
                value_item = QTableWidgetItem(str(value))
                self.table.setItem(row_position, 1, value_item)

    def load_matlab_data(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Open MATLAB Data File", "", "MATLAB Files (*.mat);;All Files (*)", options=options)
            print(f"File path: {file_path}")
        
            if file_path:
                mat_to_py_instance = MatToPy_Base()
                is_hdf5, data = mat_to_py_instance.is_hdf5_matlab_file(file_path)
                if is_hdf5:
                    hdf5_instance = MatToPyHDF5()
                    self.data = hdf5_instance.import_data(file_path)
                    data_dict = hdf5_instance.access_objects_in_dataset(self.data)

                    #Access the objects in 'Sub'
                    for item in data_dict.values():
                        print(item)
                    print("File path: ", file_path)
                else:
                    #Load standard MATLAB data
                    data_dict = MatplotlibViewer.load_standard_mat(file_path)
                    self.data = data_dict.get('StructTimeSmaller', None) #Note that StructTimeSmaller needs to be replaced with the actual name of the Matlab file on your machine
            
                if data_dict is not None:
                    #Display data
                    if hasattr(self.data, 'shape'):
                        self.data_label.setText(f'Data shape: {self.data.shape}')
                    else:
                        self.data.label.setText('Data shape: (Not applicable)')

                    #Populate table
                    if isinstance(self.data, np.ndarray):
                        self.table.setRowCount(self.data.shape[0])
                        self.table.setColumnCount(self.data.shape[1])

                        for i in range(self.data.shape[0]):
                            for j in range(self.data.shape[1]):
                                item = QTableWidgetItem(str(self.data[i, j]))
                                self.table.setItem(i, j, item)
                    else:
                        print("Data is not an array.")
                    
                    for key, value in data_dict.items():
                        print(f"Key: {key}, Value: {value}")
                else:
                    print("Data import failed!")
            
        except Exception as e:
            print(f"Error importing data: {e}")
            return None



    @staticmethod
    def load_standard_mat(file_path):
        try:
            data_dict = scipy.io.loadmat(file_path)
            return data_dict
        except Exception as e:
            print(f"Error loading standard MATLAB file: {e}")
            return None


    def extract_hdf5_data(self, hdf5_reference):
        #Print attributes and keys to understand the HDF5 structure
        print(f"Attributes: {dict(hdf5_reference.attrs)}")
        print(f"Keys: {list(hdf5_reference.keys())}")

        try:
            #Extract data based on the HDF5 structure
            extracted_data = hdf5_reference['sub_char'][:]
            return extracted_data
        except Exception as e:
            print(f"Error extracting HDF5 data: {e}")
            return None


    def display_group_data(self, group_index):
        if self.data is not None and group_index < len(self.data):
            group_data = self.data[group_index]
            #Display the group data in the table (this will need to be modified)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MatplotlibViewer()
    sys.exit(app.exec_())
