import streamlit as st
import matplotlib.pyplot as plt
from fpdf import *
import base64
import numpy as np
from tempfile import NamedTemporaryFile

def create_download_link(val, filename):
	b64 = base64.b64encode(val)  # val looks like b'...'
	return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

def create_pdf_task1(figs,name,title,FileName,placeholder,Is,Us,Bs,logo1='figures/FCUP.jpg',logo2='figures/FEUP.jpg'):
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
	pdf.cell(45, 10,'Varying tube current',border=border,align='L',ln=1)
	pdf.cell(2, 10,'',border=0,align='L',ln=0)
	pdf.cell(55, 10,r'I1 (mA): %.2f'%Is[0],border=0,align='L',ln=0)
	pdf.cell(57, 10,r'I2 (mA): %.2f'%Is[1],border=0,align='L',ln=0)
	pdf.cell(30, 10,r'I3 (mA): %.2f'%Is[2],border=0,align='L',ln=1)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[0].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)
		
	pdf.cell(0, 5, '',border=border,align='L',ln=1)

	pdf.cell(45, 10,'Varying tube high voltage',border=border,align='L',ln=1)
	pdf.cell(2, 10,'',border=0,align='L',ln=0)
	pdf.cell(55, 10,r'U1 (kV): %.2f'%Us[0],border=0,align='L',ln=0)
	pdf.cell(57, 10,r'U2 (kV): %.2f'%Us[1],border=0,align='L',ln=0)
	pdf.cell(30, 10,r'U3 (kV): %.2f'%Us[2],border=0,align='L',ln=1)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[1].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160,h=0)

	pdf.cell(0, 5, '',border=border,align='L',ln=1)

	pdf.cell(45, 10,'Projection effect',border=border,align='L',ln=1)
	pdf.cell(2, 10,'',border=0,align='L',ln=0)
	pdf.cell(55, 10,r'dx (cells): %.2f'%Bs[0],border=0,align='L',ln=0)
	pdf.cell(57, 10,r'dy (cells): %.2f'%Bs[1],border=0,align='L',ln=0)
	pdf.cell(30, 10,r'dz (cells): %.2f'%Bs[2],border=0,align='L',ln=1)
	with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
		figs[2].savefig(tmpfile.name, bbox_inches='tight')
		pdf.image(tmpfile.name,w=160*2/3,h=0)


	html = create_download_link(pdf.output(dest="S").encode("latin-1"), FileName)
	placeholder.markdown(html, unsafe_allow_html=True)

	base64_pdf = base64.b64encode(pdf.output(dest="S").encode("latin-1")).decode('utf-8')

	# Embedding PDF in HTML
	pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="670" height="957" type="application/pdf"></iframe>'

	# Displaying File
	st.markdown(pdf_display, unsafe_allow_html=True)

	return

def create_pdf_task2(figs,name,title,FileName,placeholder,placeholder_pdf,mu1,mu2,s1,s2,logo1='figures/FCUP.jpg',logo2='figures/FEUP.jpg'):
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
	Count = 0
	for fig in figs:
		Count += 1
		with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
			fig.savefig(tmpfile.name, bbox_inches='tight')
			pdf.cell(45, 10, '',border=border,align='L',ln=1)
			pdf.image(tmpfile.name,25,60,w=160,h=0)
	pdf.cell(0, 70, '',border=border,align='L',ln=1)
	pdf.set_font('Arial', '' , 10)
	pdf.cell(45, 10,r'Linear attenuation coefficient without filter: %.2f'%mu1,border=border,align='L',ln=0)
	pdf.cell(115, 10,r'Half-value layer (HVL): %.2f'%s1,border=border,align='R',ln=1)
	pdf.cell(45, 10,r'Linear attenuation coefficient with filter: %.2f'%mu2,border=border,align='L',ln=0)
	pdf.cell(115, 10,r'Half-value layer (HVL): %.2f'%s1,border=border,align='R',ln=1)

	pdf.cell(45, 10,'',border=border,align='L',ln=1)
	#for i in range(4):
	#	pdf.cell(25, 10,r'Student %d:'%(i+1),border=border,align='L',ln=0)
	#	pdf.cell(135, 10,70*'_',border=border,align='R',ln=1)


	html = create_download_link(pdf.output(dest="S").encode("latin-1"), FileName)
	placeholder.markdown(html, unsafe_allow_html=True)

	base64_pdf = base64.b64encode(pdf.output(dest="S").encode("latin-1")).decode('utf-8')

	# Embedding PDF in HTML
	pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="670" height="957" type="application/pdf"></iframe>'

	# Displaying File
	placeholder_pdf.markdown(pdf_display, unsafe_allow_html=True)

	return

