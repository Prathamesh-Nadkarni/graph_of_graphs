import pandas as pd
import json

Probability_csv = 'probabilities.csv'
df = pd.read_csv(Probability_csv, index_col='age')  # Assuming 'age' is the column to use as an index

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

# Initialize dictionary to store edge weights
EdgeDict = {}

# Iterate over each category to calculate edge weights
for category in categories:
    category_df = df.copy()  # Make a copy of the DataFrame
    
    # Calculate edge weights for each category
    EdgePercentage = {}
    for x in categories:
        if x != category:
            category_df[f'{category}-{x}'] = df[category] / df[x]
            EdgePercentage[x] = category_df[f'{category}-{x}'].mean().round(3)  # Calculate average edge weight and round to 3 decimal places
    
    # Remove NaN values from the dictionary
    EdgePercentage = {k: v for k, v in EdgePercentage.items() if not pd.isna(v)}
    
    # Add edge weights to EdgeDict
    EdgeDict[category] = EdgePercentage

# Save edge weights to a JSON file
with open('Demograph_Edges.json', 'w') as f:
    json.dump(EdgeDict, f, indent=4)

# Print the edge weights
print(json.dumps(EdgeDict, indent=4))
