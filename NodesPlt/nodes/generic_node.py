from NodeGraphQt import BaseNode
from enum import Enum
import pandas as pd
import numpy as np

class PortValueType(Enum):
    FLOAT = 1
    INTEGER = 2
    STRING = 3
    BOOL = 4
    LIST = 5
    NP_ARRAY = 6
    PD_DATAFRAME = 7

def get_color_from_enum(enum_value):
    if enum_value == PortValueType.FLOAT:
        return (255, 0, 0)
    elif enum_value == PortValueType.INTEGER:
        return (0, 255, 0)
    elif enum_value == PortValueType.STRING:
        return (0, 0, 255)
    elif enum_value == PortValueType.LIST:
        return (100, 0, 255)
    elif enum_value == PortValueType.NP_ARRAY:
        return (0, 100, 255)
    elif enum_value == PortValueType.PD_DATAFRAME:
        return (100, 100, 255)
    elif enum_value == PortValueType.BOOL:
        return (255, 255, 255)

def get_reset_value_from_enum(enum_value):
    if enum_value == PortValueType.FLOAT:
        return None
    elif enum_value == PortValueType.INTEGER:
        return None
    elif enum_value == PortValueType.STRING:
        return None
    elif enum_value == PortValueType.LIST:
        return None
    elif enum_value == PortValueType.NP_ARRAY:
        return None
    elif enum_value == PortValueType.PD_DATAFRAME:
        return pd.DataFrame()
    elif enum_value == PortValueType.BOOL:
        return None
    
def check_type(value, enum_value):
    if enum_value == PortValueType.FLOAT:
        return type(value) == float
    elif enum_value == PortValueType.INTEGER:
        return type(value) == int
    elif enum_value == PortValueType.STRING:
        return type(value) == str
    elif enum_value == PortValueType.LIST:
        return type(value) == list
    elif enum_value == PortValueType.NP_ARRAY:
        return type(value) == np.ndarray
    elif enum_value == PortValueType.PD_DATAFRAME:
        return type(value) == pd.DataFrame
    elif enum_value == PortValueType.BOOL:
        return type(value) == bool
    else:
        raise ValueError
    

class Countainer():
    # def __init__(self, init_value, enum_value:PortValueType, name):
    #     if check_type(init_value, enum_value):
    #         self.countained_value = init_value
    #         self.enum_value = enum_value
    #         self.defined = True
    #         self.name = name
    #     else:
    #         raise TypeError

    def __init__(self, enum_value:PortValueType):
        self.countained_value = get_reset_value_from_enum(enum_value)
        self.enum_value = enum_value
        self.defined = False
        self.name = ""

    def reset(self):
        self.countained_value = None
        self.defined = False
        self.name = ""

    def set_property(self, value):
        if check_type(value, self.enum_value):
            self.countained_value = value
            self.defined = True
        else:
            raise TypeError

    def get_property(self):
        return self.countained_value

    def is_defined(self):
        return self.defined

    def set_defined(self, is_defined):
        self.defined = is_defined

    def get_property_type(self):
        return self.enum_value




class GenericNode(BaseNode):
    def __init__(self):
        super(GenericNode, self).__init__()

        self.output_type_list = {"is_valid": PortValueType.BOOL}

        self.create_property("is_valid", True)

        self.is_reseting = False

        self.output_properties = {}
        self.input_properties = {}


    def set_property(self, name, value, push_undo=True):
        if name == "is_valid":
            super(GenericNode, self).set_property(name, value, push_undo=push_undo)
        elif ( not name in self.output_type_list ) or ( check_type(value, self.output_type_list[name]) ):
            super(GenericNode, self).set_property(name, value, push_undo=push_undo)

            if not self.is_reseting:
                self.update_values()

        
    def on_input_connected(self, in_port, out_port):
        super(GenericNode, self).on_input_connected(in_port, out_port)

        self.update_values()


    def on_input_disconnected(self, in_port, out_port):
        super(GenericNode, self).on_input_disconnected(in_port, out_port)

        self.update_values()


    def update_values(self):

        self.check_inputs()

        if self.get_property("is_valid"):
            self.update_from_input()
        else:
            self.is_reseting = True
            self.reset_outputs()
            self.is_reseting = False

        self.propagate()


    def get_value_from_port(self, port_name):
        if port_name in self.inputs().keys():
            if len(self.inputs()[port_name].connected_ports()) > 0:
                connected_port_name = self.inputs()[port_name].connected_ports()[0].name()
                if self.inputs()[port_name].connected_ports()[0].node().get_output_property(connected_port_name).is_defined():
                    return self.inputs()[port_name].connected_ports()[0].node().get_output_property(connected_port_name)
            return None
        else:
            raise ValueError("Wrong port name given:", port_name)


    def check_inputs(self):
        raise NotImplementedError
    

    def update_from_input(self):
        raise NotImplementedError
    

    def propagate(self):
        for output_id in range(len(self.outputs())):
            for connected_id in range(len(self.output(output_id).connected_ports())):
                self.output(output_id).connected_ports()[connected_id].node().update_values()
    

    def reset_outputs(self):
        for output_name in self.outputs():
            self.output_properties[output_name].reset()
    
    
    def add_custom_input(self, input_name, type_enum):
        self.create_output_property(input_name, type_enum)
        self.add_input(input_name, color=get_color_from_enum(type_enum))

        
    def add_custom_output(self, output_name, type_enum):
        self.create_output_property(output_name, type_enum)
        self.add_output(output_name, color=get_color_from_enum(type_enum))

        self.output_type_list[output_name] = type_enum

    def create_output_property(self, output_name, type_enum):
        self.output_properties[output_name] = Countainer(type_enum)

    def create_input_property(self, output_name, type_enum):
        self.input_properties[output_name] = Countainer(type_enum)
    
    def get_output_property(self, output_name):
        if output_name in self.output_properties:
            return self.output_properties[output_name]
        else:
            raise ValueError

    def set_output_property(self, output_name, value):
        if output_name in self.output_properties:
            self.output_properties[output_name].set_property(value)
            self.output_properties[output_name].set_defined(True)
        else:
            raise ValueError