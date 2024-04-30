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
        
        #self.create_product_to_demographic(p_to_d_data)
        self.create_demographic_to_social(d_to_s_data)

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
        pass

    def create_product_to_demographic(self, pd_data):
        # needs to be tested! adapted from Extracting_Values.py
        Product_dataset = pd.read_csv(pd_data)
        Product_Demographic = Product_dataset[['Age','ProductCategory']]
        Product_Demographic = Product_Demographic.dropna()
        self.P_to_D.add_nodes_from(self.P)
        self.P_to_D.add_nodes_from(self.D)
        Ages = [age for age in range(utils.MIN_AGE+utils.age_interval, utils.MAX_AGE+1, utils.AGE_STEP)]
        Product_Nodes = self.P.nodes
        for x in Product_Nodes:
            Node_Dataframe = Product_Demographic[Product_Demographic['ProductCategory'] == x]
            Total = Node_Dataframe.shape[0]
            for y in range(0, len(Ages)):
                if y == 0:
                    self.P_to_D.add_edge(x, str(utils.MIN_AGE) + "-" + str(Ages[y]),
                                         weight=Node_Dataframe[(Node_Dataframe['Age'] >= utils.MIN_AGE) & (Node_Dataframe['Age'] <= Ages[y])].shape[0]/Total)
                else:
                    self.P_to_D.add_edge(x, str(Ages[y-1] + 1) + "-" + str(Ages[y]),
                                         weight=Node_Dataframe[(Node_Dataframe['Age'] > Ages[y-1]) & (Node_Dataframe['Age'] <= Ages[y])].shape[0]/Total)

    def create_demographic_to_social(self, ds_data):
        # needs to be tested!!!

        # ds_data = id: (age, sm)
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