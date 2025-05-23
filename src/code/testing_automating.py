import sys
import os
import pandas as pd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from models.auto_bri_calc import briCalc
from models.auto_preprocessing import preprocess
from models.auto_state_map import state_map
from models.all import map

df = pd.read_csv('../../data/aq_data_230525.csv')
map(df)