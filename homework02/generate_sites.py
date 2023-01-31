#!/usr/bin/env python3

import random
import json

def generate_lat() -> float:
    """
    This function generates a random latitude between 16 and 18 degrees.
    
    Arguments:
        None
    
    Returns:
        latitude (float): latitude of the robot in degrees.

    """
    return random.uniform(16.0, 18.0)

def generate_lon() -> float:
    """
    This function generates a random longitude between 82 and 84 degrees.
    
    Arguments:
        None

    Returns:
        longitude (float): longitude of robot in degrees

    """
    return random.uniform(82.0, 84.0)

def generate_comp() -> str:
    """
    This function returns a random metorite composition from a list consisting of 'stony', 'iron', and 'stony-iron'.
    
    Arguments:
        None

    Returns: 
        composition (string): stony, iron, or stony iron.
    """
    comp = ['stony', 'iron', 'stony-iron']
    ind = round(random.uniform(0.0, 2.49))
    return comp[ind]

def main():
    """
    This function generates a list of five dictionaries containing site_id, latitude, longitude, and composition information 
    on meteorite landing sites that a robot shall visit. It then writes them to a JSON file.
    """


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
