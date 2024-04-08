import model
import utils

def main():
    m = model.Model(utils.parse("prod"), utils.parse("demo"), utils.parse("sm"))
    print(m.query("toothpaste"))

if __name__ == "__main__":
    main()