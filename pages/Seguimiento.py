#Librerias


import json

import streamlit as st

import pandas as pd




from streamlit_extras.colored_header import colored_header
from streamlit_echarts import st_echarts

from streamlit_lottie import st_lottie


#Recoger info del modelo



 
    
def print_result(data):
   
    
    option = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value","max":100},
    "series": [{"data": data, "type": "line"}],
    }
    
            
    st_echarts(
    options=option, height="400px",
    )


        

       
        



ejemplos_key=[]
ejemplos_values=[]


data = pd.read_csv('config/empleados.csv', sep=';')

ejemplos_dict = data.to_dict()

ejemplos_key=list(ejemplos_dict['keys'].values())
values=list(ejemplos_dict['values'].values())
valuesStr = [str(x) for x in values]
ejemplos_dict= dict(zip(ejemplos_key, valuesStr))




#data temporal


dict_Empleados=  json.load( open( "empleados_data/weekData.json" ) )





#animated

path = "images/animated/employee.json"
with open(path,"r") as file:
    urlEmployee = json.load(file)  





#Layout

st.set_page_config(
    layout="wide", page_title="Stress Monitor", page_icon="images/logo_top.png"
)



#Load CSS

css_file = open("config/estiloPage2.css","r").read()
st.markdown(css_file,unsafe_allow_html=True)




#Logo y titulo


c1, c2 = st.columns([0.2,0.7])


with c1:
    
    st_lottie(urlEmployee,
                    reverse=False,
                    height=110,
                    width=110,
                    speed=1,
                    loop=True,
                    quality='high',
                    key='test'
                )
    

with c2:
    st.caption("")
    new_title = '<p style="color:#00629b; font-size: 70px;">Stress Monitor</p>'
    st.markdown(new_title, unsafe_allow_html=True)

    
    




#### Pantalla


#Side Bar  con filtros




with st.sidebar:
    
    
    tab_title = '<p style="color:#00629b; font-size: 40px;">Control Panel</p>'
    st.markdown(tab_title, unsafe_allow_html=True)
    
    option = st.selectbox(
    "Select Employee",
    (ejemplos_key))
    

    cs1, cs2 = st.columns([0.2,0.8])
   
    
    with cs1:
        
        st.image(
            'images/logo_gsi.png',
            width=75,
        )
        

    with cs2:
        st.markdown(""" App created by [Intelligent Systems Group](https://gsi.upm.es).""")


colored_header(
    label='',
    description='',
    color_name="blue-90",
)

with st.container():
    print_result(dict_Empleados[ejemplos_dict[option]])
    


# Funciones de impresion de resultados
