# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 19:42:00 2021

@author: Vukasin
"""


import pandas as pd

data = pd.read_csv('./Data/usedCleaned20.csv')

print(data.columns)

# Get bradns
def get_brands():
    return sorted(list(data['Marka'].unique()))

# Get models
def get_models(brend):
    return sorted(list(data[data['Marka']==brend]['Model'].unique()))

# Get car types
def get_car_types(brend, model):
    return list(data[(data['Model']==model) & (data['Marka']==brend)]['Karoserija'].unique())
        
# Get car year
def get_car_year(model):
    return int(data[data['Model']==model]['Godiste'].min()), int(data[data['Model']==model]['Godiste'].max())

# Get car volume
def get_car_volume(model, karoserija):
    return sorted(list(data[(data['Model']==model) & (data['Karoserija']==karoserija)]['Kubikaza'].unique()))

# Get fuel type
def get_fuel_type(model, karoserija):
    return list(data[(data['Model']==model) & (data['Karoserija']==karoserija)]['Gorivo'].unique())

# Get engine power
def get_engine_power(kubikaza):
    return sorted(list(data[(data['Kubikaza']==kubikaza)]['Snaga motora'].unique()))

# Get engine emmision class
def get_emmision_class():
    return sorted(list(data['EKM'].unique()))

# Get car drive system
def get_drive(model, car_type):
    return sorted(list(data[(data['Model']==model) & (data['Karoserija']==car_type)]['Pogon'].unique()))

# Get type of shift
def get_shift(model, car_type):
    return sorted(list(data[(data['Model']==model) & (data['Karoserija']==car_type)]['Menjac'].unique()))

# Get number of doors
def get_no_doors(model, car_type):
    return sorted(list(data[(data['Model']==model) & (data['Karoserija']==car_type)]['Broj vrata'].unique()))

# Get car colors
def get_colors():
    return sorted(list(data['Boja'].unique()))

# Get colors of enterior
def get_enterior_color():
    return sorted(list(data['Boja enterijera'].unique()))
# Get materials
def get_material():
    return sorted(list(data['Materijal enterijera'].unique()))
    