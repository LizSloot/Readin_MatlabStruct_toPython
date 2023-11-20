#this function is here only to double-check the import, right now it doesn't work for HDF5 files


import numpy as np

def show_data(struct):
    
    new_struct = struct['Sub']
    print(new_struct.dtype.names) #prints fields in the struct 'Sub' ie events, meas_char ...
    
    for field_name in new_struct.dtype.names:
        field_value = new_struct[field_name]
        print(f'Field: {field_name}')
        print(f'Data Type: {type(field_value)}')
        print(field_value)
        print("====================")
