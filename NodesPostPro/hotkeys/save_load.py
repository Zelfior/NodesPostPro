import os
import json

from NodeGraphQt.base.graph import NodeGraph, SubGraph
from NodeGraphQt.nodes.port_node import PortInputNode, PortOutputNode
from NodeGraphQt.base.commands import PortConnectedCmd
from NodeGraphQt.nodes.base_node import BaseNode

from NodesPostPro.nodes.node_heritage import *

def save_session(graph:NodeGraph, file_path):
    """
    Saves the current node graph session layout to a `JSON` formatted file.

    See Also:
        :meth:`NodeGraph.serialize_session`,
        :meth:`NodeGraph.deserialize_session`,
        :meth:`NodeGraph.load_session`,

    Args:
        file_path (str): path to the saved node layout.
    """
    #   Getting nodes order
    node_list = graph.all_nodes()

    node_children = []

    for node in node_list:
        node_children.append(get_heritage(node, propagate=False)[0])

    node_order = sort_propagation(node_children)

    #   Getting data
    serialized_data = graph._serialize(graph.all_nodes())

    #   Reordering data
    sorted_nodes = {}
    
    for node_name in node_order:
        for serial_node in serialized_data["nodes"]:
            if serialized_data["nodes"][serial_node]["name"] == node_name:
                sorted_nodes[serial_node] = serialized_data["nodes"][serial_node]

    serialized_data["nodes"] = sorted_nodes

    #   Saving
    file_path = file_path.strip()
    with open(file_path, 'w') as file_out:
        json.dump(
            serialized_data,
            file_out,
            indent=2,
            separators=(',', ':')
        )
        
def load_session(graph:NodeGraph, file_path):
    """
    Load node graph session layout file.

    See Also:
        :meth:`NodeGraph.deserialize_session`,
        :meth:`NodeGraph.serialize_session`,
        :meth:`NodeGraph.save_session`

    Args:
        file_path (str): path to the serialized layout file.
    """

    for node in graph.all_nodes():
        node.set_to_update(False)
        
    file_path = file_path.strip()
    if not os.path.isfile(file_path):
        raise IOError('file does not exist: {}'.format(file_path))

    graph.clear_session()
    import_session(graph, file_path)

    for node in graph.all_nodes():
        node.set_to_update(True)


def import_session(graph:NodeGraph, file_path):
    """
    Import node graph session layout file.

    Args:
        file_path (str): path to the serialized layout file.
    """

    print("custom import session")

    file_path = file_path.strip()
    if not os.path.isfile(file_path):
        raise IOError('file does not exist: {}'.format(file_path))

    try:
        with open(file_path) as data_file:
            layout_data = json.load(data_file)
    except Exception as e:
        layout_data = None
        print('Cannot read data from file.\n{}'.format(e))

    if not layout_data:
        return

    _deserialize(graph, layout_data)
    graph._undo_stack.clear()
    graph._model.session = file_path

    graph.session_changed.emit(file_path)
    
def get_node_data(data, node_name):
    for n_id, n_data in data.get('nodes', {}).items():
        if n_data["name"] == node_name:
            return n_data
    return

def _deserialize(graph, data, relative_pos=False, pos=None):
    """
    deserialize node data.
    (used internally by the node graph)

    Args:
        data (dict): node data.
        relative_pos (bool): position node relative to the cursor.
        pos (tuple or list): custom x, y position.

    Returns:
        list[NodeGraphQt.Nodes]: list of node instances.
    """
    # update node graph properties.
    for attr_name, attr_value in data.get('graph', {}).items():
        if attr_name == 'layout_direction':
            graph.set_layout_direction(attr_value)
        elif attr_name == 'acyclic':
            graph.set_acyclic(attr_value)
        elif attr_name == 'pipe_collision':
            graph.set_pipe_collision(attr_value)
        elif attr_name == 'pipe_slicing':
            graph.set_pipe_slicing(attr_value)
        elif attr_name == 'pipe_style':
            graph.set_pipe_style(attr_value)

        # connection constrains.
        elif attr_name == 'accept_connection_types':
            graph.model.accept_connection_types = attr_value
        elif attr_name == 'reject_connection_types':
            graph.model.reject_connection_types = attr_value

    ###
    #####
    #######
    ##      modif
    nodes_dict = {}

    for n_id, n_data in data.get('nodes', {}).items():
        nodes_dict[n_id] = n_data["name"]


    input_link_per_node = {}

    connections = data.get('connections', [])
    for connection in connections:
        nid_in, pname_in = connection.get('in', ('', ''))
        nid_out, pname_out = connection.get('out', ('', ''))

        if nodes_dict[nid_in] in input_link_per_node:
            input_link_per_node[nodes_dict[nid_in]].append(connection)
        else:
            input_link_per_node[nodes_dict[nid_in]]= [connection]

    ##      end modif
    #######
    #####
    ###

    # build the nodes.
    nodes = {}
    for n_id, n_data in data.get('nodes', {}).items():
        identifier = n_data['type_']
        node = graph._node_factory.create_node_instance(identifier)

        if node:
            node.NODE_NAME = n_data.get('name', node.NODE_NAME)
            
            nodes[n_id] = node
            node.set_to_update(False)
            ###     Creation des liens avec les nodes parent

            graph.add_node(node, n_data.get('pos'))

            # for prop in node.model.properties.keys():
            #     if prop in n_data.keys():
            #         node.model.set_property(prop, n_data[prop])
            # # set custom properties.
            # for prop, val in n_data.get('custom', {}).items():
            #     node.model.set_property(prop, val)
            #     if isinstance(node, BaseNode):
            #         if prop in node.view.widgets:
            #             node.view.widgets[prop].set_value(val)

            if n_data.get('port_deletion_allowed', None):
                node.set_ports({
                    'input_ports': n_data['input_ports'],
                    'output_ports': n_data['output_ports']
                })

    if relative_pos:
        graph._viewer.move_nodes([n.view for n in node_objs])
        [setattr(n.model, 'pos', n.view.xy_pos) for n in node_objs]
    elif pos:
        graph._viewer.move_nodes([n.view for n in node_objs], pos=pos)
        [setattr(n.model, 'pos', n.view.xy_pos) for n in node_objs]

                
    node_objs = nodes.values()

    for node in node_objs:
        print("Initializing", node.name())
        if node.name() in input_link_per_node:
            for connection in input_link_per_node[node.name()]:

                nid, pname = connection.get('in', ('', ''))
                in_node = nodes.get(nid) or graph.get_node_by_id(nid)

                if not in_node:
                    continue
                in_port = in_node.inputs().get(pname) if in_node else None


                nid, pname = connection.get('out', ('', ''))
                out_node = nodes.get(nid) or graph.get_node_by_id(nid)
                if not out_node:
                    continue
                out_port = out_node.outputs().get(pname) if out_node else None

                if in_port and out_port:
                    # only connect if input port is not connected yet or input port
                    # can have multiple connections.
                    # important when duplicating nodes.
                    allow_connection = any([not in_port.model.connected_ports,
                                            in_port.model.multi_connection])
                    if allow_connection:
                        graph._undo_stack.push(PortConnectedCmd(in_port, out_port))

                    # Run on_input_connected to ensure connections are fully set up after deserialization.
                    in_node.on_input_connected(in_port, out_port)

        node.set_to_update(True)
        node.update_values()
        node.set_to_update(False)

        n_data = get_node_data(data, node.name())

        for prop in node.model.properties.keys():
            if prop in n_data.keys():
                node.model.set_property(prop, n_data[prop])
        # set custom properties.
        for prop, val in n_data.get('custom', {}).items():
            node.model.set_property(prop, val)
            if isinstance(node, BaseNode):
                if prop in node.view.widgets:
                    node.view.widgets[prop].set_value(val)

        node.set_to_update(True)
        node.update_values()


    return node_objs