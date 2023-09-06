from NodeGraphQt import NodeBaseWidget

from PySide2 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.gridspec import SubplotSpec 

import NodeGraphQt

from NodeGraphQt.widgets.node_widgets import _NodeGroupBox

import pandas as pd
import numpy as np
import os

from NodesPostPro.nodes.generic_node import GenericNode, PortValueType, check_type
from NodesPostPro.nodes.custom_widgets import IntSelector_Widget
from NodesPostPro.nodes.cast_nodes import is_float
from NodesPostPro.nodes.container import PltContainer

from matplotlib.colors import LogNorm, Normalize


def plot_element_on_axis(figure : Figure, axis : Axes, element):

    if element['element_type'] == "plot":
        # if not "X" in element:
        #     return None
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "priority"]}
        return axis.plot(element['X'], element['Y'], **kwargs_dict)
        
    elif element['element_type'] == "fill_between":
        # if not "X" in element:
        #     return None
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y1", "Y2", "element_type", "priority"]}
        return axis.fill_between(element['X'], element['Y1'], element['Y2'], **kwargs_dict)
        
    elif element['element_type'] == "imshow":
        # if not "X" in element:
        #     return None
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "priority", "norm"]}
        kwargs_dict["aspect"] = "auto"

        if element["norm"] == "log":
            scale = LogNorm()
        else:
            scale = Normalize()

        return axis.imshow(element['Y'], norm = scale, **kwargs_dict)

    elif element['element_type'] == "scatter":
        # if not "X" in element:
        #     return None
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "Color", "Color array", "priority", "markersize"]}

        if "Color array" in element:
            if type(element["Color array"]) == pd.DataFrame:
                kwargs_dict["c"] = element["Color array"].values.tolist()
            else:
                kwargs_dict["c"] = list(element["Color array"])

            if not "cmap" in kwargs_dict:
                kwargs_dict["cmap"] = "viridis"
        elif "Color" in element:
            kwargs_dict["c"] = element["Color"]

        if "markersize" in element:
            kwargs_dict["s"] = element["markersize"]

        return axis.scatter(element['X'], element['Y'], **kwargs_dict)

    elif element['element_type'] == "hist":
        # if not "X" in element:
        #     return None
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "element_type", "priority"]}
        return axis.hist(element['X'], **kwargs_dict)
                


class PltCanvasWidget(QtWidgets.QWidget):
    def __init__(self, width = 6, height = 6, parent=None):
        super(PltCanvasWidget, self).__init__(parent)
        self.fig = Figure(figsize=(width, height))
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.base_grid_spec = self.fig.add_gridspec(1, 1)

        self.layout_ = QtWidgets.QHBoxLayout(self)
        self.layout_.setContentsMargins(-5, -5, -5, -5)
        self.layout_.addWidget(self.canvas)


    def get_value(self):
        return ''
    
    def update_figure(self, width, height):
        self.fig.clear()
        self.base_grid_spec = self.fig.add_gridspec(1, 1)

        self.fig.set_figwidth(width)
        self.fig.set_figheight(height)

        self.canvas.adjustSize()





class pltWidget(NodeBaseWidget):
    def __init__(self, parent=None, name=''):
        super(pltWidget, self).__init__(parent)

        # set the name for node property.
        self.set_name('Plot_Widget')

        self.canvas = PltCanvasWidget()
        # set the custom widget.
        self.set_custom_widget(self.canvas)

        self.title = ""

    def sort_by_priority(self, array):
        if array == None:
            return None
        
        new_array = []

        for element in array:
            if len(new_array) == 0:
                new_array.append(element)
            else:
                i = 0
                while i < len(new_array) and new_array[i]["priority"] < element["priority"]:
                    i += 1 
                new_array.insert(i, element)

        return new_array

    def plot_on_axis(self, fig:Figure, axis:Axes, parameters:dict, array1:list, array2:list):

        array1 = self.sort_by_priority(array1)
        array2 = self.sort_by_priority(array2)

        mappables= []

        if array1 is not None:
            for element in array1:
                el = plot_element_on_axis(fig, axis, element)

                if element['element_type'] == "imshow":
                    mappables.append(el)
        else:
            axis.yaxis.set_visible(False)
                
        if array2 is not None:
            twinx_axes = axis.twinx()

            for element in array2:
                el = plot_element_on_axis(fig, twinx_axes, element)

                if element['element_type'] == "imshow":
                    mappables.append(el)
        else:
            twinx_axes = None
                

        if "Title" in parameters:
            axis.set_title(parameters["Title"])

        if "X_min" in parameters:
            if "X_max" in parameters:
                axis.set_xlim((parameters["X_min"], parameters["X_max"]))
            else:
                axis.set_xlim((parameters["X_min"], None))
        elif "X_max" in parameters:
            axis.set_xlim((None, parameters["X_max"]))

        if "Y_min" in parameters:
            if "Y_max" in parameters:
                axis.set_ylim((parameters["Y_min"], parameters["Y_max"]))
            else:
                axis.set_ylim((parameters["Y_min"], None))
        elif "Y_max" in parameters:
            axis.set_ylim((None, parameters["Y_max"]))


        if "X label" in parameters:
            axis.set_xlabel(parameters["X label"])
            
        if "Y label 1" in parameters:
            if array1 is not None:
                axis.set_ylabel(parameters["Y label 1"])
            
        if "Y label 2" in parameters:
            if twinx_axes is not None:
                twinx_axes.set_ylabel(parameters["Y label 2"])



        if parameters["legend"]:
            if twinx_axes != None:
                h1, l1 = axis.get_legend_handles_labels()
                h2, l2 = twinx_axes.get_legend_handles_labels()
                axis.legend(handles=h1+h2, labels=l1+l2)
            else:
                axis.legend()

        if parameters["color_bar"]:
            if len(mappables) > 0:
                self.canvas.fig.colorbar(mappables[0])
            
        if parameters["x_log"]:
            axis.set_xscale('log')
        else:   
            axis.set_xscale('linear')
            
        if parameters["y_log"]:
            axis.set_yscale('log')
        else:   
            axis.set_yscale('linear')

    def update_iteration(self, figure_list, current_subgrid):

            cut = figure_list["cut_direction"]

            if cut is None:
                if list(figure_list.keys()) == ["cut_direction"]:
                    axis = self.canvas.fig.add_subplot(current_subgrid)
                    axis.set_visible(False)

                else:
                    assert len(figure_list["list"]) == 1

                    input_arrays_1 = figure_list["list"][0]["array1"]
                    input_arrays_2 = figure_list["list"][0]["array2"]
                    plot_parameters = figure_list["list"][0]["parameters"]

                    axis = self.canvas.fig.add_subplot(current_subgrid)
                    self.plot_on_axis(self.canvas.fig, axis, plot_parameters, input_arrays_1, input_arrays_2)
            else:
                assert len(figure_list["list"]) == 2

                if type(current_subgrid) == SubplotSpec:
                    base_spec = current_subgrid
                else:
                    base_spec = current_subgrid[0]

                if cut == "V":
                    new_specs = base_spec.subgridspec(2, 1, height_ratios=[figure_list["ratio1"], figure_list["ratio2"]])

                if cut == "H":
                    new_specs = base_spec.subgridspec(1, 2, width_ratios=[figure_list["ratio1"], figure_list["ratio2"]])

                self.update_iteration(figure_list["list"][0], new_specs[0])
                self.update_iteration(figure_list["list"][1], new_specs[1])


    def update_plot(self, figure_list):

        plot_parameters = figure_list["parameters"]
        if "width" in plot_parameters:
            self.canvas.update_figure(int(plot_parameters["width"]), int(plot_parameters["height"]))

            #   On reset le custom widget du canvas pour qu'il prenne en compte la nouvelle taille
            group = _NodeGroupBox(self._label)
            group.add_node_widget(self.canvas)
            self.setWidget(group)

        else:
            self.canvas.fig.clear()  # clear the axes content
            self.canvas.base_grid_spec = self.canvas.fig.add_gridspec(1, 1)

        cut = figure_list["cut_direction"]

        if cut == None:
            input_arrays_1 = figure_list["list"][0]["array1"]
            input_arrays_2 = figure_list["list"][0]["array2"]
            plot_parameters = figure_list["list"][0]["parameters"]

            axis = self.canvas.fig.add_subplot(self.canvas.base_grid_spec[0])
            self.plot_on_axis(self.canvas.fig, axis, plot_parameters, input_arrays_1, input_arrays_2)
        else:
            self.update_iteration(figure_list, self.canvas.base_grid_spec[0])

        self.canvas.fig.tight_layout()
        self.canvas.canvas.draw()  # actually draw the new content

    def get_value(self):
        return ''

    def set_value(self, value):
        pass



def are_plottable_compatible(plot1, plot2):
    plot1 = np.squeeze(np.array(plot1))
    plot2 = np.squeeze(np.array(plot2))

    return plot1.shape == plot2.shape















class ImShowNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'ImShow'

    def __init__(self):
        super(ImShowNode, self).__init__()

        # X, cmap=None, norm=None
        # self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_combo_menu('norm', 'norm', items=["linear", "log"])
        
        self.priority_widget = self.add_int_selector(name="Priority", label='Priority')
        self.priority_widget.set_range(0, 50)

        self.add_custom_input('alpha', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "imshow"

    def check_inputs(self):
        is_valid, message = self.is_input_valid("Y")

        self.set_property("is_valid", is_valid)

        if not is_valid:
            self.change_label("Information", message, True)
        else:
            if len(self.get_value_from_port("Y").get_property().shape) != 2:
                self.change_label("Information", "Y input should have 2 dimensions.", True)
                self.set_property("is_valid", False)

        for input in self.input_properties:
            if not input == "Y":

                input_value = self.get_value_from_port(input)

                if input_value is not None:
                    is_valid, message = self.is_input_valid(input)

                    self.set_property("is_valid", is_valid and self.get_property("is_valid"))

                    if not is_valid:
                        self.change_label("Information", message, True)

                   
    def update_from_input(self):
        
        properties_dict = {"element_type": self.element_type}

        for input in self.input_properties:
            input_value = self.get_value_from_port(input)

            if input_value is not None:
                properties_dict[input] = input_value.get_property()

        properties_dict['norm'] = self.get_property('norm')

        properties_dict['origin']='lower'

        properties_dict['priority'] = int(self.priority_widget.get_value())

        self.set_output_property("Element", properties_dict, False)

        self.change_label("Information", "", True)









class PltElementNode(GenericNode):

    def __init__(self):
        super(PltElementNode, self).__init__()

        self.element_type = "undefined"
        self.y_name = 'Y'

    def update_function(self, input_dict, first = False):
        element_dict = {"element_type": self.element_type}

        for input in self.input_properties:
            if input in input_dict:
                element_dict[input] = input_dict[input]

        if (not "X" in element_dict):# and (self.y_name in element_dict) and (element_dict[self.y_name] is not None):
            element_dict["X"] = list(range(len(element_dict[self.y_name])))

        self.change_label("Information", "", False)

        return element_dict

    def add_linestyle_combo(self):
        self.add_combo_menu('linestyle', 'linestyle', items=['solid', 'dotted', 'dashed', 'dashdot'])













class PlotNode(PltElementNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Plot'

    def __init__(self):
        super(PlotNode, self).__init__()

        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_custom_input('color', PortValueType.STRING)
        
        self.add_linestyle_combo()

        self.add_custom_input('linewidth', PortValueType.FLOAT)
        
        self.priority_widget = self.add_int_selector("Priority", 'Priority')
        self.priority_widget.set_range(0, 50)

        self.add_combo_menu('marker', 'marker', items=["None", ".", ",", "o", "s", "D"])

        self.add_custom_input('markersize', PortValueType.FLOAT)

        self.add_custom_input('alpha', PortValueType.FLOAT)


        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "plot"

        self.is_iterated_compatible = True

    def check_function(self, input_dict, first=False):
        if (not "Y" in input_dict) or (type(input_dict["Y"]) == str):
            return False, "Y is not valid", "Information"

        for input_name in ["X", "Y"]:
            if check_type(input_dict[input_name], PortValueType.PD_DATAFRAME):
                health_check = input_dict[input_name].apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
                for key in range(len(health_check)):
                    if not health_check[key]:
                        return False, "Column "+health_check.index[key]+" of Y is not valid", "Information"

        if ("X" in input_dict) and (not type(input_dict["X"]) == str) and (not are_plottable_compatible(input_dict["X"], input_dict["Y"])):
            return False, "X and Y are not compatible", "Information"
        
        for value in input_dict:
            if not value in ["X", "Y"]:
                if type(input_dict[value]) == str and "Error_" in input_dict[value] and (not "is not defined" in input_dict[value]):
                    return False, input_dict[value].replace("Error_", ""), "Information"

        return True, "", "Information"

                   
    def update_function(self, input_dict, first = False):
        element_dict = super(PlotNode, self).update_function(input_dict, first)

        element_dict['linestyle'] = self.get_property('linestyle')

        if self.get_property('marker') != "None":
            element_dict['marker'] = self.get_property('marker')

        element_dict['priority'] = int(self.priority_widget.get_value())

        return {"Element":element_dict}












class FillBetweenNode(PltElementNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Fill Between'

    def __init__(self):
        super(FillBetweenNode, self).__init__()

        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y1', PortValueType.PLOTTABLE)
        self.add_custom_input('Y2', PortValueType.PLOTTABLE)
        self.add_custom_input('Where', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_custom_input('color', PortValueType.STRING)

        
        self.priority_widget = self.add_int_selector("Priority", 'Priority')
        self.priority_widget.set_range(0, 50)

        self.add_custom_input('alpha', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "fill_between"
        self.y_name = 'Y1'

        self.is_iterated_compatible = True

                
    def check_function(self, input_dict, first=False):
        for key in ["X", "Y1", "Y2"]:
            if (not key in input_dict) or (type(input_dict[key]) == str):
                return False, key+" is not valid", "Information"
            if len(np.squeeze(np.array(input_dict[key])).shape) > 1:
                return False, key+" should be 1D", "Information"

        for input_name in ["X", "Y1", "Y2"]:
            if check_type(input_dict[input_name], PortValueType.PD_DATAFRAME):
                health_check = input_dict[input_name].apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
                for key in range(len(health_check)):
                    if not health_check[key]:
                        return False, "Column "+health_check.index[key]+" of Y is not valid", "Information"

        if not are_plottable_compatible(input_dict["X"], input_dict["Y1"]):
            return False, "X and Y1 are not compatible", "Information"

        if not are_plottable_compatible(input_dict["X"], input_dict["Y2"]):
            return False, "X and Y2 are not compatible", "Information"

        if not are_plottable_compatible(input_dict["X"], input_dict["Y1"]):
            return False, "X and Y1 are not compatible", "Information"

        if (type(input_dict["Where"]) != str) and not are_plottable_compatible(input_dict["X"], input_dict["Where"]):
            return False, "X and Where are not compatible", "Information"
        
        if (type(input_dict["Where"]) != str) and len(np.squeeze(np.array(input_dict["Where"])).shape):
            return False, "Where input should be 1D", "Information"
        
        for value in input_dict:
            if not value in ["X", "Y1", "Y2", "Where"]:
                if type(input_dict[value]) == str and "Error_" in input_dict[value] and (not "is not defined" in input_dict[value]):
                    return False, input_dict[value].replace("Error_", ""), "Information"
                
        return True, "", "Information"

                   
    def update_function(self, input_dict, first = False):
        element_dict = super(FillBetweenNode, self).update_function(input_dict, first)

        if not "X" in element_dict:
            return {"Element":element_dict}
        
        for key in ["X", "Y1", "Y2"]:
            element_dict[key] = np.squeeze(np.array(element_dict[key]))

        if "Where" in element_dict:
            element_dict["where"] = np.squeeze(np.array(element_dict["Where"]))
            del element_dict["Where"]

        element_dict['priority'] = int(self.priority_widget.get_value())

        return {"Element":element_dict}











class ScatterNode(PltElementNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Scatter'

    def __init__(self):
        super(ScatterNode, self).__init__()

        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_custom_input('Color', PortValueType.STRING)
        
        self.add_custom_input('Color array', PortValueType.PLOTTABLE)
        
        self.add_custom_input('cmap', PortValueType.STRING)

        self.add_custom_input('linewidth ', PortValueType.FLOAT)
        
        self.priority_widget = self.add_int_selector("Priority", 'Priority')        
        self.priority_widget.set_range(0, 50)

        self.add_combo_menu('marker', 'marker', items=["None", ".", ",", "o", "s", "D"])
        
        self.add_custom_input('markersize', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "scatter"

        self.is_iterated_compatible = True


    def check_function(self, input_dict, first=False):
        if (not "Y" in input_dict) or (type(input_dict["Y"]) == str):
            return False, "Y is not valid", "Information"

        if ("X" in input_dict) and (not type(input_dict["X"]) == str) and (not are_plottable_compatible(input_dict["X"], input_dict["Y"])):
            return False, "X and Y are not compatible", "Information"

        for value in input_dict:
            if not value in ["X", "Y"]:
                if type(input_dict[value]) == str and "Error_" in input_dict[value] and (not "is not defined" in input_dict[value]):
                    return False, input_dict[value].replace("Error_", ""), "Information"

        for input_name in ["X", "Y"]:
            if check_type(input_dict[input_name], PortValueType.PD_DATAFRAME):
                health_check = input_dict[input_name].apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
                for key in range(len(health_check)):
                    if not health_check[key]:
                        return False, "Column "+health_check.index[key]+" of Y is not valid", "Information"

        return True, "", "Information"

                   
    def update_function(self, input_dict, first = False):
        element_dict = super(ScatterNode, self).update_function(input_dict, first)

        if self.get_property('marker') != "None":
            element_dict['marker'] = self.get_property('marker')

        element_dict['priority'] = int(self.priority_widget.get_value())

        return {"Element":element_dict}
















class HistNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Hist'

    def __init__(self):
        super(HistNode, self).__init__()

        # X, cmap=None, norm=None
        # self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Bins', PortValueType.INTEGER)
        self.add_custom_input('Weight', PortValueType.PLOTTABLE)

        self.add_custom_input('X min', PortValueType.FLOAT)
        self.add_custom_input('X max', PortValueType.FLOAT)

        self.add_custom_input('color', PortValueType.STRING)

        self.add_checkbox("density", text='Density')
        self.add_checkbox("cumulative", text='Cumulative')
        self.add_checkbox("log", text='Log')

        self.add_custom_input('label', PortValueType.STRING)

        self.add_combo_menu('histtype', 'histtype', items=['bar', 'barstacked', 'step', 'stepfilled'])
        
        self.priority_widget = self.add_int_selector("Priority", 'Priority')        
        self.priority_widget.set_range(0, 50)

        self.add_custom_input('alpha', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "hist"



    def check_function(self, input_dict, first=False):
        if (not "X" in input_dict) or (type(input_dict["X"]) == str):
            return False, "X is not valid", "Information"

        if ("Weight" in input_dict) and (not type(input_dict["Weight"]) == str) and (not are_plottable_compatible(input_dict["X"], input_dict["Weight"])):
            return False, "X and Weight are not compatible", "Information"

        for value in input_dict:
            if not value in ["X", "Weight"]:
                if type(input_dict[value]) == str and "Error_" in input_dict[value] and (not "is not defined" in input_dict[value]):
                    return False, input_dict[value].replace("Error_", ""), "Information"

        for input_name in ["X", "Weight"]:
            if check_type(input_dict[input_name], PortValueType.PD_DATAFRAME):
                health_check = input_dict[input_name].apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
                for key in range(len(health_check)):
                    if not health_check[key]:
                        return False, "Column "+health_check.index[key]+" of Y is not valid", "Information"

        return True, "", "Information"

                   
    def update_function(self, input_dict, first = False):
        element_dict = {"element_type": self.element_type}

        for input in self.input_properties:
            if input in input_dict:
                element_dict[input] = input_dict[input]

        element_dict['histtype'] = input_dict['histtype'] 
        element_dict['density'] = input_dict['density'] 
        element_dict['cumulative'] = input_dict['cumulative'] 
        element_dict['log'] = input_dict['log'] 

        if "Weight" in element_dict:
            element_dict["weights"] = element_dict["Weight"]
            del element_dict["Weight"]

        if "Bins" in element_dict:
            element_dict["bins"] = element_dict["Bins"]
            del element_dict["Bins"]

        if "X min" in element_dict:
            if "X max" in element_dict:
                element_dict["range"] = [element_dict["X min"], element_dict["X max"]]
                del element_dict["X max"]
            else:
                element_dict["range"] = [element_dict["X min"], max(np.array(element_dict["X"]).flatten())]
            del element_dict["X min"]

        elif "X max" in element_dict:
            element_dict["range"] = [min(np.array(element_dict["X"]).flatten()), element_dict["X max"]]
            del element_dict["X max"]

        element_dict['priority'] = int(self.priority_widget.get_value())

        return {"Element":element_dict}






















class GenericFigureNode(GenericNode):
    def __init__(self):
        super(GenericFigureNode, self).__init__()



    def reset_outputs(self):
        super(GenericFigureNode, self).reset_outputs()

        if check_type(self.get_property("canvas_width"), PortValueType.INTEGER) and \
            check_type(self.get_property("canvas_height"), PortValueType.INTEGER):
            self.plot_widget.update_plot({
                            "cut_direction": None, 
                            "parameters":{"width":self.get_property("canvas_width"), "height":self.get_property("canvas_height")},
                            "list":[
                                    {
                                        "array1": None, 
                                        "array2": None, 
                                        "parameters": {"legend": False, "x_log":False, "y_log":False, "color_bar":False}
                                    }
                                ]})
        else:
            
            self.plot_widget.update_plot({
                            "cut_direction": None, 
                            "parameters":{"width":6, "height":6},
                            "list":[
                                    {
                                        "array1": None, 
                                        "array2": None, 
                                        "parameters": {"legend": False, "x_log":False, "y_log":False, "color_bar":False}
                                    }
                                ]})

        self.change_label("Information", "", False)





class PltFigureNode(GenericFigureNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Figure'

    def __init__(self):
        super(PltFigureNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Plottable 1', PortValueType.DICT, multi_input=True)
        self.add_custom_input('Input Plottable 2', PortValueType.DICT, multi_input=True)
        
        self.add_twin_input('Title', PortValueType.STRING)
        # self.add_custom_input('Title', PortValueType.STRING)
        
        self.add_custom_input('X_min', PortValueType.FLOAT)
        self.add_custom_input('X_max', PortValueType.FLOAT)
        
        self.add_custom_input('Y_min', PortValueType.FLOAT)
        self.add_custom_input('Y_max', PortValueType.FLOAT)
        
        self.add_custom_input('X label', PortValueType.STRING)
        self.add_custom_input('Y label 1', PortValueType.STRING)
        self.add_custom_input('Y label 2', PortValueType.STRING)
        
        self.add_custom_output('Figure', PortValueType.FIGURE)
        
        self.add_checkbox("x_log", text='X log scale')
        self.add_checkbox("y_log", text='Y log scale')
        self.add_checkbox("legend", text='Legend')
        self.add_checkbox("color_bar", text='Color bar')

        self.add_text_input("canvas_width", "Width", "6")
        self.add_text_input("canvas_height", "Height", "6")

        self.plot_widget = pltWidget(self.view, name="plot")

        self.create_property('Plot_Widget', None)

        self.view.add_widget(self.plot_widget)
        self.view.draw_node()
        
        self.add_label("Information")

        self.reset_outputs()

        self.is_iterated_compatible = True


    def update_from_input(self):
        if not self.get_value_from_port("Input Plottable 1") == None or not self.get_value_from_port("Input Plottable 2") == None:

            if self.get_value_from_port("Input Plottable 1", multiple=True) == None:
                self.input_arrays_1 = None
            else:
                self.input_arrays_1 = []
                for element in self.get_value_from_port("Input Plottable 1", multiple=True):
                    if element.is_iterated():
                        self.input_arrays_1 += element.get_iterated_property()
                    else:
                        self.input_arrays_1.append(element.get_property())
                
            if self.get_value_from_port("Input Plottable 2", multiple=True) == None:
                self.input_arrays_2 = None
            else:
                self.input_arrays_2 = []
                for element in self.get_value_from_port("Input Plottable 2", multiple=True):
                    if element.is_iterated():
                        self.input_arrays_2 += element.get_iterated_property()
                    else:
                        self.input_arrays_2.append(element.get_property())

            plot_parameters = {"legend":self.get_property("legend"),
                                    "x_log":self.get_property("x_log"),
                                    "y_log":self.get_property("y_log"),
                                    "color_bar":self.get_property("color_bar")}
            
            plot_parameters["width"] = self.get_property("canvas_width")
            plot_parameters["height"] = self.get_property("canvas_height")

            for input_ in self.input_properties:
                if self.is_input_valid(input_)[0]:
                    plot_parameters[input_] = self.get_value_from_port(input_).get_property()

            if self.get_twin_input("Title").get_property() != "":
                plot_parameters["Title"] = self.get_twin_input("Title").get_property()

            self.plot_widget.update_plot({
                        "cut_direction": None, 
                        "parameters":{"width":self.get_property("canvas_width"), "height":self.get_property("canvas_height")},
                        "list":[
                                {
                                    "array1": self.input_arrays_1, 
                                    "array2": self.input_arrays_2, 
                                    "parameters": plot_parameters
                                }
                            ]})

            self.set_output_property("Figure", PltContainer(self.plot_widget.canvas.fig,
                                                                {
                                                                    "cut_direction": None,
                                                                    "parameters":{"width":self.get_property("canvas_width"), "height":self.get_property("canvas_height")},
                                                                    "list":[
                                                                        {
                                                                            "axis": self.plot_widget.canvas.canvas,
                                                                            "array1": self.input_arrays_1, 
                                                                            "array2": self.input_arrays_2, 
                                                                            "parameters": plot_parameters,
                                                                            "cut_direction": None
                                                                        }]
                                                                }
                                                            ), False)

    def check_inputs(self):
        if not self.get_value_from_port("Input Plottable 1") == None:
            is_valid, message = self.is_input_valid("Input Plottable 1")

            self.set_property("is_valid", is_valid)

            if not is_valid:
                self.change_label("Information", message, True)

        if not self.get_value_from_port("Input Plottable 2") == None:
            
            is_valid, message = self.is_input_valid("Input Plottable 2")

            self.set_property("is_valid", is_valid)

            if not is_valid:
                self.change_label("Information", message, True)

        if self.get_value_from_port("Input Plottable 1") == None and self.get_value_from_port("Input Plottable 2") == None:
            self.set_property("is_valid", False)
            self.change_label("Information", "No input plottable given", True)

        if not is_float(self.get_property("canvas_height")):
            self.set_property("is_valid", False)
            self.change_label("Information", "Given height should be a float", True)

        if not is_float(self.get_property("canvas_width")):
            self.set_property("is_valid", False)
            self.change_label("Information", "Given width should be a float", True)




class SaveFigureNode(GenericNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Save Figure'

    def __init__(self):
        super(SaveFigureNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Figure', PortValueType.FIGURE)

        self.add_custom_input('File name', PortValueType.STRING)

        self.add_text_input("canvas_dpi", "DPI", "100")
        
        self.add_label("Information")

    def update_from_input(self):
        print("Saving figure at path :", os.path.abspath(self.get_value_from_port("File name").get_property()))
        self.change_label("Information", "", False)

        figure = self.get_value_from_port("Input Figure").get_property().get_property("Figure")

        try:
            figure.savefig(os.path.abspath(self.get_value_from_port("File name").get_property()), dpi=int(self.get_property("canvas_dpi")))
        except Exception as e:
            self.change_label("Information", str(e), True)

    def check_inputs(self):

        is_valid_1, message_1 = self.is_input_valid("Input Figure")

        self.set_property("is_valid", is_valid_1)

        if not is_valid_1:
            self.change_label("Information", message_1, True)
            

        is_valid_1, message_1 = self.is_input_valid("File name")

        self.set_property("is_valid", self.get_property("is_valid") and is_valid_1)

        if not is_valid_1:
            self.change_label("Information", message_1, True)
        else:
            abs_path = os.path.dirname(os.path.abspath(self.get_value_from_port("File name").get_property()))

            if not os.path.isdir(abs_path):
                self.set_property("is_valid", False)
                self.change_label("Information", "Given path folder does not exist", True)

        if not is_float(self.get_property("canvas_dpi")):
            self.set_property("is_valid", False)
            self.change_label("Information", "Given DPI should be a float", True)






class GenericSplitNode(GenericFigureNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    # NODE_NAME = 'Vertical Split'

    def __init__(self):
        super(GenericSplitNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Figure 1', PortValueType.FIGURE)
        self.add_custom_input('Input Figure 2', PortValueType.FIGURE)

        self.add_twin_input('Ratio 1', PortValueType.INTEGER, default="1")
        self.add_twin_input('Ratio 2', PortValueType.INTEGER, default="1")

        self.add_custom_output('Figure', PortValueType.FIGURE)
        
        self.add_text_input("canvas_width", "Width", "6")
        self.add_text_input("canvas_height", "Height", "6")

        self.plot_widget = pltWidget(self.view, name="plot")

        self.create_property('Plot_Widget', None)

        self.view.add_widget(self.plot_widget)
        self.view.draw_node()

        self.add_label("Information")

        self.reset_outputs()

        self.cut_key = ""

    def update_from_input(self):
        self.change_label("Information", "", False)

        if self.is_input_valid("Input Figure 1")[0]:
            param_list_1 = self.get_value_from_port("Input Figure 1").get_property().get_property("Parameters_list")
        else:
            param_list_1 = {"cut_direction": None}
            
        if self.is_input_valid("Input Figure 2")[0]:
            param_list_2 = self.get_value_from_port("Input Figure 2").get_property().get_property("Parameters_list")
        else:
            param_list_2 = {"cut_direction": None}

        self.set_output_property("Figure", PltContainer(self.plot_widget.canvas.fig,
                                                        {
                                                            "cut_direction": self.cut_key,
                                                            "ratio1":int(self.get_property("Ratio 1")), 
                                                            "ratio2":int(self.get_property("Ratio 2")),
                                                            "parameters":{"width":self.get_property("canvas_width"), "height":self.get_property("canvas_height")},
                                                            "list":[param_list_1, param_list_2]
                                                        }), False)
        
        self.plot_widget.update_plot({
                                        "cut_direction": self.cut_key,
                                        "ratio1":int(self.get_property("Ratio 1")), 
                                        "ratio2":int(self.get_property("Ratio 2")),
                                        "parameters":{"width":self.get_property("canvas_width"), 
                                        "height":self.get_property("canvas_height"), },
                                        "list":[param_list_1, param_list_2]
                                    })

    def check_inputs(self):
        is_valid_1, message_1 = self.is_input_valid("Input Figure 1")
        is_valid_2, message_2 = self.is_input_valid("Input Figure 2")

        self.set_property("is_valid", is_valid_1 or is_valid_2)

        if not is_valid_1 or is_valid_2:
            self.change_label("Information", "None of the input figure is valid.", True)
        else:
            for key in ["canvas_height", "canvas_width"]:
                if self.get_property("is_valid"):
                    is_valid, message = self.is_input_valid(key)

                    if not is_valid:
                        self.set_property("is_valid", is_valid)
                        self.change_label("Information", message, True)
                        
            for key in ["Ratio 1", "Ratio 2"]:
                if self.get_property("is_valid"):
                    is_valid, message = self.is_twin_input_valid(key)

                    if not is_valid:
                        self.set_property("is_valid", is_valid)
                        self.change_label("Information", message, True)





class VerticalSplitNode(GenericSplitNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Vertical Split'

    def __init__(self):
        super(VerticalSplitNode, self).__init__()

        self.cut_key = "V"
        

class HorizontalSplitNode(GenericSplitNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Horizontal Split'

    def __init__(self):
        super(HorizontalSplitNode, self).__init__()

        self.cut_key = "H"