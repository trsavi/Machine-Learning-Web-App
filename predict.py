# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 21:08:46 2021

Form after submitting car specifications

@author: Vukasin
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls

import pickle

df_enc = pd.read_csv("./Data/carsCleaned.csv")
df_enc = df_enc.drop(columns='Cena')
df_enc = pd.get_dummies(df_enc)


model = pickle.load(open('ml_model', 'rb'))
columns = ['Brend', 'Model','Godiste','Karoserija', 'Kubikaza', 'Gorivo', 'Kilometraza','Snaga']

def predict_price(*params):
    
    params = [[k] for k in params[0]]
    
    params = dict(zip(columns, params))
    
    df1 = pd.get_dummies(pd.DataFrame(params))
    dummies_frame = df_enc
    df1 = df1.reindex(columns = dummies_frame.columns, fill_value=0)
    
    value = df1.iloc[0].values
    value = np.array(value).reshape((1,-1))
    
    prediction = model.predict(value).astype(int)
    return prediction
    
