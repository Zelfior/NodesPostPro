from nodes.generic_node import GenericNode, PortValueType


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
        self.add_custom_output('Value', PortValueType.FLOAT)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Value', 'Value', tab='widgets')

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid",self.get_property("Value").lstrip("-").is_digit())
    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Value").set_property(float(self.get_property("Value")))



class InputIntegerNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Input'

    # initial default node name.
    NODE_NAME = 'Integer'

    def __init__(self):
        super(InputFloatNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Value', PortValueType.FLOAT)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Value', 'Value', tab='widgets')

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid",self.get_property("Value").lstrip("-").is_digit() and float(self.get_property("Value").lstrip("-")) == int(self.get_property("Value").lstrip("-")))
    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Value").set_property(int(self.get_property("Value")))

        

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
        self.add_custom_output('Value', PortValueType.INTEGER)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Value', 'Value', tab='widgets')

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid",self.get_property("Value").lstrip("-").is_digit() and float(self.get_property("Value").lstrip("-")) == int(self.get_property("Value").lstrip("-")))
    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Value").set_property(int(self.get_property("Value")))


        

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
        self.add_custom_output('Value', PortValueType.STRING)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Value', 'Value', tab='widgets')

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid", True)
    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Value").set_property(self.get_property("Value"))

        

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
        self.add_custom_output('Value', PortValueType.BOOL)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Value', 'Value', tab='widgets')

    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid",self.get_property("Value").lower().replace(" ", "") in ['yes', 'true', '1', "1.", 'no', 'false', '0', '0.'])
    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        if self.get_property("Value").lower().replace(" ", "") in ['yes', 'true', '1', "1."]:
            self.get_output_property("Value").set_property(True)
        else:
            self.get_output_property("Value").set_property(False)