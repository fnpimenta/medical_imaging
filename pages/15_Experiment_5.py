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
apptitle = 'Medical Imaging - Experiment 5'
icon = Image.open('feup_logo.ico')
st.set_page_config(page_title=apptitle, page_icon=icon)
st.title('Study of the ionization current')


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
d = 564.02/2

with st.expander('**Theory**',True):
	st.write(r'''
		X-radiation is detectable on account of its physical effects (for example, x-rays cause air and other gases to become electrically conductive). 
		
		In the quantitative detection of x-rays, we can exploit this
		ionizing effect, e.g. by measuring the ionization current in a
		plate capacitor filled with air or another gas. Due the way it is
		designed and built, this type of arrangement is called an
		ionization chamber.

		In the detection of x-rays, an x-ray beam passes through a
		diaphragm and strikes a plate capacitor in such a way that it
		does not directly fall on the plates. This prevents falsification
		of the measurement results due to the photoeffect at the
		capacitor plates. The x-rays ionize a part of the gas volume in
		the capacitor. When we apply a voltage UC to the capacitor,
		the charge carriers, electrons or ions, are collected at the
		capacitor plates. The current generated at the capacitor in this
		way corresponds to an ionization current (IC) in the outer circuit
		that can be measured using a measuring amplifier.

		As UC increases, more and more charge carriers are collected at the capacitor plates. Thus, the ionization current IC increases with the voltage UC. When UC is
		increased beyond a certain point, IC ultimately reaches a saturation value, as all charge carriers formed by the incident radiation per unit of time are captured (except for negligible
		recombination losses). This saturation value is an indicator for the intensity of the incident x-radiation.''')
	st.write('')

tabs = st.tabs(['**Tube current impact**' , '**Tube voltage impact**' ])
figs = []

# with tabs[0]:
# 	st.write("**X-ray apparatus preparation**")
# 	st.write(r'''
# 		1. Set the tube high voltage $\Delta V=30$ kV
# 		2. Set the emission current $I=0.80$ mA
# 		''')	

# 	st.write("**Making the experiment**")
# 	st.write(r'''
# 		1. Start the measurement with the **HV** key
# 		2. Increase the capacitor volatge in steps from 0 V to 300 V and register the ionization current
# 		3. Repeat the analysis for different tube currents.''')

# 	st.write('**Data Analysis**')

# 	st.write('Upload the measurement outputs.')

# 	st.write('')

# 	cols = st.columns(3)
# 	file = []
# 	file.append(cols[0].file_uploader("Experiment 1",accept_multiple_files=False,key='exp5_1_1'))
# 	file.append(cols[1].file_uploader("Experiment 2",accept_multiple_files=False,key='exp5_1_2'))
# 	file.append(cols[2].file_uploader("Experiment 3",accept_multiple_files=False,key='exp5_1_3'))
	
# 	n_files = len(file)
# 	error_check = np.zeros(n_files)

# 	evs = np.zeros(n_files)
# 	Is = np.zeros(n_files)
	
# 	for i in range(len(file)):
# 		if not(file[i]==None):
# 			error_check[i] += 1
# 			file[i].seek(0)
# 			data = pd.read_csv(file[i],skiprows=4,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
# 			b_mins[i] = data.iloc[0,0]

# 			dN = len(np.arange(b_mins[i],b_max+d_beta,d_beta))
# 			file[i].seek(0)
# 			data = pd.read_csv(file[i],skiprows=18+dN,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
# 			evs[i] = data.iloc[0,0]
# 			Is[i] = data.iloc[0,2]

# 	fig = plt.figure(figsize = (12,4))
# 	gs = gridspec.GridSpec(1,2,wspace=0.2,hspace=0.3)
# 	ax = []
# 	ax.append(plt.subplot(gs[0,0]))
# 	ax.append(plt.subplot(gs[0,1]))

# 	for i in range(n_files):
# 		if error_check[i]:
# 			betas = np.arange(b_mins[i],b_max+d_beta,d_beta)
# 			full_betas = np.arange(b_mins[i],b_max+0.01,0.01)
# 			lambdas = 2*d*np.sin(np.pi/180*betas)
# 			full_lambdas = 2*d*np.sin(np.pi/180*full_betas)
# 			energies = 1239.8/lambdas
# 			file[i].seek(0)
# 			data = pd.read_csv(file[i],skiprows=18,nrows=len(betas),sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
# 			y = data.iloc[:,0]
# 			cs = CubicSpline(betas, y)

# 			ax[0].plot(lambdas,y,'.',color=default_colors[i],clip_on=False,label='V=%.1f kV; I=%.2f mA'%(evs[i],Is[i]))
# 			ax[0].plot(full_lambdas,cs(full_betas),'--',color=default_colors[i],lw=1,clip_on=False)

# 	if sum(error_check)==0:
# 		for j in range(len(ax)):
# 			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')


# 	ax[0].set_ylabel('R (counts per second)' )
# 	#ax[0].set_title('Measured values')

# 	#ax[0].set_xlim(right=max(lambdas))
# 	ax[0].set_ylim(0,)
# 	ax[0].set_xlabel('Wavelength (pm)')
# 	if sum(error_check)>0:
# 		ax[0].axvline(71.080,0,1,c='k',ls='--')
# 		ax[0].axvline(63.095,0,1,c='k',ls='--')
# 		ax[0].annotate(text=r'71.080 pm',xy=(71.080,ax[0].set_ylim()[1]),ha='center',va='bottom',clip_on=False)
# 		ax[0].annotate(text=r"63.095 pm",xy=(63.095,ax[0].set_ylim()[1]),ha='center',va='bottom',clip_on=False)
# 	ax[0].legend(frameon=False,ncols=4,markerscale=1,bbox_to_anchor=(0.5,1.1),loc='lower center')
# 	plt.show()
# 	st.pyplot(fig)
# 	figs.append(fig)
	

# with tabs[1]:
# 	st.write("**X-ray apparatus preparation**")
# 	st.write(r'''
# 		1. Set the tube high voltage $\Delta V=30$ kV
# 		2. Set the emission current $I=0.80$ mA
# 		''')	

# 	st.write("**Making the experiment**")
# 	st.write(r'''
# 		1. Start the measurement with the **HV** key
# 		2. Increase the capacitor volatge in steps from 0 V to 300 V and register the ionization current
# 		3. Repeat the analysis for different tube voltages.''')

# 	st.write('')

# 	n_files = 4
# 	d_beta = 0.1
# 	b_max = 8
# 	cols = st.columns(n_files)
# 	file = []

# 	error_check = np.zeros(n_files)
# 	evs = np.zeros(n_files)
# 	b_mins = np.zeros(n_files)
# 	l_mins = np.zeros(n_files)

# 	p_mins = np.zeros(n_files)
# 	p_maxs = np.zeros(n_files)
# 	d_betas = np.zeros(n_files) 

# 	cols = st.columns(n_files)
	
# 	for i in range(n_files):
# 		with cols[i].expander('Experiment %d'%(i+1),True):
# 			file.append(st.file_uploader("Data",accept_multiple_files=False,key='D%d'%i))
# 			if not(file[i]==None):
# 				error_check[i] += 1
# 				file[i].seek(0)
# 				data = pd.read_csv(file[i],skiprows=4,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
# 				b_mins[i] = data.iloc[0,0]

# 				dN = len(np.arange(b_mins[i],b_max+d_beta,d_beta))
# 				file[i].seek(0)
# 				data = pd.read_csv(file[i],skiprows=18+dN,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
# 				evs[i] = data.iloc[0,0]

# 			p_mins[i] = st.number_input(r'First point',value=3,key='p1%d'%i,disabled=(0==error_check[i]))
# 			p_maxs[i] = st.number_input(r'Last point',value=10,key='p2%d'%i,disabled=(0==error_check[i]))


# 	fig = plt.figure(figsize = (10,3.5))
# 	gs = gridspec.GridSpec(1,2,wspace=0.2,hspace=0.3)
# 	ax = []
# 	ax.append(plt.subplot(gs[0,0]))
# 	ax.append(plt.subplot(gs[0,1]))

# 	labels = ['No filter','Zr filter','Cu filter']
# 	for i in range(n_files):
# 		if error_check[i]:
# 			betas = np.arange(b_mins[i],b_max+d_beta,d_beta)
# 			full_betas = np.arange(b_mins[i],b_max+0.01,0.01)
# 			lambdas = 2*d*np.sin(np.pi/180*betas)
# 			full_lambdas = 2*d*np.sin(np.pi/180*full_betas)
# 			energies = 1239.8/lambdas

# 			file[i].seek(0)
# 			data = pd.read_csv(file[i],skiprows=18,nrows=len(betas),sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')

# 			y = np.array(data.iloc[:,0])
# 			cs = CubicSpline(betas, y)

# 			x_filt = lambdas[int(p_mins[i]-1):int(p_maxs[i]-1)]
# 			y_filt = y[int(p_mins[i]-1):int(p_maxs[i]-1)]
			
# 			coeff = np.polyfit(x_filt, y_filt, 1)
# 			l_mins[i] = -coeff[1]/coeff[0]

# 			ax[0].plot(lambdas,y,'.',color=default_colors[i],ms=2,clip_on=False,label='V=%.1f kV'%evs[i])
# 			ax[0].plot(x_filt,y_filt,'.',color=default_colors[i],ms=5,clip_on=False)
# 			ax[0].plot(lambdas,np.poly1d(coeff)(lambdas),'--',lw=1,color=default_colors[i],ms=1,clip_on=True)
	
# 			ax[1].plot(1/evs[i],l_mins[i],'o',color=default_colors[i],clip_on=False)

# 	if sum(error_check)>1:
# 		coeff = np.polyfit(1/evs[error_check>0],l_mins[error_check>0], 1)
# 		ax[1].plot([0,1/min(evs[error_check>0])],[np.poly1d(coeff)(0),np.poly1d(coeff)(1/min(evs[error_check>0]))],'--k',
# 					lw=1,ms=1,clip_on=True,label='$\lambda_{min}=%.2f+%.2f\cdot\dfrac{1}{V}$'%(coeff[1],coeff[0]))
		
# 	if sum(error_check)==0:
# 		for j in range(len(ax)):
# 			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')

# 	#ax[0].set_title('Measured values')
# 	#ax[0].set_xlim()
# 	ax[0].set_ylim(0,2000)
# 	ax[0].set_xlabel('Wavelength (pm)')
# 	ax[0].set_ylabel('$R$ (counts per second)' )

# 	#ax[0].set_title('Measured values')
# 	ax[1].set_xlabel('1/Tube voltage (1/kV)')
# 	ax[1].set_ylabel('$\lambda_{min}$ (pm)' )
# 	ax[1].legend(frameon=False)
# 	ax[0].legend(frameon=False,ncols=4,markerscale=5,bbox_to_anchor=(1.1,1.1),loc='lower center')
# 	plt.show()
# 	st.pyplot(fig)
# 	figs.append(fig)
	

# st.write('')
# st.write('**Export report**')
# st.write('After filling in all the tabs above, you can download your report that should be attached as an appendix to the final reports.')
# st.write('Please note that the pdf preview does not work in some browsers, but you should still be able to download the file.')

# group_number = st.number_input("Group number",key='g_1_2',min_value=1,max_value=20,value=None)
# exp_c = st.columns([0.25,0.25,0.5])
# export_as_pdf = exp_c[0].button("Generate Report",key='pdf_1_2')

# if export_as_pdf:
# 	try:
# 		create_pdf_task3(figs,group_number,
# 						'Experiment 3: X-ray beam spectra',
# 						'G%.2d_Exp3_report'%group_number,exp_c[1])
# 	except:
# 		st.error('Something went wrong. Check that you have filled in the group number.', icon="⚠️")



