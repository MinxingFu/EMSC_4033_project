from .dependencies import *

def atmospheric_stability(wind_speed, day_time, day_type):
    # Check if it is daytime or nighttime
    if day_time: 
        # Check if the provided day_type is valid for daytime
        if day_type not in ['Strong', 'Moderate', 'Slight']:
            raise ValueError('Only support Strong, Moderate, or Slight for daytime')
        else:
            # Determine the stability class based on the wind speed and day_type
            if day_type == 'Strong':
                if wind_speed < 2:
                    return 'A'
                elif wind_speed < 3:
                    return 'A-B'
                elif wind_speed < 5:
                    return 'B'
                else:
                    return 'C'
            elif day_type == 'Moderate':
                if wind_speed < 2:
                    return 'A-B'
                elif wind_speed < 3:
                    return 'B'
                elif wind_speed < 5:
                    return 'B-C'
                elif wind_speed < 6:
                    return 'C-D'
                else:
                    return 'D'
            elif day_type == 'Slight':
                if wind_speed < 2:
                    return 'B'
                elif wind_speed < 5:
                    return 'C'
                else:
                    return 'D'
    else: # Check if the provided day_type is valid for nighttime
        if day_type not in ['Cloudy', 'Clear']:
            raise ValueError('Only support Clear or Cloudy for nighttime')
        else: # Determine the stability class based on the wind speed and day_type
            if day_type == 'Cloudy':
                if wind_speed < 3:
                    return 'E'
                else:
                    return 'D'
            elif day_type == 'Clear':
                if wind_speed < 3:
                    return 'F'
                elif wind_speed < 5:
                    return 'E'
                else:
                    return 'D'

def empr_cons(stability_class, urban):
    # Define the valid stability classes for urban and rural cases
    if urban is True:
        if ('A' and 'B' in stability_class) or (stability_class == 'A') or (stability_class == 'B'):
            return 0.32, 0.0004, 0.5, 0.24, 0.0001, -0.5
        elif stability_class == 'C':
            return 0.22, 0.0004, 0.5, 0.2, 0, None
        elif stability_class == 'D':
            return 0.16, 0.0004, 0.5, 0.14, 0.0003, 0.5
        elif ('E' and 'F' in stability_class) or (stability_class == 'E') or (stability_class == 'F'):
            return 0.11, 0.0004, 0.5, 0.08, 0.0015, 0.5
        else:
            print('Only support A-B, C, D, E-F classes')
            return
    elif urban is False:
        if stability_class == 'A':
            return 0.22, 0.0001, 0.5, 0.2, 0, None
        elif stability_class == 'B':
            return 0.16, 0.0001, 0.5, 0.12, 0, None
        elif stability_class == 'C':
            return 0.11, 0.0001, 0.5, 0.08, 0.0002, 0.5
        elif stability_class == 'D':
            return 0.06, 0.0001, 0.5, 0.03, 0.0003, 1
        elif stability_class == 'F':
            return 0.04, 0.0001, 0.5, 0.016, 0.0003, 1
        else:
            print('Only support A, B, C, D, F classes')
            return

def emp_sigma_y(a, b, c, x):
    return (a * x) / np.power((1 + b * x), c) # Calculate the value of sigma_y using the given parameters

def emp_sigma_z(d, e, f, x):
    if f is None: # Check if f is None
        return d * x # Calculate the value of sigma_z without the f parameter
    else:
        return (d * x) / np.power(1 + e * x, f) # Calculate the value of sigma_z using the given parameters
    
def Drax_sigma_y(stability, x, sigma_v, u):
    t = x / u
    
    if stability == "Stable":
        TL_y = 1000 * 1.64
    else:
        TL_y = 1000 * 1.64

    theta = np.arctan(sigma_v / u)
    fy = 1 / (1 + (t / TL_y) ** 0.5)

    return theta * x * fy  #returns the Drax value of sigma_y.

#The Drax sigma_y value is determined by the stability condition, distance, vertical standard deviation, and wind speed.
def Drax_sigma_z(stability, x, sigma_w, u):
    t = x / u
    
    if stability == "Stable":
        TL_z = 100 * 1.64
    else:
        TL_z = 500 * 1.64

    phi = np.arctan(sigma_w / u)

    fz = 1 / (1 + 0.9 * (t / TL_z) ** 0.5)

    return phi * x * fz #returns the Drax sigma_z value.

def concentration(x, y, z, Q, u, sigma_y, sigma_z, H):
  
 # phi_x calculates the downwind dispersion based on the emission rate and wind speed.
    def phi_x(Q, u):
        return Q/u

# phi_y calculates the crosswind dispersion using a normal distribution formula. 
# It takes into account the crosswind  variance and the y-coordinate.    
    def phi_y(sigma_y, y):
        
        if np.sum(sigma_y) > 0.0:
            return 1/(np.sqrt(2*np.pi)*sigma_y)*np.exp(-np.power(y,2)/(2*np.power(sigma_y,2)))
        else:
            return 0.0

# phi_z calculates the vertical dispersion using a formula that considers the vertical-wind variance, the z-coordinate, and the effective source height.
    def phi_z(sigma_z, z, H):
        
        if np.sum(sigma_z) > 0.0:
                return 1/(np.sqrt(2*np.pi)*sigma_z)*(np.exp(-np.power(z-H, 2)/(2*np.power(sigma_z,2))) + np.exp(-np.power(z+H,2)/(2*np.power(sigma_z,2))))
        else:
            return 0.0
# The function returns the product of these three components, representing the concentration at the specified point in space.        
    return phi_x(Q,u)*phi_y(sigma_y, y)*phi_z(sigma_z, z, H)
