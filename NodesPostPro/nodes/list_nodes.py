from NodeGraphQt import BaseNode
from NodesPostPro.nodes.generic_node import GenericNode, PortValueType

import numpy as np




class GetListElementNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'List'

    # initial default node name.
    NODE_NAME = 'Get element'

    def __init__(self):
        super(GetListElementNode, self).__init__()

        #   Create input port for input array
        self.add_custom_input('Input List', PortValueType.LIST)
        self.add_twin_input('Input Index', PortValueType.INTEGER, default="0")

        #   Create output ports for :
        #       The output array corresponding to the given axis value
        self.add_custom_output('Output Element', PortValueType.ANY)

        self.add_label("Information")

        self.is_iterated_compatible = True


    def check_function(self, input_dict, first=False):
        if (not "Input List" in input_dict) or type(input_dict["Input List"]) == str:
            return False, "Input List is not valid", "Information"
        
        if not "Input Index" in input_dict or type(input_dict["Input Index"]) == str:
            return False, "Input Index is not valid", "Information"
        
        if input_dict["Input Index"] >= len(input_dict["Input List"]):
            return False, "Input Index should be lesser than list length", "Information"

        return True, "", "Information"

    def update_function(self, input_dict, first=False):
        output_dict = {'Output Element': input_dict["Input List"][input_dict["Input Index"]]}
        output_dict["__message__Information"] = "Type: "+str(output_dict["Output Element"].__class__.__name__)
        return output_dict
