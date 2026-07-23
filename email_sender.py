import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

OWNER_EMAIL = "uzhavarunavupodi@gmail.com"

def send_invoice_to_owner(invoice_path, order):

    with open(invoice_path, "rb") as f:
        pdf_data = f.read()

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": OWNER_EMAIL,
        "subject": f"New Order - {order['order_id']}",
        "text": f"""
New Order Received

Order ID: {order['order_id']}
Customer: {order['name']}
Phone: {order['phone']}
Address: {order['address']}
Product: {order['product']}
Weight: {order['weight']} g
Quantity: {order['quantity']}
Amount: ₹{order['amount']}
""",
        "attachments": [
            {
                "filename": f"{order['order_id']}.pdf",
                "content": pdf_data
            }
        ]
    })

    print("✅ Email sent successfully using Resend")