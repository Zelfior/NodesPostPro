from nodes.generic_node import GenericNode, PortValueType

import pandas as pd
import os


class LoadFileNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Pandas'

    # initial default node name.
    NODE_NAME = 'Read CSV file'

    def __init__(self):
        super(LoadFileNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output DataFrame', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Columns names', PortValueType.LIST)

        #   create QLineEdit text input widget for the file path
        self.button = self.add_button_widget("Browse file")
        self.button.set_link(self.get_file_name)

        file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        example_path = os.path.join(file_path,'test.csv')
        self.add_text_input('Filename', 'File name', example_path, tab='widgets')

        self.add_label("Information")


    def check_inputs(self):
        print("File found", os.path.isfile(self.get_property("Filename")))

        #   we set in the "is_valid" property a boolean saying if a file is present at the given path
        if os.path.isfile(self.get_property("Filename")):
            self.set_property("is_valid", True)
        else:
            self.set_property("is_valid", False)
            self.change_label("Information", "No file at the given path.", True)

    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Output DataFrame").set_property(pd.read_csv(self.get_property("Filename"), sep = ","))
        self.get_output_property("Columns names").set_property(list(self.get_output_property("Output DataFrame").get_property().columns))

        column_count = len(self.get_output_property("Output DataFrame").get_property().columns)
        lines_count = len(self.get_output_property("Output DataFrame").get_property())
        
        self.change_label("Information", "Columns : "+str(column_count)+", lines : "+str(lines_count), False)










        

class GetColumnSelectorNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Pandas'

    # initial default node name.
    NODE_NAME = 'Get column selector'

    def __init__(self):
        super(GetColumnSelectorNode, self).__init__()

        #   Create input port for input dataframe
        self.add_custom_input('Input DataFrame', PortValueType.PD_DATAFRAME)

        #   Create output ports for :
        #       The output dataframe corresponding to the given column
        #       The selected column name
        self.add_custom_output('Output DataFrame', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Selected column name', PortValueType.STRING)

        #   Create the QComboBox menu to select the desired column.
        self.add_combo_menu('Column name', 'Column name', items=[])

        self.add_label("Information")
        self.change_label("Information", "No information", False)

    def check_inputs(self):
        #   Checks if the Input DataFrame is:
        #       -   plugged
        #       -   defined (if the previous node has its outputs defined)
        #       -   is a pandas DataFrame
        

        is_valid, message = self.is_input_valid("Input DataFrame")

        self.set_property("is_valid", is_valid)

        if not is_valid:
            self.change_label("Information", message, True)

    
    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       -   If the combo widget labels are different from the DataFrame columns, we update the combo widget
        #       -   The "Output DataFrame" output becomes the column asked as a DataFrame

        if self.get_value_from_port("Input DataFrame").is_iterated():
            if list(self.get_value_from_port("Input DataFrame").get_iterated_property()[0].columns) != self.view.widgets["Column name"].all_items():
                self.view.widgets["Column name"].clear()
                self.view.widgets["Column name"].add_items(list(self.get_value_from_port("Input DataFrame").get_property().columns))

            input_property = self.get_value_from_port("Input DataFrame").get_iterated_property()

            self.set_output_property('Output DataFrame', [input_property[i][self.get_property("Column name")].to_frame() for i in range(len(input_property))], True)
            self.set_output_property('Selected column name', self.get_property("Column name"), False)
            
            self.change_label("Information", "Lines : "+str(len(self.get_output_property("Output DataFrame").get_property()[0])+" x "+str(len(self.get_output_property("Output DataFrame").get_property()))), False)

        else:
            if list(self.get_value_from_port("Input DataFrame").get_property().columns) != self.view.widgets["Column name"].all_items():
                self.view.widgets["Column name"].clear()
                self.view.widgets["Column name"].add_items(list(self.get_value_from_port("Input DataFrame").get_property().columns))

            self.set_output_property('Output DataFrame', self.get_value_from_port("Input DataFrame").get_property()[self.get_property("Column name")].to_frame(), False)
            self.set_output_property('Selected column name', self.get_property("Column name"), False)
            
            self.change_label("Information", "Lines : "+str(len(self.get_output_property("Output DataFrame").get_property())), False)

    def reset_outputs(self):
        super(GetColumnSelectorNode, self).reset_outputs()

        #   If this node is reseted, the combo widget also needs to be cleared
        self.view.widgets["Column name"].clear()
        self.view.widgets["Column name"].add_items([])







class GetColumnNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Pandas'

    # initial default node name.
    NODE_NAME = 'Get column from name'

    def __init__(self):
        super(GetColumnNode, self).__init__()

        #   Create input port for input dataframe
        self.add_custom_input('Input DataFrame', PortValueType.PD_DATAFRAME)
        self.add_twin_input('Column name', PortValueType.STRING)

        #   Create output ports for :
        #       The output dataframe corresponding to the given column
        #       The selected column name
        self.add_custom_output('Output DataFrame', PortValueType.PD_DATAFRAME)

        self.add_label("Information")
        self.change_label("Information", "No information", False)

    def check_inputs(self):
        #   Checks if the Input DataFrame is:
        #       -   plugged
        #       -   defined (if the previous node has its outputs defined)
        #       -   is a pandas DataFrame
        
        is_dataframe_valid, message = self.is_input_valid("Input DataFrame")

        if not is_dataframe_valid:
            self.change_label("Information", message, True)
            self.set_property("is_valid", False)

        if is_dataframe_valid:
            is_dataframe_valid, message = self.is_twin_input_valid("Column name")

            if is_dataframe_valid:
                if self.get_twin_input("Column name").get_property() in self.get_value_from_port("Input DataFrame").get_property().columns:
                    is_col_name_valid = True
                else:
                    is_col_name_valid = False
                    self.change_label("Information", "Given name is not in the dataframe columns.", True)
            else:
                is_col_name_valid = False
            
            self.set_property("is_valid", is_col_name_valid)


            if is_col_name_valid:
                if self.get_twin_input("Column name").is_iterated() and self.get_value_from_port("Input Dataframe").is_iterated():
                    if len(self.get_twin_input("Column name").get_iterated_property()) != len(self.get_twin_input("Input Dataframe").get_iterated_property()):

                        self.set_property("is_valid", False)
                        self.change_label("Information", "Inputs should use the same iterator.", True)

    
    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       -   If the combo widget labels are different from the DataFrame columns, we update the combo widget
        #       -   The "Output DataFrame" output becomes the column asked as a DataFrame

        input_dataframe = self.get_value_from_port("Input DataFrame")
        input_name = self.get_value_from_port("Column name")

        if input_dataframe.is_iterated():
            input_dataframe_property = input_dataframe.get_iterated_property()

            if input_name.is_iterated():
                self.set_output_property('Output DataFrame', [input_dataframe_property[i][input_name.get_iterated_property()[i]].to_frame() for i in range(len(input_dataframe_property))], True)

            else:
                self.set_output_property('Output DataFrame', [input_dataframe_property[i][input_name.get_property()].to_frame() for i in range(len(input_dataframe_property))], True)
                
                self.change_label("Information", "Lines : "+str(len(self.get_output_property("Output DataFrame").get_property()[0])+" x "+str(len(self.get_output_property("Output DataFrame").get_property()))), False)


        else:
            input_dataframe_property = input_dataframe.get_property()

            if input_name.is_iterated():
                self.set_output_property('Output DataFrame', [input_dataframe_property[input_name.get_iterated_property()[i]].to_frame() for i in range(len(input_name.get_iterated_property()))], True)
                
                self.change_label("Information", "Lines : "+str(len(self.get_output_property("Output DataFrame").get_property()[0])+" x "+str(len(input_name.get_iterated_property()))), False)



            else:
                self.set_output_property('Output DataFrame', input_dataframe_property[input_name.get_property()].to_frame(), False)
                
                self.change_label("Information", "Lines : "+str(len(self.get_output_property("Output DataFrame").get_property())), False)

