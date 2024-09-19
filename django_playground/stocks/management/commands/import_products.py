import requests
from django.core.management.base import BaseCommand

from django_playground.stocks.models import Product


class Command(BaseCommand):
    help = "Import products from dummyjson.com API"

    def handle(self, *args, **kwargs):
        url = "https://dummyjson.com/products?limit=300"
        response = requests.get(url)  # noqa: S113

        if response.status_code == 200:  # noqa: PLR2004
            products_data = response.json().get("products", [])

            for product_data in products_data:
                product, created = Product.objects.update_or_create(
                    sku=product_data["sku"],
                    defaults={
                        "title": product_data["title"],
                        "description": product_data["description"],
                        "category": product_data["category"],
                        "price": product_data["price"],
                        "discount_percentage": product_data["discountPercentage"],
                        "rating": product_data["rating"],
                        "stock": product_data["stock"],
                        "tags": product_data.get("tags", []),
                        "brand": product_data.get("brand", ""),
                        "weight": product_data["weight"],
                        "dimensions": product_data["dimensions"],
                        "warranty_information": product_data.get("warrantyInformation", ""),
                        "shipping_information": product_data.get("shippingInformation", ""),
                        "availability_status": product_data.get("availabilityStatus", ""),
                        "return_policy": product_data.get("returnPolicy", ""),
                        "minimum_order_quantity": product_data.get("minimumOrderQuantity", 1),
                        "meta": product_data["meta"],
                        "thumbnail": product_data.get("thumbnail", ""),
                        "images": product_data.get("images", []),
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created product: {product.title}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated product: {product.title}"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch products: {response.status_code}"))
