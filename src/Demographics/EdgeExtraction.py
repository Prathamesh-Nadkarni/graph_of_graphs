import pandas as pd
import json

Probability_csv = 'probabilities.csv'
df = pd.read_csv(Probability_csv, index_col='Age')  # Assuming 'Age' is the column to use as an index

def clean_numeric(value):
    if isinstance(value, str):  # Check if the value is a string
        value = value.strip('.')  # Strip trailing period
        try:
            return pd.to_numeric(value)  # Convert to numeric type
        except ValueError:
            return pd.NA  # Return missing value if conversion fails
    else:
        return value  # Return the value unchanged if it's not a string
    

categories = ['TikTok', 'Twitter', 'Instagram', 'Facebook', 'YouTube']
category_dfs = {}

for column in categories:
    df[column] = df[column].apply(clean_numeric)

df = df.dropna()

for category in categories:
    category_dfs[category] = df[df[category] == df[categories].max(axis=1)]

# Example to access and print each DataFrame
EdgeDict = {}
for category, category_df in category_dfs.items():
    print(f"DataFrame where '{category}' has the highest probability:")
    sum = 0
    for x in categories:
        if x != category:
            average = category_df[x].astype(float).sum() / len(category_df[x])
            sum = sum + average
            print(x, average)

    EdgePercentage = {}

    for x in categories:
        if x != category:
            average = category_df[x].astype(float).sum() / len(category_df[x])
            print(x," Edge Percentage", average/sum)
            EdgePercentage[x] = float(format(average/sum, ".4f"))
    
    EdgeDict[category] = EdgePercentage

with open('Demograph_Edges.json', 'w') as f:
    json.dump(EdgeDict, f, indent=4)
