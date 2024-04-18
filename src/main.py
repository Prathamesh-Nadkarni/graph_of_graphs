import model
import utils

def main():
    product_data = utils.parse_json(r"src\Product Network\Product_Edges.json")
    demographic_data = utils.synth_age_demographics(low=20, high=80, step=5, n_samples=5000) # utils.parse("demo")
    social_data = utils.parse("sm")
    m = model.Model(product_data, demographic_data, social_data)
    print(m.query("toothpaste"))
    #m.visualize(m.P)


if __name__ == "__main__":
    main()