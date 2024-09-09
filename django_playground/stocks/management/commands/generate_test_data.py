from django.core.management.base import BaseCommand

from django_playground.stocks.factories import CategoryFactory
from django_playground.stocks.factories import ProductFactory
from django_playground.stocks.factories import StockMovementFactory
from django_playground.stocks.factories import SupplierFactory


class Command(BaseCommand):
    help = "Generate bulk test data for stock management system"

    def handle(self, *args, **kwargs):
        CategoryFactory.create_batch(20)
        SupplierFactory.create_batch(60)
        ProductFactory.create_batch(300)
        StockMovementFactory.create_batch(10000)

        self.stdout.write(self.style.SUCCESS("Bulk test data generated successfully!"))
