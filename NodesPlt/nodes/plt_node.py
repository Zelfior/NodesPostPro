from NodeGraphQt import BaseNode, BaseNodeCircle, NodeBaseWidget
from functools import wraps
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from NodeGraphQt.constants import NodePropWidgetEnum, PortTypeEnum
from Qt import QtCore, QtWidgets

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from nodes.generic_node import GenericNode, PortValueType, get_reset_value_from_enum

class PltCanvasWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PltCanvasWidget, self).__init__(parent)
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.axes = self.fig.add_subplot(111)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)





class pltWidget(NodeBaseWidget):
    def __init__(self, parent=None, name=''):
        super(pltWidget, self).__init__(parent)

        # set the name for node property.
        self.set_name('my_widget')

        # set the label above the widget.
        self.set_label('Custom Widget')

        self.canvas = PltCanvasWidget()
        # set the custom widget.
        self.set_custom_widget(self.canvas)

        self.to_plot = []

        self.title = ""

    def update_plot(self):
        self.canvas.axes.cla()  # clear the axes content

        for element in self.to_plot:
            if element['type'] == "plot":
                self.canvas.axes.plot(element['x'], element['y'])

        if not self.title == "":
            self.canvas.title = self.title

        self.canvas.canvas.draw()  # actually draw the new content

    def update_plot_list(self, array):
        self.to_plot = array

        self.update_plot()



    def get_value(self):
        widget = self.get_custom_widget()
        return ''














class PltNode(GenericNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'plot input array'

    def __init__(self):
        super(PltNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Array', PortValueType.PD_DATAFRAME)
        
        self.add_custom_input('Title', PortValueType.STRING)
        
        self.add_custom_input('X_min', PortValueType.FLOAT)
        self.add_custom_input('X_max', PortValueType.FLOAT)
        
        self.add_custom_input('Y_min', PortValueType.FLOAT)
        self.add_custom_input('Y_max', PortValueType.FLOAT)
        
        self.add_checkbox("x_log", text='X log scale')
        self.add_checkbox("y_log", text='Y log scale')
        
        self.input_array = pd.DataFrame()

        self.plot_widget = pltWidget(self.view, name="plot")

        self.view.add_widget(self.plot_widget)
        self.view.draw_node()

        self.plot_widget.update_plot()

    def update_from_input(self):
        self.input_array = self.get_value_from_port("Input Array")

        print("**********************", self.input_array)
        # self.plot_widget.title = self.get_input("Title")

        self.plot_widget.update_plot_list([{'type':"plot", 'x':list(range(len(self.input_array))), 'y':self.input_array}])



    def check_inputs(self):
        print("////////////////////////////////     returned input:", self.get_value_from_port("Input Array"))
        self.set_property("is_valid", type(self.get_value_from_port("Input Array")) == pd.DataFrame)

        
    def get_property(self, name):
        if name == 'Input Array':
            return self.input_array

        return super().get_property(name)
    
    def set_property(self, name, value, push_undo=True):
        if name == 'Input Array':
            self.input_array = value
            
        else:
            return super().set_property(name, value, push_undo)
        