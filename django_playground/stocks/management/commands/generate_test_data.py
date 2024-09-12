from django.core.management.base import BaseCommand

from django_playground.stocks.factories import CategoryFactory
from django_playground.stocks.factories import ProductFactory
from django_playground.stocks.factories import StockMovementFactory
from django_playground.stocks.factories import SupplierFactory
from django_playground.stocks.models import Category


class Command(BaseCommand):
    help = "Generate bulk test data for stock management system"

    def add_arguments(self, parser):
        parser.add_argument(
            "--init",
            action="store_true",
            help="Initialize only if no data exists in the Category table",
        )

    def handle(self, *args, **kwargs):
        init = kwargs["init"]

        if init and Category.objects.exists():
            self.stdout.write(self.style.WARNING("Data already exists in the Category table. Initialization skipped."))
            return

        CategoryFactory.create_batch(20)
        SupplierFactory.create_batch(60)
        ProductFactory.create_batch(300)
        StockMovementFactory.create_batch(10000)

        self.stdout.write(self.style.SUCCESS("Bulk test data generated successfully!"))
