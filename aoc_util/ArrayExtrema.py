import networkx as nx
import numpy as np


def detect_local_minima(array2d):
    """
    Takes a 2D array and returns a boolean mask of the local minima positions
    """
    # Add a border around the existing array to ensure minima can be found on the borders
    bordered_array = np.pad(array2d, pad_width=1, mode='constant', constant_values=np.max(array2d))

    # Construct boolean mask of local minima locations
    minima_spots = ((bordered_array < np.roll(bordered_array,  1, 0)) &
                    (bordered_array < np.roll(bordered_array, -1, 0)) &
                    (bordered_array < np.roll(bordered_array,  1, 1)) &
                    (bordered_array < np.roll(bordered_array, -1, 1)))

    # Remove border added previously
    for axis in [0, 1]:
        minima_spots = np.delete(minima_spots, [0, -1], axis=axis)

    return minima_spots


def detect_basin_size(height_array):
    # Get array of all position combinations? maybe?
    height_mgrid = np.mgrid[0:height_array.shape[0], 0:height_array.shape[1]]
    node_array = np.moveaxis(height_mgrid, 0, 2)

    # Construct graph, removing nodes of 9
    Graph = nx.grid_graph(height_array.shape[::-1])
    Graph.remove_nodes_from(map(tuple, node_array[height_array == 9]))

    # Split graph into distinct basins, each with a length equal to its size
    basin_connections = nx.connected_components(Graph)

    # Calculate product of top 3 basin sizes
    pzl_soln = np.product(sorted(map(len, basin_connections))[-3:])
    return pzl_soln