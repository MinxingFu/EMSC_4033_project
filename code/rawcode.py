#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import datetime
from pysolar.solar import get_altitude, get_azimuth
import pytz
import numpy as np
import csv
from mpl_toolkits.mplot3d import Axes3D


# In[2]:


def atmospheric_stability(wind_speed, day_time, day_type):
    
    if day_time: 
        
        if day_type not in ['Strong', 'Moderate', 'Slight']:
            raise ValueError('Only support Strong, Moderate, or Slight for daytime')
        else:
           
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
    else: 
        if day_type not in ['Cloudy', 'Clear']:
            raise ValueError('Only support Clear or Cloudy for nighttime')
        else: 
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



wind_speed_intervals = {
    'Strong': {
        True: [[0, 2], [2, 3], [3, 5], [5, float('inf')]],
        False: [[0, float('inf')]]
    },
    'Moderate': {
        True: [[0, 2], [2, 3], [3, 5], [5, 6], [6, float('inf')]],
        False: [[6, float('inf')]]
    },
    'Slight': {
        True: [[0, 2], [2, 5], [5, float('inf')]],
        False: [[5, float('inf')]]
    },
    'Cloudy': {
        True: [[0, 3], [3, float('inf')]],
        False: [[3, float('inf')]]
    },
    'Clear': {
        True: [[0, 3], [3, 5], [5, float('inf')]],
        False: [[5, float('inf')]]
    }
}


day_types = ['Strong', 'Moderate', 'Slight', 'Cloudy', 'Clear']


results = []


for day_type in day_types:

    day_time = day_type in ['Strong', 'Moderate', 'Slight']


    wind_speed_intervals_day = wind_speed_intervals[day_type][True]
    wind_speed_intervals_night = wind_speed_intervals[day_type][False]


    for speed_interval in wind_speed_intervals_day:
        stability = atmospheric_stability(np.mean(speed_interval), day_time, day_type)
        results.append([speed_interval, day_time, day_type, stability])


        stability = atmospheric_stability(np.mean(speed_interval), day_time, day_type)
        results.append([speed_interval, day_time, day_type, stability])


csv_file = 'stability_classes.csv'


with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Wind Speed Interval', 'Day Time', 'Day Type', 'Stability Class'])
    writer.writerows(results)
    
csv_file = 'stability_classes.csv'


# In[3]:



def empr_cons(stability_class, urban):
    
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
        

scenarios = [
    ('A', True),
    ('A-B',True),
    ('B', True),
    ('C', True),
    ('D', True),
    ('E-F',True),
    ('E', True),
    ('F', True),
    ('A', False),
    ('B', False),
    ('C', False),
    ('D', False),
    ('F', False)
]


results = []


for stability_class, urban in scenarios:

    constants = empr_cons(stability_class, urban)
    

    results.append([stability_class, urban] + list(constants))


csv_file = 'empirical_constants.csv'


with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Stability Class', 'Urban', 'a', 'b', 'c', 'd', 'e', 'f'])
    writer.writerows(results)


# In[4]:


def emp_sigma_y(a, b, c, x):
    return (a * x) / np.power((1 + b * x), c)

def emp_sigma_z(d, e, f, x):
    if f is None: 
        return d * x 
    else:
        return (d * x) / np.power(1 + e * x, f)


# In[5]:



API_KEY = '75e9336157d81b8e43fa1671f82ad0f2'

def get_wind_data(lat, lon):

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'

    response = requests.get(url)
    data = response.json()

    if 'wind' in data:
        wind_speed = data['wind']['speed']
        wind_dir = data['wind']['deg']
        return wind_speed, wind_dir
    else:
        return None

lat = 39.9096834
lon = 116.398954
wind_data = get_wind_data(lat, lon) 


if wind_data is not None:
    wind_speed, wind_dir = wind_data
    print(f'Wind speed: {wind_speed} m/s')
    print(f'Wind direction: {wind_dir} degrees')
else:
    print('Unable to retrieve wind data')
    
tz = pytz.timezone('Asia/Shanghai') 


dt = datetime.datetime.now(tz) 
sea = get_altitude(lat, lon, dt) 
# output
print("current time: ", dt)
print("sun elevation angle: ", sea)


# In[6]:



day_time = input("Is it day or night? (Enter 'day' or 'night'): ").lower() == 'day'
day_time = bool(day_time)  
day_type = input("Enter the day type (Strong, Moderate, Slight for daytime; Clear or Cloudy for nighttime): ")


urban = input("Is it an urban environment? (Enter 'yes' or 'no'): ").lower() == 'yes'
urban = bool(urban) 

print(day_time)
print(day_type)
print(urban)


# In[7]:



stability_class = atmospheric_stability(wind_speed, day_time, day_type)


constants = empr_cons(stability_class, urban)

print('Stability Class: ', stability_class)
print('empr_cons: ', constants)
x = np.linspace(100, 100000, 100000) 
a, b, c, d, e, f = constants 
emp_sigma_y = emp_sigma_y(a, b, c, x) 
emp_sigma_z = emp_sigma_z(d, e, f, x) 


# In[8]:


import matplotlib.pyplot as plt

x = np.linspace(100, 100000, 100000)
plt.figure(figsize=(10, 10))
plt.loglog(x, emp_sigma_y, label='$\sigma_y$')
plt.loglog(x, emp_sigma_z, label='$\sigma_z$')
plt.grid(True, which='both', ls='--')
plt.xlabel('x(m)')
plt.legend()
plt.title('The parameters obtained by the first method')
plt.show()


# In[9]:



def Drax_sigma_y(stability, x, sigma_v, u):
    t = x / u
    
    if stability == "Stable":
        TL_y = 1000 * 1.64
    else:
        TL_y = 1000 * 1.64

    theta = np.arctan(sigma_v / u)
    fy = 1 / (1 + (t / TL_y) ** 0.5)

    return theta * x * fy  #returns the Drax value of sigma_y.


# In[10]:



def Drax_sigma_z(stability, x, sigma_w, u):
    t = x / u
    
    if stability == "Stable":
        TL_z = 100 * 1.64
    else:
        TL_z = 500 * 1.64

    phi = np.arctan(sigma_w / u)

    fz = 1 / (1 + 0.9 * (t / TL_z) ** 0.5)

    return phi * x * fz 


# In[11]:


stability = input("Enter the stability type (Stable or Unstable): ")
sigma_v = 10
sigma_w = 10
u = wind_speed
x = np.linspace(100, 100000, 100000) 
Drax_sigma_y_values = Drax_sigma_y(stability, x, sigma_v, u)
Drax_sigma_z_values = Drax_sigma_z(stability, x, sigma_w, u)

plt.figure(figsize=(10, 10))
plt.loglog(x, Drax_sigma_y_values, label='Drax_sigma_y')
plt.loglog(x, Drax_sigma_z_values, label='Drax_sigma_z')
plt.grid(True, which='both', ls='--')
plt.xlabel('x')
plt.legend()
plt.title('The parameters obtained by the second method')
plt.show()


# In[12]:



def concentration(x, y, z, Q, u, sigma_y, sigma_z, H):
  

    def phi_x(Q, u):
        return Q/u


 
    def phi_y(sigma_y, y):
        
        if np.sum(sigma_y) > 0.0:
            return 1/(np.sqrt(2*np.pi)*sigma_y)*np.exp(-np.power(y,2)/(2*np.power(sigma_y,2)))
        else:
            return 0.0


    def phi_z(sigma_z, z, H):
        
        if np.sum(sigma_z) > 0.0:
                return 1/(np.sqrt(2*np.pi)*sigma_z)*(np.exp(-np.power(z-H, 2)/(2*np.power(sigma_z,2))) + np.exp(-np.power(z+H,2)/(2*np.power(sigma_z,2))))
        else:
            return 0.0
        
    return phi_x(Q,u)*phi_y(sigma_y, y)*phi_z(sigma_z, z, H)


# In[13]:



def emp_sigma_y(a, b, c, x):
    return (a * x) / np.power((1 + b * x), c) 

def emp_sigma_z(d, e, f, x):
    if f is None: 
        return d * x 
    else:
        return (d * x) / np.power(1 + e * x, f)
x = np.linspace(0, 100, 200)  
y = np.linspace(-50, 50, 200)  
z = 35  
Q = 1000  
u = wind_speed 
sigma_y = emp_sigma_y(a, b, c, x)
sigma_z = emp_sigma_z(d, e, f, x)  
H = 30  



X, Y = np.meshgrid(x, y)


conc = concentration(X, Y, z, Q, u, sigma_y, sigma_z, H)


plt.figure(figsize=(10, 10))
plt.imshow(conc, cmap='viridis', origin='lower', extent=(0, 100, -50, 50))
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.colorbar(label='Concentration')
plt.title('Concentration Distribution')
plt.show()


# In[14]:


p = np.linspace(0, 100, 200)  
pz = np.linspace(20, 40, 200)  
Q = 1000  
u = wind_speed  
sigma_y = emp_sigma_y(a, b, c, x)  
sigma_z = emp_sigma_z(d, e, f, x)  
H = 30 

conc = np.zeros((len(p), len(pz)))

for i, x in enumerate(p): 
    for k, z in enumerate(pz):
        conc[k, i] = concentration(x, 0, z, Q, u, sigma_y[i], sigma_z[i], H)

plt.figure(figsize=(10, 10))

plt.contourf(p, pz, conc, cmap='viridis', levels=np.linspace(0, 5, 100))
plt.colorbar()
plt.xlabel('x(m)')
plt.ylabel('Emission Height(m)')
plt.show()


# In[15]:



num_points = 5000  
px = np.random.uniform(0, 1000, num_points)  
py = np.random.uniform(-100, 100, num_points) 
pz = np.random.uniform(0, 60, num_points)  

Q = 100
u = wind_speed  
H = 30  


sigma_y = emp_sigma_y(a, b, c, x)  
sigma_z = emp_sigma_z(d, e, f, x) 

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')


ctemp = concentration(px, py, pz, Q, u, sigma_y, sigma_z, H)


ax.scatter(px, py, pz, c=ctemp, cmap='YlOrRd', alpha=1.0)


ax.set_xlabel('X(m)')
ax.set_ylabel('Y(m)')
ax.set_zlabel('Z(m)')
ax.set_title('Gas Diffusion Concentration')


plt.colorbar
plt.show()


# In[16]:


num_points = 5000  
px = np.random.uniform(0, 200, num_points)  
py = np.random.uniform(-100, 100, num_points)  
pz = 35

Q = 10000  
u = wind_speed  
H = 30  


sigma_y = emp_sigma_y(a, b, c, x)  
sigma_z = emp_sigma_z(d, e, f, x)


concentration_values = concentration(px, py, pz, Q, u, sigma_y, sigma_z, H)


data = list(zip(px, py, concentration_values))


file_path = 'data_points.csv'


with open(file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['x', 'y', 'concentration'])  
    writer.writerows(data) 

print(f"CSV file '{file_path}' has been generated with {num_points} data points.")


# In[17]:


import math




longitude_ref = 116.398954 
latitude_ref = 39.9096834 

def convert_coordinates_to_lat_lon(x, y, longitude_ref, latitude_ref):
    
    earth_radius = 6371000  
   
    lon = longitude_ref + math.degrees(x / earth_radius / math.cos(math.radians(latitude_ref)))
    lat = latitude_ref + math.degrees(y / earth_radius)

   
    lon = round(lon, 6)
    lat = round(lat, 6)

    return lon, lat




data_points = []
with open('data_points.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  
    for row in reader:
        x, y, concentration = float(row[0]), float(row[1]), float(row[2])
        data_points.append((x, y, concentration))


converted_data_points = []
for x, y, concentration in data_points:
    lon, lat = convert_coordinates_to_lat_lon(x, y, longitude_ref, latitude_ref)
    converted_data_points.append({'lon': lon, 'lat': lat, 'Concentration': concentration})


output_file = 'converted_data.csv'


with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['lon', 'lat', 'Concentration']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(converted_data_points)

print("Data conversion and CSV file generation completed.")


# In[21]:


from bokeh.io import output_notebook
import pandas as pd
import os 
from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions
from bokeh.models import ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from bokeh.models import ColorBar
output_notebook()
bokeh_width, bokeh_height = 500,400


# In[22]:


df = pd.read_csv('converted_data.csv')
df.head()


# In[23]:



os.environ["GOOGLE_API_KEY"] = "AIzaSyBI147RwjnsUBRoaRVLvAmDmbKrPeDyuVs"
api_key = os.environ["GOOGLE_API_KEY"]


# In[24]:



def plot(lat, lng, zoom=12, map_type='roadmap'):

    gmap_options = GMapOptions(lat=lat, lng=lng, 
                               map_type=map_type, zoom=zoom)

    p = gmap(api_key, gmap_options, 
             width=bokeh_width, height=bokeh_height)
   
    center = p.circle([lng], [lat], size=10, alpha=1, color='red')
    show(p)
    return p

p = plot(lat, lon, map_type='terrain')


# In[25]:


df.shape 
dfb = df[df['Concentration']>0.].copy() 


def plot(df, lat, lng, zoom=17, map_type='roadmap'):
    gmap_options = GMapOptions(lat=lat, lng=lng, 
                               map_type=map_type, zoom=zoom)
    p = gmap(api_key, gmap_options, title='Simulation graph of pollutant concentration distribution', 
             width=bokeh_width, height=bokeh_height)
  
    source = ColumnDataSource(df)
  
    
    mapper = linear_cmap('Concentration', palette, 0., 10.)  
   
    center = p.circle('lon', 'lat',  size=3, alpha=1,       
                      color=mapper, source=source)
    
    color_bar = ColorBar(color_mapper=mapper['transform'],   
                         location=(0,0), title='Concentration ')
    p.add_layout(color_bar, 'right')
    show(p)
    return p

p = plot(dfb, lat, lon, map_type='satellite')


# In[ ]:




