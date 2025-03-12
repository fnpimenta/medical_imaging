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
apptitle = 'Medical Imaging - Experiment 4'
icon = Image.open('feup_logo.ico')
st.set_page_config(page_title=apptitle, page_icon=icon)
st.title('Study of the photoelectric cross-section')

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
default_colors = ['tab:blue','tab:orange','tab:green']
d = 564.02/2

with st.expander('**Theory**',True):
	st.write(r'''
		Although the Geiger-Mueller counters cannot be used as spectrometers on their own, when coupled to an adequate experimental setup the energy distribution of the incident radiation can be probed.
		By using a crystal lattice as target, the radiation is reflected by the different atomic planes. For a given incident angle, some particular wavelengths lead to constructive interference.
		By simple geometrical considerations, it can be easily seen that this condition can be expressed as:
		$$
			\lambda = \dfrac{2}{n}\cdot d\cdot \sin\theta
		$$
		where $n$ is a positive integer that defines the diffraction order, $d$ is the lattice spacing and $\theta$ is the glancing angle, measured with respect to the crystal planes.
		By probing using different glancing angles, a Geiger-Mueller counter can be used to characterise the different wavelengths, or, equivalently, the energy distribution of the beam, since:
		$$
			\lambda = \dfrac{c}{f} = \dfrac{h\cdot c}{E_\gamma} \approx \dfrac{1239.8 (\text{nm/eV})}{E_\gamma}
		$$
		where the last expression is valid for wavelentghs in nanometers (nm) and energies in eV.
		''')
	st.write('')

tabs = st.tabs(['**Beam spectra analysis**' , '**Duane-Hunt relation**' ])
figs = []

with tabs[0]:
	st.write("**X-ray apparatus preparation**")
	st.write(r'''
		1. Mount the collimator and install the Geiger counter on the respective support
		2. Install the target with varying thickness in the goniometer
		2. Set the tube high voltage $\Delta V=35$ kV
		3. Set the emission current $I=0.80$ mA
		4. Set the aparatus mode to **COUPLED**
		5. Set the angular position $\Delta\beta=0º$
		6. Set the measuring time $\Delta t=5$ s
		''')	

	st.write("**Making the experiment**")
	st.write(r'''
		1. Start the measurement with the **SCAN** key
		2. Repeat the measurement for $\beta\in[3º,8º]$ with an angular step of 0.1º
		3. Repeat the measurements with the zirconium filter
		4. Repeat the measurements with the copper filter''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs')

	st.write('')

	cols = st.columns(3)
	file = []
	file.append(cols[0].file_uploader("Without filter",accept_multiple_files=False))
	file.append(cols[1].file_uploader("With zirconium filter",accept_multiple_files=False))
	file.append(cols[2].file_uploader("With cupper filter",accept_multiple_files=False))

	n_files = len(file)
	error_check = np.zeros(n_files)

	for i in range(len(file)):
		if not(file[i]==None):
			error_check[i] += 1

	cols = st.columns(3)
	b_min = cols[0].number_input(r'$\beta_{min}$',value=4)
	b_max = cols[1].number_input(r'$\beta_{max}$',value=8)
	d_beta = cols[2].number_input(r'$\Delta\beta$',value=0.1)
	
	betas = np.arange(b_min,b_max+d_beta,d_beta)
	full_betas = np.arange(b_min,b_max+0.01,0.01)
	lambdas = 2*d*np.sin(np.pi/180*betas)
	full_lambdas = 2*d*np.sin(np.pi/180*full_betas)
	energies = 1239.8/lambdas

	fig = plt.figure(figsize = (9,6))
	gs = gridspec.GridSpec(1,1,wspace=0.2,hspace=0.3)
	ax = []
	ax.append(plt.subplot(gs[0,0]))

	labels = ['No filter','Zr filter','Cu filter']
	for i in range(n_files):
		if error_check[i]:
			file[i].seek(0)
			data = pd.read_csv(file[i],skiprows=18,nrows=len(betas),sep='\s+',header=None,skip_blank_lines=False,encoding_errors='ignore')
			y = data.iloc[:,0]
			cs = CubicSpline(betas, y)

			ax[0].plot(lambdas,y,'.',color=default_colors[i],clip_on=False)
			ax[0].plot(full_lambdas,cs(full_betas),'--',color=default_colors[i],lw=1,clip_on=False)

	if sum(error_check)==0:
		for j in range(len(ax)):
			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')

	ax[0].set_ylabel('$R$ (counts per second)' )
	ax[0].set_title('Measured values')

	ax[0].set_xlim(right=max(lambdas))
	ax[0].set_ylim(0,)
	ax[0].set_xlabel('Wavelength (nm)')

	plt.show()
	st.pyplot(fig)
	figs.append(fig)
	st.caption(r'It was assumed a crystal lattice such that $2\cdot d=%.2f$ nm. The dashed lines were obtained using a cubic spline and are only included as a visual aid, not representing the experimental data.'%(2*d))

