# -*- coding: utf-8 -*-
"""

Main python file for Streamlit app

Author: Vukasin 

"""

import streamlit as st
import carClass, predict
import pandas as pd

### Info

st.title("Predviđanje cene polovnih automobila")


st.write(""" Predikcija cene polovnog automobila se izračunava na osnovu unetih parametrata u opcijama sa leve strane. """)
         
st.sidebar.write(""" # Specifikacije automobila """)


## Entering car specification

brand = st.sidebar.selectbox("Izaberi brend", carClass.get_brands())

model = st.sidebar.selectbox("Izaberi model", carClass.get_models(brand))

year = st.sidebar.slider("Izaberi godište", 2000, 2017)

car_type = st.sidebar.selectbox("Izaberi karoseriju", carClass.get_car_types(model))

volume = st.sidebar.selectbox("Izaberi kubikažu", carClass.get_car_volume(model, car_type))

fuel = st.sidebar.selectbox("Izaberi tip goriva", carClass.get_fuel_type(model, car_type))

mileage = st.sidebar.slider('Izaberi kilometražu',50000,300000)

power = st.sidebar.slider('Izaberi snagu motora (KS)',60,250)

submit = st.sidebar.button('Izračunaj cenu')

## Import dataframe and encode it

st.write(predict.predict_price([brand, model, year, car_type, volume, fuel, mileage, power]))
