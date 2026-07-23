import smtplib
import os
from email.message import EmailMessage

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")

OWNER_EMAIL = "uzhavarunavupodi@gmail.com"


def send_invoice_to_owner(invoice_path, order):

    print("Inside send_invoice_to_owner()")

    msg = EmailMessage()

    msg["Subject"] = f"🛒 New Order - {order['order_id']}"
    msg["From"] = EMAIL
    msg["To"] = OWNER_EMAIL

    msg.set_content(f"""
🌿 Uzhavar Unavu Podi

New Order Received

Order ID:
{order['order_id']}

Customer:
{order['name']}

Phone:
{order['phone']}

Address:
{order['address']}

Product:
{order['product']}

Weight:
{order['weight']}

Quantity:
{order['quantity']}

Amount:
₹{order['amount']}
""")

    with open(invoice_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(invoice_path)
        )

    print("Connecting to Gmail...")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as smtp:

            print("Connected")

            smtp.login(EMAIL, PASSWORD)

            print("Logged in")

            smtp.send_message(msg)

            print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ SMTP ERROR:", e)