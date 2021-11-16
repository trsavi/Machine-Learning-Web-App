# -*- coding: utf-8 -*-
"""

Main python file for Streamlit app

Author: Vukasin 

"""

import streamlit as st

### Info

st.title("Predicting used car price")


st.write("Prediction is based on car specification that you can enter in left sidemenu")
         
st.sidebar.write(""" # Car specifications """)

## Entering car specification

brand = st.sidebar.selectbox("Select Brand", ("Mazda","Audi", "BMW"))

model = st.sidebar.selectbox("Select Model", ("308","C4", "508"))

mileage = st.sidebar.slider('Enter mileage',50000,250000)