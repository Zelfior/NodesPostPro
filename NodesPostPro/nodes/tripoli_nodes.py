from NodesPostPro.nodes.generic_node import GenericNode, PortValueType

import numpy as np
import os



class tripoli_postpro():


    def read_data(self, file_name):
        self.all_data_value = []
        self.all_data_sigma = []

        lines_output = {}
        file_name = file_name.replace("_value.general", "").replace("_sigma.general", "")

        for val in ["_value.general", "_sigma.general"]:
            lines_output[file_name] = []
            file_input = open(file_name+val, "r")

            Lines = file_input.readlines()

            file_input.close()

            data = []

            data_started = False
            for line in range(0,len(Lines)):
                if data_started:
                    data.append(float(Lines[line].replace("\n","")))

                elif Lines[line].startswith("grid"):
                    coords = Lines[line].split("=")[-1].split(" x ")

                    for j in range(0,len(coords)):
                        coords[j] = int(coords[j])

                    self.square_width = coords[0] - 1
                    self.square_depth = coords[1] - 1
                    self.square_height = coords[2] - 1

                    
                elif Lines[line].startswith("positions"):
                    list_coord = Lines[line].split("=")[-1].split(",")[3:]

                    for j in range(0,len(list_coord)):
                        list_coord[j] = float(list_coord[j])

                    self.cell_x_coordinates = []
                    self.cell_y_coordinates = []
                    self.cell_z_coordinates = []
                    
                    self.cell_x_bounds = []
                    self.cell_y_bounds = []
                    self.cell_z_bounds = []

                    for j in range(0, self.square_width):
                        self.cell_x_coordinates.append((list_coord[j]+list_coord[j+1])/2)

                        self.cell_x_bounds.append(list_coord[j])
                    self.cell_x_bounds.append(list_coord[j+1])

                    for j in range(0, self.square_depth):
                        self.cell_y_coordinates.append((list_coord[j+self.square_width+1]+list_coord[j+1+self.square_width+1])/2)

                        self.cell_y_bounds.append(list_coord[j+self.square_width+1])
                    self.cell_y_bounds.append(list_coord[j+1+self.square_width+1])

                    for j in range(0, self.square_height):
                        self.cell_z_coordinates.append((list_coord[j+self.square_width+self.square_depth+2]+list_coord[j+1+self.square_width+self.square_depth+2])/2)

                        self.cell_z_bounds.append(list_coord[j+self.square_width+self.square_depth+2])
                    self.cell_z_bounds.append(list_coord[j+1+self.square_width+self.square_depth+2])

                elif Lines[line].replace("\n","") == "Data":
                    data_started = True
                    lines_output[file_name].append(Lines[line].replace("\n",""))
                else:
                    lines_output[file_name].append(Lines[line].replace("\n",""))

            if "value" in val:
                self.all_data_value.append(data)
            elif "sigma" in val:
                self.all_data_sigma.append(data)

        self.all_data_value = np.array(self.all_data_value)[0]
        self.all_data_sigma = np.array(self.all_data_sigma)[0]

        len_x = len(self.cell_x_coordinates)
        len_y = len(self.cell_y_coordinates)
        len_z = len(self.cell_z_coordinates)

        self.data_value = self.all_data_value.reshape([len_z, len_y, len_x], order = "C")
        self.data_sigma = self.all_data_sigma.reshape([len_z, len_y, len_x], order = "C")

        self.data_value = np.transpose(self.data_value, (2, 1, 0))
        self.data_sigma = np.transpose(self.data_sigma, (2, 1, 0))

        self.cell_x_coordinates = np.array(self.cell_x_coordinates)
        self.cell_y_coordinates = np.array(self.cell_y_coordinates)
        self.cell_z_coordinates = np.array(self.cell_z_coordinates)
        
        self.cell_x_bounds = np.array(self.cell_x_bounds)
        self.cell_y_bounds = np.array(self.cell_y_bounds)
        self.cell_z_bounds = np.array(self.cell_z_bounds)



class TripoliExtendedMeshNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Tripoli'

    # initial default node name.
    NODE_NAME = 'Extended mesh'

    def __init__(self):
        super(TripoliExtendedMeshNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Value Array', PortValueType.NP_ARRAY)
        self.add_custom_output('Sigma Array', PortValueType.NP_ARRAY)
        
        self.add_custom_output('X bounds', PortValueType.NP_ARRAY)
        self.add_custom_output('Y bounds', PortValueType.NP_ARRAY)
        self.add_custom_output('Z bounds', PortValueType.NP_ARRAY)
        
        self.add_custom_output('X centers', PortValueType.NP_ARRAY)
        self.add_custom_output('Y centers', PortValueType.NP_ARRAY)
        self.add_custom_output('Z centers', PortValueType.NP_ARRAY)

        self.button = self.add_button_widget("Browse file")
        self.button.set_link(self.get_file_name)
        
        #   create QLineEdit text input widget for the file path
        file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        example_path = os.path.join(file_path, 'example_files','exemple_value.general')
        self.add_twin_input('Filename', PortValueType.STRING, default = example_path)


        self.add_label("Size array")
        self.change_label("Size array", "Load file to display size", False)
        self.add_label("Size X bounds")
        self.add_label("Size Y bounds")
        self.add_label("Size Z bounds")
        self.add_label("Size X centers")
        self.add_label("Size Y centers")
        self.add_label("Size Z centers")

        self.TP = tripoli_postpro()

        self.is_iterated_compatible = True

        self.update_values()


    def check_function(self, input_dict, first = False):
        if (not "Filename" in input_dict) or ("is not defined" in input_dict["Filename"]):
            self.change_label("Size X bounds" , "", False)
            self.change_label("Size Y bounds" , "", False)
            self.change_label("Size Z bounds" , "", False)
            self.change_label("Size X centers", "", False)
            self.change_label("Size Y centers", "", False)
            self.change_label("Size Z centers", "", False)
            return False, "Filename is not valid", "Size array"
        
        if not os.path.isfile(input_dict["Filename"]):
            self.change_label("Size X bounds" , "", False)
            self.change_label("Size Y bounds" , "", False)
            self.change_label("Size Z bounds" , "", False)
            self.change_label("Size X centers", "", False)
            self.change_label("Size Y centers", "", False)
            self.change_label("Size Z centers", "", False)
            return False, "No file at given path", "Size array"
    
        return True, "", "Size array"

    def update_function(self, input_dict, first=False):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path

        self.TP.read_data(input_dict["Filename"])

        output_dict = {"Value Array":self.TP.data_value,
                       "Sigma Array":self.TP.data_sigma,
                       "X bounds":self.TP.cell_x_bounds,
                       "Y bounds":self.TP.cell_y_bounds,
                       "Z bounds":self.TP.cell_z_bounds,
                       "X centers":self.TP.cell_x_coordinates,
                       "Y centers":self.TP.cell_y_coordinates,
                       "Z centers":self.TP.cell_z_coordinates}

        output_dict["__message__Size array"] = "Array shape "+str(self.TP.data_value.shape)
        output_dict["__message__Size X bounds"] = "X bounds shape "+str(self.TP.cell_x_bounds.shape)
        output_dict["__message__Size Y bounds"] = "Y bounds shape "+str(self.TP.cell_y_bounds.shape)
        output_dict["__message__Size Z bounds" ] = "Z bounds shape "+str(self.TP.cell_z_bounds.shape)
        output_dict["__message__Size X centers"] = "X centers shape "+str(self.TP.cell_x_coordinates.shape)
        output_dict["__message__Size Y centers"] = "Y centers shape "+str(self.TP.cell_y_coordinates.shape)
        output_dict["__message__Size Z centers"] = "Z centers shape "+str(self.TP.cell_z_coordinates.shape)

        return output_dict