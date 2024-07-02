import re
import pm4py
import pydotplus
from pydotplus.graphviz import Dot
from pm4py.visualization.dfg import visualizer as dfg_visualizer
from pm4py.util import constants
from pm4py.objects.dfg.obj import DFG
from IPython.display import display, Image

def view_graphviz_dfg(dfg, edge_markings=[]):
    """
    Visualizes a Directly-Follows Graph (DFG) using Graphviz with highlighted edges.

    Parameters:
        dfg (tuple): Tuple containing DFG object, start activities, and end activities.
        edge_markings (list): List of EdgeMarking objects specifying edge colors.
    """
    gviz_graph = dfg_to_gviz_digraph(dfg[0], dfg[1], dfg[2])

    dot = gviz_to_dot(gviz_graph)

    for edge_marking in edge_markings:
        dot = dot_change_edge_color(dot, edge_marking.src, edge_marking.dest, edge_marking.color)

    display(Image(dot.create_png()))

def gviz_to_dot(gviz):
    """
    Converts a Graphviz object to a Dot object.

    Parameters:
        gviz: Graphviz object to convert.

    Returns:
        Dot: Converted Dot object.
    """
    gviz_dot = gviz.source
    # remove leading minus ('-') from node labels as pydotplus cannot read such labels in Dot language
    gviz_dot = re.sub(r"-\d", "", gviz_dot)
    dot = pydotplus.graph_from_dot_data(gviz_dot)
    return dot

def dfg_to_gviz_digraph(dfg: DFG, start_activities: dict, end_activities: dict):
    """
    Converts a Directly-Follows Graph (DFG) to a Graphviz object.

    Parameters:
        dfg (DFG): Directly-Follows Graph object.
        start_activities (dict): Dictionary containing start activities.
        end_activities (dict): Dictionary containing end activities.

    Returns:
        Graphviz: Converted Graphviz object.
    """
    dfg_parameters = dfg_visualizer.Variants.FREQUENCY.value.Parameters
    parameters = {}
    parameters[dfg_parameters.FORMAT] = constants.DEFAULT_FORMAT_GVIZ_VIEW
    parameters[dfg_parameters.START_ACTIVITIES] = start_activities
    parameters[dfg_parameters.END_ACTIVITIES] = end_activities
    parameters["bgcolor"] = 'white'
    gviz = dfg_visualizer.apply(dfg, variant=dfg_visualizer.Variants.FREQUENCY,
                                parameters=parameters)
    return gviz

def dot_change_edge_color(dot: Dot, src_label:str, dst_label: str, color_name: str) -> Dot:
    """
    Changes the color of an edge between source and destination nodes in a Dot object.

    Parameters:
        dot (Dot): Dot object to modify.
        src_label (str): Label of the source node.
        dst_label (str): Label of the destination node.
        color_name (str): Name of the color (e.g., 'red', no color code).

    Returns:
        Dot: Modified Dot object.
    """
    for edge in dot.get_edge_list():
        src = edge.get_source()
        src_node = get_node_by_name(dot, src)
        dst = edge.get_destination()
        dst_node = get_node_by_name(dot, dst)
        edge_src_label = src_node.get_label().replace("\"", '')
        edge_dst_label = dst_node.get_label().replace("\"", '')
        if (src_label in edge_src_label) and (dst_label in edge_dst_label):
            edge.set_color(color_name)
    return dot

def get_node_by_name(dot: Dot, node_name: str):
    """
    Gets a node within a Dot object by its name.

    Parameters:
        dot (Dot): Dot object to search within.
        node_name (str): Name of the node to find.

    Returns:
        Dot: Node with the specified name if found, None otherwise.
    """
    for node_i in dot.get_node_list():
        if node_i.get_name()==node_name:
            return node_i
    return None