
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

year = st.sidebar.slider("Izaberi godište", year_min, year_max+1)

car_type = st.sidebar.selectbox("Izaberi karoseriju", carClass.get_car_types(brand, model))

volume = st.sidebar.selectbox("Izaberi kubikažu", carClass.get_car_volume(model, car_type))

fuel = st.sidebar.selectbox("Izaberi tip goriva", carClass.get_fuel_type(model, car_type))

mileage_min, mileage_max = carClass.get_car_mileage(model)
mileage_min = mileage_min-10000
mileage_max = mileage_max+10000
mileage = st.sidebar.slider('Izaberi kilometražu',mileage_min,mileage_max)

power_ = carClass.get_engine_power(model, volume)

power = st.sidebar.selectbox('Izaberi snagu motora (KS)',power_)

#emission = st.sidebar.selectbox('Izaberi emisionu klasu motora',carClass.get_emmision_class(model))

drive = st.sidebar.selectbox('Izaberi pogon',carClass.get_drive(model, car_type))

shift = st.sidebar.selectbox('Izaberi menjac',carClass.get_shift(model, car_type))

#doors = st.sidebar.selectbox('Izaberi broj vrata',carClass.get_no_doors(model, car_type))

color = st.sidebar.selectbox('Izaberi boju auta',carClass.get_colors())

#color_ent = st.sidebar.selectbox('Izaberi boju enterijera',carClass.get_enterior_color())

#ent_material = st.sidebar.selectbox('Izaberi materijal enterijera',carClass.get_material())




## Import dataframe and encode it

predicted_price, predicted_price_p, predicted_price_m = predict.predict_price([brand, model, year, mileage, car_type, fuel, volume, power, drive,
                                         shift, color])


st.header("Predviđena cena: {}€ ±5%".format(int(predicted_price[0])))
fig_year = predict.plot_predictd_years(predicted_price_m[0], predicted_price[0], predicted_price_p[0], year)
st.plotly_chart(fig_year, use_container_width=True)


## Show similar cars 

car = {'Marka' : brand,
       'Model' : model,
       'Godiste': year,
       'Karoserija': car_type,
       'Kubikaza' : volume,
       'Gorivo': fuel,
       'Kilometraza': mileage,
       'Snaga motora' : power,
       'Pogon': drive,
       'Menjac': shift,
       'Boja': color,
       'Cena': int(predicted_price[0])}

show_plot = st.sidebar.checkbox('Analiziraj cenu po godištu')

submit = st.sidebar.checkbox('Uporedi automobile')
    
if show_plot:
        
    fig = predict.plot_avg(car)

    st.plotly_chart(fig, use_container_width=True)


if submit:
    similar_cars = predict.recommend_car(car)
    if similar_cars is not None:
        
        # CSS to inject contained in a string
        hide_table_row_index = """
                    <style>
                    tbody th {display:none}
                    .blank {display:none}
                    </style>
                    """
        
        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        
        st.write("Pronašli smo sledeće automobile koji su slični izabranom:")
        st.table(similar_cars)
    else:
        st.write("Nismo pronašli slične automobile, pokušajte da promenite neke od parametara")

