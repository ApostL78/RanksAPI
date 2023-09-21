import stripe


def get_item_session(item):
    tax = None
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=_make_line_items([item], tax),
        mode='payment',
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )
    return session


def get_order_session(order):
    coupon = None
    if order.discount:
        coupon = stripe.Coupon.create(
            percent_off=order.discount.percent_off,
            duration=order.discount.duration,
        )
    tax = None
    if order.tax and order.tax.description:
        tax = stripe.TaxRate.create(
            display_name=order.tax.display_name,
            inclusive=order.tax.inclusive,
            percentage=order.tax.percentage,
            description=order.tax.description,
        )
    elif order.tax:
        tax = stripe.TaxRate.create(
            display_name=order.tax.display_name,
            inclusive=order.tax.inclusive,
            percentage=order.tax.percentage,
        )
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=_make_line_items([item for item in order.items.all()], tax),
        mode="payment",
        discounts=[{
            "coupon": str(coupon.id)
        }] if coupon else None,
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )
    return session


def _make_line_items(items, tax):
    line_items = []
    for item in items:
        item_data = {
            'price_data': {
                'product_data': {
                    "name": item.name,
                    "description": item.description,
                },
                "unit_amount": int(item.price * 100),
                "currency": "usd",
            },
            'tax_rates': [tax.id] if tax else None,
            "quantity": 1,
        }
        if not item.description:
            item_data["price_data"]["product_data"].pop("description")
        line_items.append(item_data)
    return line_items
