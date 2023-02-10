from analyze_water import calculate_turbidity, calculate_time_to_Ts
import pytest

def test_calculate_turbidity():
    assert calculate_turbidity(2.0, 8.0) == 16.0
    assert calculate_turbidity(3.2, 4.5) == 14.4
    assert isinstance( calculate_turbidity(0.0, 2.0), float ) == True

def test_calculate_time_to_Ts():
    assert calculate_time_to_Ts(1.1992) == 8.99
    assert calculate_time_to_Ts(0.9852) == 0
    assert isinstance(calculate_time_to_Ts(0.9852), float) == True
