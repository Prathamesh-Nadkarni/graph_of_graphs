from typing import Dict
import networkx as nx
import matplotlib.pyplot as plt

class Model:
    def __init__(self, product_data: Dict, demographic_data: Dict, social_data: Dict):
        self.P = nx.Graph()
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
        self.D.add_nodes_from(demographic_data.keys())

    def create_social(self, social_data):
        self.S.add_nodes_from(social_data.keys())

    def visualize(self, network):
        pos = nx.spring_layout(network)
        nx.draw(network, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='#FF5733', font_size=15)
        edge_labels = nx.get_edge_attributes(network, 'weight')
        nx.draw_networkx_edge_labels(network, pos, edge_labels=edge_labels)
        plt.show()