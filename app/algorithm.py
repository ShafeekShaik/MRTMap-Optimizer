import sys
import csv
import matplotlib.pyplot as plt
import networkx as nx
 
class Graph(object):
    def __init__(self, csv_file):
        self.nodes = self.read_nodes_from_csv(csv_file)
        self.graph = self.construct_graph(csv_file)
        
    def read_nodes_from_csv(self, csv_file):
        nodes = set()
        #node_coordinates = {}
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                source = row['Source']
                target = row['Target']
                nodes.add(source)
                nodes.add(target)
                #node_coordinates[source] = (float(row['Source_X']), float(row['Source_Y']))
                # You can set default coordinates for target nodes if needed
                #node_coordinates.setdefault(target, (0.0, 0.0))
        return list(nodes)
        
    def construct_graph(self, csv_file):
        graph = {}
        for node in self.nodes:
            
            graph[node] = {}

        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                source = row['Source']
                target = row['Target']
                weight = int(row['Weight'])

                if source not in graph:
                    graph[source] = {}
                if target not in graph:
                    graph[target] = {}

                graph[source][target] = weight
                graph[target][source] = weight
        return graph
    
    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]
        
def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())

    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0
    shortest_path[start_node] = 0

    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, {node: shortest_path[node] for node in previous_nodes if node != start_node}

    
def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    bruh = " -> ".join(reversed(path))

    return bruh



def visualize_graph(graph, shortest_path):
    G = nx.Graph()

    for node in graph.get_nodes():
        G.add_node(node)

    for source in graph.get_nodes():
        for target in graph.get_outgoing_edges(source):
            G.add_edge(source, target, weight=graph.value(source, target))

    pos = nx.spring_layout(G, seed=42)

    # Create a list of node colors, where the nodes in the shortest path are highlighted
    node_colors = ['red' if node  in shortest_path else 'lightblue' for node in G.nodes()]

    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5)
    plt.title("MRT Graph with Shosrtest Path")
    plt.axis("off")
    plt.show()


csv_file= "S:/SIT Tri 3/DSAG/Projec/hub/Project_input/Attendance/MRTMap-Optimizer/app/mrt.csv"
graph = Graph(csv_file)

def short_path(start,end):
    start_node = start
    target_node = end
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node = start_node)
    shortest_path = print_result(previous_nodes, shortest_path, start_node, target_node)
    return shortest_path





















# short_path("DT22 Jalan Besar", "DT33 Tampines East")

# nodes = graph.get_nodes()
# for i in nodes:
    # print(i)
#These two are where to input the start and end nodes should be the main concern
# node = 'CC10 DT26 MacPherson'  # Replace 'A' with the desired node

# neighbors = graph.get_outgoing_edges(node)

# print(f"Neighbors of node {node}:")
# for neighbor in neighbors:
#     print(neighbor)
	
#print_result(previous_nodes, shortest_path, start_node, target_node)
# print(shortest_path)
# visualize_graph(graph,shortest_path)
