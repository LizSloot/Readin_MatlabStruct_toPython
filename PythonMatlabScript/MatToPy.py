#this module handles the imports of data in either HDF5 or standard MAT format
import h5py 
import scipy
import numpy as np


from collections import deque
from os import name


class MatToPy_Base:
        def __init__(self) -> None:
            self.name = str #name of the variable in which the dataset is saved
            self.path = ""  #path to the .mat file
            self.data = []  #values inside the imported dataset
        
            
        def is_hdf5_matlab_file(self, file_path):
            """
            Check if an imported Matlab file is in standard .mat format or if it is HDF5 format. Useful for debugging and 
            when instantiating the dataset object
            
            Args: 
                self.path (str): The path to the Matlab data file.
            Returns:
                Prints out a text message depending on what type of file format python detected.
            """
            try:
                print(f"Trying to open file: {file_path}")
                with h5py.File(file_path, 'r') as f:
                    print("HDF5 file!")
                    return True, None
            except OSError:
                print("Not an HDF5 file!")
                return False, None
            except Exception as e:
                print(f"Error opening file: {e}")
                return False


        def import_data(self, file_path):
            """
            Handles the data import from Matlab into Python. Checks for format type of the data and populates self.data accordingly.
            
            Args:
                self.path (str): The path to the Matlab data file.
                self.data (python collection or h5py dict): The dataset imported form Matlab.
            Returns:
                Loads the dataset into memory or throws an Exception if there is an error.
            """
            raise NotImplementedError("Subclasses must implement import_data")            
            
        
            
        
        # # Example usage:
        # matlab_file_path = 'your_data_file.mat'  # Replace with the path to your MATLAB data file
        # field_to_find = 'Age'                   # Replace with the name of the field you want to retrieve

        # field_value, field_position = get_field_value_and_position(matlab_file_path, field_to_find)
        # if field_value is not None:
        #     print(f"{field_to_find} = {field_value}")
        #     print(f"Position of {field_to_find} = {'.'.join(map(str, field_position))}")

        
class MatToPySTD(MatToPy_Base):
    def import_data(self, file_path):
        try:
            print(f"Attempting to open file: {file_path}")
            self.data = scipy.io.loadmat(file_path)
            print(f"Keys in Matlab file: {self.data.keys()}")
            return self.data
        except Exception as e:
            print(f"Error importing data from .mat file: {e}")
            return None
        
    def get_field_value_and_position_stdmat(self, field_name):
        """
        Get the value of a specific field from a Matlab data file and its position.

        Args:
            self.path (str): The path to the Matlab data file.
            field_name (str): The name of the field to retrieve.

        Returns:
            A tuple containing the field value and its position as a list of indices.
            If the field is not found, returns (None, None).
        """
        try:
            # Initialize a queue for BFS traversal of the data dictionary
            queue = deque([(self.data, [])])

            while queue:
                current_data, current_path = queue.popleft()

                for key, value in current_data.items():
                    new_path = current_path + [key]

                    # If the current key matches the field name, return its value and position
                    if key == field_name:
                        return value, new_path

                    # If the current value is a nested dictionary, add it to the queue for traversal
                    if isinstance(value, dict):
                        queue.append((value, new_path))

            # Field not found
            print(f"Field '{field_name}' not found in the MATLAB data.")
            return None, None

        except Exception as e:
            print(f"Error loading MATLAB data file: {e}")
            return None, None
        

    def explore_mat_structure_and_access_data(self, target_group_name):
        try:
            
            # Check if the target group or variable exists
            if target_group_name in self.data:
                target_data = self.data[target_group_name]

                # If it's a dictionary, it may represent a group, so we explore its keys
                if isinstance(target_data, dict):
                    print(f"Contents of group '{target_group_name}':")
                    for key in target_data:
                        print(f"  - {key}")

                # If it's not a dictionary, it may be a variable with data
                else:
                    print(f"Data in variable '{target_group_name}':")
                    print(target_data)

            else:
                print(f"Group or variable '{target_group_name}' not found in file!")

        except FileNotFoundError:
            print(f"MAT file not found at path: {self.path}")
        except Exception as e:
            print(f"Error loading or exploring MAT file: {e}")


    def access_matlab_subfield(self, field_name, subfield_name):
        """
        Access the subfields of the Matlab struct. Implementation still in progress, but the idea is to be able to click on each subfield
        and see the data underneath in the window
        Args: Name of the main field and of the subfield.
        Returns: subfield variable of type passed, depending on the data format imported
        """
        try:
            # Load the .mat file into a Python dictionary
            data_dict = scipy.io.loadmat(self.path)

            # Access the field
            field = data_dict[field_name]

            # Access the subfield
            subfield = field[subfield_name]

            return subfield
        except KeyError:
            print(f"Field '{field_name}' or subfield '{subfield_name}' not found in the .mat file.")
            return None
        except Exception as e:
            print(f"Error accessing subfield: {e}")
            return None
        
        if subfield_data is not None:
            # Now you can access specific subfields like P_IC_cnt
            variables = subfield_data[subfield_name]
            print(f"Data in '{field_name}.{subfield_name}.P_IC_cnt':")
            print(P_IC_cnt_data)
        


class MatToPyHDF5(MatToPy_Base):

    @staticmethod
    def access_objects_in_dataset(dataset):
        sub_data = {}
        for i, obj_ref in enumerate(dataset):
            sub_data[i] = obj_ref
        return sub_data

    def import_data(self, file_path):
        try:
            print(f"Attempting to open file: {file_path}")
            with h5py.File(file_path, 'r') as hf:
                # Print the keys in the HDF5 file
                print("Keys in HDF5 file:", list(hf.keys()))

                # Now, attempt to access the dataset 'Sub'
                dataset_name = 'Sub'  # Update with your actual dataset name
                if dataset_name in hf:
                    # Access the object references
                    object_references = hf[dataset_name][()]
                    print(f"Object references in dataset '{dataset_name}':")
                    print(object_references)

                    # Return the dataset directly
                    return object_references
                else:
                    print(f"Dataset '{dataset_name}' not found in file!")
                    return None
        except Exception as e:
            print(f"Error importing data from HDF5 file: {e}")
            return None

        
    def get_field_value_and_position_HDF5(self, field_name):
        try:
            with h5py.File(self.path, 'r') as hf:
                if field_name in hf:
                    return hf[field_name][()]
                else:
                    print(f"Field '{field_name}' not found in file!")
                    return None
        except Exception as e:
            print(f"Error opening HDF5 data file : {e}")
            return None

    def explore_hdf5_structure_and_access_data(self, group, target_group_name):
        try:
            if target_group_name in group:
                target_data = group[target_group_name]
                
                if isinstance(target_data, h5py.Group):
                    print(f"Contents of group: '{target_group_name}': ")
                    for key in target_data:
                        print(f" - {key}")
                elif isinstance(target_data, h5py.Dataset):
                    data = target_data[()] #Access the data in the dataset
                    print(f"Data in dataset '{target_group_name}':")
                    print(data)
                    return data
                else:
                    print(f"Group or dataset '{target_group_name}' not found in file!")
        except Exception as e:
            print(f"Error exploring or accessing HDF5 data: {e}")
        return None
        

#TODO: Test all of the above, see how it works. Try for BOTH file types and for longer inputs (so first subject ankle angle in x dimension all stried for instance)
#      Idea: See how many subfields each field has and make it possible to take inputs from all of those (eg: first subject -> Left side -> ankle angle -> x direction -> all strides)
#      and print out exactly what that is. Alternatively, try making a GUI with drop-down boxes (I think this is the best choice for people not used to python console). 
