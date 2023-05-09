from nodes.generic_node import GenericNode, PortValueType, check_cast_type_from_string

import random
    

class RandomUniformNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Random'

    # initial default node name.
    NODE_NAME = 'Uniform'

    def __init__(self):
        super(RandomUniformNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.FLOAT)

        self.add_twin_input("Min", PortValueType.FLOAT, default = "0.")
        self.add_twin_input("Max", PortValueType.FLOAT, default = "1.")

        self.add_label("Information", "")


    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid", True)

        for twin in self.twin_inputs:
            valid, message = self.is_twin_input_valid(twin)

            self.set_property("is_valid", valid and self.get_property("is_valid"))

            if not valid:
                self.change_label("Information", message, True)

        if self.get_property("is_valid"):
            if float(self.get_twin_input("Min").get_property()) > float(self.get_twin_input("Max").get_property()):
                self.set_property("is_valid", False)
                self.change_label("Information", "Max should be greater than Min.", True)


    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Output Value").set_property(random.uniform(float(self.get_twin_input("Min").get_property()),float(self.get_twin_input("Max").get_property())))
        self.change_label("Information", str(self.get_output_property("Output Value").get_property()), False)



class RandomIntegerNode(GenericNode):
    """
        Node giving a float as output.
    """

    # unique node identifier.
    __identifier__ = 'Random'

    # initial default node name.
    NODE_NAME = 'Random Integer'

    def __init__(self):
        super(RandomIntegerNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Value', PortValueType.INTEGER)

        self.add_twin_input("Min", PortValueType.INTEGER, default = "0")
        self.add_twin_input("Max", PortValueType.INTEGER, default = "1")

        self.add_label("Information", "")

        self.is_iterated_compatible = True


    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if the string is a float
        self.set_property("is_valid", True)

        for twin in self.twin_inputs:
            valid, message = self.is_twin_input_valid(twin)

            self.set_property("is_valid", valid and self.get_property("is_valid"))

            if not valid:
                self.change_label("Information", message, True)

        if self.get_property("is_valid"):
            is_min_iterator = self.get_twin_input("Min").is_iterated()
            is_max_iterator = self.get_twin_input("Max").is_iterated()

            if is_max_iterator or is_min_iterator:
                is_valid = True

                if self.get_property("is_valid"):

                    if is_min_iterator:
                        min_array = self.get_twin_input("Min").get_iterated_property()
                    else:
                        min_array = [int(self.get_twin_input("Min").get_property())]*len(self.get_twin_input("Max").get_iterated_property())

                    if is_max_iterator:
                        max_array = self.get_twin_input("Max").get_iterated_property()
                    else:
                        max_array = [int(self.get_twin_input("Max").get_property())]*len(self.get_twin_input("Min").get_iterated_property())

                    for i in range(len(max_array)):
                        if max_array[i] < min_array[i]:
                            is_valid = False

                if not is_valid:
                    self.set_property("is_valid", False)
                    self.change_label("Information", "Max should be greater than Min.", True)


    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        is_min_iterator = self.get_twin_input("Min").is_iterated()
        is_max_iterator = self.get_twin_input("Max").is_iterated()

        print(is_min_iterator, is_max_iterator)

        if is_max_iterator or is_min_iterator:
            if is_min_iterator:
                min_array = self.get_twin_input("Min").get_iterated_property()
            else:
                min_array = [int(self.get_twin_input("Min").get_property())]*len(self.get_twin_input("Max").get_iterated_property())

            if is_max_iterator:
                max_array = self.get_twin_input("Max").get_iterated_property()
            else:
                max_array = [int(self.get_twin_input("Max").get_property())]*len(self.get_twin_input("Min").get_iterated_property())

            self.set_output_property("Output Value", [random.randint(min_array[i],max_array[i]) for i in range(len(min_array))], True)
            self.change_label("Information", str(self.get_output_property("Output Value").get_iterated_property()[0])+" x "+str(len(min_array)), False)
        else:
            self.set_output_property("Output Value", random.randint(int(self.get_twin_input("Min").get_property()),int(self.get_twin_input("Max").get_property())), False)
            self.change_label("Information", str(self.get_output_property("Output Value").get_property()), False)
