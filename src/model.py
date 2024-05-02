from functools import reduce
from typing import Dict
import networkx as nx
import py4cytoscape as p4c
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import utils

class Model:
    def __init__(self, product_data, demographic_data, social_data, p_to_d_data, d_to_s_data):
        self.P = nx.DiGraph()
        self.P_to_D = nx.DiGraph()
        self.D = nx.DiGraph()
        self.D_to_S = nx.DiGraph()
        self.S = nx.DiGraph()
        
        self.create_product(product_data)
        self.create_demographic(demographic_data)
        self.create_social(social_data)
        
        self.create_product_to_demographic(p_to_d_data)
        self.create_demographic_to_social(d_to_s_data)

        self.N = reduce(nx.compose, (self.P, self.D, self.S, self.P_to_D, self.D_to_S))
        

    def query(self, product):
        
        #this makes Electronics like tiktok and twitter and insta!
        #we need to differentiate the product_to_demographic edges more...
        #self.N['Electronics']['18-21']['weight'] = 0.5
        #self.N['Electronics']['22-25']['weight'] = 0.5
        
        weights = {}
        visited_per_parent = {}
        queue = [(product, 0)]

        def node_subgraph(node):
                if node in self.P.nodes():
                    return 'P'
                if node in self.D.nodes():
                    return 'D'
                if node in self.S.nodes():
                    return 'S'
        while queue:
            current_node, current_log_weight = queue.pop(0)
            if current_node in self.S.nodes():
                if current_node not in weights:
                    weights[current_node] = 0
                weights[current_node] += np.exp(current_log_weight)
            
            if current_node not in visited_per_parent:
                visited_per_parent[current_node] = set()
            parent_visited = visited_per_parent[current_node]
            for neighbor in self.N.neighbors(current_node):
                if neighbor not in parent_visited:
                    edge_weight = self.N[current_node][neighbor]['weight']
                    # discount same-network paths, not when moving to next network
                    discount = 0.1 if node_subgraph(current_node) == node_subgraph(neighbor) else 1
                    next_log_weight = current_log_weight + np.log(discount) + np.log(edge_weight)
                    visited_per_parent[current_node].add(neighbor)
                    queue.append((neighbor, next_log_weight))
        total_weight = sum(weights.values())
        normalized_weights = {node: weight / total_weight for node, weight in weights.items()}
        return normalized_weights

    def create_product(self, product_data):
        self.P.add_nodes_from(product_data.keys())
        for x in product_data.keys():
            EdgeDict = product_data[x]
            edge_names = EdgeDict.keys()
            for y in edge_names:
                self.P.add_edge(x,y,weight = EdgeDict[y])

    def create_demographic(self, demographic_data):
        # id:(age_range, [friend_1_range, ...])
        ages = set(value[0] for value in demographic_data.values())
        self.D.add_nodes_from(ages)
        for _, (age, friends) in demographic_data.items():
            for friend in friends:
                if not self.D.has_edge(age, friend):
                    self.D.add_edge(age, friend, weight=0)
                self.D[age][friend]['weight'] += 1
        for age in self.D.nodes():
            total_weight = sum(self.D[age][friend]['weight'] for friend in self.D.neighbors(age))
            for friend in self.D.neighbors(age):
                self.D[age][friend]['weight'] /= total_weight


    def create_social(self, social_data):
        self.S.add_nodes_from(['TikTok', 'Twitter', 'Instagram', 'Facebook', 'YouTube'])
        for x in social_data.keys():
            EdgeDict = social_data[x]
            edge_names = EdgeDict.keys()
            for y in edge_names:
                self.S.add_edge(x,y,weight = EdgeDict[y])

    def create_product_to_demographic(self, pd_data):
        Product_dataset = pd.read_csv(pd_data)
        Product_Demographic = Product_dataset[['Age','ProductCategory']]
        Product_Demographic = Product_Demographic.dropna()
        self.P_to_D.add_nodes_from(self.P)
        self.P_to_D.add_nodes_from(self.D)
        Ages = [age for age in range(utils.MIN_AGE+utils.AGE_STEP, utils.MAX_AGE+1, utils.AGE_STEP)]
        Product_Nodes = self.P.nodes
        for x in Product_Nodes:
            Node_Dataframe = Product_Demographic[Product_Demographic['ProductCategory'] == x]
            Total = Node_Dataframe.shape[0]
            for y in range(len(Ages)):
                low, high = utils.MIN_AGE if y == 0 else Ages[y-1], Ages[y]-1
                self.P_to_D.add_edge(x, str(low) + "-" + str(high),
                                        weight=Node_Dataframe[(Node_Dataframe['Age'] >= low) & (Node_Dataframe['Age'] <= high)].shape[0]/Total)

    def create_demographic_to_social(self, ds_data):
        self.D_to_S.add_nodes_from(self.D)
        self.D_to_S.add_nodes_from(self.S)

        age_ranges = self.D.nodes()

        for _, (age, socials) in ds_data.items():
            age_range = utils.age_to_range(age)
            if age_range not in age_ranges:
                continue
            for social in socials:
                if social not in self.S.nodes():
                    continue
                if not self.D_to_S.has_edge(age_range, social):
                    self.D_to_S.add_edge(age_range, social, weight=0)
                self.D_to_S[age_range][social]['weight'] += 1
        for age_range in age_ranges:
            total_weight = sum(self.D_to_S[age_range][social]['weight'] for social in self.D_to_S.neighbors(age_range))
            for social in self.D_to_S.neighbors(age_range):
                self.D_to_S[age_range][social]['weight'] /= total_weight

    def visualize_cytoscape(self, network, add_weights=True):
        try:
            suid = p4c.networks.create_network_from_networkx(network)
        except:
            print('Visualization requires Cytoscape to be running https://cytoscape.org/')
            return
        style_name = f'{suid} style'
        # default style mapping
        defaults = {'NODE_SHAPE': 'rectangle', 'NODE_FILL_COLOR': 'orange', 'EDGE_TARGET_ARROW_SHAPE': 'arrow'}

        # create mappings
        mappings = []
        mappings.append(p4c.map_visual_property('NODE_LABEL', 'name', 'p'))
        if add_weights:
            mappings.append(p4c.map_visual_property('EDGE_LABEL', 'weight', 'p'))
        mappings.append(p4c.map_visual_property('EDGE_STROKE_UNSELECTED_PAINT', 'weight', 'c', [0.0, 1.0], ['blue','red']))
        mappings.append(p4c.map_visual_property('EDGE_TRANSPARENCY', 'weight', 'c', [0.0, 0.5, 1.0], [0, 200, 255]))
        
        p4c.styles.create_visual_style(style_name, defaults=defaults, mappings=mappings)
        p4c.styles.set_visual_style(style_name, suid)
