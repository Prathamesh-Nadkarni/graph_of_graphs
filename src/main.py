import model
import utils
import networkx as nx
import py4cytoscape as p4c

def main():
    product_data = utils.parse_json(r"Product Network\Product_Edges.json")
    demographic_data = utils.parse_json(r'data\age_friends.json')
    social_data = None

    p_to_d_data = r'src\ConnectionProductDemoGraphic\data\retail_data.csv'
    d_to_s_data = utils.parse_csv(r'data\age_gender_sm.csv', columns=[0, 2])

    m = model.Model(product_data, demographic_data, None, p_to_d_data, d_to_s_data)
    m.visualize_cytoscape(m.P)
    m.visualize_cytoscape(m.D, add_weights=False)
    m.visualize_cytoscape(m.D_to_S, add_weights=True)

    #print(m.query("toothpaste"))



if __name__ == "__main__":
    main()