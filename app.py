import razorpay
import os
import sqlite3
import uuid
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "uzhavar_unavu_podi_2026"
client = razorpay.Client(
    auth=(
        "rzp_live_TEFImfUGcLzBQ7",
        "hGmzCpNm45Ff5wVHMFbezvfx"
    )
)
# -------------------------
# Product Data
# -------------------------

products = [
    {
        "id": 1,
        "name": "Paruppu Podi",
        "image": "paruppu.png",
        "prices": {
            "50": 30,
            "100": 60,
            "150": 90,
            "200": 120,
            "250": 150
        }
    },
    {
        "id": 2,
        "name": "Idly Podi",
        "image": "idly.png",
        "prices": {
            "50": 30,
            "100": 60,
            "150": 90,
            "200": 120,
            "250": 150
        }
    },
    {
        "id": 3,
        "name": "Garlic Podi",
        "image": "garlic.png",
        "prices": {
            "50": 35,
            "100": 70,
            "150": 105,
            "200": 140,
            "250": 175
        }
    },
    {
        "id": 4,
        "name": "Pirandai Podi",
        "image": "pirandai.png",
        "prices": {
            "50": 45,
            "100": 90,
            "150": 135,
            "200": 180,
            "250": 225
        }
    },
    {
        "id": 5,
        "name": "Kollu Podi",
        "image": "kollu.png",
        "prices": {
            "50": 45,
            "100": 90,
            "150": 135,
            "200": 180,
            "250": 225
        }
    },
    {
        "id": 6,
        "name": "Curry Leaves Podi",
        "image": "curry.png",
        "prices": {
            "50": 40,
            "100": 80,
            "150": 120,
            "200": 160,
            "250": 200
        }
    },
    {
        "id": 7,
        "name": "Murungai Podi",
        "image": "murungai.png",
        "prices": {
            "50": 40,
            "100": 80,
            "150": 120,
            "200": 160,
            "250": 200
        }
    }
]
# -------------------------
# Home Page
# -------------------------

@app.route("/")
def home():
    return render_template("index.html", products=products)

# -------------------------
# Products Page
# -------------------------

@app.route("/products")
def products_page():
    return render_template("products.html", products=products)

# -------------------------
# Order Page
# -------------------------

@app.route("/order/<int:id>", methods=["GET", "POST"])
def order(id):

    product = products[id - 1]

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]
        quantity = request.form["quantity"]
        weight = request.form["weight"]
        amount = request.form["amount"]
        if name.strip() == "" or phone.strip() == "" or address.strip() == "":
          return "Please fill all required fields."

        order_id = "UUP-" + uuid.uuid4().hex[:8].upper()

        session["order"] = {
            "order_id": order_id,
            "name": name,
            "phone": phone,
            "address": address,
            "product": product["name"],
            "weight": weight,
            "quantity": quantity,
            "amount": amount
        }

        return redirect("/payment")

    return render_template("order.html", product=product)
@app.route("/admin")
def admin():

    search = request.args.get("search", "")
    status = request.args.get("status", "All")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    query = "SELECT * FROM orders WHERE 1=1"
    params = []

    if search:
        query += " AND (customer_name LIKE ? OR order_id LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if status != "All":
        query += " AND status=?"
        params.append(status)

    query += " ORDER BY id DESC"

    cursor.execute(query, params)
    orders = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM orders")
    total_sales = cursor.fetchone()[0] or 0

    conn.close()

    return render_template(
        "admin.html",
        orders=orders,
        total_orders=total_orders,
        total_sales=total_sales,
        search=search,
        status=status
    )
@app.route("/add-to-cart/<int:id>", methods=["POST"])
def add_to_cart(id):

    product = products[id - 1]

    quantity = int(request.form["quantity"])
    weight = request.form["weight"]

    price = product["prices"][weight]

    cart = session.get("cart", [])

    found = False

    for item in cart:
        if item["id"] == id and item["weight"] == weight:
            item["quantity"] += quantity
            found = True
            break

    if not found:
        cart.append({
            "id": id,
            "name": product["name"],
            "weight": weight,
            "price": price,
            "quantity": quantity
        })

    session["cart"] = cart

    return redirect("/cart")
@app.route("/cart")
def cart():

    cart = session.get("cart", [])

    total = 0

    for item in cart:

        item["subtotal"] = item["price"] * item["quantity"]

        total += item["subtotal"]

    return render_template(
        "cart.html",
        cart=cart,
        total=total
    )
@app.route("/checkout")
def checkout():
    return render_template("checkout.html")
@app.route("/payment")
def payment():

    if "order" not in session:
        return redirect("/")
    order = session["order"]

    amount = int(float(order["amount"]) * 100)

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    order["razorpay_order_id"] = razorpay_order["id"]

    session["order"] = order

    return render_template(
    "payment.html",
    order=order,
    razorpay_order_id=razorpay_order["id"],
    razorpay_key="rzp_live_TEFImfUGcLzBQ7"
)
@app.route("/payment-success")
def payment_success():

    payment_id = request.args.get("payment_id")

    razor_order = request.args.get("order_id")

    signature = request.args.get("signature")

    order = session.get("order")

    params = {

        "razorpay_order_id": razor_order,

        "razorpay_payment_id": payment_id,

        "razorpay_signature": signature

    }

    try:

        client.utility.verify_payment_signature(params)

    except:

        return "Payment Verification Failed"

    conn = sqlite3.connect("database.db")

    cur = conn.cursor()

    cur.execute("""

    INSERT INTO orders

    (order_id,name,phone,address,product,weight,quantity,amount)

    VALUES(?,?,?,?,?,?,?,?)

    """,

    (

        "UUP-"+uuid.uuid4().hex[:8].upper(),

        order["name"],

        order["phone"],

        order["address"],

        order["product"],

        order["weight"],

        order["quantity"],

        order["amount"]

    ))

    conn.commit()

    conn.close()

    session.pop("order",None)

    return redirect(f"/success/{order['order_id']}")
@app.route("/update-status/<int:id>", methods=["POST"])
def update_status(id):

    status = request.form["status"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")
@app.route("/delete-order/<int:id>", methods=["POST"])
def delete_order(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")
@app.route("/invoice/<int:id>")
def invoice(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE id=?", (id,))
    order = cursor.fetchone()
    print(order)
    conn.close()

    if not order:
        return "Order Not Found"

    filename = f"invoice_{order[1]}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>🌿 Uzhavar Unavu Podi</b>", styles["Title"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Order ID:</b> {order[1]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Customer:</b> {order[2]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Phone:</b> {order[3]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Address:</b> {order[4]}", styles["Normal"]))

    story.append(Paragraph(f"<b>Product:</b> {order[5]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Weight:</b> {order[6]} g", styles["Normal"]))
    story.append(Paragraph(f"<b>Quantity:</b> {order[7]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Total Amount:</b> ₹{order[8]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Status:</b> {order[9]}", styles["Normal"]))
    story.append(Paragraph("<br/><br/>", styles["Normal"]))
    story.append(Paragraph("Thank you for shopping with Uzhavar Unavu Podi!", styles["Heading2"]))

    doc.build(story)

    return send_file(filename, as_attachment=True)
@app.route("/track", methods=["GET", "POST"])
def track():

    order = None

    if request.method == "POST":

        order_id = request.form["order_id"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
        order = cursor.fetchone()

        conn.close()

    return render_template("track.html", order=order)    
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/remove-item/<int:index>")
def remove_item(index):

    cart = session.get("cart", [])

    if index < len(cart):

        cart.pop(index)

    session["cart"] = cart

    return redirect("/cart")
@app.route("/increase/<int:index>")
def increase(index):

    cart = session.get("cart", [])

    cart[index]["quantity"] += 1

    session["cart"] = cart

    return redirect("/cart")
@app.route("/decrease/<int:index>")
def decrease(index):

    cart = session.get("cart", [])

    if cart[index]["quantity"] > 1:

        cart[index]["quantity"] -= 1

    session["cart"] = cart

    return redirect("/cart")
@app.route("/clear-cart")
def clear_cart():

    session["cart"] = []

    return redirect("/cart")
@app.route("/success/<order_id>")
def success(order_id):
    return render_template(
        "success.html",
        order_id=order_id
    )
    return redirect(f"/success/{order['order_id']}")
if __name__ == "__main__":
    app.run(debug=True)