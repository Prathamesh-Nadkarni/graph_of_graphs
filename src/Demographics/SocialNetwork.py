import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("DemographicsSM.csv")

# Convert gender to numeric
gender_encoder = LabelEncoder()
data['gender'] = gender_encoder.fit_transform(data['gender'])

# Separate features and target
X = data[['age', 'gender']].values
y = data['platform'].values

# Train the classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X, y)

# Predict probabilities for the whole dataset
probabilities = classifier.predict_proba(X)

# Sort the probabilities and store in a DataFrame
sorted_probabilities = np.hstack((X, probabilities))
sorted_columns = ['age', 'gender', 'Facebook', 'Instagram', 'TikTok', 'Twitter', 'YouTube']
result_df = pd.DataFrame(sorted_probabilities, columns=sorted_columns)

# Convert gender back to categorical
result_df['gender'] = gender_encoder.inverse_transform(result_df['gender'].astype(int))

# Convert age to integer
result_df['age'] = result_df['age'].astype(int)

# Round probabilities to 3 decimal points
result_df[['Facebook', 'Instagram', 'TikTok', 'Twitter', 'YouTube']] = result_df[['Facebook', 'Instagram', 'TikTok', 'Twitter', 'YouTube']].round(3)

# Save probabilities to a CSV file
result_df.to_csv("probabilities.csv", index=False)
