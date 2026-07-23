import os
import base64
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

OWNER_EMAIL = "uzhavarunavupodi@gmail.com"


def send_invoice_to_owner(invoice_path, order):

    with open(invoice_path, "rb") as f:
        pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": OWNER_EMAIL,
        "subject": f"🛒 New Order - {order['order_id']}",
        "text": f"""
🌿 Uzhavar Unavu Podi

New Order Received

Order ID: {order['order_id']}
Customer: {order['name']}
Phone: {order['phone']}
Address: {order['address']}
Product: {order['product']}
Weight: {order['weight']}
Quantity: {order['quantity']}
Amount: ₹{order['amount']}
""",
        "attachments": [
            {
                "filename": f"{order['order_id']}.pdf",
                "content": pdf_base64
            }
        ]
    })

    print("✅ Email sent successfully")