# Homework 04: Flask Application for Querying the ISS' Orbital Ephemeris

## Description
Knowing the current position and velocity of the ISS is vital to ensuring that it does not collide with anything else that is in orbit. Fortunately, data concerning the ISS' orbital ephemeris (position and velocity) is publically avaliable. However, siftig through this data for the information desired is time consuming, so the ability to query and return informaiton pertaining to a particular epoch (point in time) is important.

### Flask
This program uses the Python Flask library. Flask is a web framework used to develop generalized web applications. To install Flask, please enter the following command into your terminal:

```
pip3 install --user flask
```

### Required Data
Data required for this app is the [ISS Trajectory Data](https://spotthestation.nasa.gov/trajectory_data.cfm) provided by Spot The Station in XML format, which is accessed using the Python `requests` library. If requests is not installed on your machine, please install it using the following command in your terminal:

```
pip3 install --user requests
```

### iss_tracker.py

## Usage
