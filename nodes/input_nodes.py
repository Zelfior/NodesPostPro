from nodes.generic_node import GenericNode, PortValueType, check_cast_type_from_string

    

class InputFloatNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Input'

    # initial default node name.
    NODE_NAME = 'Float'

    def __init__(self):
        super(InputFloatNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.FLOAT)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Value', 'Value', "")

        

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid",check_cast_type_from_string(self.get_property("Value"), PortValueType.FLOAT))
    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Output Value").set_property(float(self.get_property("Value")))



class InputIntegerNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Input'

    # initial default node name.
    NODE_NAME = 'Integer'

    def __init__(self):
        super(InputIntegerNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.INTEGER)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Value', 'Value', "")

        

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid",check_cast_type_from_string(self.get_property("Value"), PortValueType.INTEGER))
    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Output Value").set_property(int(self.get_property("Value")))



        

class InputStringNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Input'

    # initial default node name.
    NODE_NAME = 'String'

    def __init__(self):
        super(InputStringNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.STRING)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Value', 'Value', "")

        

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid", True)
    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Output Value").set_property(str(self.get_property("Value")))

        

class InputBooleanNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Input'

    # initial default node name.
    NODE_NAME = 'Boolean'

    def __init__(self):
        super(InputBooleanNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.BOOL)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Value', 'Value', "")

        

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid",check_cast_type_from_string(self.get_property("Value"), PortValueType.BOOL))


    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        if self.get_property("Value").lower().replace(" ", "") in ['yes', 'true', '1', "1."]:
            self.get_output_property("Output Value").set_property(True)
        else:
            self.get_output_property("Output Value").set_property(False)



            

class InputListNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Input'

    # initial default node name.
    NODE_NAME = 'List'

    def __init__(self):
        super(InputListNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Table', PortValueType.LIST)

        #   create QLineEdit text input widget for the file path
        self.add_twin_input('Rows count', PortValueType.INTEGER, default="5")
        
        self.table = self.add_table_input("Input Table", "Input Table") #    // bug ici, changer row count envoie la valeur dans cette table
        #   widget.value_changed.connect(lambda k, v: self.set_property(k, v)) present dans le add_text_input
        

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid", check_cast_type_from_string(self.get_property("Rows count"), PortValueType.INTEGER))
    

    def update_function(self, input_dict, first=False):

        self.table.table_widget.set_length(input_dict["Rows count"])

        output_dict = {}
        output_dict["Output Table"] = self.table.table_widget.get_value()

        return output_dict