from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
import datetime
import io

def generate_pickup_report(owner_details: dict[str, str], item_details: dict[str, str]):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    img_file = open("assets/BTUw.png", "rb")
    styles = getSampleStyleSheet()
    elements = []

    # Header
    title = Paragraph("Back2U Item Pickup Report", styles["Title"])
    image = Image(img_file, width=1.2*inch, height=1.2*inch)
    data = [[title, image]]
    table = Table(data, colWidths=[4.8*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Date
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_paragraph = Paragraph(f"<b>Generated on:</b> {today}", styles["Normal"])
    elements.append(date_paragraph)
    elements.append(Spacer(1, 24))

    # Section 1
    section1_title = Paragraph("<b>1. Pickup Person Credentials</b>", styles["Heading2"])
    elements.append(section1_title)
    elements.append(Spacer(1, 12))
    person_data = [
        ["Name", owner_details["name"]],
        ["Surname", owner_details["surname"]],
        ["Email Address", owner_details["email"]],
        ["PESEL Number", owner_details["pesel"]],
    ]
    person_table = Table(person_data, colWidths=[2.5 * inch, 3.5 * inch])
    person_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ]))
    elements.append(person_table)
    elements.append(Spacer(1, 24))

    # Section 2
    section2_title = Paragraph("<b>2. Item Description</b>", styles["Heading2"])
    elements.append(section2_title)
    elements.append(Spacer(1, 12))
    item_data = []

    for trait, value in item_details.items():
        if value is not None or value == "":
            item_data.append([trait, value])

    item_table = Table(item_data, colWidths=[2.5 * inch, 3.5 * inch])
    item_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ]))
    elements.append(item_table)
    elements.append(Spacer(1, 24))

    # Signature section
    signature = Paragraph(
        "<b>Receptionist Signature:</b> ____________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
        "<b>Date:</b> ____________",
        styles["Normal"]
    )
    elements.append(signature)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    pdf_bytes = buffer.read()
    buffer.close()
    img_file.close()

    return pdf_bytes