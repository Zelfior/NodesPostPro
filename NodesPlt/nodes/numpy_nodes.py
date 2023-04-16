from NodeGraphQt import BaseNode, BaseNodeCircle
from functools import wraps
from nodes.generic_node import GenericNode, PortValueType
from NodeGraphQt import BaseNode, NodeBaseWidget
from Qt import QtWidgets

import numpy as np
import os




class IntSelectorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, name=''):
        super(IntSelectorWidget, self).__init__(parent)

        self.val_min = 0
        self.val_max = 0

        self.int_selector = QtWidgets.QSpinBox(self)
        self.int_selector.setRange(self.val_min, self.val_max)
        self.int_selector.setSingleStep(1)
        self.int_selector.setValue(0)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.addWidget(self.int_selector)


    def set_range(self, val_min, val_max):
        if self.get_value() > val_max:
            self.set_value(val_max)
        if self.get_value() < val_min:
            self.set_value(val_min)

        self.val_min = val_min
        self.val_max = val_max

        self.int_selector.setRange(val_min, val_max)

    def get_value(self):
        return self.int_selector.value()

    def get_range(self):
        return [self.val_min, self.val_max]

    def set_value(self, value):
        return self.int_selector.setValue(value)
    


class IntSelector_Widget(NodeBaseWidget):
    def __init__(self, parent=None, name='', label=''):
        super(IntSelector_Widget, self).__init__(parent)

        # set the name for node property.
        self.set_name(name)

        # set the label above the widget.
        self.set_label(label)

        self.int_selector_widget = IntSelectorWidget(name = name)

        self.int_selector_widget.int_selector.valueChanged.connect(self.on_value_changed)

        self.set_custom_widget(self.int_selector_widget)

    def get_value(self):
        return self.int_selector_widget.get_value()

    def get_range(self):
        return self.int_selector_widget.get_range()

    def set_range(self, val_min, val_max):
        return self.int_selector_widget.set_range(val_min, val_max)
    

class SetAxisNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Numpy'

    # initial default node name.
    NODE_NAME = 'Set axis'

    def __init__(self):
        super(SetAxisNode, self).__init__()

        #   Create input port for input dataframe
        self.add_custom_input('Input Array', PortValueType.NP_ARRAY)

        #   Create output ports for :
        #       The output dataframe corresponding to the given column
        #       The selected column name
        self.add_custom_output('Output Array', PortValueType.NP_ARRAY)

        #   Create the QComboBox menu to select the desired column.

        self.axis_widget = IntSelector_Widget(self.view, name="Axis", label='Axis to set')
        self.value_widget = IntSelector_Widget(self.view, name="Value", label='Axis value')

        self.axis_widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.value_widget.value_changed.connect(lambda k, v: self.set_property(k, v))

        self.view.add_widget(self.axis_widget)
        self.view.draw_node()
        self.view.add_widget(self.value_widget)
        self.view.draw_node()

        self.add_label("Information")


    def check_inputs(self):
        input_given = self.get_value_from_port("Input Array")
        
        #   Checks if the Input DataFrame is:
        #       -   plugged
        #       -   defined (if the previous node has its outputs defined)
        #       -   is a pandas DataFrame
        self.set_property("is_valid", input_given is not None \
                                            and input_given.is_defined() \
                                                and input_given.get_property_type() == PortValueType.NP_ARRAY)
        
        if input_given is None or not input_given.is_defined():
            self.change_label("Information", "Input not plugged to valid Array.", True)
        elif not input_given.get_property_type() == PortValueType.NP_ARRAY:
            self.change_label("Information", "Plugged port is not a Array.", True)
    
    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       -   If the combo widget labels are different from the DataFrame columns, we update the combo widget
        #       -   The "Output DataFrame" output becomes the column asked as a DataFrame
        # if list(self.get_value_from_port("Input DataFrame").get_property().columns) != self.view.widgets["Column name"].all_items():
        #     self.view.widgets["Column name"].clear()
        #     self.view.widgets["Column name"].add_items(list(self.get_value_from_port("Input DataFrame").get_property().columns))

        if self.axis_widget.get_range()[-1] != len(self.get_value_from_port("Input Array").get_property().shape) - 1:
            self.axis_widget.set_range(0, len(self.get_value_from_port("Input Array").get_property().shape) - 1)

            
        if self.value_widget.get_range()[-1] != self.get_value_from_port("Input Array").get_property().shape[self.axis_widget.get_value()] - 1:
            self.value_widget.set_range(0, self.get_value_from_port("Input Array").get_property().shape[self.axis_widget.get_value()] - 1)

        self.set_output_property('Output Array', np.take(self.get_value_from_port("Input Array").get_property(), self.value_widget.get_value(), self.axis_widget.get_value()))
        
        self.change_label("Information", "Output shape : "+str(self.get_output_property("Output Array").get_property().shape), False)

    def reset_outputs(self):
        super(SetAxisNode, self).reset_outputs()

        #   If this node is reseted, the combo widget also needs to be cleared
        # self.view.widgets["Column name"].clear()
        # self.view.widgets["Column name"].add_items([])

