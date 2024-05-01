import model
import utils
import networkx as nx
import py4cytoscape as p4c

def main():
    product_data = utils.parse_json(r"src\Product Network\Product_Edges.json")
    demographic_data = utils.parse_json(r'src\data\age_friends.json')
    social_data = utils.parse_json(r'src\Socials\Social_edges.json')

    p_to_d_data = r'src\data\retail_data.csv'
    d_to_s_data = utils.parse_json(r'src\data\age_to_sm.json')
    
    m = model.Model(product_data, demographic_data, social_data, p_to_d_data, d_to_s_data)
    '''
    m.visualize_cytoscape(m.P, add_weights=True)
    m.visualize_cytoscape(m.P_to_D, add_weights=True)
    m.visualize_cytoscape(m.D, add_weights=True)
    m.visualize_cytoscape(m.D_to_S, add_weights=True)
    m.visualize_cytoscape(m.S, add_weights=True)
    '''
    m.visualize_cytoscape(m.N, add_weights=True)
    print(m.query('Electronics'))
    print(m.query('Health & Beauty'))



if __name__ == "__main__":
    main()