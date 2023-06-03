import numpy as np
import pandas as pd
import math
import requests
import datetime
from pysolar.solar import get_altitude, get_azimuth
import pytz
import csv
from mpl_toolkits.mplot3d import Axes3D
from bokeh.io import output_notebook
import os 
from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions
from bokeh.models import ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from bokeh.models import ColorBar