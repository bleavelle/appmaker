import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def process_pdf(input_pdf, num_copies, start_number):
    writer = PdfWriter()
    x_coord, y_coord = 465, 285  # Coordinates for number placement
    font_size = 16  # Font size for the number
    
    for i in range(num_copies):
        reader = PdfReader(input_pdf)
        page = reader.pages[0]
        
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica-Bold", font_size)
        can.drawString(x_coord, y_coord, f"{start_number + i:04d}")
        can.save()
        
        packet.seek(0)
        new_pdf = PdfReader(packet)
        
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)
    
    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output

st.title('PDF Processor')
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
num_copies = st.number_input("Number of copies", min_value=1, value=1)
start_number = st.number_input("Starting number", min_value=1, value=1)

if uploaded_file is not None:
    if st.button('Process PDF'):
        input_pdf = BytesIO(uploaded_file.read())
        output_pdf = process_pdf(input_pdf, num_copies, start_number)
        
        st.download_button(
            label="Download processed PDF",
            data=output_pdf,
            file_name="processed_" + uploaded_file.name,
            mime="application/pdf"
        )
