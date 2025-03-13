import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import CubicSpline
from matplotlib import cm
import os
from scipy import signal

from PIL import Image

from Print import * 

# -- Set page config
apptitle = 'Medical Imaging - Experiment 3'
icon = Image.open('feup_logo.ico')
st.set_page_config(page_title=apptitle, page_icon=icon)
st.title('X-ray spectra and Duane-Hunt law')

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
		Although the Geiger-Mueller counters cannot be used as spectrometers on their own, when coupled to an adequate experimental setup the energy distribution of the incident radiation can be probed.
		By using a crystal lattice as target, the radiation is reflected by the different atomic planes. For a given incident angle, some particular wavelengths lead to constructive interference, as illustrated below:
		''')
	st.markdown('''<a href="https://en.wikipedia.org/wiki/Bragg%27s_law">
                <center>
                <img height= 300px 
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Bragg_diffraction_2.svg/600px-Bragg_diffraction_2.svg.png" 
                title="Bragg's law"/>
                </center>
                ''',unsafe_allow_html=True)
	st.write(r'''
		By simple geometrical considerations, it can be easily seen that this condition can be expressed as:
		$$
			\lambda = \dfrac{2}{n}\cdot d\cdot \sin\theta
		$$
		where $n$ is a positive integer that defines the diffraction order, $d$ is the lattice spacing and $\theta$ is the glancing angle, measured with respect to the crystal planes.
		By probing using different glancing angles, a Geiger-Mueller counter can be used to characterise the different wavelengths, or, equivalently, the energy distribution of the beam, since:
		$$
			\lambda = \dfrac{c}{f} = \dfrac{h\cdot c}{E_\gamma}
		$$
		where $h$ is the Planck constant and $c$ is the speed of light in the vacuum.
		
		Finally, note that the Duane-Hunt law defines the minimum wavelength (or maximum frequency) for a given tube voltage, $\Delta V$, as:
		$$
			\lambda_{min} = \dfrac{h\cdot c}{e\cdot\Delta V}
		$$
		Using the minimum wavelength obtained for different tube voltages you should obtain a linear relation against $1/\Delta V$, with slope $m$ given by:
		$$
			m = \dfrac{h\cdot c}{e}
		$$
		where $e$ is the elementary electron charge. By assuming $c=2.9979\times10^8$ m/s and $e=1.6022\times10^{-19}$ C you can use the result above to constrain the Planck's constant value.
		''')
	st.write('')

tabs = st.tabs(['**Beam spectra analysis**' , '**Duane-Hunt relation**' ])
figs = []

with tabs[0]:
	st.write("**X-ray apparatus preparation**")
	st.write(r'''
		1. Mount the collimator and install the Geiger counter on the respective support
		2. Install the NaCl crystal on the support attached to the goniometer
		2. Set the tube high voltage $\Delta V=30$ kV
		3. Set the emission current $I=0.80$ mA
		4. Set the aparatus mode to **COUPLED**
		5. Set the measuring time $\Delta t=5$ s
		''')	

	st.write("**Making the experiment**")
	st.write(r'''
		1. Start the measurement with the **SCAN** key
		2. Repeat the measurement for $\beta\in[3º,8º]$ with an angular step of 0.1º (you may tune the lower bound of the angular positions based on the tube high voltage used)
		3. Repeat the measurements with a different current
		4. Repeat the measurements with a different tube voltage''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs.')

	st.write('')

	cols = st.columns(3)
	file = []
	file.append(cols[0].file_uploader("Reference file",accept_multiple_files=False))
	file.append(cols[1].file_uploader("Varying current",accept_multiple_files=False))
	file.append(cols[2].file_uploader("Varying voltage",accept_multiple_files=False))
	d_beta = 0.1
	b_max = 8

	n_files = len(file)
	error_check = np.zeros(n_files)

	b_mins = np.zeros(n_files)
	evs = np.zeros(n_files)
	Is = np.zeros(n_files)
	
	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=4,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			b_mins[i] = data.iloc[0,0]

			dN = len(np.arange(b_mins[i],b_max+d_beta,d_beta))
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18+dN,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			evs[i] = data.iloc[0,0]
			Is[i] = data.iloc[0,2]

	fig = plt.figure(figsize = (9,4))
	gs = gridspec.GridSpec(1,1,wspace=0.2,hspace=0.3)
	ax = []
	ax.append(plt.subplot(gs[0,0]))

	for i in range(n_files):
		if error_check[i]:
			betas = np.arange(b_mins[i],b_max+d_beta,d_beta)
			full_betas = np.arange(b_mins[i],b_max+0.01,0.01)
			lambdas = 2*d*np.sin(np.pi/180*betas)
			full_lambdas = 2*d*np.sin(np.pi/180*full_betas)
			energies = 1239.8/lambdas
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18,nrows=len(betas),sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			y = data.iloc[:,0]
			cs = CubicSpline(betas, y)

			ax[0].plot(lambdas,y,'.',color=default_colors[i],clip_on=False,label='V=%.1f kV; I=%.2f mA'%(evs[i],Is[i]))
			ax[0].plot(full_lambdas,cs(full_betas),'--',color=default_colors[i],lw=1,clip_on=False)

	if sum(error_check)==0:
		for j in range(len(ax)):
			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')


	ax[0].set_ylabel('R (counts per second)' )
	#ax[0].set_title('Measured values')

	#ax[0].set_xlim(right=max(lambdas))
	ax[0].set_ylim(0,)
	ax[0].set_xlabel('Wavelength (pm)')
	if sum(error_check)>0:
		ax[0].axvline(71.080,0,1,c='k',ls='--')
		ax[0].axvline(63.095,0,1,c='k',ls='--')
		ax[0].annotate(text=r'71.080 pm',xy=(71.080,ax[0].set_ylim()[1]),ha='center',va='bottom',clip_on=False)
		ax[0].annotate(text=r"63.095 pm",xy=(63.095,ax[0].set_ylim()[1]),ha='center',va='bottom',clip_on=False)
	ax[0].legend(frameon=False,ncols=4,markerscale=1,bbox_to_anchor=(0.5,1.1),loc='lower center')
	plt.show()
	st.pyplot(fig)
	figs.append(fig)
	st.caption(r'It was assumed a crystal lattice such that $2\cdot d=%.2f$ nm. The dashed lines were obtained using a cubic spline and are only included as a visual aid, not representing the experimental data.'%(2*d))


with tabs[1]:
	st.write("**X-ray apparatus preparation**")
	st.write(r'''
		1. Mount the collimator and install the Geiger counter on the respective support
		2. Install the NaCl crystal on the support attached to the goniometer
		2. Set the tube high voltage $\Delta V=30$ kV
		3. Set the emission current $I=0.80$ mA
		4. Set the aparatus mode to **COUPLED**
		5. Set the measuring time $\Delta t=5$ s
		''')	

	st.write("**Making the experiment**")
	st.write(r'''
		1. Start the measurement with the **SCAN** key
		2. Repeat the measurement for $\beta\in[3º,8º]$ with an angular step of 0.1º (you may tune the lower bound of the angular positions based on the tube high voltage used)
		3. Repeat the measurements with different tube voltages''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs. In this case you may use any file format, since you will have to define the range for the fit in each case.')

	st.write('')

	n_files = 4
	d_beta = 0.1
	b_max = 8
	cols = st.columns(n_files)
	file = []

	error_check = np.zeros(n_files)
	evs = np.zeros(n_files)
	b_mins = np.zeros(n_files)
	l_mins = np.zeros(n_files)

	p_mins = np.zeros(n_files)
	p_maxs = np.zeros(n_files)
	d_betas = np.zeros(n_files) 

	cols = st.columns(n_files)
	
	for i in range(n_files):
		with cols[i].expander('Experiment %d'%(i+1),True):
			file.append(st.file_uploader("Data",accept_multiple_files=False,key='D%d'%i))
			if not(file[i]==None):
				error_check[i] += 1
				file[i].seek(0)
				data = pd.read_csv(file[i],skiprows=4,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
				b_mins[i] = data.iloc[0,0]

				dN = len(np.arange(b_mins[i],b_max+d_beta,d_beta))
				file[i].seek(0)
				data = pd.read_csv(file[i],skiprows=18+dN,nrows=1,sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
				evs[i] = data.iloc[0,0]

			p_mins[i] = st.number_input(r'First point',value=3,key='p1%d'%i,disabled=(0==error_check[i]))
			p_maxs[i] = st.number_input(r'Last point',value=10,key='p2%d'%i,disabled=(0==error_check[i]))


	fig = plt.figure(figsize = (10,3.5))
	gs = gridspec.GridSpec(1,2,wspace=0.2,hspace=0.3)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))

	labels = ['No filter','Zr filter','Cu filter']
	for i in range(n_files):
		if error_check[i]:
			betas = np.arange(b_mins[i],b_max+d_beta,d_beta)
			full_betas = np.arange(b_mins[i],b_max+0.01,0.01)
			lambdas = 2*d*np.sin(np.pi/180*betas)
			full_lambdas = 2*d*np.sin(np.pi/180*full_betas)
			energies = 1239.8/lambdas

			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18,nrows=len(betas),sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')

			y = np.array(data.iloc[:,0])
			cs = CubicSpline(betas, y)

			x_filt = lambdas[int(p_mins[i]-1):int(p_maxs[i]-1)]
			y_filt = y[int(p_mins[i]-1):int(p_maxs[i]-1)]
			
			coeff = np.polyfit(x_filt, y_filt, 1)
			l_mins[i] = -coeff[1]/coeff[0]

			ax[0].plot(lambdas,y,'.',color=default_colors[i],ms=2,clip_on=False,label='V=%.1f kV'%evs[i])
			ax[0].plot(x_filt,y_filt,'.',color=default_colors[i],ms=5,clip_on=False)
			ax[0].plot(lambdas,np.poly1d(coeff)(lambdas),'--',lw=1,color=default_colors[i],ms=1,clip_on=True)
	
			ax[1].plot(1/evs[i],l_mins[i],'o',color=default_colors[i],clip_on=False)

	if sum(error_check)>1:
		coeff = np.polyfit(1/evs[error_check>0],l_mins[error_check>0], 1)
		ax[1].plot([0,1/min(evs[error_check>0])],[np.poly1d(coeff)(0),np.poly1d(coeff)(1/min(evs[error_check>0]))],'--k',
					lw=1,ms=1,clip_on=True,label='$\lambda_{min}=%.2f+%.2f\cdot\dfrac{1}{V}$'%(coeff[1],coeff[0]))
		
	if sum(error_check)==0:
		for j in range(len(ax)):
			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')

	#ax[0].set_title('Measured values')
	#ax[0].set_xlim()
	ax[0].set_ylim(0,2000)
	ax[0].set_xlabel('Wavelength (nm)')
	ax[0].set_ylabel('$R$ (counts per second)' )

	#ax[0].set_title('Measured values')
	ax[1].set_xlabel('1/Tube voltage (1/kV)')
	ax[1].set_ylabel('$\lambda_{min}$ (pm)' )
	ax[1].legend(frameon=False)
	ax[0].legend(frameon=False,ncols=4,markerscale=5,bbox_to_anchor=(1.1,1.1),loc='lower center')
	plt.show()
	st.pyplot(fig)
	figs.append(fig)
	st.caption(r'It was assumed a crystal lattice such that $2\cdot d=%.2f$ nm.'%(2*d))


st.write('')
st.write('**Export report**')
st.write('After filling in all the tabs above, you can download your report that should be attached as an appendix to the final reports.')
st.write('Please note that the pdf preview does not work in some browsers, but you should still be able to download the file.')

group_number = st.number_input("Group number",key='g_1_2',min_value=1,max_value=20,value=None)
exp_c = st.columns([0.25,0.25,0.5])
export_as_pdf = exp_c[0].button("Generate Report",key='pdf_1_2')

if export_as_pdf:
	try:
		create_pdf_task3(figs,group_number,
						'Experiment 3: X-ray beam spectra',
						'G%.2d_Exp3_report'%group_number,exp_c[1])
	except:
		st.error('Something went wrong. Check that you have filled in the group number.', icon="⚠️")


