from NodesPostPro.nodes.container import *

import numpy as np
import pandas as pd

    # FLOAT = 1
    # INTEGER = 2
    # STRING = 3
    # BOOL = 4
    # LIST = 5
    # NP_ARRAY = 6
    # PD_DATAFRAME = 7
    # PLOTTABLE = 8
    # DICT = 9
    # FIGURE = 10
    # ANY = 11
    # NUMBER = 12

def make_couples():
    return [
        [1., [PortValueType.FLOAT, PortValueType.NUMBER, PortValueType.ANY]],
        [1, [PortValueType.INTEGER, PortValueType.NUMBER, PortValueType.ANY]],
        ["eqgr", [PortValueType.STRING, PortValueType.ANY]],
        [True, [PortValueType.BOOL, PortValueType.ANY]],
        [5., [PortValueType.FLOAT, PortValueType.NUMBER, PortValueType.ANY]],
        [[1., 2., 3.], [PortValueType.LIST, PortValueType.PLOTTABLE, PortValueType.ANY]],
        [np.array([1,2,3]), [PortValueType.NP_ARRAY, PortValueType.PLOTTABLE, PortValueType.ANY]],
        [pd.DataFrame([1,2,3]), [PortValueType.PD_DATAFRAME, PortValueType.PLOTTABLE, PortValueType.ANY]]
    ]
    
def test_check_type_valid():
    valid_couples = make_couples()

    for value in valid_couples:
        for type_ in value[1]:
            assert check_type(value[0], type_)