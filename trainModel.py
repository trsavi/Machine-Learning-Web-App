# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:22:19 2021

@author: Vukasin 
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error


# Importing dataset

data = pd.read_csv('./Data/cleanedPolovni.csv')

data.head()