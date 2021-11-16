# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:22:19 2021

@author: Vukasin 
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error


# Importing dataset

data = pd.read_csv('./Data/carsPolovni.csv')

from sklearn.preprocessing import OneHotEncoder

# create an object of the OneHotEncoder
OHE = OneHotEncoder()
OHE = OneHotEncoder(cols=['Brend',
                             'Model',
                             'Karoserija',
                             'Gorivo'],use_cat_names=True)
# encode the categorical variables
data = OHE.fit_transform(data)

print(data.info())