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
default_colors = ['tab:blue','tab:orange','tab:green','tab:red']

with st.expander('**Theory**',True):
	st.write(r'''
		The intensity, $I$, of light traveling into an absorbing body is governed by the differential equation:
		$$
			dI = -\mu Idx
		$$
		where $\mu$ is the attenuation coefficient, that depends on the material and the wavelength of the incident beam, $\lambda$. Assuming $\mu$ constant along the path, it follows:
		$$
			I = I_0e^{-\mu d}
		$$
		where $I$ and $I_0$ are the transmitted and incident radiation intensities, and $d$ is the target thickness.
	''')
	st.write(r'''
			By defning the transmittance as the ratio between the counting rate behind and in front of the target as:
			$$ 
				\mathcal{T} = \frac{R}{R_0} = \frac{I}{I_0}
			$$
			the Beer-Lambert absorption law can be experimentally tested by noting that:
			$$
				\ln\mathcal{T} = -\mu d
			$$
			''')
	st.write(r'''
			Alternatively, you may obtain a linear fit directly on the count rate noting that:
			$$
				\ln R =\ln R_0 -\mu d
			$$
			''')
	st.write('')

	try:
		mu0 = st.number_input('$\mu$',min_value=0.0,value=0.1)
		mus = np.logspace(-2,0,base=10)
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
		st.error('Something went wrong.', icon="⚠️")

tabs = st.tabs(['**Tube current impact**' ,'**Tube voltage impact**' ,'**Filter impact**' , '**Target material impact**' ])
figs = []


with tabs[0]:
	st.write("**X-ray apparatus preparation**")
	st.write(r'''
		1. Mount the collimator and install the Geiger counter on the respective support
		2. Install the target with varying thickness in the goniometer
		2. Set the tube high voltage $\Delta V=20$ kV
		3. Set the emission current $I=0.04$ mA
		4. Set the aparatus mode to **TARGET**
		5. Set the angular position $\Delta\beta=0º$
		6. Set the measuring time $\Delta t=20$ s
		''')	

	st.write("**Making the experiment**")
	st.write(r'''
		1. Start the measurement with the **SCAN** key
		2. Repeat the measurement for $\beta\in[0º,60º]$ with an angular step of 10º
		3. Repeat the measurements with different tube currents''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs')

	st.write('')

	cols = st.columns(3)
	file = []
	file.append(cols[0].file_uploader("Experiment 1",accept_multiple_files=False))
	file.append(cols[1].file_uploader("Experiment 2",accept_multiple_files=False))
	file.append(cols[2].file_uploader("Experiment 3",accept_multiple_files=False))

	n_files = len(file)
	error_check = np.zeros(n_files)

	evs = np.zeros(n_files)
	Is = np.zeros(n_files)
	
	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1
			dN = 7
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18+dN,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			
			evs[i] = data.iloc[0,0]
			Is[i] = data.iloc[0,2]

	fig = plt.figure(figsize = (12,4))
	gs = gridspec.GridSpec(1,2,wspace=0.25,hspace=0.1)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))

	linear_coef = []
	linear_func = []

	for i in range(n_files):
		if error_check[i]:
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18,nrows=7,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			th_mm = [0.5*x for x in range(len(data))]
			y = data.iloc[:,0]

			linear_coef.append(np.polyfit(th_mm, np.log(y), 1))
			linear_func.append(np.poly1d(linear_coef[i]))

			expression = r'$R(t)=%.1f\cdot e^{%.3fx}$'%(np.exp(linear_coef[i][1]),linear_coef[i][0])

			ax[0].plot(th_mm,y,'o',label='V=%.1f kV; I=%.2f mA'%(evs[i],Is[i]),color=default_colors[i])
			ax[0].plot(th_mm,np.exp(linear_func[i](th_mm)),'--',label=expression,color=default_colors[i])

			ax[1].plot(th_mm,y,'o',color=default_colors[i])
			ax[1].plot(th_mm,np.exp(linear_func[i](th_mm)),'--',color=default_colors[i])
		else:
			linear_coef.append(0)
			linear_func.append(0)
	if sum(error_check)==0:
		ax[0].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
		ax[1].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
	
	ax[1].set_yscale('log')

	ax[0].set_xlabel('Thickness (mm)')
	ax[0].set_ylabel('$R$ (counts per second)' )

	ax[1].set_xlabel('Thickness (mm)')
	ax[1].set_ylabel('$\log R$' )
	ax[0].set_ylim(0,)
	if sum(error_check)>0:
		ax[0].legend(
				loc='upper center',
	 			bbox_to_anchor=(1.1,-0.2),
				ncol=sum(error_check),
				fancybox=False,
				framealpha=1,
				fontsize=12,
				frameon=False)
	plt.show()
	st.pyplot(fig)
	figs.append(fig)


with tabs[1]:
	st.write("**X-ray apparatus preparation**")
	st.write(r'''
		1. Mount the collimator and install the Geiger counter on the respective support
		2. Install the target with varying thickness in the goniometer
		2. Set the tube high voltage $\Delta V=20$ kV
		3. Set the emission current $I=0.04$ mA
		4. Set the aparatus mode to **TARGET**
		5. Set the angular position $\Delta\beta=0º$
		6. Set the measuring time $\Delta t=20$ s
		''')	

	st.write("**Making the experiment**")
	st.write(r'''
		1. Start the measurement with the **SCAN** key
		2. Repeat the measurement for $\beta\in[0º,60º]$ with an angular step of 10º
		3. Repeat the measurements with different tube voltages''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs')

	st.write('')

	cols = st.columns(4)
	file = []
	file.append(cols[0].file_uploader("Experiment 1",accept_multiple_files=False,key='exp2_2_1'))
	file.append(cols[1].file_uploader("Experiment 2",accept_multiple_files=False,key='exp2_2_2'))
	file.append(cols[2].file_uploader("Experiment 3",accept_multiple_files=False,key='exp2_2_3'))
	file.append(cols[3].file_uploader("Experiment 4",accept_multiple_files=False,key='exp2_2_4'))

	n_files = len(file)
	error_check = np.zeros(n_files)

	evs = np.zeros(n_files)
	Is = np.zeros(n_files)
	
	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1
			dN = 7
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18+dN,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			
			evs[i] = data.iloc[0,0]
			Is[i] = data.iloc[0,2]

	fig = plt.figure(figsize = (12,4))
	gs = gridspec.GridSpec(1,2,wspace=0.25,hspace=0.1)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))

	linear_coef = []
	linear_func = []

	for i in range(n_files):
		if error_check[i]:
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18,nrows=7,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			th_mm = [0.5*x for x in range(len(data))]
			y = data.iloc[:,0]

			linear_coef.append(np.polyfit(th_mm, np.log(y), 1))
			linear_func.append(np.poly1d(linear_coef[i]))

			expression = r'$R(t)=%.1f\cdot e^{%.3fx}$'%(np.exp(linear_coef[i][1]),linear_coef[i][0])

			ax[0].plot(th_mm,y,'o',label='V=%.1f kV; I=%.2f mA'%(evs[i],Is[i]),color=default_colors[i])
			ax[0].plot(th_mm,np.exp(linear_func[i](th_mm)),'--',label=expression,color=default_colors[i])

			ax[1].plot(th_mm,y,'o',color=default_colors[i])
			ax[1].plot(th_mm,np.exp(linear_func[i](th_mm)),'--',color=default_colors[i])
		else:
			linear_coef.append(0)
			linear_func.append(0)
	if sum(error_check)==0:
		ax[0].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
		ax[1].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
	
	ax[1].set_yscale('log')

	ax[0].set_xlabel('Thickness (mm)')
	ax[0].set_ylabel('$R$ (counts per second)' )

	ax[1].set_xlabel('Thickness (mm)')
	ax[1].set_ylabel('$\log R$' )
	ax[0].set_ylim(0,)
	
	if sum(error_check)==0:
		for j in range(2):
			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
	else:
		ax[0].legend(
					loc='upper center',
		 			bbox_to_anchor=(1.1,-0.2),
					ncol=sum(error_check),
					fancybox=False,
					framealpha=1,
					fontsize=12,
					frameon=False)
	plt.show()
	st.pyplot(fig)
	figs.append(fig)


with tabs[2]:
	st.write("**X-ray apparatus preparation**")
	st.write(r'''
		1. Mount the collimator and install the Geiger counter on the respective support
		2. Install the target with varying thickness in the goniometer
		2. Set the tube high voltage $\Delta V=20$ kV
		3. Set the emission current $I=0.04$ mA
		4. Set the aparatus mode to **TARGET**
		5. Set the angular position $\Delta\beta=0º$
		6. Set the measuring time $\Delta t=20$ s
		''')	

	st.write("**Making the experiment**")
	st.write(r'''
		1. Start the measurement with the **SCAN** key
		2. Repeat the measurement for $\beta\in[0º,60º]$ with an angular step of 10º
		3. Repeat the measurements with the zirconium filter''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs')

	st.write('')
	
	cols0 = st.columns(2)
	file = []
	file.append(cols0[0].file_uploader("Without filter",accept_multiple_files=False))
	file.append(cols0[1].file_uploader("With zirconium filter",accept_multiple_files=False))
	n_files = len(file)
	error_check = np.zeros(n_files)

	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1

	fig = plt.figure(figsize = (12,4))
	gs = gridspec.GridSpec(1,2,wspace=0.25,hspace=0.1)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))

	labels = ['Without filter', 'With filter']
	linear_coef = []
	linear_func = []

	for i in range(n_files):
		if error_check[i]:
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18,nrows=7,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			th_mm = [0.5*x for x in range(len(data))]
			y = data.iloc[:,0]

			linear_coef.append(np.polyfit(th_mm, np.log(y), 1))
			linear_func.append(np.poly1d(linear_coef[i]))

			expression = r'$R(t)=%.1f\cdot e^{%.3fx}$'%(np.exp(linear_coef[i][1]),linear_coef[i][0])

			ax[0].plot(th_mm,y,'o',label=labels[i],color=default_colors[i])
			ax[0].plot(th_mm,np.exp(linear_func[i](th_mm)),'--',label=expression,color=default_colors[i])

			ax[1].plot(th_mm,y,'o',color=default_colors[i])
			ax[1].plot(th_mm,np.exp(linear_func[i](th_mm)),'--',color=default_colors[i])
		else:
			linear_coef.append(0)
			linear_func.append(0)
	if sum(error_check)==0:
		ax[0].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
		ax[1].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
	
	ax[1].set_yscale('log')

	ax[0].set_xlabel('Thickness (mm)')
	ax[0].set_ylabel('$R$ (counts per second)' )

	ax[1].set_xlabel('Thickness (mm)')
	ax[1].set_ylabel('$\log R$' )
	ax[0].set_ylim(0,)

	if sum(error_check)==0:
		for j in range(2):
			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
	
	elif sum(error_check) == 2:
		order = [0,2,1,3]
		handles, labels_ = ax[0].get_legend_handles_labels()
		if len(handles):
			ax[0].legend([handles[j] for j in order], [labels_[j] for j in order],
						loc='upper left',
			 			bbox_to_anchor=(0,-0.2),
						ncol=2,
						fancybox=False,
						framealpha=1,
						fontsize=12,
						frameon=False)
	else:
		ax[0].legend(
			loc='upper left',
 			bbox_to_anchor=(0,-0.2),
			ncol=2,
			fancybox=False,
			framealpha=1,
			fontsize=12,
			frameon=False)
	
	plt.show()
	st.pyplot(fig)
	figs.append(fig)

with tabs[3]:
	st.write("**X-ray apparatus preparation**")
	st.write(r'''
		1. Mount the collimator and install the Geiger counter on the respective support
		2. Install the target with varying material in the goniometer
		2. Set the tube high voltage $\Delta V=20$ kV
		3. Set the emission current $I=0.01$ mA
		4. Set the aparatus mode to **TARGET**
		5. Set the angular position $\Delta\beta=0º$
		6. Set the measuring time $\Delta t=20$ s
		''')	

	st.write("**Making the experiment**")
	st.write(r'''
		1. Start the measurement with the **SCAN** key
		2. Repeat the measurement for $\beta\in[0º,60º]$ with an angular step of 10º
		3. You may need to increase the tube current (for instance, $I=0.10$ mA) for the heavier elements (Fe and above).
		''')
	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs')

	st.write('')

	

	file = []
	file.append(st.file_uploader("Measured data",accept_multiple_files=False))


	cols = st.columns(2)
	I1 = cols[0].number_input("Current used for the lighter elements (mA)",value=0.02)
	I2 = cols[1].number_input("Current used for the heavier elements (mA)",value=1.00)
	bk_noise = 0.243
	dx_cm = 5e-2

	#Bs.append(cols[2].number_input("$\Delta z$ (mm)"))
	#Bs.append(cols[3].number_input("$\Delta \ell$ (mm)"))

	n_files = len(file)
	error_check = np.zeros(n_files)

	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1

	fig = plt.figure(figsize = (12,8))
	gs = gridspec.GridSpec(2,2,wspace=0.2,hspace=0.3)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))
	ax.append(plt.subplot(gs[1,0]))
	ax.append(plt.subplot(gs[1,1]))

	for i in range(n_files):
		if error_check[i]:
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18,nrows=7,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			zs = [0,6,13,26,29,40,47]
			y = data.iloc[:,0]

			if (I1>0) and (I2>0): 
				y_corr = (y-bk_noise)*1/I1
				y_corr[3:] *= I1/I2
			else:
				y_corr = (y-bk_noise)*1

			T_corr = y_corr/y_corr[0]
			mus = -np.log(T_corr)/dx_cm

			ax[0].plot(zs,y,'o',color=default_colors[i],clip_on=False)
			ax[1].plot(zs,1e-3*y_corr,'o',color=default_colors[i],clip_on=False)

			ax[2].plot(zs,T_corr,'o',color=default_colors[i],clip_on=False)
			ax[3].plot(zs,mus,'o',color=default_colors[i],clip_on=False)

	if sum(error_check)==0:
		for j in range(4):
			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')

	ax[0].set_ylabel('$R$ (counts per second)' )
	ax[1].set_ylabel(r'$R\times 10^{-3}$ (counts per second)' )
	ax[0].set_title('Measured values')
	ax[1].set_title('Equivalent values for $I=1.00$ mA')

	ax[2].set_ylabel('Transmittance $\mathcal{T}$ (-)' )
	ax[3].set_ylabel('Attenuation coefficient $\mu$ (cm$^{-1}$)' )
	for j in range(4):
		ax[j].set_xlim(0,)
		ax[j].set_ylim(0,)
		ax[j].set_xlabel('Atomic number (Z)')


	plt.show()
	st.pyplot(fig)
	figs.append(fig)
	st.caption(r'It was assumed that the background radiation corresponds to 0.243 (s$^{-1}$) and the target thickness to be $d=0.05$ cm')


st.write('')
st.write('**Export report**')
st.write('After filling in all the tabs above, you can download your report that should be attached as an appendix to the final reports.')
st.write('Please note that the pdf preview does not work in some browsers, but you should still be able to download the file.')

group_number = st.number_input("Group number",key='g_1_2',min_value=1,max_value=20,value=None)
exp_c = st.columns([0.25,0.25,0.5])
export_as_pdf = exp_c[0].button("Generate Report",key='pdf_1_2')

if export_as_pdf:
	try:
		create_pdf_task2(figs,group_number,
						'Experiment 2: Measuring attenuation',
						'G%.2d_Exp2_report'%group_number,exp_c[1],
						 [I1,I2])
	except:
		st.error('Something went wrong. Check that you have filled in the group number.', icon="⚠️")


