import csv
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

class PDFGenerator:
    def __init__(self, attribute_csv, recommendation_csv, output_file):
        self.attribute_csv = attribute_csv
        self.recommendation_csv = recommendation_csv
        self.output_file = output_file
        self.attributes = []
        self.recommendations = {}
        self.page_width, self.page_height = A4
        self.header_height = 50
        self.footer_height = 30
        self.margin = 20
        self.content_start_y = self.page_height - self.header_height - self.margin

    def load_data(self):
        with open(self.attribute_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.attributes.append(row)

        with open(self.recommendation_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for column in row:
                    if column.startswith('recommended_'):
                        attribute_name = column.replace('recommended_', '')
                        if attribute_name not in self.recommendations:
                            self.recommendations[attribute_name] = []
                        self.recommendations[attribute_name].append(row[column])

    def draw_header(self, pdf):
        pdf.setFillColorRGB(0.8, 0, 0)
        pdf.rect(0, self.page_height - 40, self.page_width, 40, stroke=0, fill=1)
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont('Helvetica-Bold', 16)
        pdf.drawString(30, self.page_height - 30, 'WELLS FARGO')
        pdf.setFillColorRGB(1, 0.84, 0)
        pdf.rect(0, self.page_height - 50, self.page_width, 10, stroke=0, fill=1)

    def draw_footer(self, pdf):
        page_num = pdf.getPageNumber()
        pdf.setFont('Helvetica', 10)
        pdf.setFillColor(colors.black)
        pdf.drawString(self.page_width / 2, 20, str(page_num))

    def generate_table_data(self, attribute_name, attribute_data):
        data = [['S.N.', 'Data', 'Recommendation']]
        recommendations = self.recommendations.get(attribute_name, ['N/A'] * len(attribute_data))
        for idx, data_point in enumerate(attribute_data[:5], 1):
            recommendation = recommendations[idx - 1] if idx - 1 < len(recommendations) else 'N/A'
            data.append([idx, data_point, recommendation])
        return data

    def draw_table(self, pdf, data, x_start, y_start):
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        col_widths = [30, 160, 330]  # Modify these values as per your requirements

        table = Table(data, colWidths=col_widths)
        table.setStyle(table_style)

        table_width, table_height = table.wrap(0, 0)
        if y_start - table_height < self.footer_height + 20:
            self.draw_footer(pdf)
            pdf.showPage()
            self.draw_header(pdf)
            y_start = self.page_height - self.header_height - self.margin - 20

        for i, row in enumerate(data):
            if i == 0:
                continue  # Skip header row
            if 'correct' in row[2].lower():
                table_style.add('TEXTCOLOR', (2, i), (2, i), colors.green)
            elif 'incorrect' or 'missing':
                table_style.add('TEXTCOLOR', (2, i), (2, i), colors.red)

        table.setStyle(table_style)
        table.drawOn(pdf, x_start, y_start - table_height)
        return y_start - table_height - 20  # Return the new y position after drawing the table

    def create_pdf(self):
        self.load_data()
        pdf = canvas.Canvas(self.output_file, pagesize=A4)
        self.draw_header(pdf)
        pdf.setFillColor(colors.black)

        y_start = self.content_start_y
        x_start = 30

        for attribute_name in self.attributes[0].keys():
            data_values = [attr[attribute_name] for attr in self.attributes]
            table_data = self.generate_table_data(attribute_name, data_values)
            
            # Draw the attribute name as header
            pdf.setFont('Helvetica-Bold', 12)
            y_start -= 10
            pdf.setFillColor(colors.black)
            pdf.drawString(x_start, y_start, f"Attribute Name: {attribute_name}")
            y_start -= 20
            
            # Draw the table and update y_start
            y_start = self.draw_table(pdf, table_data, x_start, y_start)

            if y_start < 100:  # Check if we need to move to the next page
                self.draw_footer(pdf)
                pdf.showPage()
                self.draw_header(pdf)
                y_start = self.content_start_y
                pdf.setFont('Helvetica-Bold', 12)

        self.draw_footer(pdf)
        pdf.save()

# Example usage
attribute_csv_path = 'attribute.csv'
recommendation_csv_path = 'recommendations.csv'
output_pdf_path = 'output_check.pdf'

pdf_generator = PDFGenerator(attribute_csv_path, recommendation_csv_path, output_pdf_path)
pdf_generator.create_pdf()
