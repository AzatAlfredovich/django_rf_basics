import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product_name):
    product = stripe.Product.create(name=product_name)
    return product


def create_stripe_price(amount, product_id):
    """Создание цены в Stripe"""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product_id,
    )
    return price


def create_stripe_session(price):
    """Создание сессии в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("url")
