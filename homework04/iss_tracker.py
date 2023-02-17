from flask import Flask, request
import requests
import xmltodict
import math
from typing import List

app = Flask(__name__)

def iss_data() -> dict:
    """
    Pulls trajectory data (position, velocity) from the ISS from NASA.
 
    Arguments:
        None
    Returns:
        iss_data (dict): a dictionary of trajectory data for the ISS in km and km/s.
    """
    r = requests.get('https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    return xmltodict.parse(r.text)

@app.route('/', methods=['GET'])
def data_set() -> List[dict]:
    """
    Provides ISS Trajectory data as a list of dictionaries.

    Arguments:
        None
    Returns:
        iss_data (List[dict]): a list of dictionaries containing trajectory data for the ISS in km and km/s.
    """
    data = iss_data()
    return data['ndm']['oem']['body']['segment']['data']['stateVector'] 

@app.route('/epochs', methods=['GET'])
def list_of_all_epochs() -> list:
    """
    This function lists all of the epochs provided in the data pulled from NASA.

    Arguments:
        None
    Returns:
        epochs (dict): dict of all epochs in the data set and their indicies, epochs in J2000 format.
    """
    data = data_set()
    epochs = {}
    for i in range(len(data)):
        epochs[data[i]['EPOCH']] = i
    return epochs

@app.route('/epochs/<int:epoch>', methods=['GET'])
def state_vector(epoch:int) -> dict:
    """
    Returns the position of the ISS at a specified epoch.

    Arguments:
        epoch (int): index of the epoch of interest.
    Returns:
        state vector (dict): x, y, and z position vector of the ISS in km.
    """
    data = data_set()
    epoch_data = data[epoch]
    d = {}
    d['x'] = epoch_data['X']['#text']
    d['y'] = epoch_data['Y']['#text']
    d['z'] = epoch_data['Z']['#text']
    return d

@app.route('/epochs/<int:epoch>/speed', methods=['GET'])
def inst_speed(epoch:int) -> dict:
    """
    Returns the instantaneous speed of the ISS at a specified epoch.

    Arguments:
        epoch (int): index of the epoch of interest.
    Returns:
        state vector (dict): speed of the ISS in km/s.
    """
    data = data_set()
    epoch_data = data[epoch]
    d = {}
    xdot = float(epoch_data['X_DOT']['#text'])
    ydot = float(epoch_data['Y_DOT']['#text'])
    zdot = float(epoch_data['Z_DOT']['#text'])
    d['speed'] = math.sqrt(xdot*xdot + ydot*ydot + zdot*zdot)
    return d


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
