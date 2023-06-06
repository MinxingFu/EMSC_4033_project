## EMSC4033 - Project Report

### Instruction

Gaussain plume model attempts to capture the physical processes associated with particle transport in the atmosphere. Transport and diffusion in the atmosphere are caused by winds.

In this project, we will use the Gaussian plume diffusion model, which represents the concentration distribution downwind of the point source as a Gaussian distribution. This code enables the visualization of the parameters of the Gaussian diffusion model and the concentration diffusion. During the running process, the program will ask you to enter some content, don't worry, there are detailed instructions. In addition to realizing visualization, two csv files will be produced, which are related to the parameter calculation link. The purpose is to present some important information more intuitively to readers for easy understanding.


In the code, Apikey of Google Map and Apikey of Open Weather Map are needed. For OpenWeatherMap, API_KEY = 'Enter your Apikey', url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}' Use; for Google Map, you need to set the environment variable in your computer as follows: 

os.environ["GOOGLE_API_KEY"] = "AIzaSyBI147RwjnsUBRoaRVLvAmDmbKrPeDyuVs"           api_key = os.environ["GOOGLE_API_KEY"].


When you input the coordinate origin and its time zone, the real-time atmospheric stability of the location can be generated, and the Gaussian diffusion model can generate two-dimensional and three-dimensional visualization images.


The progress of the project is carried out according to the following steps: determination of parameters - visualization of parameters - calculation of concentration - two-dimensional and three-dimensional visualization of concentration, visualization on Google Map.

### List of dependencies+short description

`requests`: The requests package is used for making HTTP requests. It allows you to send HTTP requests to a specified URL and handle the responses.


`datetime`: It allows you to work with dates, times, and time intervals, and perform various operations like formatting, parsing, and arithmetic calculations on dates and times.


`pysolar.solar`: Provides functions to calculate the solar position (altitude and azimuth) for a given location and time. 


`pytz`: Provides functionality to localize and convert datetime objects to different time zones.


`numpy` and `math`: Realize complex operations.


`csv`: It provides functionality to parse CSV data into Python data structures and vice versa.


`mpl_toolkits.mplot3d`: It enables the creation of 3D visualizations, including 3D scatter plots.


`from bokeh.io import output_notebookdisplay`: plot and visualization directly in a Jupyter notebook or a compatible notebook environment.


`from bokeh.io import show`: rendering the plot and displaying it in the output.


`from bokeh.plotting import gmap`:create a plot based on Google Maps data.


`from bokeh.models import GMapOptions`:specify the desired map type, zoom level, and other parameters.


`from bokeh.models import ColumnDataSource`:storing and organizing the data that will be visualized in the plot.


`from bokeh.transform import linear_cmap`:map a range of data values to a corresponding range of colors.


`from bokeh.palettes import Plasma256 as palette`:a set of 256 colors that can be used to represent data in a plot.


`from bokeh.models import ColorBar`:  create a color bar that represents the mapping between data values and colors in the plot.


`import os`:  provide access to various operating system functionalities. It allows the code to interact with the operating system, such as accessing files and directories.

### Testing

`test_atmospheric_stability` function:


"stability classes", which are based on empirical estimates of σy and σz. While stability classes are no longer the preferred method for calculating dispersion parameters, they are still commonly used in many contamination screening applications.Test cases for atmospheric stability.


`test_empr_cons` function:


Empirical constants are obtained according to the stability level and the location. Test case for empirical constants.


`test_emp_sigma_y` function:


After obtaining the stability and empirical constants, we can start to define the parameter. Test case for empirical sigma y.


`test_emp_sigma_z` function:


Test case for empirical sigma y.


`test_Drax_sigma_y()` function:


test case for the original function. It sets up the necessary variables and calculates the expected result based on the provided inputs.


`test_Drax_sigma_z()` function:


Similar to the previous function.


`test_concentration()` function:


It sets up the variables, calculates the expected result based on the provided inputs using the helper functions, and compares the actual and expected results using assert np.isclose().


### Some important results
* 3D Gaussian plume model visualization


![image](https://github.com/MinxingFu/EMSC_4033_project/assets/129235714/25a734cb-9e61-42da-b845-2ebc8744aec8)


* Taking Beijing as the origin, UTC time is 2023-06-06 00:46:50.612255+08:00, the diffusion map when the wind direction is 341°.


![image](https://github.com/MinxingFu/EMSC_4033_project/assets/129235714/f86fee3a-28d4-43f9-8bc5-69605be1466f)

### Limitations


In reality, in addition to the influencing factors discussed above, there are also parameters such as aerosol type, aerosol humidity, and air humidity that need to be included in the discussion. Furthermore, one of the major drawbacks of the standard Gaussian plume model is that it cannot handle changes in wind direction. 


### Future Improvements	


Through the above code, we calculate the parameters sigma_y and sigma_z through two different methods, and use the real-time wind speed, atmospheric conditions, and time of Beijing to draw the corresponding two parameter curves. Then, using the parameters calculated by the first method, the concentration-diffusion diagrams in the x-y plane and x-z plane were plotted. Finally, we simulated a concentration scatterplot of 5000 points in 3D space and Google map. How to build a time stack and determine the state of clouds at night is the direction that needs to be improved in the next step. 


In addition, Several extensions to the Gaussian plume model have been proposed to account for variations in the wind field, including the segmented Gaussian plume model and the Gaussian puff model.


### Reference


* Dean, C. L. (2015). Efficient MCMC Inference for Remote Sensing of Emission Sources. Master's thesis, Massachusetts Institute of Technology.

* Davies, & Thomson, D. J. (1999). Comparisons of some parametrizations of wind direction variability with observations. Atmospheric Environment (1994), 33(29), 4909–4917. https://doi.org/10.1016/S1352-2310(99)00287-3
