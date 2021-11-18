# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 19:42:00 2021

@author: Vukasin
"""


import pandas as pd

data = pd.read_csv('./Data/carsPolovni.csv')

def get_brands():
    return list(data['Brend'].unique())

def get_models(brend):
    return list(data[data['Brend']==brend]['Model'].unique())

def get_car_types(model):
    return list(data[data['Model']==model]['Karoserija'].unique())

def get_car_volume(model, karoserija):
    return sorted(list(data[(data['Model']==model) & (data['Karoserija']==karoserija)]['Kubikaza'].unique()))

def get_fuel_type(model, karoserija):
    return list(data[(data['Model']==model) & (data['Karoserija']==karoserija)]['Gorivo'].unique())

def get_engine_power(model, kubikaza):
    return list(data[(data['Model']==model) & (data['Kubikaza']==kubikaza)]['Snaga'].unique())