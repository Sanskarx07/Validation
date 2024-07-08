from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

class PDFReport:
    def __init__(self, output_filename, page_size=A4, margin=0.5 * inch, spacing=0.2 * inch):
        self.output_filename = output_filename
        self.page_size = page_size
        self.margin = margin
        self.spacing = spacing
        self.canvas = canvas.Canvas(output_filename, pagesize=page_size)
        self.current_y = self.page_size[1] - self.margin

    def _draw_images_in_row(self, image_paths, box_x, box_y, box_width, box_height):
        num_images = len(image_paths)
        available_width = box_width - (num_images - 1) * self.spacing
        img_width = available_width / num_images
        img_height = box_height

        for i, image_path in enumerate(image_paths):
            x = box_x + i * (img_width + self.spacing)
            y = box_y

            img = Image.open(image_path)
            aspect = img.width / img.height

            if aspect > img_width / img_height:
                img_draw_width = img_width
                img_draw_height = img_width / aspect
            else:
                img_draw_height = img_height
                img_draw_width = img_height * aspect

            x_offset = (img_width - img_draw_width) / 2
            y_offset = (img_height - img_draw_height) / 2

            self.canvas.drawImage(image_path, x + x_offset, y + y_offset, img_draw_width, img_draw_height)

    def add_images(self, image_lists):
        for image_list in image_lists:
            num_images = image_list[0]
            caption = image_list[1]
            image_paths = image_list[2:num_images + 2]

            box_width = self.page_size[0] - 2 * self.margin
            box_height = (self.page_size[1] - 2 * self.margin - self.spacing) / 2

            # Check if there is enough space on the current page for the box and caption
            required_height = box_height + 0.5 * inch + self.spacing  # Adjust caption space
            if self.current_y - required_height < self.margin:
                self.canvas.showPage()
                self.current_y = self.page_size[1] - self.margin

            box_x = self.margin
            box_y = self.current_y - box_height

            self._draw_images_in_row(image_paths, box_x, box_y, box_width, box_height)

            # Add caption below the box, centered
            caption_x = self.page_size[0] / 2
            caption_y = box_y + 1 * inch  # Adjust as necessary for spacing
            self.canvas.drawCentredString(caption_x, caption_y, caption)

            self.current_y = caption_y - self.spacing

    def save(self):
        self.canvas.save()

# Example usage
image_lists = [
    [2, "Caption for first set of images", "tm_ta.png", "loc_ta.png"],
    [3, "Caption for second set of images", "custgender.png", "custgender_transaction.png", "tm_ta.png"]
]

pdf_report = PDFReport("output_box.pdf")
pdf_report.add_images(image_lists)
pdf_report.save()
