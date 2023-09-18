#Librerias

import csv
import pickle
import streamlit as st

import pandas as pd

import pandas as pd
import stress_demo_utils as detect
from sentence_transformers import SentenceTransformer

from streamlit_extras.colored_header import colored_header
from streamlit_extras import add_vertical_space

import json
from streamlit_lottie import st_lottie
from streamlit_echarts import st_echarts



#Recoger info del modelo

def calcula_estres(correo: str):
    
    clean_text=detect.preprocess(correo)
    text_embs=detect.get_embedding(clean_text,st.session_state.embs)
    
    
    keys=["original","prediction","prob"]
    #no funciona get proba
    values=[correo,detect.get_pred(text_embs,st.session_state.modelo),detect.get_pred(text_embs,st.session_state.modelo)]
   
    # cargar el modelo y pasarele el texto
    st.session_state.datos =dict(zip(keys, values))
    

 
    
def print_result():
    
   
    if st.session_state.datos['original']=="":
        st.warning("The email was empty")
    else: 
        
        rc1, rc2 = st.columns([0.4,0.4])


        with rc1:
            
            if st.session_state.datos['prediction']==0 :
                st_lottie(urlCalm,
                    reverse=False,
                    height=400,
                    width=400,
                    speed=1,
                    loop=True,
                    quality='high',
                    key='test'
                )
            else:
                st_lottie(urlStress,
                    reverse=False,
                    height=400,
                    width=400,
                    speed=1,
                    loop=True,
                    quality='high',
                    key='test'
                )
        with rc2:
            add_vertical_space.add_vertical_space(5)
            liquidfill_option = {
                "series": [{"type": "liquidFill", "data": [0.7]}]
            }
            st_echarts(liquidfill_option)
            
        
        
        






# Cargar csv con ejemplos 

ejemplos_key=[]
ejemplos_values=[]


data = pd.read_csv('config/examples.csv', sep=';', quoting=csv.QUOTE_ALL)

ejemplos_dict = data.to_dict()

ejemplos_key=list(ejemplos_dict['keys'].values())
values=list(ejemplos_dict['values'].values())
ejemplos_dict= dict(zip(ejemplos_key, values))





# cargar imagenes animadas

path = "images/animated/calm.json"
with open(path,"r") as file:
    urlCalm = json.load(file)
  
path = "images/animated/stress.json"
with open(path,"r") as file:
    urlStress = json.load(file)  

  
import os
print(os.listdir('./'))



#Layout

st.set_page_config(
    layout="wide", page_title="Stress Detector", page_icon="images/logo_top.png"
)



#Load CSS

css_file = open("config/estiloMain.css","r").read()
st.markdown(css_file,unsafe_allow_html=True)




#Logo y titulo


c1, c2 = st.columns([0.2,0.7])


with c1:
    
    st.image(
        'images/logo.png',
        width=110,
    )
    

with c2:
    st.caption("")
    new_title = '<p style="color:#00629b; font-size: 70px;">Stress Detector</p>'
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
    "Select Mail",
    (ejemplos_key))
    areaText = st.text_area("EMail",ejemplos_dict[option],height=240)
    
  
  
    cs1, cs2 = st.columns([0.2,0.8])
   
    
    with cs1:
        
        st.image(
            'images/logo_gsi.png',
            width=75,
        )
        

    with cs2:
        st.markdown(""" App created by [Intelligent Systems Group](https://gsi.upm.es).""")
        
     
        
    

#Intelligent Systems Group
#Universidad Politécnica de Madrid
#E.T.S.I. Telecomunicación - C-211 | Avda. Complutense, 30 | 28040 Madrid | Spain

# Pantalla principal
colored_header(
    label='',
    description='',
    color_name="blue-90",
)

with st.container():
    calcula_estres(areaText)
    print_result()
 
 



 


    

# Funciones de impresion de resultados
