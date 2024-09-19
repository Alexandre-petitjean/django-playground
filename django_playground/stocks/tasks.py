# tasks.py
from time import sleep

from celery import shared_task


@shared_task
def burn_stock_task(product_id, quantity: int, reason: str) -> str:
    sleep(5)
    return create_stock_movement(product_id, movement_type="out", quantity=quantity, description=reason)


@shared_task
def order_stock_task(product_id, quantity: int, reason: str) -> str:
    sleep(5)
    return create_stock_movement(product_id, movement_type="in", quantity=quantity, description=reason)


def create_stock_movement(product_id, movement_type: str, quantity: int, description: str) -> str:
    from django_playground.stocks.models import Product

    prod = Product.objects.get(id=product_id)
    prod.stock_movements.create(movement_type=movement_type, quantity=quantity, description=description)
    prod.save()

    if movement_type == "in":
        msg = f"Order {quantity} items from product {prod} for reason: {description}"
    else:
        msg = f"Burned {quantity} items from product {prod} for reason: {description}"

    return msg
