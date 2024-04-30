import json
import numpy as np
import csv
import pandas as pd

MIN_AGE = 18
MAX_AGE = 70
AGE_STEP = 4


def parse_csv(filename, columns = None):
    data = {}
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line, row in enumerate(reader):
            data[line] = [row[i] for i in columns] if columns else row
    return data

def age_to_range(age):
        index = (int(age) - MIN_AGE) // AGE_STEP
        return f"{MIN_AGE + index * AGE_STEP}-{MIN_AGE + (index + 1) * AGE_STEP - 1}"

def synth_age_demographics(low, high, step, n_samples, outfile):
    n_ranges = (high-low)//step
    ranges = list(f'{low + i*step}-{low + (i+1)*step - 1}' for i in range(n_ranges))
    print(ranges)
    NUM_FRIENDS = 30
    VARIANCE = 1
    age_data = {}
    for sample in range(n_samples):
        noisy_num_friends = np.clip(np.round(np.random.normal(loc=NUM_FRIENDS, scale=NUM_FRIENDS//3)), 0, NUM_FRIENDS*3).astype(int)
        range_idx = np.random.randint(0, n_ranges)
        friends_idx = np.round(np.random.normal(loc=range_idx, scale=VARIANCE, size=noisy_num_friends)).astype(int)
        friends = list(ranges[f_idx] for f_idx in friends_idx if 0 <= f_idx and f_idx <= n_ranges-1)
        age_data[sample] = (ranges[range_idx], friends)
    with open(outfile, 'w') as json_file:
        json.dump(age_data, json_file)

def synth_age_to_socials(n_samples, infile, outfile):
    df = pd.read_csv(infile)
    data = {}
    age_to_sm_probs = {}
    for _, row in df.iterrows():
        age_range = row['age']
        age_to_sm_probs[age_range] = list(map(float, row.values[1:]))
    print(age_to_sm_probs)
    for sample in range(n_samples):
        age_range = np.random.choice(list(age_to_sm_probs.keys()))
        age_min, age_max = map(int, age_range.split('-'))
        age = np.random.randint(age_min, age_max + 1)
        social_medias = list(df.columns[1:])
        probabilities = age_to_sm_probs[age_range]
        chosen_medias = []
        for i in range(len(social_medias)):
            if np.random.random() < probabilities[i]:
                chosen_medias.append(social_medias[i])
        data[sample] = (age, chosen_medias)
    with open(outfile, 'w') as json_file:
        json.dump(data, json_file)

def parse_json(filename):
    with open(filename, 'r') as file:
        parsed_dict = json.load(file)
    return parsed_dict
