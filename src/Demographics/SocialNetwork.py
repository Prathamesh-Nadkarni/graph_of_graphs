import csv
from collections import defaultdict

# Initialize dictionaries to store counts and probabilities
counts = defaultdict(int)
probabilities = defaultdict(dict)

# Read data from the CSV file
with open('demographicsSM.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        age, gender, platform = row
        counts[(age, gender, platform)] += 1

# Calculate total number of individuals for each age and gender
totals = defaultdict(int)
for (age, gender, _), count in counts.items():
    totals[(age, gender)] += count

# Calculate probabilities
for (age, gender, platform), count in counts.items():
    probability = count / totals[(age, gender)]
    probabilities[(age, gender)][platform] = probability

# Sort the probabilities by age and gender
sorted_probabilities = sorted(probabilities.items())

# Write sorted probabilities to a CSV file
with open('probabilities2.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Age', 'Gender', 'TikTok', 'Facebook', 'Twitter', 'Instagram', 'YouTube'])
    for (age, gender), platform_probs in sorted_probabilities:
        row = [age, gender]
        row.extend([platform_probs.get(platform, 0) for platform in ['TikTok', 'Facebook', 'Twitter', 'Instagram', 'YouTube']])
        writer.writerow(row)
