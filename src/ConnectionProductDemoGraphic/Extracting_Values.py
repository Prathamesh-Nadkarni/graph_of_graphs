import pandas as pd
import numpy as np
import json

def DemographicRange(age_interval:int, last_age:int) -> list:
    return [age for age in range(18+age_interval, last_age+1, age_interval)]

def main(age_interval:int = 4, last_age:int = 70):
    Product_dataset = pd.read_csv('src\\ConnectionProductDemoGraphic\\data\\retail_data.csv')
    Product_Demographic = Product_dataset[['Age','ProductCategory']]
    Product_Demographic = Product_Demographic.dropna()
    Age_Nodes = DemographicRange(age_interval=age_interval, last_age=last_age)
    Product_Nodes = ['Health & Beauty', 'Electronics', 'Books', 'Groceries', 'Home & Kitchen']
    product_dict = {}
    
    for x in Product_Nodes:
        Edge_dict = {}
        Node_Dataframe = Product_Demographic[Product_Demographic['ProductCategory'] == x]
        Total = Node_Dataframe.shape[0]
        for y in range(0, len(Age_Nodes)):
            if y == 0:
                Edge_dict["18" + "-" + str(Age_Nodes[y])] = Node_Dataframe[(Node_Dataframe['Age'] >= 18) & (Node_Dataframe['Age'] <= Age_Nodes[y])].shape[0]/Total
            else:
                Edge_dict[str(Age_Nodes[y-1] + 1) + "-" + str(Age_Nodes[y])] = Node_Dataframe[(Node_Dataframe['Age'] > Age_Nodes[y-1]) & (Node_Dataframe['Age'] <= Age_Nodes[y])].shape[0]/Total
        product_dict[x] = Edge_dict
    with open('src\ConnectionProductDemoGraphic\Product_to_Demographic_Edges.json', 'w') as f:
        json.dump(product_dict, f, indent=4)

if __name__ == "__main__":
    main()