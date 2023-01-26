#!/usr/bin/env python3

import random
import json

def generate_lat():
    return random.uniform(16.0, 18.0)

def generate_lon():
    return random.uniform(82.0, 84.0)

def generate_comp():
    comp = ['stony', 'iron', 'stony-iron']
    ind = round(random.uniform(0.0, 2.49))
    return comp[ind]

def main():
    
    list = []

    for i in range(1,6):
        temp = {}
        temp['site_id'] = i
        temp['latitude'] = generate_lat()
        temp['longitude'] = generate_lon()
        temp['composition'] = generate_comp()
        list.append(temp)

    dict = {'sites': list}
    
    with open('landing_sites.json', 'w') as out:
        json.dump(dict, out, indent=2)

if __name__ == '__main__':
    main()
