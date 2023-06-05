# EMSC4033 project plan template

## Project title


Gaussian plume model visualization


## Executive summary


The Gaussian plume model attempt to capture the physical processes associated with particle transport in the atmosphere. The Gaussian plume model is an idealized model that can be used to simulate the diffusion process of a gas point source under certain conditions. This project aims to use different methods to calculate the parameters in the Gaussian plume model, to visualize the model on different planes, and to visualize it in 3D space. Finally, the Gaussian diffusion of a given coordinate point at a given time is simulated in reality on Google Maps.


## Goals

Draw the concentration distribution map of point source in the direction of diffusion, taking into account wind speed, wind direction, and atmospheric stability.


The desired result would be a 2D diffusion map with different planes, a 3D diffusion map, and a real-time diffusion map drawn using Google Maps.

## Background and Innovation  


In this program, we will use the Gaussian plume diffusion model, which represents the concentration distribution downwind of the point source as a Gaussian distribution. In particular, the Gaussian plume model is only valid under these assumptions:
* The source is emitting at a constant rate.
* The source is a mathematical point (i.e. has no area).
* Wind speed and direction are constant across space and time.
* Statistics of turbulence are constant across space and time.
* The wind speed is sufficiently strong such that dispersion in the downwind direction is negligible compared to the advection (plume rise).
* Mass is conserved within the plume, or the pollutant neither deposits onto the ground nor undergoes chemical reaction within the atmosphere.


![image](https://github.com/MinxingFu/EMSC_4033_project/assets/129235714/4ae3a12b-62b3-4d0d-9131-00856bdcd438)


Through this diffusion formula, we can draw the concentration distribution map of the  diffusion area according to different source point concentrations when the coordinates of the original point, the wind speed, wind direction and atmospheric stability of the point are known. The python library to be used, including but not limited to `numpy`, `matplotlib.pyplot`, `requests`, `pysolar.solar`, `mpl_toolkits.mplot3d`, `csv`, `requests`.


## Resources & Timeline

* Wind speed and direction information is available from the Open Weather Map. For OpenWeatherMap, `API_KEY = 'Enter your Apikey'`, url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}' Use
* Through `pysolar.solar` and `pytz` packages, we can get wind speed and solar radiation level to calculate Atmospheric stability.
Concentration diffusion profile is implemented by code.
* Drawing We use Google Map, through a series of packages in `bokeh`, we can adjust the drawing parameters and get the desired diffusion map.
* April: Obtain the apikeys required by OPEN WEATHER MAP and Google Map, and write code to obtain wind speed, wind direction, sun altitude angle, and UTC time for a given coordinate.
* Early May: Write the code to calculate the parameters for the two different methods and to calculate the concentration formula.
* Mid-to-late May: Visualize the Gaussian plume model in 2D and 3D, and use Google map to analyze the real diffusion situation.
## Testing, validation, documentation

Use `pytest` to verify whether functions such as calculating atmospheric stability, concentration, and empirical parameters are valid.
