import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
import os
from scipy import signal

from PIL import Image

# -- Set page config
apptitle = 'Imagiologia Médica - Experiência 2'
icon = Image.open('feup_logo.ico')
st.set_page_config(page_title=apptitle, page_icon=icon)
st.title('Atenuação de raio-X')

with st.expander('**Teoria**',True):
	st.write(r'''
		A variação da intensidade, $I$, de um feixe de raio-X (ou de qualquer radiação eletromagnética) pode ser definida por meio da equação diferencial:
		$$
			dI = -\mu Idx
		$$
		em que $\mu$ é o coeficiente de atenuação linear, que depende do material e do comprimento de onda da radiação incidente, $\lambda$. Assumindo $\mu$ constante ao longo de todo a espessura do alvo, vem que:
		$$
			I = I_0e^{-\mu d}
		$$
		em que $I$ and $I_0$ são a intensidade da radiação transmitida e incidente, e $d$ é a espessura atravessada.
	''')
	st.write(r'''
			Definindo a transmitância como a razão entre as itnensidades obtidas experimentalmente com e sem o alvo absorvente:
			$$ 
				\mathcal{T} = \frac{R}{R_0} = \frac{I}{I_0}
			$$
			a lei de absorção de Beer-Lambert pode ser facilmente testada experimentalmente notando que:
			$$
				\ln\mathcal{T} = -\mu d
			$$
			''')
	st.write('')

	try:
		mu0 = st.number_input('$\mu$',min_value=0.0,value=0.1)
		mus = np.logspace(-2,0,base=np.exp(1))
		colors = cm.rainbow(np.linspace(0,1,len(mus)))
		x = np.linspace(0,10)

		fig = plt.figure(figsize=(12,4))
		gs = gridspec.GridSpec(1,2,hspace=0.1,wspace=0.25)

		ax = plt.subplot(gs[0,0])
		ay = plt.subplot(gs[0,1])

		for i in range(len(mus)):
			mu = mus[i]
			y = np.exp(-mu*x)
			ax.plot(x,y,color=colors[i])
			ay.semilogy(x,y,color=colors[i])
		ax.plot(x,np.exp(-mu0*x),'k')
		ay.semilogy(x,np.exp(-mu0*x),'k')

		st.pyplot(fig)
	except:
		st.error('Something went wrong. Check the file format or try reloading it.', icon="⚠️")


PALETTE = [
	"#ff4b4b",
	"#ffa421",
	"#ffe312",
	"#21c354",
	"#00d4b1",
	"#00c0f2",
	"#1c83e1",
	"#803df5",
	"#808495",
]

tabs = st.tabs(['**P6.3.2.1**' , '**P6.3.2.2**' , '**P6.3.2.3**'])

with tabs[0]:
	st.write(r'''
			**Atenuação de raio-X em função do material e espessura**
			''',unsafe_allow_html=True)
	with st.expander('**Setup experimental**',True):
		st.write("**X-ray apparatus preparation**")
		st.write(r'''
			1. Set the tube high voltage $U=20$ kV
			2. Set the emission current $I=0.04$ mA
			3. Set the aparatus mode to **TARGET**
			4. Set the angular position $\Delta\beta=0º$
			5. Set the measuring time $\Delta t=20$ s
			''')
		st.write("**Making the experiment**")
		st.write(r'''
			1. Start the measurement with the **SCAN** key
			2. Repeat the measurement for $\beta\in[0º,60º]$ with an angular step of 10º
			3. Repeat the measurements with the zirconium filter''')

	with st.expander('**Data Analysis**',True):
		st.write('')

	with st.expander('**Export report**',True):
		st.write('')

tabs[1].write('''<div style="text-align: justify">
		\nAtenuação de raio-X em função do comprimento de onda da radiação incidente</div>''',unsafe_allow_html=True)
	
tabs[2].write('''<div style="text-align: justify">
		\nAtenuação de raio-X em função do número atómico </div>''',unsafe_allow_html=True)
