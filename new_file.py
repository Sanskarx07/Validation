import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

class PDFCreator:
    def __init__(self, output_pdf_name, heading, navbar_title):
        self.output_pdf_name = output_pdf_name
        self.heading = heading
        self.navbar_title = navbar_title
        self.page_number = 1
        self.c = None

    def add_navbar(self):
        # Draw the red navbar background
        self.c.setFillColor(HexColor('#B31B1B'))
        self.c.rect(0, 770, 612, 30, fill=1)

        # Draw the yellow rectangle
        self.c.setFillColor(HexColor('#FFD700'))
        self.c.rect(0, 765, 612, 3, fill=1)

        # Add white navbar title
        self.c.setFillColor(HexColor('#FFFFFF'))
        self.c.setFont('Helvetica-Bold', 12)
        self.c.drawString(72, 780, self.navbar_title)

    def add_page_number(self):
        self.c.setFillColor(HexColor('#000000'))
        self.c.setFont('Helvetica', 10)
        self.c.drawRightString(600, 20, f"Page {self.page_number}")
        self.page_number += 1

    def add_heading(self):
        self.c.setFont('Helvetica-Bold', 16)
        self.c.drawCentredString(300, 720, self.heading)
        self.c.line(72, 710, 540, 710)

    def add_text_file(self, txt_file_path):
        with open(txt_file_path, 'r') as file:
            lines = file.readlines()

        self.c.setFont('Helvetica', 12)
        text = self.c.beginText(72, 680)
        for line in lines:
            text.textLine(line.strip())
        self.c.drawText(text)

    def add_image(self, image_path):
        self.c.drawImage(image_path, 72, 400, width=5*inch, height=5*inch, preserveAspectRatio=True)

    def create_pdf(self, text_files_folder, images_folder):
        self.c = canvas.Canvas(self.output_pdf_name, pagesize=letter)

        # Process text files
        for txt_file in sorted(os.listdir(text_files_folder)):
            if txt_file.endswith('.txt'):
                self.c.showPage()
                self.add_navbar()
                self.add_heading()
                self.add_text_file(os.path.join(text_files_folder, txt_file))
                self.add_page_number()
        
        # Process image files
        for img_file in sorted(os.listdir(images_folder)):
            if img_file.endswith(('.png', '.jpg', '.jpeg')):
                self.c.showPage()
                self.add_navbar()
                self.add_heading()
                self.add_image(os.path.join(images_folder, img_file))
                self.add_page_number()

        self.c.save()

# Usage
if __name__ == "__main__":
    output_pdf_name = "output.pdf"
    heading = "Analysis Report"
    navbar_title = "Wells Fargo"

    text_files_folder = "text_file"
    images_folder = "image_file"

    pdf_creator = PDFCreator(output_pdf_name, heading, navbar_title)
    pdf_creator.create_pdf(text_files_folder, images_folder)
