# tasks.py
from celery import shared_task
from time import sleep



@shared_task
def burn_stock_task(product_id, quantity:int=None, reason:str=None) -> str:
    from django_playground.stocks.models import Product

    sleep(10)
    prod = Product.objects.get(id=product_id)
    if quantity is None:
        quantity = prod.quantity_in_stock
        prod.quantity_in_stock = 0
    else:
        prod.quantity_in_stock -= quantity
    prod.save()
    return f"Burned {quantity} items from product {prod.name} for reason: {reason}"
