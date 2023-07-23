import sys
import csv
import matplotlib.pyplot as plt
import networkx as nx
import folium
from config import basedir
import os
class Graph(object):
    def __init__(self, csv_file):
        self.nodes = set()
        self.node_coordinates = {}
        self.graph = self.construct_graph(csv_file)

    def construct_graph(self, csv_file):
        graph = {}

        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the first row (column headers)
            for row in reader:
                node = row[0]
                neighbor = row[1]
                weight = int(row[2])
                node_x = float(row[3])
                node_y = float(row[4])
                walk = row[5]

                self.nodes.add(node)
                #self.nodes.add(neighbor)
                self.node_coordinates[node] = (node_x, node_y)
                #self.node_coordinates[neighbor] = (node_x, node_y)
                
                if node not in graph:
                    graph[node] = {}
                if neighbor not in graph:
                    graph[neighbor] = {}

                graph[node][neighbor] = {"weight": weight, "walk": walk}
                graph[neighbor][node] = {"weight": weight, "walk": walk}

        return graph
        
    def get_nodes(self):
        return self.nodes

    def get_outgoing_edges(self, node):
        connections = []
        if node in self.graph:
            connections = list(self.graph[node].keys())
        return connections
    
    def value(self, node1, node2):
        if node1 in self.graph and node2 in self.graph[node1]:
            return self.graph[node1][node2]["weight"], self.graph[node1][node2]["walk"]
        else:
            return None, None

    
        
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
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)[0]
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, {node: shortest_path[node] for node in previous_nodes if node != start_node}

    
def print_result(previous_nodes, shortest_path, start_node, target_node, graph):
    path = []
    total_time = 0
    total_walk_time = 0
    node = target_node

    while node != start_node:
        path.append(node)
        prev_node = previous_nodes[node]
        time, walk = graph.value(prev_node, node)
        total_time += time
        if walk == "Y":
            total_walk_time += time
        node = prev_node

    # Add the start node manually
    path.append(start_node)

    # Reverse the path to get the correct order
    path = list(reversed(path))

    timing = "The following journey will take {} minutes long, including {} minutes of walking.".format(shortest_path[target_node], total_walk_time)
    # print("Path:")
    path_taken = f"{path[0]}"
    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        distance, walk = graph.value(from_node, to_node)

        if walk == "Y":
            path_taken += f" -- walk to --> {to_node}"
        else:
            path_taken += f" --> {to_node}"
            
    fol_path = " -> ".join(path)
    # path_taken += "Total Time: {} km".format(total_time)
    # path_taken += "Total Walk Time: {} km".format(total_walk_time)
    # return " -> ".join(path)
    return fol_path, timing, path_taken


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



def visualize_graph_folium(graph, shortest_path):
    G = nx.Graph()

    for node in graph.get_nodes():
        G.add_node(node)

    for source in graph.get_nodes():
        for target in graph.get_outgoing_edges(source):
            G.add_edge(source, target, weight=graph.value(source, target)[0])

    # Convert the set of nodes to a list
    nodes_list = list(graph.get_nodes())
    coordinates = list(graph.node_coordinates.values())
    average_lat = sum(lat for lat, _ in coordinates) / len(coordinates)
    average_lon = sum(lon for _, lon in coordinates) / len(coordinates)

    # Create a Folium map centered at the average coordinates
    m = folium.Map(location=[average_lat, average_lon], zoom_start=12)

    # Create a Folium map centered at the first node coordinates
    #m = folium.Map(location=list(graph.node_coordinates.values())[0], zoom_start=14)

    # Iterate over the edges and add them to the map
    for source, target in G.edges:
        if source in shortest_path and target in shortest_path:
            source_coordinates = graph.node_coordinates[source]
            target_coordinates = graph.node_coordinates[target]
            weight, walk = graph.value(source, target)

            # Set color based on the "walk" attribute
            color = 'green' if walk == 'Y' else 'red' if walk == 'N' else 'gray'

            folium.PolyLine(locations=[source_coordinates, target_coordinates], color=color).add_to(m)

    # Iterate over the nodes and add them to the map
    for node in nodes_list:
        if node in shortest_path:
            color = 'red'
            node_coordinates = graph.node_coordinates[node]
            label = folium.Html(f'<b>{node}</b>', script=True)
            popup = folium.Popup(label, max_width=150)
            folium.Marker(location=node_coordinates, icon=folium.Icon(color=color), popup=popup).add_to(m)
            folium.Marker(location=node_coordinates, icon=folium.DivIcon(html=f'<b>{node}</b>', icon_size=(30, 10))).add_to(m)

    return m
    
    
def visualizeshort_graph_folium(graph, shortest_path):
    G = nx.Graph()

    for node in graph.get_nodes():
        G.add_node(node)

    for source in graph.get_nodes():
        for target in graph.get_outgoing_edges(source):
            G.add_edge(source, target, weight=graph.value(source, target))

    # Convert the set of nodes to a list
    nodes_list = list(graph.get_nodes())

    # Create a Folium map centered at the first node coordinates
    m = folium.Map(location=list(graph.node_coordinates.values())[0], zoom_start=10)
    

    # Iterate over the edges and add them to the map
    for source, target in G.edges:
        if source in shortest_path and target in shortest_path:
            source_coordinates = graph.node_coordinates[source]
            target_coordinates = graph.node_coordinates[target]
            color = 'red' if (source in shortest_path and target in shortest_path) else 'gray'
            folium.PolyLine(locations=[source_coordinates, target_coordinates], color=color).add_to(m)

    # Iterate over the nodes and add them to the map
    for node in nodes_list:
        if node in shortest_path:
            color = 'red'
            node_coordinates = graph.node_coordinates[node]
            label = folium.Html(f'<b>{node}</b>', script=True)
            popup = folium.Popup(label, max_width=150)
            folium.Marker(location=node_coordinates, icon=folium.Icon(color=color), popup=popup).add_to(m)
            folium.Marker(location=node_coordinates, icon=folium.DivIcon(html=f'<b>{node}</b>', icon_size=(30, 10))).add_to(m)

    return m


csv_file= csv_file= os.path.join(basedir,'app','mrt.csv')

graph = Graph(csv_file)


def short_path_finder(start,end):
    start_node = start
    target_node = end
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node = start_node)
    shortest_path,timing, path_taken  = print_result(previous_nodes, shortest_path, start_node, target_node, graph)
    m = visualize_graph_folium(graph, shortest_path)
    m.save("app/templates/shortest_path_map.html")
    return timing, path_taken

