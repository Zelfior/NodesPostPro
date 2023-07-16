from NodesPostPro.nodes.generic_node import GenericNode, PortValueType, check_cast_type_from_string
from Qt import QtWidgets, QtCore, QtGui
import matplotlib



class InputColorNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Input'

    # initial default node name.
    NODE_NAME = 'Color'

    def __init__(self):
        super(InputColorNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.COLOR)

        #   create QLineEdit text input widget for the file path
        # color_picker = self.add_color_picker_input('Value', 'Value')
        self.button = self.add_button_widget(name="       ")

        self.color = [255, 0, 0]

        self.button.set_link(self.select_color)
        self.button.button_widget.setStyleSheet("background-color : rgb"+str(tuple(self.color)))

    def select_color(self):
        self.color = list(QtWidgets.QColorDialog.getColor().getRgb()[0:3])
        self.button.button_widget.setStyleSheet("background-color : rgb"+str(tuple(self.color)))
        self.update_values()

    def check_inputs(self):
        self.set_property("is_valid",True)

    def update_from_input(self):
        self.get_output_property("Output Value").set_property('#{:02x}{:02x}{:02x}'.format(self.color[0], self.color[1], self.color[2]))



class ColorMapPickerNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Color'

    # initial default node name.
    NODE_NAME = 'Colormap'

    def __init__(self):
        super(ColorMapPickerNode, self).__init__()

        self.add_combo_menu("Color map", "Color map", ["viridis", "plasma", "inferno", "magma", "cividis", "Greys"])
        self.add_twin_input("Factor", PortValueType.FLOAT)

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.COLOR)

        self.add_label("Information")

        self.is_iterated_compatible = True

    def check_function(self, input_dict, first=False):
        if not "Color map" in input_dict or ("is not defined" in input_dict["Color map"]):
            return False, "Input Factor is not valid", "Information"
        
        if not "Factor" in input_dict or type(input_dict["Factor"]) == str:
            return False, "Input Factor is not valid", "Information"
        
        if (not input_dict["Factor"] <= 1.) or (not input_dict["Factor"] >= 0.):
            return False, "Factor should be between 0. and 1.", "Information"
    
        return True, "", "Information"


    def update_function(self, input_dict, first=False):
        
        cmap = matplotlib.cm.get_cmap(input_dict["Color map"])

        rgba = cmap(input_dict["Factor"])

        output_dict = {'Output Value': '#{:02x}{:02x}{:02x}'.format(int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255))}
        output_dict["__message__Information"] = "Color hexa: "+output_dict["Output Value"]
        return output_dict