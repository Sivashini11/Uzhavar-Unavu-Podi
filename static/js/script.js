function updatePrice(select){

    const prices = JSON.parse(select.dataset.prices);

    const weight = select.value;

    const card = select.closest(".product");

    const qty = parseInt(card.querySelector(".quantity span").innerText);

    card.querySelector(".price").innerText =
        "₹" + prices[weight] * qty;

}

function changeQty(button, value){

    const card = button.closest(".product");

    const qtySpan = card.querySelector(".quantity span");

    let qty = parseInt(qtySpan.innerText);

    qty += value;

    if(qty < 1){

        qty = 1;

    }

    qtySpan.innerText = qty;

    const select = card.querySelector(".weight-select");

    updatePrice(select);

}