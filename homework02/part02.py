#!/usr/bin/env python3

import json
import math

def calc_gcd(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float, radius:float) -> float:
    lat1, lon1, lat2, lon2 = map( math.radians, [latitude_1, longitude_1, latitude_2, longitude_2] )
    d_sigma = math.acos( math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(abs(lon1-lon2)))
    return ( radius * d_sigma )

def composition_sample_time(comp):
    if comp == 'stony':
        return 1
    if comp == 'iron':
        return 2
    if comp == 'stony-iron':
        return 3

def main():
    mars_radius = 3389.5  # km

    with open('landing_sites.json', 'r') as f:
        data = json.load(f)
    
    lat1 = 16.0
    lon1 = 82.0
    max_speed = 10  # km / hr

    legs = []

    for i in range(len(data['sites'])):
        temp = {}
        temp['leg'] = i+1
        lat2 = data['sites'][i]['latitude']
        lon2 = data['sites'][i]['longitude']
        dist = calc_gcd(lat1, lon1, lat2, lon2, mars_radius)
        temp['time to travel'] = dist / max_speed
        temp['time to sample'] = composition_sample_time(data['sites'][i]['composition'])
        legs.append(temp)

    total_time = 0
    for i in range(len(legs)):
        print(f'leg = {legs[i]["leg"]}, time to travel = {round(legs[i]["time to travel"], 2)}, time to sample = {legs[i]["time to sample"]}')
        total_time += legs[i]['time to travel'] + legs[i]['time to sample']

    print('===============================')
    print(f'number of legs = {len(legs)}, total time elapsed = {total_time}')

if __name__ == '__main__':
    main()
