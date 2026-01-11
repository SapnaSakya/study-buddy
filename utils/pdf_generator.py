from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_pdf(content):
    file = "study_notes.pdf"
    c = canvas.Canvas(file, pagesize=A4)
    text = c.beginText(40, 800)

    for line in content.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.save()
    return file