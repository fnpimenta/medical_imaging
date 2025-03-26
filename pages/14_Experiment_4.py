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
default_colors = ['tab:blue','tab:orange','tab:green','tab:red']
d = 564.02/2

with st.expander('**Theory**',True):
	st.write(r'''
		As you have seen in <a href="https://medicalimagingfeup.streamlit.app/Experiment_2">Experiment 2</a>, the attenuation of x-rays passing through matter is described
		by Lambert’s law:
		$$
			I = I_0e^{-\mu d}
		$$
		where $\mu$ is the linear attenuation coefficient, that depends on the material and the wavelength of the incident beam, $\lambda$. 
		Alternatively, you may use the result above to epress the transmittance as:
		$$
			\mathcal{T} = \dfrac{I}{I_0}\cdot e^{-\mu d}
		$$ 
		Note that $\mu$ includes the contributions from all relevant interactions that, in this case, are mostly governed by the photoelectrc effect and Compton scattering:
		$$
			\mu = \mu_{PE} + \mu_C 
		$$
		where $\mu_{PE}$ and $\mu_C$ are the attenuation coefficients associated with the photoelectric effect and Compton scattering, respectively, that depend on the mass and the density of the irradiated material. 
		Alternatively, you can define the corresponding atomic cross section as:
		$$
			\sigma_{PE} = \dfrac{\mu_{PE}}{\rho}\cdot \dfrac{A}{N_A}\\
			\sigma_{C} = \dfrac{\mu_{C}}{\rho}\cdot \dfrac{A}{N_A} \\
		$$
		where $\rho$ is the mass density and $A$ the atomic weight of the irradiated material and $N_A=6.022\times10^{23}$ mol$^{-1}$ is the Avogadro's number.
		Note that the intearction dependence is fully contained in the linear attenuation coefficients, while the remaining terms depend on the material, implying that the measured cross section, $\sigma$, is still given by:
		$$
			\sigma = \sigma_{PE} + \sigma_{C}
		$$
		In the energy range that you will probe, the Compton cross section is well approximated by a constant value given by:
		$$
			\sigma_C \approx 0.2\cdot \dfrac{A}{N_A} \left[\dfrac{\text{ cm}^2}{\text{g}}\right]
		$$
		while, outside of the absorption edges, the photoelectric cross section is given by:
		$$
			\sigma_{PE} = C\cdot\lambda^m\cdot Z^4 
		$$
		where $C$ is a constant and for most materials $m\approx3$.
		Under these assumptions, you can easily see that the photoelectric cross section can be experimentally characterised from the measured transmittance as:
		$$
			\sigma_{PE} = -\dfrac{\ln\mathcal{T}}{\rho\cdot d}\cdot \dfrac{A}{N_A} - 0.2\cdot \dfrac{A}{N_A} \left[\dfrac{\text{ cm}^2}{\text{g}}\right]
		$$
		Once the cross section has been estimated, you can easily verify the theoretical predicted behaviour and constrain the value of $m$ by noting that:
		$$
			\ln \sigma_{PE} = \ln\left[C\cdot \lambda^m\cdot Z^4 \right] = m\ln\left[\lambda\right] + \ln\left[C\cdot Z^4 \right] 
		$$
		which is just a linear relation between $\ln\sigma_{PE}$ and $\ln\lambda$ with slope $m$.
		The relevant parameters for the Copper (Cu) and Zirconium (Zr) that will be used in this experiment are given below:
		''',unsafe_allow_html=True)
	st.write('''
		| Element   | Z |  $\\rho$ (g/cm$^3$) |  A (g/mol)| d (cm)|
		| -------- | ------- | ------- | ------- | ------- |
		| Cu | 29 | 8.92 | 63.55 | 0.007 | 
		| Zr | 40 | 6.49 | 91.22 | 0.005 |
		''')
	st.write('')

tabs = st.tabs(['**Wavelength dependency**'])
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
		3. Repeat the measurements with the zirconium filter
		4. Repeat the measurements with the copper filter''')

	st.write('**Data Analysis**')

	st.write('Upload the measurement outputs')

	st.write('')

	cols = st.columns(3)
	file = []
	file.append(cols[0].file_uploader("Without filter",accept_multiple_files=False))
	file.append(cols[1].file_uploader("With copper filter",accept_multiple_files=False))
	file.append(cols[2].file_uploader("With zirconium filter",accept_multiple_files=False))
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

	fig = plt.figure(figsize = (10,7))
	gs = gridspec.GridSpec(2,2,wspace=0.2,hspace=0.3)
	ax = []
	ax.append(plt.subplot(gs[0,0]))
	ax.append(plt.subplot(gs[0,1]))

	ax.append(plt.subplot(gs[1,0]))
	ax.append(plt.subplot(gs[1,1]))


	labels = ['No filter','Cu filter','Zr filter']
	rhos = [8.92,6.49]
	xs = [0.007,0.005]
	As = [63.55,91.22]
	N_A = 6.02214076e23
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
			if i == 0:
				y0 = data.iloc[:,0]
			cs = CubicSpline(lambdas, y)

			ax[0].plot(lambdas,y,'.',color=default_colors[i],clip_on=False,label=labels[i])
			ax[0].plot(full_lambdas,cs(full_lambdas),'--',color=default_colors[i],lw=1,clip_on=False)
			if i>0:
				transmittance = y/y0
				lambda_min = lambdas[energies<evs[0]][1]
				lambda_min_filter = lambdas>lambda_min
				lambda_max = 63
				lambda_max_filter = lambdas<=lambda_max 
				lambda_filter = lambda_min_filter & lambda_max_filter

				cs = CubicSpline(lambdas[lambda_min_filter], transmittance[lambda_min_filter])
				ax[1].plot(lambdas[lambda_min_filter],100*transmittance[lambda_min_filter],'.',color=default_colors[i],clip_on=False,label=labels[i])		
				ax[1].plot(full_lambdas[full_lambdas>(lambda_min+1)],100*cs(full_lambdas[full_lambdas>(lambda_min+1)]),'--',color=default_colors[i],lw=1,clip_on=False)

				tau = -(np.log(transmittance)/(rhos[i-1]*xs[i-1]) + 0.2)*As[i-1]/N_A
				ax[2].plot(lambdas[lambda_min_filter],1e21*tau[lambda_min_filter],'.',color=default_colors[i],clip_on=False,label=labels[i])		
				ax[3].plot(np.log(lambdas[lambda_min_filter]),np.log(1e21*tau[lambda_min_filter]),'.',ms=2,color=default_colors[i],clip_on=False)		
				ax[3].plot(np.log(lambdas[lambda_filter]),np.log(1e21*tau[lambda_filter]),'.',color=default_colors[i],clip_on=False)		

				coeff = np.polyfit(np.log(lambdas[lambda_filter]), np.log(1e21*tau[lambda_filter]), 1)
				if coeff[1]>0:
					ax[3].plot(np.log(lambdas[lambda_filter]),np.poly1d(coeff)(np.log(lambdas[lambda_filter])),'--',color=default_colors[i],
						   	   label='$\ln\sigma=%.2f\cdot\ln\lambda$+%.2f'%(coeff[0],coeff[1]))
				else:
					ax[3].plot(np.log(lambdas[lambda_filter]),np.poly1d(coeff)(np.log(lambdas[lambda_filter])),'--',color=default_colors[i],
						   	   label='$\ln\sigma=%.2f\cdot\ln\lambda$%.2f'%(coeff[0],coeff[1]))

	if sum(error_check)==0:
		for j in range(len(ax)):
			ax[j].annotate('No data found',(0.5,0.5),ha='center',xycoords='axes fraction')

	ax[0].set_ylabel('R (counts per second)' )
	ax[1].set_ylabel('Transmittance (%)' )
	ax[2].set_ylabel(r'$\sigma_{PE}$ $\times10^{21}$ (cm$^2$)' )
	ax[3].set_ylabel(r'$\ln\left[\sigma_{PE}\times10^{21}\right]$')

	ax[0].set_ylim(0,)
	ax[1].set_xlim(ax[0].get_xlim())
	ax[2].set_xlim(ax[0].get_xlim())
	
	ax[0].set_xlabel('Wavelength (pm)')
	ax[1].set_xlabel('Wavelength (pm)')
	ax[2].set_xlabel('Wavelength (pm)')
	ax[3].set_xlabel(r'$\ln\lambda$' )
	ax[0].legend(frameon=False,ncols=4,markerscale=1,bbox_to_anchor=(1.1,1.1),loc='lower center')
	ax[3].legend(frameon=False)
	
	plt.show()
	st.pyplot(fig)
	figs.append(fig)
	st.caption(r'It was assumed a crystal lattice such that $2\cdot d=%.2f$ nm. The dashed lines on the top plots were obtained using a cubic spline and are only included as a visual aid, not representing the experimental data.'%(2*d))
	st.caption(r'The transmittance was computed only for energies above the tube high voltage.')


st.write('')
st.write('**Export report**')
st.write('After filling in all the tabs above, you can download your report that should be attached as an appendix to the final reports.')
st.write('Please note that the pdf preview does not work in some browsers, but you should still be able to download the file.')

group_number = st.number_input("Group number",key='g_1_2',min_value=1,max_value=20,value=None)
exp_c = st.columns([0.25,0.25,0.5])
export_as_pdf = exp_c[0].button("Generate Report",key='pdf_1_2')

if export_as_pdf:
	try:
		create_pdf_task4(figs,group_number,
						'Experiment 4: Photoelectric cross-section',
						'G%.2d_Exp4_report'%group_number,exp_c[1])
	except:
		st.error('Something went wrong. Check that you have filled in the group number.', icon="⚠️")




