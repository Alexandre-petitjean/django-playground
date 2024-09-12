# Create your models here.
import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    A product in stock. Related to :model:`stocks.Category` and :model:`stocks.Supplier`.
    reorder_threshold: Quantity at which the product should be reordered.
    auto_reorder: Whether the product should be reordered automatically.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(Supplier, related_name="products", on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    quantity_in_stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_threshold = models.IntegerField(default=10)
    auto_reorder = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class StockMovement(models.Model):
    """
    Represents a stock movement (incoming or outgoing) of a product.
    Each line in the table represents a movement of a certain quantity of a product.
    """

    class MovementType(models.TextChoices):
        INCOMING = "in", "Incoming"
        OUTGOING = "out", "Outgoing"

    product = models.ForeignKey(
        Product,
        related_name="stock_movements",
        on_delete=models.CASCADE,
    )
    movement_type = models.CharField(max_length=3, choices=MovementType, default=MovementType.INCOMING, blank=False)
    quantity = models.IntegerField()
    date = models.DateTimeField(default=timezone.now())
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} - {self.quantity} - {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.movement_type == self.MovementType.INCOMING:
            self.product.quantity_in_stock += self.quantity
        elif self.movement_type == self.MovementType.OUTGOING:
            self.product.quantity_in_stock -= self.quantity

        if self.product.quantity_in_stock < 0:
            msg = "Stock quantity cannot be negative"
            raise ValueError(msg)

        self.product.save()
