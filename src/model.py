from typing import Dict
import networkx as nx

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

    def create_demographic(self, demographic_data):
        self.D.add_nodes_from(demographic_data.keys())

    def create_social(self, social_data):
        self.S.add_nodes_from(social_data.keys())