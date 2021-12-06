# -*- coding: utf-8 -*-
"""

Main python file for Streamlit app

Author: Vukasin 

"""

import streamlit as st
import carClass
import predict_recommend as predict
import pandas as pd


### Info

st.title("Predviđanje cene polovnih automobila")


st.write(""" Predikcija cene polovnog automobila se izračunava na osnovu unetih parametrata u opcijama sa leve strane. """)
         
st.sidebar.write(""" # Specifikacije automobila """)


## Entering car specification

brand = st.sidebar.selectbox("Izaberi brend", carClass.get_brands())

model = st.sidebar.selectbox("Izaberi model", carClass.get_models(brand))

year_min, year_max = carClass.get_car_year(model)

year = st.sidebar.slider("Izaberi godište", year_min, year_max)

car_type = st.sidebar.selectbox("Izaberi karoseriju", carClass.get_car_types(brand, model))

volume = st.sidebar.selectbox("Izaberi kubikažu", carClass.get_car_volume(model, car_type))

fuel = st.sidebar.selectbox("Izaberi tip goriva", carClass.get_fuel_type(model, car_type))

mileage = st.sidebar.slider('Izaberi kilometražu',50000,300000)

power = st.sidebar.selectbox('Izaberi snagu motora (KS)',carClass.get_engine_power(volume))

emission = st.sidebar.selectbox('Izaberi emisionu klasu motora',carClass.get_emmision_class())

drive = st.sidebar.selectbox('Izaberi pogon',carClass.get_drive(model, car_type))

shift = st.sidebar.selectbox('Izaberi menjac',carClass.get_shift(model, car_type))

doors = st.sidebar.selectbox('Izaberi broj vrata',carClass.get_no_doors(model, car_type))

color = st.sidebar.selectbox('Izaberi boju auta',carClass.get_colors())

color_ent = st.sidebar.selectbox('Izaberi boju enterijera',carClass.get_enterior_color())

ent_material = st.sidebar.selectbox('Izaberi materijal enterijera',carClass.get_material())


submit = st.sidebar.checkbox('Uporedi automobile')


## Import dataframe and encode it

predicted_price = predict.predict_price([brand, model, year, mileage, car_type, fuel, volume, fuel , power, emission, drive,
                                         shift, doors, color, color_ent, ent_material])
#st.write(predicted_price)
st.header("Predviđena cena: {}€ ±5%".format(int(predicted_price[0])))
## Show similar cars 

car = {'Brend' : brand,
       'Model' : model,
       'Godiste': year,
       'Karoserija': car_type,
       'Kubikaza' : volume,
       'Gorivo': fuel,
       'Kilometraza': mileage,
       'Snaga' : power,
       'Cena': int(predicted_price[0])}



if submit:
    similar_cars = predict.recommend_car(car)
    st.table(similar_cars)
    show_plot = st.checkbox('Analiziraj cenu po godištu')
    
    if show_plot:
        
        fig = predict.plot_avg(model)
        
        st.plotly_chart(fig, use_container_width=True)
    