import model
import utils


def main():
    m = model.Model(utils.parse_json("src\Product Network\Product_Edges.json"), utils.parse("demo"), utils.parse("sm"))
    print(m.query("toothpaste"))
    m.visualize(m.P)


if __name__ == "__main__":
    main()