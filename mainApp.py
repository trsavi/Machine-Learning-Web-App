# -*- coding: utf-8 -*-
"""

Main python file for Streamlit app

Author: Vukasin 

"""

import streamlit as st
import carClass

### Info

st.title("Predicting used car price")


st.write("Prediction is based on car specification that you can enter in left sidemenu")
         
st.sidebar.write(""" # Car specifications """)


## Entering car specification

brand = st.sidebar.selectbox("Select Brand", carClass.get_brands())

model = st.sidebar.selectbox("Select Model", carClass.get_models(brand))

car_type = st.sidebar.selectbox("Select car type", carClass.get_car_types(model))

car_volume = st.sidebar.selectbox("Select engine volume", carClass.get_car_volume(model))

car_volume = st.sidebar.selectbox("Select fuel type", carClass.get_fuel_type(model, car_type))

mileage = st.sidebar.slider('Enter mileage',50000,250000)

power = st.sidebar.slider('Enter engine power',60,250)


