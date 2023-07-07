from nodes.generic_node import GenericNode


def sort_propagation(nodes_heritage:dict):
    children_dict = {}

    node_list = []

    for node in nodes_heritage:
        children_dict[node["name"]] = node["children"]
        if not node["name"] in node_list:
            node_list.append(node["name"])

    unsorted_nodes = node_list.copy()
    node_order = []

    while len(unsorted_nodes) > 0:

        for i in range(len(unsorted_nodes)):
            node = unsorted_nodes[i]

            is_valid = True

            for child in children_dict[node]:
                if not child in node_order:
                    is_valid = False
            
            if is_valid:
                node_order.insert(0, node)
                del unsorted_nodes[i]
                break

    return node_order


def get_propagation_order(base_node:GenericNode):
    nodes_heritage = get_heritage(base_node, True)

    return sort_propagation(nodes_heritage)

def get_heritage(base_node:GenericNode, propagate:bool):
    children_list = [{"name": base_node.name(), "children": []}]

    for port_name in base_node.outputs():
        port = base_node.outputs()[port_name]
        if len(port.connected_ports()) > 0:
            for connected_port in port.connected_ports():
                if not connected_port.node().name() in children_list[0]["children"]:
                    children_list[0]["children"].append(connected_port.node().name())

                    if propagate:
                        children_list += get_heritage(connected_port.node(), propagate)

    return children_list

def get_children_dict(base_node:GenericNode, propagate=True):
    children_dict = {}

    for port_name in base_node.outputs():
        port = base_node.outputs()[port_name]
        if len(port.connected_ports()) > 0:
            for connected_port in port.connected_ports():
                if not connected_port.node().name() in children_dict:
                    children_dict[connected_port.node().name()]=connected_port.node()

                    if propagate:
                        new_node_children = get_children_dict(connected_port.node())

                        for node_name in new_node_children:
                            if not node_name in children_dict:
                                children_dict[node_name] = new_node_children[node_name]

    return children_dict
