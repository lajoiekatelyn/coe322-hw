#!/usr/bin/env python3

import json

def main():
    with open('landing_sites.json', 'r') as f:
        data = json.load(f)

    print(data)

if __name__ == '__main__':
    main()
