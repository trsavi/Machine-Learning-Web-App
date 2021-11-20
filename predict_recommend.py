# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 21:08:46 2021

Form after submitting car specifications

@author: Vukasin
"""

import pandas as pd
import numpy as np
import random

import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px
import pickle

cars = pd.read_csv("./Data/carsCleaned.csv")
df_enc = cars.drop(columns='Cena')
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
    
def recommend_car(car):
    
    mileage = car['Kilometraza']
    year = car['Godiste']
    volume = car['Kubikaza']
    power = car['Snaga']
    car_type =  car['Karoserija']
    price = car['Cena']
    
    if car_type=='Limuzina ' or car_type=='Karavan ':
        car_type=['Limuzina ', 'Karavan ']
    elif car_type=='Dzip/SUV ':
        car_type=['Dzip/SUV ', 'Karavan ']
    elif car_type=='Monovolumen (MiniVan) ':
        car_type=['Monovolumen (MiniVan) ']
    else:
        car_type = ['Hecbek ']
    
    mileage_high = mileage + 20000
    mileage_low = mileage - 20000
    
    year_high = year + 1
    year_low = year - 1
    
    volume_high = volume + volume*0.25
    volume_low = volume -  volume*0.25
    
    power_high = power + power*0.25
    power_low =  power - power*0.25
    
    price_high = price + price*0.1
    price_low = price - price*0.1
    
    try:
        df = cars[
                  (cars['Godiste']<=year_high) & (cars['Godiste']>=year_low) 
                  & (cars['Karoserija'].isin(car_type)) 
                  & (cars['Kilometraza']<=mileage_high) & (cars['Kilometraza']>=mileage_low)
                  & (cars['Kubikaza']>=volume_low) & (cars['Kubikaza']<=volume_high) 
                  & (cars['Snaga']>=power_low) & (cars['Snaga']<=power_high)
                  & (cars['Cena']>=price_low) & (cars['Cena']<=price_high)]
        #(cars['Cena']>=price_low) & (cars['Cena']<=price_high)
        
        random_similar = df.sample(n=5, random_state=1)#.values.tolist()
        
        #print(random_similar)
        return random_similar
    except Exception as e:
        print(e)
        
def plot_avg(model_name):
    mean_price = cars[(cars['Model']==model_name)]
    fig = px.line(data_frame=mean_price.groupby(['Godiste'])['Cena'].mean().reset_index(), x="Godiste", y="Cena", title='Prosečna cena po godištu')

    return fig






















