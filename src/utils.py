import json

def parse(filename):
    return {}

def synth_age_demographics(low, high, step):
    n = (high-low)//step
    ranges = list(f'{low + i*step}-{low + (i+1)*step}' for i in range(n))

    NUM_FRIENDS = 30
    age_data = {}
    for sample in range(3):
        friends = np.clip(np.round(np.random.normal(loc=NUM_FRIENDS, scale=NUM_FRIENDS//3)), 0, NUM_FRIENDS*3).astype(int)
        range_idx = np.random.randint(0, n)
        friends_idx = np.clip(np.round(np.random.normal(loc=range_idx, scale=1.5, size=friends)), 0, n-1).astype(int)
        friends = list(ranges[f_idx] for f_idx in friends_idx)
        age_data[sample] = (ranges[range_idx], friends)
    return age_data

def parse_json(filename):
    with open(filename, 'r') as file:
        parsed_dict = json.load(file)
    return parsed_dict
