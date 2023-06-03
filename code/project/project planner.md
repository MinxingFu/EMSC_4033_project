# EMSC4033 project plan template

## Project title


Gaussian plume model visualization


## Executive summary


Atmospheric diffusion models attempt to capture the physical processes associated with particle transport in the atmosphere. Transport and diffusion in the atmosphere are caused by winds, which consist of large and small eddies. The massive eddies are called "winds" and transport particles downwind. Smaller scale eddies, known as "turbulence", cause particles to disperse randomly in both cross-wind direction and vertical direction.


## Goals

Draw the concentration distribution map of point source in the direction of diffusion, taking into account wind speed, wind direction, and atmospheric stability.

## Background and Innovation  

The initial ignition point after the fire is approximately regarded as a point source. According to the Gaussian diffusion model, the diffusion of a continuous point source (toxic smoke) satisfies the formula:

![image](https://user-images.githubusercontent.com/129235714/232651487-0770d2de-9429-4cf1-912c-350e69568eb0.png)

- C is the toxic smoke concentration at point (x, y, x).
- q is the aversion concentration of ignition point.
- σy and σx are the standard deviations in the horizontal and vertical directions respectively, that is, the diffusion parameters, which are determined by the stability of the atmosphere.
- u is the average wind speed.
- X is the distance from a point in the direction of wind propagation to the fire point.
- Y is the distance from a point in the vertical direction of the wind direction to the fire point.
- Z is the height of the point.
Through this diffusion formula, we can draw the concentration distribution map of the smoke diffusion area according to different initial smoke concentrations when the coordinates of the ignition point, the wind speed, wind direction and atmospheric stability of the point are known. According to the distribution map, the community in the area where the concentration of toxic gas is greater than the safe value is given a disaster prevention warning. The python library to be used, including but not limited to numpy, matplotlib.pyplot.
## Resources & Timeline

Wind speed and direction information is available from the Australian Bureau of Meteorology website.
Atmospheric stability can be obtained from wind speed and solar radiation level.
Concentration diffusion profile is implemented by code.

## Testing, validation, documentation

Use `pytest` to verify whether functions such as calculating atmospheric stability, concentration, and empirical parameters are valid.
