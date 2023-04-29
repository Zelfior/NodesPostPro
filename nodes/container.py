from enum import Enum
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    FIGURE = 9

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
        return type(value) in [plt.Figure, plt.axis]
    else:
        raise ValueError
    

class Container():
    """
        The countainer is initialized empty and undefined
    """
    def __init__(self, enum_value:PortValueType):
        self.countained_value = None
        self.enum_value = enum_value
        self.defined = False
        self.name = ""

    """
        Sets the contained value as none, and sets as not defined
    """
    def reset(self):
        self.countained_value = None
        self.defined = False
        self.name = ""

    """
        If the given value type correspond to the container enum, the value is updated and is set as defined
    """
    def set_property(self, value):
        if check_type(value, self.enum_value):
            self.countained_value = value
            self.defined = True
        else:
            raise TypeError

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

