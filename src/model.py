from typing import Dict
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class Model:
    def __init__(self, product_data: Dict, demographic_data: Dict, social_data: Dict):
        self.P = nx.DiGraph()
        self.D = nx.Graph()
        self.S = nx.Graph()
        self.create_product(product_data)
        self.create_demographic(demographic_data)
        self.create_social(social_data)

    def query(self, product):
        return []

    def create_product(self, product_data):
        self.P.add_nodes_from(product_data.keys())
        for x in product_data.keys():
            EdgeDict = product_data[x]
            edge_names = EdgeDict.keys()
            for y in edge_names:
                self.P.add_edge(x,y,weight = EdgeDict[y])

    def create_demographic(self, demographic_data):
        # id:(age_range, [friend_1_range, ...])
        age_ranges = set(value[0] for value in demographic_data.values())
        self.D.add_nodes_from(age_ranges)

    def create_social(self, social_data):
        self.S.add_nodes_from(social_data.keys())

    def adjust_label_pos(self, pos, edge, rad):
        """ Adjust the position of edge labels for curved edges. """
        src, tgt = edge
        src_pos, tgt_pos = np.array(pos[src]), np.array(pos[tgt])
        midpoint = (src_pos + tgt_pos) / 2
        
        vector = tgt_pos - src_pos
        
        perpendicular = np.array([-vector[1], vector[0]])
        normalized_perpendicular = perpendicular / np.linalg.norm(perpendicular)
        
        label_pos = midpoint + normalized_perpendicular * rad
        return label_pos

    def visualize(self, network):
        left_curved_edges = [('Health & Beauty', 'Electronics'),('Electronics', 'Books'),('Books', 'Groceries'),('Groceries', 'Home & Kitchen'),('Home & Kitchen', 'Health & Beauty'), ('Electronics', 'Groceries'), ('Electronics', 'Home & Kitchen'),('Books', 'Health & Beauty'),('Books', 'Home & Kitchen'),('Health & Beauty', 'Groceries')]
        right_curved_edges = [('Electronics', 'Health & Beauty'),('Health & Beauty', 'Home & Kitchen'),('Home & Kitchen', 'Groceries'), ('Groceries', 'Books'),('Books', 'Electronics'),('Groceries', 'Electronics'), ('Home & Kitchen', 'Electronics'),('Health & Beauty', 'Books'),('Home & Kitchen', 'Books'),('Groceries', 'Health & Beauty')]
        
        pos = nx.circular_layout(network)

        nx.draw_networkx_nodes(network, pos, node_color='skyblue', node_size=3000)

        for edge in network.edges(data=True):
            if (edge[0],edge[1]) in left_curved_edges:
                style = 'arc3,rad=0.1'
            elif (edge[0],edge[1]) in right_curved_edges:
                style = 'arc3,rad=0.1'
            else:
                style = 'arc3,rad=0'
            nx.draw_networkx_edges(network, pos, edgelist=[(edge[0],edge[1])], connectionstyle=style,
                                arrowstyle='-|>', arrowsize=10, edge_color='gray')

        
        edge_labels = nx.get_edge_attributes(network, 'weight')
        
        formatted_edge_labels = {k: f"{v:.4f}" for k, v in edge_labels.items()}

        label_positions = {}
        for edge in formatted_edge_labels:
            rad = 0.1 if edge in left_curved_edges else 0.1 if edge in right_curved_edges else 0
            label_positions[edge] = self.adjust_label_pos(pos, edge, rad)
        
        for edge, label in formatted_edge_labels.items():
            label_pos = label_positions[edge]
            plt.text(label_pos[0], label_pos[1], s=label, bbox=dict(facecolor='white', alpha=0.5),
                    horizontalalignment='center', verticalalignment='center')

        nx.draw_networkx_labels(network, pos, font_size=12)

        plt.title("Network Visualization with Curved Edges and Weights")
        plt.axis('off')
        plt.show()