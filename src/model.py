from typing import Dict
import networkx as nx
import py4cytoscape as p4c
import matplotlib.pyplot as plt
import numpy as np

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
            total_weight = sum(self.D[age][neighbor]['weight'] for neighbor in self.D.neighbors(age))
            for friend in self.D.neighbors(age):
                self.D[age][friend]['weight'] /= total_weight


    def create_social(self, social_data):
        pass

    def create_product_to_demographic(self, pd_data):
        pass

    def create_demographic_to_social(self, ds_data):
        # ds_data = age -> social media ranked (list)
        self.D_to_S.add_nodes_from(self.D)
        self.D_to_S.add_nodes_from(self.S)
        


    
    
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

    '''
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
    '''