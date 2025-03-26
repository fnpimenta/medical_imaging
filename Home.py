import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os 

from copy import deepcopy
from scipy.integrate import odeint
from scipy.signal import find_peaks
from scipy import signal

from PIL import Image

# -- Set page config
apptitle = 'Medical Imaging'
icon = Image.open("feup_logo.ico")
st.set_page_config(page_title=apptitle, page_icon=icon )

cols = st.columns(3)

#cols[0].markdown("[![Foo](https://sigarra.up.pt/feup/WEB_GESSI_DOCS.download_file?p_name=F-370784536/logo_cores_oficiais.jpg),](https://sigarra.up.pt/feup/pt/web_page.inicial)")
#cols[2].markdown("[![Foo](https://paginas.fe.up.pt/~icfeup/wp-content/themes/ic-wai/img/vendor/instituto-da-construcao-logo.svg)](https://paginas.fe.up.pt/~icfeup)")
cols[0].markdown('''<a href="https://www.fe.up.pt">
                    <img height= 80px 
                    src="https://sigarra.up.pt/feup/pt/imagens/LogotipoSI" 
                    title="FEUP webpage"/>
                    ''',unsafe_allow_html=True)

cols[2].markdown('''<a href="https://www.fc.up.pt">
                    <img height= 80px 
                    src="https://sigarra.up.pt/fcup/pt/imagens/LogotipoSI" 
                    title="FCUP webpage" />
                    ''',unsafe_allow_html=True)

# Title the app
st.title('''Medical Imaging
            \n2$^{nd}$ term, 2024/2025
            \nFrancisco Pimenta, fnpimenta@fe.up.pt''')


tabs = st.tabs(['**Experiments**'  ])

with tabs[0]:
    st.markdown("""<div style="text-align: justify">
                Experiments list:
                </div>""",unsafe_allow_html=True)
    st.write('''
        1. Observation of x-ray imagens
        2. X-ray attenuation curves
        3. X-ray beam spectra and Duane-Hunt relation
        4. Study of the photoelectric cross-section
        5. Study of the ionization current
        ''')

with tabs[1]:
    st.write("")
    #st.write('''<div style="text-align: justify">
    #            \nThis course will focus on the numerical modelling of wind turbines. 
    #            However, and in order to provide to the attendees with~the basic concepts regardingof wind energy, 
    #            fundamental for a correct implementation and interpretation of numerical models, it also includes modules aimed at exposing the basic theoretical concepts that govern the operation of the most common wind turbines. 
    #            At the end of the course participants should:</div>''',unsafe_allow_html=True)
    #st.write("- know the main components of a wind turbine")
    #st.write("- understand the mechanism for generating electricity from wind;")
    #st.write("- know how to generate realistic wind fields in order to represent the wind loads;")
    #st.write("- understand the structural behaviour of foundation, tower and blades and know how to model the main components;")
    #st.write("- understand the aerodynamic behaviour of the rotor and know how to model it;")
    #st.write("- know the rotor control mechanisms and know how to model them in a simplified way;")
    #st.write("- know the operating principles of floating platforms for offshore wind turbines and their basic modelling;")
    #st.write("- know wind turbine operating regimes and singular events and know how to model them;")
    #st.write("- know how to interpret numerical modelling results.")
