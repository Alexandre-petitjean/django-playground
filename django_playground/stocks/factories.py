import factory
from faker import Faker

from .models import Category
from .models import Product
from .models import StockMovement
from .models import Supplier

fake = Faker("fr_FR")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: fake.unique.word())
    description = factory.LazyAttribute(lambda _: fake.text())


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.LazyAttribute(lambda _: fake.unique.word())
    contact_person = factory.LazyAttribute(lambda _: fake.name())
    phone = factory.LazyAttribute(lambda _: fake.phone_number())
    email = factory.LazyAttribute(lambda _: fake.email())
    address = factory.LazyAttribute(lambda _: fake.address())


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: fake.unique.word())
    category = factory.LazyFunction(lambda: Category.objects.order_by("?").first())
    supplier = factory.LazyFunction(lambda: Supplier.objects.order_by("?").first())
    description = factory.LazyAttribute(lambda _: fake.text())
    quantity_in_stock = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=100))
    price = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=3, right_digits=2, positive=True))
    reorder_threshold = factory.LazyAttribute(lambda _: fake.random_int(min=5, max=20))
    auto_reorder = factory.LazyAttribute(lambda _: fake.boolean())


class StockMovementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockMovement

    product = factory.LazyFunction(lambda: Product.objects.order_by("?").first())
    movement_type = factory.Iterator(["in", "out"])
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=50))
    description = factory.LazyAttribute(lambda _: fake.sentence())
    date = factory.LazyAttribute(lambda _: fake.date_time_this_year())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        try:
            return super()._create(model_class, *args, **kwargs)
        except ValueError:
            return None
