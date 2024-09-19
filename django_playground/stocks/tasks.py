# tasks.py
from time import sleep

from celery import shared_task


@shared_task
def burn_stock_task(product_id, quantity: int | None = None, reason: str | None = None) -> str:
    from django_playground.stocks.models import Product
    from django_playground.stocks.models import StockMovement

    sleep(10)
    prod = Product.objects.get(id=product_id)
    if quantity is None:
        quantity = prod.stock
        prod.stock = 0
    else:
        prod.stock -= quantity

    prod.stock_movements.add(StockMovement(movement_type="out", quantity=quantity, description=reason))
    prod.save()

    return f"Burned {quantity} items from product {prod} for reason: {reason}"
