
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

cars = pd.read_csv("./Data/usedCleaned21.csv")
df_enc = cars.drop(columns='Cena')
df_enc = pd.get_dummies(df_enc)


model = pickle.load(open('model_lgb21.pkl', 'rb'))
columns = ['Marka', 'Model','Godiste','Kilometraza', 'Karoserija', 'Gorivo', 'Kubikaza','Snaga motora',  'Pogon',
           'Menjac', 'Boja']

def predict_price(*params):
    parameters = params[0]
    params = [[k] for k in parameters]
    params_plus = [[k] for k in parameters]
    params_minus = [[k] for k in parameters]
    
    #(params_plus)
    params_plus[2][0] = int(params_plus[2][0]+1)
    params_minus[2][0] = int(params_minus[2][0]-1)
    #print(params_plus[2][0])
    
    
    params = dict(zip(columns, params))
    params_plus = dict(zip(columns, params_plus))
    params_minus = dict(zip(columns, params_minus))
    
    df1 = pd.get_dummies(pd.DataFrame(params))
    df2 = pd.get_dummies(pd.DataFrame(params_plus))
    df3 = pd.get_dummies(pd.DataFrame(params_minus))
    
    dummies_frame = df_enc
    df1 = df1.reindex(columns = dummies_frame.columns, fill_value=0)
    df2 = df2.reindex(columns = dummies_frame.columns, fill_value=0)
    df3 = df3.reindex(columns = dummies_frame.columns, fill_value=0)
    
    value = df1.iloc[0].values
    value_p = df2.iloc[0].values
    value_m = df3.iloc[0].values
    
    value = np.array(value).reshape((1,-1))
    value_p = np.array(value_p).reshape((1,-1))
    value_m = np.array(value_m).reshape((1,-1))
    
    prediction = model.predict(value).astype(int)
    prediction_p = model.predict(value_p).astype(int)
    prediction_m = model.predict(value_m).astype(int)
    
    return prediction, prediction_p, prediction_m
    
def recommend_car(car):
    
    mileage = car['Kilometraza']
    year = car['Godiste']
    volume = car['Kubikaza']
    power = car['Snaga motora']
    car_type =  car['Karoserija']
    price = car['Cena']
    
    if car_type=='Limuzina' or car_type=='Karavan':
        car_type=['Limuzina', 'Karavan']
    elif car_type=='Dzip/SUV':
        car_type=['Dzip/SUV', 'Karavan']
    elif car_type=='MiniVan':
        car_type=['MiniVan']
    else:
        car_type = ['Hecbek']
    
    mileage_high = mileage + 10000
    mileage_low = mileage - 10000
    
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
                  & (cars['Snaga motora']>=power_low) & (cars['Snaga motora']<=power_high)
                  & (cars['Cena']>=price_low) & (cars['Cena']<=price_high)]
        #(cars['Cena']>=price_low) & (cars['Cena']<=price_high)
        
        random_similar = df.sample(n=5, random_state=1)#.values.tolist()
        random_similar = random_similar[['Marka', 'Model', 'Godiste', 'Kilometraza', 'Gorivo', 'Kubikaza', 'Snaga motora', 'Cena']]
        random_similar['Kubikaza'] = random_similar['Kubikaza'] .round(decimals=1)

        if random_similar is not None:
            return random_similar

    except Exception as e:
        print(e)
        
def plot_avg(car):
    price = int(car['Cena'])
    model_name = car['Model']
    year = int(car['Godiste'])
    mean_price = cars[(cars['Model']==model_name)]
    fig = px.line(data_frame=mean_price.groupby(['Godiste'])['Cena'].mean().reset_index(), x="Godiste", y="Cena", title='Prosečna cena po godištu')
    fig.add_scatter(x = [year], y = [price], name='Predviđena cena')
    fig.update_layout(
    xaxis_title="Godiste",
    yaxis_title="Cena",
    font=dict(
        #family="Courier New",
        size=15
    ),
    xaxis = dict(
        tickmode = 'linear'
    )
    )
    fig.update_traces(marker=dict(size=15))
    return fig

def plot_predictd_years(previous, current, next_y, year):
    prices = [previous, current, next_y]
    years = [year-1, year, year+1]
    #years = [int(k) for k in years]
    fig = px.bar(x=years, y=prices, title='Predviđena cena za ±1 godinu sa istim parametrima')
    fig.update_layout(
    xaxis_title="Godiste",
    yaxis_title="Cena",
    font=dict(
        #family="Courier New",
        size=15
    ),
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
    )
    )

    return fig
