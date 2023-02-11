# Homework 03: Water Turbidity Analysis

## Description
In order to analyze the samples from homework02, the robot must have clean water. The code in this project analyzes the turbidity of the five most recent water data points from `turbidity_data.json`, which is not included in the repo. After determining the turbidity of the water, the robot either proceeds or waits the appropriate amount of time for the turbidity to drop to the turbidity threshold of 1.0 NTU.

## Required Data
Data required to run the scripts included in this program is accessed via the url provided in the homework description, `https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json`, and the Python `requests` library. If `requests` is not installed on your machine, install it as follows:
```
pip3 install --user requests
```
Otherwise, the program accesses the data on it's own, given an internet connection.

### analyze_water.py
This script averages the turbidity of the last five data samples from the water data in `turbidity_data.json` using the values from the `calibration_constant`($a_0$) and `detector_current` ($I90$) keys of the dictionaries in the data, calculated as shown
$$T=a_0\cdotI90$$
Then, should the average turbidity exceed the turbidity threshold of 1.0 NTU, it will calculate the time required for the turbidity to fall below the threshold according to the equation
$$T_s=T*(1-d)^b$$
where $T_s$ is the turbidity threshold, $d$ is the decay factor (0.2%, in this case) and $b$ is the required time for the turbidity to fall to the threshold. Solving for $b$ and simplifying the logarithms results in
$$\frac{\ln(\frac{T_s}{T})}{\ln(1-d)}
The script outputs as so:
```
Average turbidity based on most recent five measurements = 1.15 NTU
WARNING: Turbidity is above threshold for safe use!
Minimum time required to return below a safe threshold = 7.08 hours
```

### test_analyze_ater.py
This script tests the functions in `analyze_water.py` using the Python `pytest` library. If `pytest` is not installed on your machine, install it as follows:
```
pip3 install --user pytest
```
The script uses assertions to ensure that the `calculate_turbidity` and `calculate_time_to_Ts` functions behave as expected. For example,

## Usage
