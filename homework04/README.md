# Homework 04: Flask Application for Querying the ISS' Orbital Ephemeris

## Description
Knowing the current position and velocity of the ISS is vital to ensuring that it does not collide with anything else that is in orbit. Fortunately, data concerning the ISS' orbital ephemeris (position and velocity) is publically avaliable. However, siftig through this data for the information desired is time consuming, so the ability to query and return informaiton pertaining to a particular epoch (point in time) is important.

### Flask
This program uses the Python Flask library. Flask is a web framework used to develop generalized web applications. To install Flask, please enter the following command into your terminal:

```
$ pip3 install --user flask
```

### Required Data
Data required for this app is the [ISS Trajectory Data](https://spotthestation.nasa.gov/trajectory_data.cfm) provided by Spot The Station in XML format, which is accessed using the Python `requests` library. If requests is not installed on your machine, please install it using the following command in your terminal:

```
$ pip3 install --user requests
```
The data can also be accessed in text format (`.txt`). Both file formats contain headers, comments, metadata, and data. The important information for this app is the data, which is in the form of a state vector consisting of position (km) and velocity (km/s).

### iss_tracker.py
This script contains the application and its queries. It pulls the ISS data from the internet and allows the user to query the entire data set, a list of epochs, position at a specific epoch, and instantaneous speed at a specific epoch.

To calculate instantaenous speed, `iss_tracker.py` uses the following equation:
```math
speed = \sqrt{\dot{x}^2+\dot{y}^2+\dot{z}^2}
```

## Usage
To launch the app, please navigate to the root of the homework04 folder. Then, enter the following into the terminal:
```
$ flask --app iss_tracker run
```
Then, open a new terminal and query the app.

### Raw Data
To query all of the raw data (with the headers, comments, and metadata removed):
```
$ curl localhost:5000/
[
  {
    "EPOCH": "2023-046T12:00:00.000Z",
    "X": {
      "#text": "-4788.3685075076201",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-4.4731764053264502",
      "@units": "km/s"
    },
    "Y": {
      "#text": "1403.5496223712601",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-5.4438825894668401",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-4613.1094793006896",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "2.9970573852109199",
      "@units": "km/s"
    }
  },
  ...

```

### List of Epochs
To obtain a dictionary of all the epochs in the data and their respective indicies, such that they can be called to find a specific position vector:
```
$ curl localhost:5000/epochs
{
  "2023-046T12:00:00.000Z": 0,
  "2023-046T12:04:00.000Z": 1,
  "2023-046T12:08:00.000Z": 2,
  "2023-046T12:12:00.000Z": 3,
  "2023-046T12:16:00.000Z": 4,
  "2023-046T12:20:00.000Z": 5,
  "2023-046T12:24:00.000Z": 6,
  "2023-046T12:28:00.000Z": 7,
  "2023-046T12:32:00.000Z": 8,
  "2023-046T12:36:00.000Z": 9,
  "2023-046T12:40:00.000Z": 10,
  ...
```
### Position Vector
```
$ localhost:5000/epoch/0
```
will return the position of the top of the data file as a dictionary, where `x`, `y`, and `z` are in km.
```
{"x":"-4788.3685075076201","y":"1403.5496223712601","z":"-4613.1094793006896"}
```
### Speed
Finally, speed can also be queried:
```
$ localhost:5000/epoch/0/speed
```
which will return the instantaneous speed of the ISS in km/s as a dictionary.
```
{"speed":7.656860830086751}
```
