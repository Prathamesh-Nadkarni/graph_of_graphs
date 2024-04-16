import model
import utils

def main():
    product_data = utils.parse("prod")
    demographic_data = utils.synth_age_demographics(low=20, high=60, step=5, n_samples=2000) # utils.parse("demo")
    social_data = utils.parse("sm")
    m = model.Model(product_data, demographic_data, social_data)
    print(m.query("toothpaste"))

if __name__ == "__main__":
    main()