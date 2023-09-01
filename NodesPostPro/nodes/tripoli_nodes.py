from NodesPostPro.nodes.generic_node import GenericNode, PortValueType

import numpy as np
import os
import functools



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

    def set_value(self, data):
        self.data_value = data

    def set_sigma(self, data):
        self.data_sigma = data


class TripoliExtendedMeshSerieNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Tripoli'

    # initial default node name.
    NODE_NAME = 'Extended mesh serie'

    def __init__(self):
        super(TripoliExtendedMeshSerieNode, self).__init__()

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
        self.button.set_link(functools.partial(self.get_file_name, "general"))
        
        #   create QLineEdit text input widget for the file path
        file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        example_path = os.path.join(file_path, 'example_files','exemple.t4_0_0_0_value.general')
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

        file_name_truncated = "_".join(input_dict["Filename"].split("_")[:-2])
        files_base_name = []

        i = 0

        while os.path.isfile(file_name_truncated+"_"+str(i)+"_value.general"):
            files_base_name.append(file_name_truncated+"_"+str(i))
            i+=1
        
        if len(files_base_name) == 1:
            self.TP.read_data(input_dict["Filename"])
        else:
            values = []
            sigmas = []

            for filename in files_base_name:
                print("reading", filename)
                self.TP.read_data(filename)

                values.append(self.TP.data_value)
                sigmas.append(self.TP.data_sigma)

            self.TP.set_value(np.stack(values, axis = -1))
            self.TP.set_sigma(np.stack(sigmas, axis = -1))

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



class AP281Node(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Tripoli'

    # initial default node name.
    NODE_NAME = 'Apollo 281'

    def __init__(self):
        super(AP281Node, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Groups bounds', PortValueType.NP_ARRAY)
        self.add_custom_output('Groups centers', PortValueType.NP_ARRAY)
        self.add_custom_output('Groups widths', PortValueType.NP_ARRAY)

        self.add_label("Size Groups bounds")
        self.add_label("Size Groups centers")
        self.add_label("Size Groups widths")

        self.ap281 = np.array([1.00000E-5, 1.1000E-04, 2.4999E-03, 4.5560E-03, 7.1453E-03, 1.0451E-02, 1.4830E-02, 2.0010E-02, 
                2.4940E-02, 2.9299E-02, 3.4400E-02, 4.0300E-02, 4.7302E-02, 5.5498E-02, 6.5199E-02, 7.6497E-02, 
                8.9797E-02, 1.0430E-01, 1.2000E-01, 1.3800E-01, 1.6190E-01, 1.9001E-01, 2.0961E-01, 2.3119E-01, 
                2.5500E-01, 2.7999E-01, 3.0501E-01, 3.2501E-01, 3.5299E-01, 3.9000E-01, 4.3158E-01, 4.7502E-01, 
                5.2001E-01, 5.5499E-01, 5.9499E-01, 6.2500E-01, 7.2000E-01, 8.2004E-01, 8.8003E-01, 9.1998E-01, 
                9.4402E-01, 9.6396E-01, 9.8196E-01, 9.9650E-01, 1.0090E00, 1.0210E00, 1.0350E00, 1.0780E00, 1.0920E00, 
                1.1040E00, 1.1161E00, 1.1300E00, 1.1480E00, 1.1700E00, 1.2140E00, 1.2509E00, 1.2930E00, 1.3310E00, 
                1.3810E00, 1.4100E00, 1.4440E00, 1.5200E00, 1.5880E00, 1.6690E00, 1.7800E00, 1.9001E00, 1.9899E00, 
                2.0701E00, 2.1570E00, 2.2171E00, 2.2730E00, 2.3301E00, 2.4699E00, 2.5500E00, 2.5901E00, 2.6201E00, 
                2.6400E00, 2.7001E00, 2.7199E00, 2.7409E00, 2.7751E00, 2.8841E00, 3.1421E00, 3.5431E00, 3.7121E00, 
                3.8822E00, 4.0000E00, 4.2198E00, 4.3098E00, 4.4198E00, 4.7679E00, 4.9332E00, 5.1100E00, 5.2101E00, 
                5.3201E00, 5.3800E00, 5.4103E00, 5.4882E00, 5.5300E00, 5.6198E00, 5.7202E00, 5.8002E00, 5.9602E00, 
                6.0599E00, 6.1601E00, 6.2802E00, 6.3598E00, 6.4321E00, 6.4818E00, 6.5149E00, 6.5391E00, 6.5561E00, 
                6.5719E00, 6.5883E00, 6.6061E00, 6.6313E00, 6.7167E00, 6.7423E00, 6.7598E00, 6.7761E00, 6.7917E00, 
                6.8107E00, 6.8353E00, 6.8702E00, 6.9178E00, 6.9943E00, 7.1399E00, 7.3802E00, 7.6004E00, 7.7400E00, 
                7.8397E00, 7.9701E00, 8.1303E00, 8.3003E00, 8.5241E00, 8.6737E00, 8.8004E00, 8.9800E00, 9.1403E00, 
                9.5000E00, 1.0579E01, 1.0804E01, 1.1053E01, 1.1270E01, 1.1590E01, 1.1709E01, 1.1815E01, 1.1980E01, 
                1.2130E01, 1.2309E01, 1.2472E01, 1.2600E01, 1.3330E01, 1.3546E01, 1.4050E01, 1.4251E01, 1.4470E01, 
                1.4595E01, 1.4730E01, 1.4866E01, 1.5779E01, 1.6050E01, 1.6550E01, 1.6831E01, 1.7446E01, 1.7565E01, 
                1.7759E01, 1.7959E01, 1.9085E01, 1.9200E01, 1.9393E01, 1.9597E01, 2.0073E01, 2.0275E01, 2.0418E01, 
                2.0520E01, 2.0602E01, 2.0685E01, 2.0768E01, 2.0976E01, 2.1060E01, 2.1145E01, 2.1230E01, 2.1336E01, 
                2.1486E01, 2.1702E01, 2.2001E01, 2.2156E01, 2.2378E01, 2.2524E01, 2.4589E01, 2.7608E01, 3.3720E01, 
                4.0169E01, 4.3996E01, 4.5791E01, 5.2673E01, 6.1442E01, 7.5046E01, 8.8952E01, 1.0865E02, 1.3270E02, 
                1.6208E02, 1.9797E02, 2.4180E02, 2.8375E02, 3.1993E02, 3.5358E02, 4.1080E02, 5.0175E02, 6.1284E02, 
                7.4852E02, 9.0750E02, 1.0650E03, 1.1350E03, 1.3451E03, 1.6140E03, 1.9105E03, 2.2196E03, 2.5788E03, 
                2.9962E03, 3.4811E03, 4.0974E03, 5.0045E03, 6.1125E03, 7.4659E03, 9.1188E03, 1.1138E04, 1.3604E04, 
                1.4900E04, 1.6201E04, 1.8585E04, 2.2699E04, 2.4999E04, 2.6100E04, 2.7394E04, 2.9281E04, 3.3460E04, 
                3.6979E04, 4.0868E04, 4.9916E04, 5.5166E04, 6.7380E04, 8.2298E04, 9.4665E04, 1.1562E05, 1.2277E05, 
                1.4000E05, 1.6500E05, 1.9501E05, 2.3001E05, 2.6783E05, 3.2065E05, 3.8388E05, 4.1250E05, 4.5602E05, 
                4.9400E05, 5.7844E05, 7.0651E05, 8.6001E05, 9.5112E05, 1.0512E06, 1.1621E06, 1.2870E06, 1.3369E06, 
                1.4058E06, 1.6365E06, 1.9014E06, 2.2313E06, 2.7253E06, 3.3287E06, 4.0657E06, 4.9659E06, 6.0653E06, 
                6.7032E06, 7.4082E06, 8.1873E06, 9.0484E06, 1.0000E07, 1.1618E07, 1.3840E07, 1.4918E07, 1.9640E07, 1.00E11])

        self.ap281_groups = np.array([0.5*(self.ap281[i]+self.ap281[i+1]) for i in range(0,len(self.ap281) - 1)])
        self.ap281_width = np.array([(self.ap281[i+1]-self.ap281[i]) for i in range(0,len(self.ap281) - 1)])

        self.update_values()

    def check_function(self, input_dict, first=False):
        return True, "", ""
    
    def update_function(self, input_dict, first=False):

        output_dict = {}

        output_dict["Groups bounds"] = self.ap281
        output_dict["Groups centers"] = self.ap281_groups
        output_dict["Groups widths"] = self.ap281_width

        output_dict["__message__Size Groups bounds"] = "Bounds shape "+str(self.ap281.shape)
        output_dict["__message__Size Groups centers"] = "Bounds shape "+str(self.ap281_groups.shape)
        output_dict["__message__Size Groups widths"] = "Bounds shape "+str(self.ap281_width.shape)

        return output_dict



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