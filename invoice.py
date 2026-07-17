from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_invoice(order):

    os.makedirs("invoices", exist_ok=True)

    filename = f"invoices/{order['order_id']}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>🌿 Uzhavar Unavu Podi</b>", styles["Title"]))
    story.append(Paragraph("Invoice", styles["Heading2"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Order ID:</b> {order['order_id']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Customer:</b> {order['name']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Phone:</b> {order['phone']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Address:</b> {order['address']}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Product:</b> {order['product']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Weight:</b> {order['weight']} g", styles["Normal"]))
    story.append(Paragraph(f"<b>Quantity:</b> {order['quantity']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Amount Paid:</b> ₹{order['amount']}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Payment Status:</b> SUCCESS", styles["Heading2"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "Thank you for shopping with Uzhavar Unavu Podi.",
            styles["Normal"]
        )
    )

    doc.build(story)

    return filename