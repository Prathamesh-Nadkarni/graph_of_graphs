import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("DemographicsSM.csv")

# Separate features and target
X = data[['age']].values
y = data['platform'].values

# Train the classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X, y)

# Predict probabilities for the whole dataset
probabilities = classifier.predict_proba(X)

# Aggregate probabilities by age
unique_ages = np.unique(X)
average_probabilities = []

for age in unique_ages:
    age_indices = np.where(X == age)[0]
    age_probabilities = probabilities[age_indices].mean(axis=0)
    average_probabilities.append(np.hstack((age, age_probabilities)))

# Store aggregated probabilities in a DataFrame
columns = ['age', 'Facebook', 'Instagram', 'TikTok', 'Twitter', 'YouTube']
result_df = pd.DataFrame(average_probabilities, columns=columns)

# Convert age to integer
result_df['age'] = result_df['age'].astype(int)

# Round probabilities to 3 decimal points
result_df[['Facebook', 'Instagram', 'TikTok', 'Twitter', 'YouTube']] = result_df[['Facebook', 'Instagram', 'TikTok', 'Twitter', 'YouTube']].round(3)

# Save probabilities to a CSV file
result_df.to_csv("probabilities.csv", index=False)
