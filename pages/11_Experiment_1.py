import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.cbook import get_sample_data
from matplotlib import cm
import os
from scipy import signal
import cv2

from PIL import Image

from Print import * 

# -- Set page config
apptitle = 'Medical Imaging - Experiment 1'
icon = Image.open('feup_logo.ico')
st.set_page_config(page_title=apptitle, page_icon=icon)
st.title('Observation of x-ray images')

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

with st.expander('**Theory**',True):
	st.write(r'''
		X-rays can be "observed" on a luminous screen in some materials. 

		Fluorescence is a luminous phenomenon that occurs in certain
		materials when these are exposed to light, x-ray or particle
		radiation. The energy of the incident radiation is used to excite
		or ionize the atoms and molecules; when these return to the
		ground state, a portion of this energy is released in the form of
		visible light. The transitions are extremely rapid (<10$^{-5}$ s), so
		that fluorescence can only be observed during irradiation.

		The ability of x-rays to pass through opaque materials and
		bodies make them particularly useful in diagnostic applications.
		Depending on the composition of the irradiated object,
		the radiation is attenuated to a greater or lesser extent. That is
		why the images on the luminous screen reveal details of the
		internal structure of objects. In this experiment, this fact is
		demonstrated using a simple object which has parts made of materials with different absorption
		properties. This experiment investigates the effect of the emission
		current I of the x-ray tube on the brightness and the effect
		of the tube high voltage U on the contrast of the luminous
		screen
		''')

tabs = st.tabs(['**Impact of tube current intensity**' , '**Impact of tube high voltage**','**X-ray projection effect**' ])
figs = []

with tabs[0]:
	st.write("**Experimental setup**:")
	st.write(r'''
		1. Set the tube high voltage $\Delta V=35$ kV
		2. Set the emission current for values up to 1 mA, $I\in[0,1]$ mA
		''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs')

	cols0 = st.columns(3)
	file = []
	file.append(cols0[0].file_uploader("$I_1$",accept_multiple_files=False))
	file.append(cols0[1].file_uploader("$I_2$",accept_multiple_files=False))
	file.append(cols0[2].file_uploader("$I_3$",accept_multiple_files=False))
		
	error_check = np.zeros(3)

	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1

	fig = plt.figure(figsize = (12,3))
	gs = gridspec.GridSpec(1,3,wspace=0.1,hspace=0.1)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))
	ax.append(plt.subplot(gs[0,2]))
	for i in range(3):
		if error_check[i]:
			image = Image.open(file[i])
			#image = cv2.imread(file[0])
			img_array = np.array(image)
			ax[i].imshow(img_array,aspect='auto')
		else:
			ax[i].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
		ax[i].set_xticklabels([])
		ax[i].set_yticklabels([])

	plt.show()
	st.pyplot(fig)
	figs.append(fig)

	Is = []
	cols = st.columns(3)
	Is.append(cols[0].number_input("$I_1$ (mA)"))
	Is.append(cols[1].number_input("$I_2$ (mA)"))
	Is.append(cols[2].number_input("$I_3$ (mA)"))


with tabs[1]:	
	st.write("**Experimental setup**:")
	st.write(r'''
		1. Set the tube current $I=1$ mA
		2. Set the tube current for values up to $\Delta V=$35 kV, $\Delta V\in[15,35]$ kV
		''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs')

	cols0 = st.columns(3)
	file = []
	file.append(cols0[0].file_uploader("$U_1$",accept_multiple_files=False))
	file.append(cols0[1].file_uploader("$U_2$",accept_multiple_files=False))
	file.append(cols0[2].file_uploader("$U_3$",accept_multiple_files=False))
		
	error_check = np.zeros(3)

	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1

	fig = plt.figure(figsize = (12,3))
	gs = gridspec.GridSpec(1,3,wspace=0.1,hspace=0.1)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))
	ax.append(plt.subplot(gs[0,2]))
	for i in range(3):
		if error_check[i]:
			image = Image.open(file[i])
			#image = cv2.imread(file[0])
			img_array = np.array(image)
			ax[i].imshow(img_array,aspect='auto')
		else:
			ax[i].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
		ax[i].set_xticklabels([])
		ax[i].set_yticklabels([])

	plt.show()
	st.pyplot(fig)
	figs.append(fig)

	Us = []
	cols = st.columns(3)
	Us.append(cols[0].number_input("$U_1$ (kV)"))
	Us.append(cols[1].number_input("$U_2$ (kV)"))
	Us.append(cols[2].number_input("$U_3$ (kV)"))


with tabs[2]:	
	st.write("**Experimental setup**:")
	st.write(r'''
		1. Set the tube current $I=1$ mA
		2. Set the tube current for values to $\Delta V$=35 kV
		''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs')

	cols0 = st.columns(2)
	file = []
	file.append(cols0[0].file_uploader("Front view",accept_multiple_files=False))
	file.append(cols0[1].file_uploader("Lateral view",accept_multiple_files=False))

	error_check = np.zeros(2)

	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1

	cols = st.columns(3)

	gridsize = cols[0].slider("Grid refinement:", value=1,min_value=1,max_value=6)
	fig = plt.figure(figsize = (8,3))
	gs = gridspec.GridSpec(1,2,wspace=0.1,hspace=0.1)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))
	for i in range(2):
		if error_check[i]:
			image = Image.open(file[i])
			#image = cv2.imread(file[0])
			img_array = np.array(image)
			ax[i].imshow(img_array,aspect='auto')

		else:
			ax[i].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')
		
		ax[i].set_xticks(np.arange(0,640,2*64/gridsize))
		ax[i].set_yticks(np.arange(0,480,2*48/gridsize))
		ax[i].set_xticklabels('')
		ax[i].set_yticklabels('')
		ax[i].grid()

	plt.show()
	st.pyplot(fig)
	figs.append(fig)

	cols = st.columns(3)
	Bs = []
	Bs.append(cols[0].number_input("$\Delta x$ (cells)"))
	Bs.append(cols[1].number_input("$\Delta y$ (cells)"))
	Bs.append(cols[2].number_input("$\Delta z$ (cells)"))

st.write('')
st.write('**Export report**')

report_text = st.text_input("Group number",key='g_1_2')
exp_c = st.columns([0.25,0.25,0.5])
export_as_pdf = exp_c[0].button("Generate Report",key='pdf_1_2')

if export_as_pdf:
	#try:
	create_pdf_task1(figs,report_text,'Experiment 1: Impact of tube current and tube voltage','Exp1_report',exp_c[1],
					 Is,Us,Bs)
	#except:
	#	st.error('Something went wrong. No file available for the analysis.', icon="⚠️")



