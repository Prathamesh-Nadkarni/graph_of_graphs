import json
import numpy as np

MIN_AGE = 18
MAX_AGE = 70
AGE_STEP = 4


def parse(filename):
    return {}

def synth_age_demographics(low, high, step, n_samples):
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
    return age_data

def parse_json(filename):
    with open(filename, 'r') as file:
        parsed_dict = json.load(file)
    return parsed_dict
