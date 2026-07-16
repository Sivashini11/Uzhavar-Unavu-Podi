let cart = JSON.parse(localStorage.getItem("cart")) || [];

let total = 0;

let html = "";

cart.forEach(item => {

    let subtotal = item.price * item.quantity;

    total += subtotal;

    html += `
        <div class="checkout-card">

            <img src="/static/images/${item.image}" width="100">

            <div>

                <h3>${item.name}</h3>

                <p>₹${item.price}</p>

                <p>Qty : ${item.quantity}</p>

                <h4>Subtotal : ₹${subtotal}</h4>

            </div>

        </div>
    `;

});

document.getElementById("checkout-items").innerHTML = html;

document.getElementById("checkout-total").innerHTML = total;

document.getElementById("amount").value = total;