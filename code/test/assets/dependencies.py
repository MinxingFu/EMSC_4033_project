import numpy as np
import pandas as pd
import math
import csv
from mpl_toolkits.mplot3d import Axes3D
from bokeh.io import output_notebook
from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions
from bokeh.models import ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from bokeh.models import ColorBar
