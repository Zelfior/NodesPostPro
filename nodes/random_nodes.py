from nodes.generic_node import GenericNode, PortValueType, check_cast_type_from_string

import random
    

class RandomUniformNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Random'

    # initial default node name.
    NODE_NAME = 'Uniform'

    def __init__(self):
        super(RandomUniformNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.FLOAT)

        self.add_twin_input("Min", PortValueType.FLOAT, default = "0.")
        self.add_twin_input("Max", PortValueType.FLOAT, default = "1.")

        self.add_label("Information", "")

        self.is_iterated_compatible = True
        
    def check_function(self, input_dict, first = False):
        if not "Min" in input_dict:
            return False, "Min value is not valid", "Information"

        if not "Max" in input_dict:
            return False, "Max value is not valid", "Information"

        if input_dict["Min"] > input_dict["Max"]:
            return False, "Max must be greater than Min", "Information"

        return True, "", "Information"

    def update_function(self, input_dict, first = False):
        output_dict = {'Output Value': random.uniform(input_dict["Min"], input_dict["Max"])} 
        output_dict["__message__Information"] = str(output_dict['Output Value'])
        return output_dict




class RandomIntegerNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Random'

    # initial default node name.
    NODE_NAME = 'Random Integer'

    def __init__(self):
        super(RandomIntegerNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.INTEGER)

        self.add_twin_input("Min", PortValueType.INTEGER, default = "0")
        self.add_twin_input("Max", PortValueType.INTEGER, default = "1")

        self.add_label("Information", "")

        self.is_iterated_compatible = True

    def check_function(self, input_dict, first = False):
        if not "Min" in input_dict:
            return False, "Min value is not valid", "Information"

        if not "Max" in input_dict:
            return False, "Max value is not valid", "Information"

        if input_dict["Min"] > input_dict["Max"]:
            return False, "Max must be greater than Min", "Information"

        return True, "", "Information"

    def update_function(self, input_dict, first = False):
        output_dict = {'Output Value': random.randint(input_dict["Min"], input_dict["Max"])} 
        output_dict["__message__Information"] = str(output_dict['Output Value'])
        return output_dict
