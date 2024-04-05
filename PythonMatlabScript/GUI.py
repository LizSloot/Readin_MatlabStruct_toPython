import traceback
import numpy as np
import ast

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
from DataTreeViz import DataTreeViewer
import CalculationModule as cm

selected_array = np.array

class MainGUI(QWidget):
    try:
        def __init__(self):
            super().__init__()

            self.init_ui()

        def init_ui(self):
            self.setWindowTitle('Main GUI')
            self.setGeometry(100, 100, 400, 200)

            self.layout = QVBoxLayout()

            self.import_button = QPushButton('Import MATLAB Data')
            self.import_button.clicked.connect(self.import_matlab_data)

            self.layout.addWidget(self.import_button)
            self.setLayout(self.layout)

        # Call this function on the variable in the CalculationModule you select in the GUI in order to get its value and work with it

        def import_matlab_data(self):
            try:
                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getOpenFileName(self, "Open MATLAB Data File", "", "MATLAB Files (*.mat);;All Files (*)", options=options)

                if file_path:
                    # Create an instance of the DataTreeViewer with the imported data
                    tree_viewer = DataTreeViewer(file_path)
                    tree_viewer.tree.itemClicked.connect(self.on_item_clicked)
                    tree_viewer.exec_()  # Show the tree visualization window
            except Exception as e:
                print("Error in import_matlab_data", e)
                traceback.print_exc()
        # This function handles clicking on a value in the data tree viewer and prints it in the console. That way, the value can be used for later calculations
        def on_item_clicked(self, item, column):
            value_text = item.text(1).strip()
            print("Value text: ", value_text)
            try:
                # Type conversion because of the Matlab file
                #value_list = ast.literal_eval(value_text)
                value_array = np.array([float(x) for x in value_text[1:-1].split()])
                print("Value array: ", value_array) # This was used for debugging


                # After writing the functions you want in the CalculationModule, apply them here to the variable of your choice
                # As an example I included a simple array sum and a print statement with the value:
                result = cm.perform_sum(value_array)
                print("Test result: ", result)




            except Exception as e:
                print("Error in turning string to valid NumPy array!")
                traceback.print_exc()

    except Exception as e:
        print("Error launching Main GUI", e)
        traceback.print_exc()


if __name__ == '__main__':
    app = QApplication([])
    main_gui = MainGUI()
    main_gui.show()
    app.exec_()
