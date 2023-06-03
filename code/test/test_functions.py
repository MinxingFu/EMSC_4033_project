import pytest
from assets.functions import *

def test_atmospheric_stability():
    # Test cases for atmospheric stability
    assert atmospheric_stability(1, True, 'Strong') == 'A'  # Expected output: 'A'
    assert atmospheric_stability(2.5, True, 'Strong') == 'A-B'  # Expected output: 'A-B'
    assert atmospheric_stability(4, True, 'Strong') == 'B'  # Expected output: 'B'
    assert atmospheric_stability(6, True, 'Strong') == 'C'  # Expected output: 'C'

def test_empr_cons():
    # Test case for empirical constants
    assert empr_cons('A', True) == (0.32, 0.0004, 0.5, 0.24, 0.0001, -0.5)  # Expected output: (0.32, 0.0004, 0.5, 0.24, 0.0001, -0.5)

def test_emp_sigma_y():
    # Test case for empirical sigma y
    assert emp_sigma_y(0.32, 0.0004, 0.5, 0.24) == (0.32 * 0.24) / np.power((1 + 0.0004 * 0.24), 0.5)  # Expected output: calculated value

def test_emp_sigma_z():
    # Test cases for empirical sigma z
    assert emp_sigma_z(0.5, 0.001, 0.8, 0.2) == (0.5 * 0.2) / np.power(1 + 0.001 * 0.2, 0.8)  # Expected output: calculated value
    assert emp_sigma_z(0.5, 0.001, None, 0.2) == 0.5 * 0.2  # Expected output: calculated value







