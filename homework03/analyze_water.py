import requests
import math


Ts = 1.0
d = 0.02


def calculate_turbidity(a0:float, I90:float) -> float:
    """
    Given a calibration constant and detector current, this function calculates the turbidity of water.

    Arguments:
        a0 (float): calibration constant
        T0 (float): ninety degree detector current
    Returns:
        T (float): turbidity of the input data points in NTU
    """

    return a0 * I90


def calculate_time_to_Ts(T0:float) -> float:
    """
    This function calculate the time it takes in hours for a water sample to fall to the turbidity threshold.

    Arguments:
        T0 (float): current turbidity in NTU
    Returns:
        b (float): time it takes for the turbidity to fall to the threshold (1.0 NTU) in hours
    """

    if ( T0 < Ts ):
        return 0.0
    else:
        return round( math.log(Ts / T0) / math.log(1.0 - d), 2 )
    

def main():
    response = requests.get(url='https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
    water_data = response.json()

    # for five most recent data points
    # average current water turbidity
    Tsum = 0
    for i in range(0, 5):
        data = water_data['turbidity_data'][i]
        a0 = data['calibration_constant']
        I90 = data['detector_current']
        Tsum += calculate_turbidity(a0, I90)

    Tavg = Tsum / 5
    print(f'Average turbidity based on most recent five measurements = {Tavg} NTU')

    if ( Tavg < Ts ):
        print('INFO: Turbidity is below threshold for safe use.')
    else:
        print('WARNING: Turbidity is ABOVE threshold for safe use!')

    time_to_Ts = calculate_time_to_Ts(Tavg)
    print(f'Minimum time required to return below a safe threshold = {time_to_Ts} hours')

if __name__ == '__main__':
    main()
