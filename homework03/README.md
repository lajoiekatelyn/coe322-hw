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
$$T=a_0\cdot I90$$
Then, should the average turbidity exceed the turbidity threshold of 1.0 NTU, it will calculate the time required for the turbidity to fall below the threshold according to the equation
$$T_s=T*(1-d)^b$$
where $T_s$ is the turbidity threshold, $d$ is the decay factor (0.2%, in this case) and $b$ is the required time for the turbidity to fall to the threshold. Solving for $b$ and simplifying the logarithms results in
$$b=\frac{\ln(T_s\div T)}{\ln(1-d)}$$

### test_analyze_water.py
This script tests the functions in `analyze_water.py` using the Python `pytest` library. If `pytest` is not installed on your machine, install it as follows:
```
pip3 install --user pytest
```
The script uses assertions to ensure that the `calculate_turbidity` and `calculate_time_to_Ts` functions behave as expected. For example, it asserts output types and results from simple test cases.

## Usage
To run `analyze_water.py`, enter the following into a terminal
```
python3 analyze_water.py
```
It will output something along the lines of
```
Average turbidity based on most recent five measurements = 1.1538822 NTU
WARNING: Turbidity is ABOVE threshold for safe use!
Minimum time required to return below a safe threshold = 7.08 hours
```
In which case, the turbidity is above the threshold (1.0 NTU), so the program provides a warning and the time it would take for the sample to reach the threshold.

If the turbidity were below the threshold, the robot would not have to wait for the sample to clear up, and the script would output as follows:
```
Average turbidity based on most recent five measurements = 0.8783 NTU
INFO: Turbidity is below threshold for safe use.
Minimum time required to return below a safe threshold = 0 hours
```

To run tests on the project, run `pytest` in the root of the repo. Unless the code is altered or breaks, it should output as follows:
```
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.8.10, pytest-7.2.1, pluggy-1.0.0
rootdir: /home/klajoie/coe322-hw/homework03
collected 2 items

test_analyze_water.py ..                                                                                                                                                                                    [100%]

================================================================================================ 2 passed in 0.08s ================================================================================================
```
Please submit an issue or a pull request in the even that the project does not pass all tests.
