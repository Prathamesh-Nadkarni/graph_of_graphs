import pandas as pd
import json

Probability_csv = 'probabilities.csv'
df = pd.read_csv(Probability_csv, index_col='age')  

def clean_numeric(value):
    if isinstance(value, str):  
        value = value.strip('.')  
        try:
            return pd.to_numeric(value)  
        except ValueError:
            return pd.NA  
    else:
        return value  

categories = ['TikTok', 'Twitter', 'Instagram', 'Facebook', 'YouTube']
category_dfs = {}

for column in categories:
    df[column] = df[column].apply(clean_numeric)

df = df.dropna()

EdgeDict = {}

for category in categories:
    category_df = df.copy()  
    
    EdgePercentage = {}
    for x in categories:
        if x != category:
            category_df[f'{category}-{x}'] = df[category] / df[x]
            EdgePercentage[x] = category_df[f'{category}-{x}'].mean().round(3)  
    
    total_weight = sum(EdgePercentage.values())
    normalized_weights = {k: (v / total_weight).round(3) for k, v in EdgePercentage.items()}
    
    EdgeDict[category] = normalized_weights

with open('Demograph_Edges.json', 'w') as f:
    json.dump(EdgeDict, f, indent=4)

print(json.dumps(EdgeDict, indent=4))
