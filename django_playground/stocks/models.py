from datetime import datetime
from typing import Optional

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import now

from django_playground.stocks.tasks import burn_stock_task
from django_playground.stocks.tasks import order_stock_task


class Category(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return f"{self.slug} - {self.name}"


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    order_schedule_time = models.DateTimeField(default=timezone.now)
    estimated_delivery_time = models.IntegerField(default=2, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    A product in stock. Related to :model:`stocks.Category` and :model:`stocks.Supplier`.
    reorder_threshold: Quantity at which the product should be reordered.
    auto_reorder: Whether the product should be reordered automatically.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    stock = models.IntegerField()
    tags = models.JSONField()
    brand = models.CharField(max_length=100, blank=True, default="")
    sku = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    dimensions = models.JSONField()
    warranty_information = models.CharField(max_length=255, blank=True, default="")
    shipping_information = models.CharField(max_length=255, blank=True, default="")
    availability_status = models.CharField(max_length=50, blank=True, default="")
    return_policy = models.CharField(max_length=255, blank=True, default="")
    minimum_order_quantity = models.IntegerField(blank=True, null=True)
    meta = models.JSONField()
    thumbnail = models.URLField(blank=True, default="https://dummyjson.com/image/150")
    images = models.JSONField()

    def __str__(self):
        return self.title

    @property
    def last_incoming_movement(self) -> Optional["StockMovement"]:
        return self.stock_movements.filter(movement_type=StockMovement.MovementType.INCOMING).last()

    @property
    def last_outgoing_movement(self) -> Optional["StockMovement"]:
        return self.stock_movements.filter(movement_type=StockMovement.MovementType.OUTGOING).last()

    def burn_stock(self, quantity: int, scheduled_date: datetime | None, reason: str):
        return burn_stock_task.apply_async(
            args=[self.id, quantity, reason],
            eta=now() if scheduled_date is None else scheduled_date,
        )

    def order_stock(self, quantity: int, scheduled_date: datetime | None, reason: str):
        return order_stock_task.apply_async(
            args=[self.id, quantity, reason],
            eta=now() if scheduled_date is None else scheduled_date,
        )


class StockMovement(models.Model):
    """
    Represents a stock movement (incoming or outgoing) of a product.
    Each line in the table represents a movement of a certain quantity of a product.
    """

    class MovementType(models.TextChoices):
        INCOMING = "in", "Incoming"
        OUTGOING = "out", "Outgoing"

    product = models.ForeignKey(Product, related_name="stock_movements", on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=3, choices=MovementType, default=MovementType.INCOMING, blank=False)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.created_at} {self.get_movement_type_display()} - {self.quantity} of {self.product.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.movement_type == self.MovementType.INCOMING:
            self.product.stock += self.quantity
        elif self.movement_type == self.MovementType.OUTGOING:
            self.product.stock -= self.quantity

        if self.product.stock < 0:
            msg = "Stock quantity cannot be negative"
            raise ValueError(msg)

        self.product.save()
