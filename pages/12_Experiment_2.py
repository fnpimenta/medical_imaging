import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
import os
from scipy import signal

from PIL import Image

from Print import * 

# -- Set page config
apptitle = 'Medical Imaging - Experiment 2'
icon = Image.open('feup_logo.ico')
st.set_page_config(page_title=apptitle, page_icon=icon)
st.title('X-ray attenuation curves')

PALETTE = [
	"#ff4b4b",
	"#ffa421",
	"#ffe312",
	"#21c354",
	"#00d4b1",
	"#00c0f2",
	"#1c83e1",
	"#803df5",
	"#808495",]

default_colors = ['tab:blue','tab:orange']

# with st.expander('**Teoria**',True):
# 	st.write(r'''
# 		A variação da intensidade, $I$, de um feixe de raio-X (ou de qualquer radiação eletromagnética) pode ser definida por meio da equação diferencial:
# 		$$
# 			dI = -\mu Idx
# 		$$
# 		em que $\mu$ é o coeficiente de atenuação linear, que depende do material e do comprimento de onda da radiação incidente, $\lambda$. Assumindo $\mu$ constante ao longo de todo a espessura do alvo, vem que:
# 		$$
# 			I = I_0e^{-\mu d}
# 		$$
# 		em que $I$ and $I_0$ são a intensidade da radiação transmitida e incidente, e $d$ é a espessura atravessada.
# 	''')
# 	st.write(r'''
# 			Definindo a transmitância como a razão entre as itnensidades obtidas experimentalmente com e sem o alvo absorvente:
# 			$$ 
# 				\mathcal{T} = \frac{R}{R_0} = \frac{I}{I_0}
# 			$$
# 			a lei de absorção de Beer-Lambert pode ser facilmente testada experimentalmente notando que:
# 			$$
# 				\ln\mathcal{T} = -\mu d
# 			$$
# 			''')
# 	st.write('')

# 	try:
# 		mu0 = st.number_input('$\mu$',min_value=0.0,value=0.1)
# 		mus = np.logspace(-2,0,base=10)
# 		colors = cm.rainbow(np.linspace(0,1,len(mus)))
# 		x = np.linspace(0,10)

# 		fig = plt.figure(figsize=(12,4))
# 		gs = gridspec.GridSpec(1,2,hspace=0.1,wspace=0.25)

# 		ax = plt.subplot(gs[0,0])
# 		ay = plt.subplot(gs[0,1])

# 		for i in range(len(mus)):

# 			mu = mus[i]
# 			y = np.exp(-mu*x)
# 			ax.plot(x,y,color=colors[i])
# 			ay.semilogy(x,y,color=colors[i])
# 		ax.plot(x,np.exp(-mu0*x),'k')
# 		ay.semilogy(x,np.exp(-mu0*x),'k')

# 		st.pyplot(fig)
# 	except:
# 		st.error('Something went wrong. Check the file format or try reloading it.', icon="⚠️")

# with st.expander('**Experimental setup**',True):
# 	st.write("**X-ray apparatus preparation**")
# 	st.write(r'''
# 		1. Set the tube high voltage $U=20$ kV
# 		2. Set the emission current $I=0.04$ mA
# 		3. Set the aparatus mode to **TARGET**
# 		4. Set the angular position $\Delta\beta=0º$
# 		5. Set the measuring time $\Delta t=20$ s
# 		''')
# 	st.write("**Making the experiment**")
# 	st.write(r'''
# 		1. Start the measurement with the **SCAN** key
# 		2. Repeat the measurement for $\beta\in[0º,60º]$ with an angular step of 10º
# 		3. Repeat the measurements with the zirconium filter''')

# with st.expander('**Data Analysis**',True):

# 	st.write('')

# 	st.write('Upload the measurement outputs')

# 	cols0 = st.columns(2)
# 	file = []
# 	file.append(cols0[0].file_uploader("Without filter",accept_multiple_files=False))
# 	file.append(cols0[1].file_uploader("With zirconium filter",accept_multiple_files=False))
	
# 	error_check = 0
# 	input_error = np.zeros(6)-2

# 	for i in range(len(file)):
# 		if not(file[i]==None):
# 			error_check += 1

# 	if error_check>0:
# 		cols = st.columns(2)
# 		#t_min = cols[0].number_input('First time instant to plot',0.0,1000.0,0.0)
# 		#t_max = cols[1].number_input('Last time instant to plot',0.0,1000.0,1000.0)
		
# 		fig = plt.figure(figsize = (12,4))

# 		gs = gridspec.GridSpec(1,2,wspace=0.25,hspace=0.1)

# 		ax1 = plt.subplot(gs[0,0])
# 		ax2 = plt.subplot(gs[0,1])	

# 		labels = ['Without filter', 'With filter']

# 		linear_coef = []
# 		linear_func = []

# 		for i in range(len(file)):				
# 			file[i].seek(0)
# 			data = pd.read_csv(file[i],skiprows=18,nrows=7,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
# 			th_mm = [0.5*x for x in range(len(data))]
# 			y = data.iloc[:,0]
# 			linear_coef.append(np.polyfit(th_mm, np.log(y), 1))
# 			linear_func.append(np.poly1d(linear_coef[i]))

# 			expression = r'$R(t)=%.1f\cdot e^{%.3fx}$'%(np.exp(linear_coef[i][1]),linear_coef[i][0])

# 			ax1.plot(th_mm,y,'o',label=labels[i],color=default_colors[i])
# 			ax1.plot(th_mm,np.exp(linear_func[i](th_mm)),'--',label=expression,color=default_colors[i])

# 			ax2.plot(th_mm,y,'o')
# 			ax2.plot(th_mm,np.exp(linear_func[i](th_mm)),'--',color=default_colors[i])

# 		ax2.set_yscale('log')

# 		ax1.set_xlabel('Thickness (mm)')
# 		ax1.set_ylabel('$R$ (counts per second)' )

# 		ax2.set_xlabel('Thickness (mm)')
# 		ax2.set_ylabel('$\log R$' )
# 		ax1.set_ylim(0,)

# 		order = [0,2,1,3]
# 		handles, labels_ = ax1.get_legend_handles_labels()

# 		ax1.legend([handles[j] for j in order], [labels_[j] for j in order],
# 					loc='upper left',
# 		 			bbox_to_anchor=(0,-0.2),
# 					ncol=2,
# 					fancybox=False,
# 					framealpha=1,
# 					fontsize=12,
# 					frameon=False)
# 		plt.show()
# 		st.pyplot(fig)

# exp = st.expander('**Export report**',False)

# with exp:
# 	report_text = st.text_input("Group number")
# 	cols = st.columns(2)
# 	s1 = cols[0].number_input("Half-value layer without filter")
# 	s2 = cols[1].number_input("Half-value layer with filter")
	
# 	exp_c = exp.columns([0.25,0.25,0.5])
# 	export_as_pdf = exp_c[0].button("Generate Report")

# 	if export_as_pdf:
# 		#try:
# 		create_pdf_task1([fig],report_text,'Experiment 2: X-ray absorption','Exp2_report',exp_c[1],exp,linear_coef[0][0],linear_coef[1][0],s1,s2)
# 		#except:
# 		#	exp.error('Something went wrong. No file available for the analysis.', icon="⚠️")
