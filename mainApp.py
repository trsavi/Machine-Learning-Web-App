
# -*- coding: utf-8 -*-
"""

Main python file for Streamlit app

Author: Vukasin 

"""

import streamlit as st
import carClass
import predict_recommend as predict
import pandas as pd
import matplotlib.pyplot as plt

### Info
st.set_page_config(layout="wide")


container = st.container()
columns = st.columns((1,1))


with container:
    st.title("Predviđanje cene polovnih automobila")
    
    
    st.subheader(""" Predikcija cene polovnog automobila se izračunava na osnovu unetih parametrata u opcijama sa leve strane. """)
    
st.sidebar.write(""" # Specifikacije automobila """)


## Entering car specification

brand = st.sidebar.selectbox("Izaberi brend", carClass.get_brands())

model = st.sidebar.selectbox("Izaberi model", carClass.get_models(brand))

year_min, year_max = carClass.get_car_year(model)

year = st.sidebar.slider("Izaberi godište", year_min, year_max)

car_type = st.sidebar.selectbox("Izaberi karoseriju", carClass.get_car_types(brand, model))

volume = st.sidebar.selectbox("Izaberi kubikažu", carClass.get_car_volume(model, car_type))

fuel = st.sidebar.selectbox("Izaberi tip goriva", carClass.get_fuel_type(model, car_type))

mileage_min, mileage_max = carClass.get_car_mileage(model, year)
mileage_min = mileage_min+10000
mileage_max = mileage_max-10000
mileage = st.sidebar.slider('Izaberi kilometražu',mileage_min,mileage_max)

power_ = carClass.get_engine_power(model, volume)

power = st.sidebar.selectbox('Izaberi snagu motora (KS)',power_)

emission = st.sidebar.selectbox('Izaberi emisionu klasu motora',carClass.get_emmision_class(model, year))

drive = st.sidebar.selectbox('Izaberi pogon',carClass.get_drive(model, car_type))

shift = st.sidebar.selectbox('Izaberi menjac',carClass.get_shift(model, car_type))

ac = st.sidebar.selectbox('Klima',carClass.get_ac(model))

color = st.sidebar.selectbox('Izaberi boju auta',carClass.get_colors())

material = st.sidebar.selectbox('Izaberi materijal enterijera',carClass.get_material())

avg_odo = mileage/2021-year

## Import dataframe and encode it

predicted_price, predicted_price_p, predicted_price_m = predict.predict_price([brand, model, year, mileage, car_type, fuel, volume, power,emission, drive,
                                         shift, ac, color, material, avg_odo])

with container:
    st.header("Predviđena cena: {}€ ±5%".format(predicted_price))
with columns[0]:
    fig_year = predict.plot_predictd_years(predicted_price_m, predicted_price, predicted_price_p, year)
    st.plotly_chart(fig_year)
with columns[1]:
    figure = predict.plot_pie()
    st.plotly_chart(figure)
    st.markdown("__Napomena__: _Ostali parametri imaju značaj > 2% na predikciju cene_")


## Show similar cars 

car = {'Marka' : brand,
       'Model' : model,
       'Godiste': year,
       'Karoserija': car_type,
       'Kubikaza' : volume,
       'Gorivo': fuel,
       'Kilometraza': mileage,
       'Snaga motora' : power,
       'EKM': emission,
       'Pogon': drive,
       'Menjac': shift,
       'Klima': ac,
       'Boja': color,
       'Materijal enterijera': material,
       'Cena': int(predicted_price)}

#show_plot = st.sidebar.checkbox('Analiziraj cenu po godištu')

submit = st.sidebar.checkbox('Pronađi slične automobile automobile/analiziraj cenu po godištu')

    
#if show_plot:
        
#    fig = predict.plot_avg(car)

#    st.plotly_chart(fig, use_container_width=True)


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
        #if show_plot:
        similar_list = similar_cars.values.tolist()
        lista_slicnih = []
        for s in similar_list:
            lista_slicnih.append(" | ".join([str(elem) for elem in s]))
        options = st.multiselect(
            'Uporedi slične automobile različitih modela',
            lista_slicnih
            )

        options = [k.replace(" | ",",").split(",")[1] for k in options]
        #(options)
        fig = predict.plot_avg(car, other=options)

        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.write("Nismo pronašli slične automobile, pokušajte da promenite neke od parametara")
        fig = predict.plot_avg(car, other=None)
        st.plotly_chart(fig, use_container_width=True)

