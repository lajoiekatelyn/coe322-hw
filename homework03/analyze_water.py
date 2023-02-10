import requests
import math


Ts = 1.0
d = 0.02


def calculate_turbidity(a0:float, I90:float) -> float:
    return a0 * I90


def calculate_time_to_Ts(T0:float) -> float:
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
        print('Info: Turbidity is below threshold for safe use')
    else:
        print('Warning: Turbidity is above threshold for safe use')

    time_to_Ts = calculate_time_to_Ts(Tavg)
    print(f'Minimum time required to return below a safe threshold = {time_to_Ts} hours')

if __name__ == '__main__':
    main()
