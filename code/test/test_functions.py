from unittest import mock
import pytest
from assets.functions import *

def test_atmospheric_stability():
    assert atmospheric_stability(1, True, 'Strong') == 'A'
    assert atmospheric_stability(2.5, True, 'Strong') == 'A-B'
    assert atmospheric_stability(4, True, 'Strong') == 'B'
    assert atmospheric_stability(6, True, 'Strong') == 'C'

def test_empr_cons():
    assert empr_cons('A', True) == (0.32, 0.0004, 0.5, 0.24, 0.0001, -0.5)


def test_emp_sigma_y():
    assert emp_sigma_y(0.32, 0.0004, 0.5, 0.24) == (0.32 * 0.24) / np.power((1 + 0.0004 * 0.24), 0.5)


def test_emp_sigma_z():
    assert emp_sigma_z(0.5, 0.001, 0.8, 0.2) == (0.5 * 0.2) / np.power(1 + 0.001 * 0.2, 0.8)
    assert emp_sigma_z(0.5, 0.001, None, 0.2) == 0.5 * 0.2
    

def test_Drax_sigma_y():
    stability = "Stable"
    x = 10
    sigma_v = 10
    u = 10
    t = x / u
    TL_y = 1000 * 1.64
    theta = np.arctan(sigma_v / u)
    fy = 1 / (1 + (t / TL_y) ** 0.5)
  
    expected_result = theta * x * fy
    result = Drax_sigma_y(stability, x, sigma_v, u)
   
    assert np.isclose(result, expected_result, atol=1e-6)
    
def test_Drax_sigma_z():
    stability = "Stable"
    x = 1000
    sigma_w = 1
    u = 10

# Calculate the expected result based on the provided inputs
    t = x / u
    if stability == "Stable":
        TL_z = 100 * 1.64
    else:
        TL_z = 500 * 1.64
    phi = np.arctan(sigma_w / u)
    fz = 1 / (1 + 0.9 * (t / TL_z) ** 0.5)
    expected_result = phi * x * fz

# Call the Drax_sigma_z function and get the actual result
    result = Drax_sigma_z(stability, x, sigma_w, u)

# Compare the actual result with the expected result
    assert np.isclose(result, expected_result, atol=1e-6)

def test_concentration():
    x = 1000
    y = 0
    z = 10
    Q = 1000
    u = 10
    sigma_y = 1
    sigma_z = 1
    H = 20

    # Helper function phi_x calculates the downwind dispersion based on the emission rate and wind speed.
    def phi_x(Q, u):
        return Q / u

    # Helper function phi_y calculates the crosswind dispersion using a normal distribution formula.
    # It takes into account the crosswind variance and the y-coordinate.
    def phi_y(sigma_y, y):
        if np.sum(sigma_y) > 0.0:
            return 1 / (np.sqrt(2 * np.pi) * sigma_y) * np.exp(-np.power(y, 2) / (2 * np.power(sigma_y, 2)))
        else:
            return 0.0

    def phi_z(sigma_z, z, H):
        if np.sum(sigma_z) > 0.0:
            return (
                1
                / (np.sqrt(2 * np.pi) * sigma_z)
                * (
                    np.exp(-np.power(z - H, 2) / (2 * np.power(sigma_z, 2)))
                    + np.exp(-np.power(z + H, 2) / (2 * np.power(sigma_z, 2)))
                )
            )
        else:
            return 0.0

    # Calculate the expected result based on the provided inputs
    expected_result = phi_x(Q, u) * phi_y(sigma_y, y) * phi_z(sigma_z, z, H)

    # Call the concentration function and get the actual result
    result = concentration(x, y, z, Q, u, sigma_y, sigma_z, H)

    # Compare the actual result with the expected result
    assert np.isclose(result, expected_result, atol=1e-6)







