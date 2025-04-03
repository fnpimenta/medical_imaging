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
default_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
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

tabs = st.tabs(['**Tube voltage impact**' , '**Tube current impact**' ])
figs = []

with tabs[0]:
	st.write("**X-ray apparatus preparation**")
	st.write(r'''
		1. Set the tube high voltage $\Delta V=30$ kV
		2. Set the emission current $I=0.80$ mA
		''')	

	st.write("**Making the experiment**")
	st.write(r'''
		1. Start the measurement with the **HV** key
		2. Increase the capacitor volatge in steps from 0 V to 300 V and register the ionization current
		3. Repeat the analysis for different tube voltages.''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs.')

	st.write('')

	file = []
	file.append(st.file_uploader("Varying voltage file",accept_multiple_files=False))

	n_files = len(file)
	error_check = np.zeros(n_files)

	evs = np.arange(15,40,5)
	ics = np.zeros(len(evs))
	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1
			file[i].seek(0)
			data = pd.read_excel(file[i])


	fig = plt.figure(figsize = (12,4))
	gs = gridspec.GridSpec(1,2,wspace=0.2,hspace=0.3)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))


	for i in range(n_files):
		if error_check[i]:
			ax[0].plot(data.iloc[:,0],data.iloc[:,1:],'.',clip_on=False,label=['V=%.1f V'%x for x in evs])
			
			for j in range(np.shape(data)[1]-1):
				coeff = np.polyfit(data.iloc[:j+2,0], data.iloc[:j+2,j+1], 1)
				ics[j] = np.mean(data.iloc[-5-2*(5-j):,j+1])
			
				ax[0].axhline(ics[j],0,1,ls='--',c=default_colors[j])
				ax[0].plot([0,350],np.poly1d(coeff)([0,350]),'--',color=default_colors[j])
		
				ax[1].plot(evs[j],ics[j],'o',color=default_colors[j])
				ax[1].plot([-8,evs[j]],[ics[j],ics[j]],clip_on=False,ls='--',color=default_colors[j])
			ax[1].plot([0]  + [float(x) for x in evs] , [0]  + [float(x) for x in ics],'--k',lw=1)
	if sum(error_check)==0:

		for j in range(len(ax)):
			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')

	ax[0].set_ylabel('I (nA)' )
	ax[0].set_xlabel('$\Delta V$ (V)')
	ax[1].set_ylabel('$I_s$ (nA)' )
	ax[1].set_xlabel('Tube High-voltage (V)')

	ax[1].yaxis.tick_right()
	ax[1].yaxis.set_label_position("right")

	ax[0].set_ylim(0,4.2)
	ax[0].set_xlim(0,325)
	ax[1].set_xlim(0,40)
	ax[1].set_ylim(0,4.2)
	ax[0].legend(frameon=False,ncols=5,markerscale=1,bbox_to_anchor=(1.1,1.1),loc='lower center')
	plt.show()
	st.pyplot(fig)
	figs.append(fig)
	

with tabs[1]:
	st.write("**X-ray apparatus preparation**")
	st.write(r'''
		1. Set the tube high voltage $\Delta V=30$ kV
		2. Set the emission current $I=0.80$ mA
		''')	

	st.write("**Making the experiment**")
	st.write(r'''
		1. Start the measurement with the **HV** key
		2. Increase the capacitor volatge in steps from 0 V to 300 V and register the ionization current
		3. Repeat the analysis for different tube currents.''')

	st.write('')

	file = []
	file.append(st.file_uploader("Varying current file",accept_multiple_files=False))

	n_files = len(file)
	error_check = np.zeros(n_files)

	it = np.arange(25,125,25)/100
	ics = np.zeros(len(it))
	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1
			file[i].seek(0)
			data = pd.read_excel(file[i])


	fig = plt.figure(figsize = (12,4))
	gs = gridspec.GridSpec(1,2,wspace=0.2,hspace=0.3)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))


	for i in range(n_files):
		if error_check[i]:
			ax[0].plot(data.iloc[:,0],data.iloc[:,1:],'.',clip_on=False,label=['I=%.2f mA'%x for x in it])
			
			for j in range(np.shape(data)[1]-1):
				coeff = np.polyfit(data.iloc[:j+2,0], data.iloc[:j+2,j+1], 1)
				ics[j] = np.mean(data.iloc[-5-2*(5-j):,j+1])
			
				ax[0].axhline(ics[j],0,1,ls='--',c=default_colors[j])
				ax[0].plot([0,350],np.poly1d(coeff)([0,350]),'--',color=default_colors[j])
		
				ax[1].plot(it[j],ics[j],'o',color=default_colors[j])
				ax[1].plot([-0.25,it[j]],[ics[j],ics[j]],clip_on=False,ls='--',color=default_colors[j])
			ax[1].plot([0]  + [float(x) for x in it] , [0]  + [float(x) for x in ics],'--k',lw=1)
	if sum(error_check)==0:
		for j in range(len(ax)):
			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')

	ax[0].set_ylabel('I (nA)' )
	ax[0].set_xlabel('$\Delta V$ (V)')
	ax[1].set_ylabel('$I_s$ (nA)' )
	ax[1].set_xlabel('Tube current (mA)')

	ax[1].yaxis.tick_right()
	ax[1].yaxis.set_label_position("right")

	ax[0].set_ylim(0,4.2)
	ax[0].set_xlim(0,325)
	ax[1].set_xlim(0,1.2)
	ax[1].set_ylim(0,4.2)
	ax[0].legend(frameon=False,ncols=5,markerscale=1,bbox_to_anchor=(1.1,1.1),loc='lower center')
	plt.show()
	st.pyplot(fig)
	figs.append(fig)
	

st.write('')
st.write('**Export report**')
st.write('After filling in all the tabs above, you can download your report that should be attached as an appendix to the final reports.')
st.write('Please note that the pdf preview does not work in some browsers, but you should still be able to download the file.')

group_number = st.number_input("Group number",key='g_1_2',min_value=1,max_value=20,value=None)
exp_c = st.columns([0.25,0.25,0.5])
export_as_pdf = exp_c[0].button("Generate Report",key='pdf_1_2')

if export_as_pdf:
	try:
		create_pdf_task5(figs,group_number,
						'Experiment 5: Ionization chamber',
						'G%.2d_Exp5_report'%group_number,exp_c[1])
	except:
		st.error('Something went wrong. Check that you have filled in the group number.', icon="⚠️")



