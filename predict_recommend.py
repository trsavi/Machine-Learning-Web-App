
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
from scipy.special import inv_boxcox, boxcox
import math

#lam_price = -0.18829260545282225
#lam_km = -0.38020162182547906


cars = pd.read_csv("./Data/usedCleanedPre.csv")
#cars['Cena'] = cars['Cena'].apply(lambda x: boxcox(x, lam_price))
#cars['prosek_god_km'] = cars['prosek_god_km'].apply(lambda x: boxcox(x, lam_km))
df_enc = cars.drop(columns=['Cena', 'Godiste','Kilometraza'])
df_enc = pd.get_dummies(df_enc)



model = pickle.load(open('./models/xg_model.pkl', 'rb'))
feature_importances = np.around((model.feature_importances_ / sum(model.feature_importances_)) * 100, 0)[:4]
results = pd.DataFrame({'Features': list(df_enc.columns[:4]),
                        'Importances': feature_importances})


columns = ['Marka', 'Model','Karoserija', 'Gorivo', 'Kubikaza','Snaga motora', 'EKM' ,'Pogon',
           'Menjac', 'Klima','Boja', 'Materijal enterijera', 'prosek_god_km','Starost', 'Km_cat']

def roundup(x):
    return int(math.ceil(int(x) / 10)) * 10

def convert_mileage(row):
    for i in range(80000, 320000, 10000):
        if row>=i and row<i+10000:
            return str(i)+"-"+str(i+10000)

def predict_price(*params):
    parameters = params[0]
    params = [[k] for k in parameters]
    params_plus = [[k] for k in parameters]
    params_minus = [[k] for k in parameters]
    

    params_plus[-2][0] = int(params_plus[-2][0]+1)
    params_minus[-2][0] = int(params_minus[-2][0]-1)
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

    prediction = roundup(model.predict(value).astype(float))
    prediction_p = roundup(model.predict(value_p).astype(float))
    prediction_m =roundup(model.predict(value_m).astype(float))

    return prediction, prediction_p, prediction_m
    
def recommend_car(car):
    
    mileage = car['Kilometraza']
    year = car['Godiste']
    volume = car['Kubikaza']
    power = car['Snaga motora']
    car_type =  car['Karoserija']
    price = car['Cena']
    model = car['Model']
    
    if car_type=='Limuzina' or car_type=='Karavan':
        car_type=['Limuzina', 'Karavan']
    elif car_type=='Dzip/SUV':
        car_type=['Dzip/SUV', 'Karavan']
    elif car_type=='MiniVan':
        car_type=['MiniVan']
    else:
        car_type = ['Hecbek']
    
    mileage_high = mileage + 20000
    mileage_low = mileage - 20000
    
    year_high = year + 1
    year_low = year - 1
    
    volume_high = volume + volume*0.15
    volume_low = volume -  volume*0.15
    
    power_high = power + power*0.20
    power_low =  power - power*0.20
    
    price_high = price + price*0.2
    price_low = price - price*0.2
    
    try:
        df = cars[
                  (cars['Godiste']<=year_high) & (cars['Godiste']>=year_low) 
                  & (cars['Karoserija'].isin(car_type)) 
                  & (cars['Kilometraza']<=mileage_high) & (cars['Kilometraza']>=mileage_low)
                  & (cars['Kubikaza']>=volume_low) & (cars['Kubikaza']<=volume_high) 
                  & (cars['Snaga motora']>=power_low) & (cars['Snaga motora']<=power_high)
                  & (cars['Cena']>=price_low) & (cars['Cena']<=price_high)
                  & (~cars['Model'].isin([model]))]
        
        #print(df.count()[0])
        if df.count()[0]>=5:
            n = 5
        else:
            n = df.count()[0]
        random_similar = df.sample(n=n, random_state=1).drop_duplicates(['Model'])
        
        random_similar = random_similar[['Marka', 'Model', 'Godiste', 'Kilometraza', 'Gorivo', 'Kubikaza', 'Snaga motora', 'Cena']]
        #random_similar['Kubikaza'] = random_similar['Kubikaza'].round(decimals=1)
        #print(random_similar)
        if random_similar is not None:
            if not random_similar.empty:
                return random_similar

    except Exception as e:
        print(e)
        
def plot_avg(car, other=None):
    price = int(car['Cena'])
    model_name = car['Model']
    year = int(car['Godiste'])
    if other==None:
        mean_price = cars[(cars['Model']==model_name)]
    else:
        other.append(model_name)
        mean_price = cars[(cars['Model'].isin(other)) & (cars['Godiste']<(cars[(cars['Model']==model_name)]['Godiste'].max()))]
    #mean_price.groupby(['Model', 'Godiste'])['Cena'].mean().reset_index()
    fig = px.line(data_frame=mean_price.groupby(['Model', 'Godiste'])['Cena'].mean().reset_index(), x="Godiste", y="Cena", title='Prosečna cena po godištu', color='Model')
    fig.add_scatter(x = [year], y = [price], name='Predviđena cena')

    fig.update_layout(
    xaxis_title="Godiste",
    yaxis_title="Cena",
    font=dict(

        size=15
    ),
    xaxis = dict(
        tickmode = 'linear'
    )
    )

    fig.update_traces(marker=dict(size=15), line=dict(width=2.5))
    return fig

def plot_predictd_years(previous, current, next_y, year):
    prices = [previous, current, next_y]
    years = [year-1, year, year+1]
    colors = ['royalblue',] * 3
    colors[1] = 'crimson'
    fig = go.Figure()
    #fig = px.bar(x=years, y=prices, title='Predviđena cena za ±1 godinu sa istim parametrima', width=500, height=500)
    fig.add_trace(go.Bar(x=years, y=prices,
    marker_color=colors))
    fig.update_layout(title = 'Predviđena cena za ±1 godinu sa istim parametrima',
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
def plot_pie():
    fig = px.bar(data_frame = results, y ='Features', x = 'Importances', orientation='h', title="Uticaj parametara na cenu automobila u %",text="Importances")
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, font=dict(
        size=15
    ),
    xaxis_title="Značaj u procentima",
    yaxis_title="Parametar"
    )
    
    return fig
    
