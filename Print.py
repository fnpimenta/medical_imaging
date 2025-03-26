import streamlit as st
import matplotlib.pyplot as plt
from fpdf import *
import base64
import numpy as np
from tempfile import NamedTemporaryFile

def create_download_link(val, filename):
	b64 = base64.b64encode(val)  # val looks like b'...'
	return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

def create_pdf_task1(figs,name,title,FileName,placeholder,U0,Is,I0,Us,Bs,logo1='figures/FCUP.jpg',logo2='figures/FEUP.jpg'):
	border = 'LRTB'*0
	pdf = FPDF()
	pdf.set_margins(25,18)
	pdf.add_page()
	pdf.set_font('Arial', 'B', 18)
	pdf.cell(45, 10, '',align='L',ln=0)
	pdf.cell(0, 10, 'Medical Imaging',align='L',ln=1)
	pdf.image(logo1,25,20,40)
	pdf.image(logo2,23,30,40)

	pdf.set_font('Arial',  '',12)
	pdf.cell(45, 10, '',border=border,align='L',ln=0)
	pdf.cell(0, 10, title,border=border,align='L',ln=1)
	pdf.cell(45, 10, '',border=border,align='L',ln=0)
	pdf.cell(0, 10,'Group number: %s'%name,border=border,align='L',ln=1)
	pdf.set_font('Arial', 'B' , 12)
	pdf.cell(45, 10,'Experimental results',border=border,align='L',ln=1)
	pdf.set_font('Arial', '' , 10)
	pdf.cell(45, 10,'Varying tube current for a tube voltage of %.2f kV'%U0,border=border,align='L',ln=1)
	pdf.cell(2, 10,'',border=0,align='L',ln=0)
	pdf.cell(55, 10,r'I1 (mA): %.2f'%Is[0],border=0,align='L',ln=0)
	pdf.cell(57, 10,r'I2 (mA): %.2f'%Is[1],border=0,align='L',ln=0)
	pdf.cell(30, 10,r'I3 (mA): %.2f'%Is[2],border=0,align='L',ln=1)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[0].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)
		
	pdf.cell(0, 5, '',border=border,align='L',ln=1)

	pdf.cell(45, 10,'Varying tube high voltage for a tube current of %.2f mA'%I0,border=border,align='L',ln=1)
	pdf.cell(2, 10,'',border=0,align='L',ln=0)
	pdf.cell(55, 10,r'V1 (kV): %.2f'%Us[0],border=0,align='L',ln=0)
	pdf.cell(57, 10,r'V2 (kV): %.2f'%Us[1],border=0,align='L',ln=0)
	pdf.cell(30, 10,r'V3 (kV): %.2f'%Us[2],border=0,align='L',ln=1)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[1].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)

	pdf.cell(0, 5, '',border=border,align='L',ln=1)

	pdf.cell(45, 10,'Projection effect',border=border,align='L',ln=1)
	pdf.cell(140, 10,r'dx (mm): %.2f'%Bs[0],border=0,align='R',ln=1)
	pdf.cell(140, 10,r'dy (mm): %.2f'%Bs[1],border=0,align='R',ln=1)
	pdf.cell(140, 10,r'dz (mm): %.2f'%Bs[2],border=0,align='R',ln=1)
	pdf.cell(140, 10,r'L (mm): %.2f'%Bs[3],border=0,align='R',ln=1)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[2].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,y=205,w=160*2/3,h=0)	



	html = create_download_link(pdf.output(dest="S").encode("latin-1"), FileName)
	placeholder.markdown(html, unsafe_allow_html=True)

	base64_pdf = base64.b64encode(pdf.output(dest="S").encode("latin-1")).decode('utf-8')

	# Embedding PDF in HTML
	pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="670" height="957" type="application/pdf"></iframe>'

	# Displaying File
	st.markdown(pdf_display, unsafe_allow_html=True)

	return

def create_pdf_task2(figs,name,title,FileName,placeholder,Is,logo1='figures/FCUP.jpg',logo2='figures/FEUP.jpg'):
	border = 'LRTB'*0
	pdf = FPDF()
	pdf.set_margins(25,18)
	pdf.add_page()
	pdf.set_font('Arial', 'B', 18)
	pdf.cell(45, 10, '',align='L',ln=0)
	pdf.cell(0, 10, 'Medical Imaging',align='L',ln=1)
	pdf.image(logo1,25,20,40)
	pdf.image(logo2,23,30,40)

	pdf.set_font('Arial',  '',12)
	pdf.cell(45, 10, '',border=border,align='L',ln=0)
	pdf.cell(0, 10, title,border=border,align='L',ln=1)
	pdf.cell(45, 10, '',border=border,align='L',ln=0)
	pdf.cell(0, 10,'Group number: %s'%name,border=border,align='L',ln=1)
	pdf.set_font('Arial', 'B' , 12)
	pdf.cell(45, 10,'Experimental results',border=border,align='L',ln=1)
	pdf.set_font('Arial', '' , 10)
	
	pdf.cell(45, 10,'Impact of the tube current on the results',border=border,align='L',ln=1)
	pdf.cell(2, 10,'',border=0,align='L',ln=0)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[0].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)
		
	pdf.cell(0, 5, '',border=border,align='L',ln=1)
	pdf.cell(45, 10,'Impact of the tube high-voltage on the results',border=border,align='L',ln=1)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[1].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)
	pdf.add_page()
	pdf.cell(45, 10,'Impact of the Zirconium filter on the results',border=border,align='L',ln=1)
	pdf.cell(2, 10,'',border=0,align='L',ln=0)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[2].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)
		
	pdf.cell(0, 5, '',border=border,align='L',ln=1)
	pdf.cell(45, 10,'Attenuation dependence on the atomic number (I1=%.2f mA and I2=%.2f mA)'%(Is[0],Is[1]),border=border,align='L',ln=1)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[3].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)


	html = create_download_link(pdf.output(dest="S").encode("latin-1"), FileName)
	placeholder.markdown(html, unsafe_allow_html=True)

	base64_pdf = base64.b64encode(pdf.output(dest="S").encode("latin-1")).decode('utf-8')

	# Embedding PDF in HTML
	pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="670" height="957" type="application/pdf"></iframe>'

	# Displaying File
	st.markdown(pdf_display, unsafe_allow_html=True)

	return

def create_pdf_task3(figs,name,title,FileName,placeholder,logo1='figures/FCUP.jpg',logo2='figures/FEUP.jpg'):
	border = 'LRTB'*0
	pdf = FPDF()
	pdf.set_margins(25,18)
	pdf.add_page()
	pdf.set_font('Arial', 'B', 18)
	pdf.cell(45, 10, '',align='L',ln=0)
	pdf.cell(0, 10, 'Medical Imaging',align='L',ln=1)
	pdf.image(logo1,25,20,40)
	pdf.image(logo2,23,30,40)

	pdf.set_font('Arial',  '',12)
	pdf.cell(45, 10, '',border=border,align='L',ln=0)
	pdf.cell(0, 10, title,border=border,align='L',ln=1)
	pdf.cell(45, 10, '',border=border,align='L',ln=0)
	pdf.cell(0, 10,'Group number: %s'%name,border=border,align='L',ln=1)
	pdf.set_font('Arial', 'B' , 12)
	pdf.cell(45, 10,'Experimental results',border=border,align='L',ln=1)
	pdf.set_font('Arial', '' , 10)
	pdf.cell(45, 10,'Impact of the tube voltage and current on the X-ray beam spectra',border=border,align='L',ln=1)
	pdf.cell(2, 10,'',border=0,align='L',ln=0)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[0].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)
		
	pdf.cell(0, 5, '',border=border,align='L',ln=1)

	pdf.cell(45, 10,'Duane-Hunt law experimental validation',border=border,align='L',ln=1)
	
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[1].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)

	html = create_download_link(pdf.output(dest="S").encode("latin-1"), FileName)
	placeholder.markdown(html, unsafe_allow_html=True)

	base64_pdf = base64.b64encode(pdf.output(dest="S").encode("latin-1")).decode('utf-8')

	# Embedding PDF in HTML
	pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="670" height="957" type="application/pdf"></iframe>'

	# Displaying File
	st.markdown(pdf_display, unsafe_allow_html=True)

	return


def create_pdf_task4(figs,name,title,FileName,placeholder,logo1='figures/FCUP.jpg',logo2='figures/FEUP.jpg'):
	border = 'LRTB'*0
	pdf = FPDF()
	pdf.set_margins(25,18)
	pdf.add_page()
	pdf.set_font('Arial', 'B', 18)
	pdf.cell(45, 10, '',align='L',ln=0)
	pdf.cell(0, 10, 'Medical Imaging',align='L',ln=1)
	pdf.image(logo1,25,20,40)
	pdf.image(logo2,23,30,40)

	pdf.set_font('Arial',  '',12)
	pdf.cell(45, 10, '',border=border,align='L',ln=0)
	pdf.cell(0, 10, title,border=border,align='L',ln=1)
	pdf.cell(45, 10, '',border=border,align='L',ln=0)
	pdf.cell(0, 10,'Group number: %s'%name,border=border,align='L',ln=1)
	pdf.set_font('Arial', 'B' , 12)
	pdf.cell(45, 10,'Experimental results',border=border,align='L',ln=1)
	pdf.set_font('Arial', '' , 10)
	pdf.cell(45, 10,'Characterisation of the photoelectric cross section dependency on the wavelength',border=border,align='L',ln=1)
	pdf.cell(2, 10,'',border=0,align='L',ln=0)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[0].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)
		
	html = create_download_link(pdf.output(dest="S").encode("latin-1"), FileName)
	placeholder.markdown(html, unsafe_allow_html=True)

	base64_pdf = base64.b64encode(pdf.output(dest="S").encode("latin-1")).decode('utf-8')

	# Embedding PDF in HTML
	pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="670" height="957" type="application/pdf"></iframe>'

	# Displaying File
	st.markdown(pdf_display, unsafe_allow_html=True)

	return