import model
import utils
import networkx as nx
import py4cytoscape as p4c

def main():
    product_data = utils.parse_json(r"Product Network\Product_Edges.json")
    demographic_data = utils.synth_age_demographics(low=utils.MIN_AGE, high=utils.MAX_AGE, step=utils.AGE_STEP, n_samples=5000) # utils.parse("demo")
    social_data = utils.parse("sm")
    m = model.Model(product_data, demographic_data, social_data)
    #print(m.query("toothpaste"))
    #m.visualize(m.P)
    m.visualize_cytoscape(m.P)
    m.visualize_cytoscape(m.D, add_weights=False)

if __name__ == "__main__":
    main()