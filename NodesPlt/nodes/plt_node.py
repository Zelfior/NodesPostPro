from NodeGraphQt import BaseNode, BaseNodeCircle, NodeBaseWidget
from functools import wraps
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from NodeGraphQt.constants import NodePropWidgetEnum, PortTypeEnum

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)




class pltWidget(NodeBaseWidget):
    def __init__(self, parent=None, name=''):
        super(pltWidget, self).__init__()
        self.canvas = MplCanvas()
        self.canvas.setMinimumHeight(24)
        # combo.addItems(items or [])
        # combo.currentIndexChanged.connect(self.on_value_changed)
        # self.canvas.clearFocus()
        self.set_custom_widget(self.canvas)



    def update_plot(self):
        self.canvas.axes.plot([0,1,2,3], [0,1,2,3])
        self.canvas.draw()  # actually draw the new content
        # self.canvas.fig.canvas.draw_idle()  # actually draw the new content


class PltNode(BaseNode):



    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'plot input array'

    def __init__(self):
        super(PltNode, self).__init__()

        # create input & output ports
        self.add_input('Input Array', color=(0, 255, 0))

        self.input_array = None

        # self.add_plt_menu()

        # combo = MplCanvas()
        # combo.setMinimumHeight(24)
        # combo.addItems(items or [])
        # combo.currentIndexChanged.connect(self.on_value_changed)
        # combo.clearFocus()
        # self.set_custom_widget(combo)
        self.create_property(
            "plot",
            value=None,
            items=[],
            widget_type=NodePropWidgetEnum.QPLOT.value,
            tab=None
        )

        widget = pltWidget(self.view, name="plot")
        self.view.add_widget(widget)
        #: redraw node to address calls outside the "__init__" func.
        self.view.draw_node()

        widget.update_plot()

        # print(self.model.properties.keys())
        # print("view", self.view)

    def add_plt_menu(self):
        
        self.figure = MplCanvas(self, width=5, height=4, dpi=100)
        self.figure.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        # mainLayout = QtWidgets.QGridLayout()
        # mainLayout.addWidget(canvas1,1,0)

        # self.setLayout(mainLayout)

        self.view.add_widget(self.figure)
        #: redraw node to address calls outside the "__init__" func.
        self.view.draw_node()


    def update_model(self):
        super(PltNode, self).update_model()

        print("update_model")
    
    def update(self):
        super(PltNode, self).update()

        print("update")

    def set_model(self, model):
        super(PltNode, self).set_model()

        print("set_model")

    def set_property(self, name, value, push_undo=True):
        super(PltNode, self).set_property(name, value, push_undo=push_undo)

        print("Set property called")
        
    def on_input_connected(self, in_port, out_port):
        super(PltNode, self).on_input_connected(in_port, out_port)

        self.plugged_input_port = out_port

        self.update_from_input()

        print("on_input_connected", in_port, out_port, self._model.name)
        
    

    def on_input_disconnected(self, in_port, out_port):
        super(PltNode, self).on_input_disconnected(in_port, out_port)

        print("on_input_disconnected", in_port, out_port, self._model.name)

    def update_from_input(self):
        if self.plugged_input_port == None:
            pass
        else:
            if self.plugged_input_port.node().is_defined:
                self.is_defined = True
                self.input_array = self.plugged_input_port.node().output_array

                print("From plt node, input array", self.input_array)


        for output_id in range(len(self.outputs())):
            for connected_id in range(len(self.output(output_id).connected_ports())):
                self.output(output_id).connected_ports()[connected_id].node().update_from_input()