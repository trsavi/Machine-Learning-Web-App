# -*- coding: utf-8 -*-
"""

Main python file for Streamlit app

Author: Vukasin 

"""

import streamlit as st

st.title("Streamlit example")
st.write(""" 
         ## This is second header""")
         
st.sidebar.write(""" 
         ### This is second header""")

st.sidebar.selectbox("Select Brand", ("Mazda","Audi", "BMW"))

model = st.sidebar.selectbox("Select Model", ("308","C4", "508"))

st.write(model)
