from enum import Enum
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.axes import Axes
"""
    All value type that can be exchanged between nodes
"""
class PortValueType(Enum):
    FLOAT = 1
    INTEGER = 2
    STRING = 3
    BOOL = 4
    LIST = 5
    NP_ARRAY = 6
    PD_DATAFRAME = 7
    PLOTTABLE = 8
    DICT = 9
    FIGURE = 10
    ANY = 11

"""
    Color association with the port type enum
"""
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
    elif enum_value == PortValueType.PLOTTABLE:
        return (255, 50, 50)
    elif enum_value == PortValueType.DICT:
        return (150, 150, 50)
    elif enum_value == PortValueType.FIGURE:
        return (0, 0, 0)
    elif enum_value == PortValueType.ANY:
        return (122, 122, 122)
    else:
        raise ValueError("No color defined for PortValueType "+str(enum_value))
    
    
"""
    Checks if the given value type corresponds to the enum.
"""
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
    elif enum_value == PortValueType.PLOTTABLE:
        return type(value) in [list, np.ndarray, pd.DataFrame]
    elif enum_value == PortValueType.DICT:
        return type(value) == dict
    elif enum_value == PortValueType.FIGURE:
        return type(value) == PltContainer
    elif enum_value == PortValueType.ANY:
        return value is not None
    else:
        raise ValueError("PortValueType "+str(enum_value)+" not implemented in function check_type")
    
"""
    Checks if the size/shape of two elements are equivalent.
"""
def are_comparable(value1, value2, enum_value):
    if enum_value == PortValueType.FLOAT:
        return check_type(value1, enum_value) and check_type(value2, enum_value)
    elif enum_value == PortValueType.INTEGER:
        return check_type(value1, enum_value) and check_type(value2, enum_value)
    elif enum_value == PortValueType.STRING:
        return check_type(value1, enum_value) and check_type(value2, enum_value)
    elif enum_value == PortValueType.LIST:
        return check_type(value1, enum_value) and check_type(value2, enum_value) and len(value1) == len(value2)
    elif enum_value == PortValueType.NP_ARRAY:
        return check_type(value1, enum_value) and check_type(value2, enum_value) and value1.shape == value2.shape
    elif enum_value == PortValueType.PD_DATAFRAME:
        return check_type(value1, enum_value) and check_type(value2, enum_value) and value1.shape == value2.shape# and value1.columns == value2.columns
    elif enum_value == PortValueType.BOOL:
        return check_type(value1, enum_value) and check_type(value2, enum_value)
    elif enum_value == PortValueType.PLOTTABLE:
        return check_type(value1, enum_value) and check_type(value2, enum_value) and value1.shape == value2.shape
    elif enum_value == PortValueType.DICT:
        return check_type(value1, enum_value) and check_type(value2, enum_value) and list(value1.keys()) == list(value2.keys())
    elif enum_value == PortValueType.FIGURE:
        return type(value1) == PltContainer and type(value2) == PltContainer
    elif enum_value == PortValueType.ANY:
        same_type = (type(value1) == type(value2))
        if same_type:
            for enum_val in PortValueType:
                if not enum_val == PortValueType.ANY:
                    if check_type(value1, enum_val):
                        return are_comparable(value1, value2, enum_val)                
        return False
    else:
        raise ValueError("PortValueType "+str(enum_value)+" not implemented in function are_comparable")

class Container():
    """
        The countainer is initialized empty and undefined
    """
    def __init__(self, enum_value:PortValueType):
        self.countained_value = None
        self.iterated_contained_value = None

        self.enum_value = enum_value
        self.defined = False
        self.name = ""
        self.iterated = False

    """
        Sets the contained value as none, and sets as not defined
    """
    def reset(self):
        self.countained_value = None
        self.defined = False
        self.iterated = False
        self.name = ""

    """
        If the given value type correspond to the container enum, the value is updated and is set as defined
    """
    def set_property(self, value):
        if check_type(value, self.enum_value):
            self.countained_value = value
            self.defined = True
            self.iterated = False

        elif value is None:
            self.defined = False
            self.iterated = False
            
        else:
            raise TypeError("Requested type: "+str(self.enum_value)+", found: "+str(type(value)))

    """
        Sets iterated property if valid.
    """
    def set_iterated_property(self, value, check_comparable = True):
        if not type(value) == list:
            raise TypeError("")

        if len(value) == 0:
            raise ValueError("Received an empty iterated value.")

        first_element = value[0]

        if not check_type(first_element, self.enum_value):
            raise TypeError("Given first element is not of the right type.")

        for i in range(1, len(value)):
            if not check_type(value[i], self.enum_value):
                raise TypeError("Element "+str(i)+" is not of the right type.")
            
            if check_comparable:
                if not are_comparable(first_element, value[i], self.enum_value):
                    print(value)
                    raise TypeError("Element "+str(i)+" is not comparable with the first element.")

        self.iterated_contained_value = value
        self.iterated = True
        self.defined = True

    """
        Returns the iterated property
    """
    def get_iterated_property(self):
        return self.iterated_contained_value

    """
        Returns the contained value
    """
    def get_property(self):
        return self.countained_value

    """
        Returns if the container is defined
    """
    def is_defined(self):
        return self.defined

    """
        Returns the container type enum
    """
    def get_property_type(self):
        return self.enum_value
    
    """ 
        Returns if the container contains internal iterated value
    """
    def is_iterated(self):
        return self.iterated
    
    """
        Sets the container iterated
    """
    def set_iterated(self, value:bool):
        self.is_iterated = value

    """
        Defines how the container object is printed
    """
    def __str__(self):
        return "-- Print Container --\nEnum:"+str(self.enum_value)+"\nDefined:"+str(self.defined)+"\nIterated:"+str(self.iterated)



class PltContainer:
    """
        The countainer is initialized empty and undefined
    """
    def __init__(self, fig, axes, parameters):
        self.fig = fig
        self.axes = axes
        self.parameters = parameters

    """
        Returns the contained value
    """
    def get_property(self, property_name:str):
        if property_name == "Figure":
            return self.fig
        elif property_name == "Axes":
            return self.axes
        elif property_name == "Parameters":
            return self.parameters
        else:
            raise ValueError("Given property name does not exist: "+property_name)
        