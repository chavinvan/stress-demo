#Librerias

import csv
import json
import pickle
import streamlit as st
import requests
import pandas as pd
import numpy as np
from PIL import Image
import pandas as pd
import stress_demo_utils as detect
from sentence_transformers import SentenceTransformer
from streamlit_elements import elements
from streamlit_elements import dashboard

from streamlit_elements import mui


from streamlit_extras.colored_header import colored_header
from streamlit_echarts import st_echarts

from streamlit_lottie import st_lottie


#Recoger info del modelo



 
    
def print_result():
    
    option = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [{"data": [10, 30, 10, 50, 20, 40, 80], "type": "line"}],
    }
    
            
    st_echarts(
    options=option, height="400px",
    )


        

       
        



ejemplos_key=[]
ejemplos_values=[]


data = pd.read_csv('config/empleados.csv', sep=';', quoting=csv.QUOTE_ALL)

ejemplos_dict = data.to_dict()

ejemplos_key=list(ejemplos_dict['keys'].values())
values=list(ejemplos_dict['values'].values())
ejemplos_dict=dictionary = dict(zip(ejemplos_key, values))


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

    
    



# Inicializacion de variables

if not "results_shown" in st.session_state:
    st.session_state["results_shown"] = False
    
if not "datos" in st.session_state:
    st.session_state["datos"] = None
    
if not "modelo" in st.session_state:
    st.session_state["modelo"] = pickle.load(open('model/svm_model.sav', 'rb'))
    
if not "embs" in st.session_state:
    st.session_state["embs"] = SentenceTransformer('all-mpnet-base-v2')
    



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
    print_result()
    


# Funciones de impresion de resultados
