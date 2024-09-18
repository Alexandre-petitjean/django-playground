# Create your models here.
import uuid
from time import sleep

from celery import shared_task
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
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


class Dimension(models.Model):
    length = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    height = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.length} x {self.width} x {self.height}"


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=100)
    user_mail = models.EmailField()

    def __str__(self):
        return f"{self.product} - {self.rating}"


class Meta(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bar_code = models.CharField(max_length=100, null=True)
    qr_code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.created_at} - {self.updated_at}"


class Product(models.Model):
    """
    A product in stock. Related to :model:`stocks.Category` and :model:`stocks.Supplier`.
    reorder_threshold: Quantity at which the product should be reordered.
    auto_reorder: Whether the product should be reordered automatically.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], default=0
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, validators=[MinValueValidator(0)]
    )
    quantity_in_stock = models.IntegerField()
    reorder_threshold = models.IntegerField()
    auto_reorder = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    brand = models.CharField(max_length=100, null=True)
    sku = models.CharField(max_length=100, null=True)
    weight = models.PositiveSmallIntegerField(default=0)
    dimensions = models.ManyToManyField(Dimension, blank=True)
    warranty_information = models.TextField(blank=True)
    shipping_information = models.TextField(blank=True)
    availability_status = models.CharField(max_length=100, default='In stock')
    reviews = models.ManyToOneRel('Review', related_name='product', on_delete=models.CASCADE, to='stocks.Review',
                                  field_name='product')
    return_policy = models.TextField(blank=True)
    minimum_order_quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    meta = models.OneToOneField(Meta, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    @shared_task
    def burn_stock_task_now(self, quantity=None, reason=None):
        sleep(10)
        if quantity is None:
            self.quantity_in_stock  = 0
            self.save()
        return f"Burned {quantity} items from product {self.name} for reason: {reason}"

class StockMovement(models.Model):
    """
    Represents a stock movement (incoming or outgoing) of a product.
    Each line in the table represents a movement of a certain quantity of a product.
    """

    class MovementType(models.TextChoices):
        INCOMING = "in", "Incoming"
        OUTGOING = "out", "Outgoing"

    product = models.ForeignKey(Product,related_name="stock_movements",on_delete=models.CASCADE)
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
