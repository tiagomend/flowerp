from django.test import TestCase

from product.models import (
    UnitOfMeasure,
    ProductCategory,
    Product,
    ItemTypeForSped
)

class UnitOfMeasureTest(TestCase):
    def setUp(self) -> None:
        self.uom = UnitOfMeasure.objects.create(
            name='Unit',
            abbreviation='UN'
        )

    def test_uom_name(self):
        self.assertEqual(self.uom.name, 'Unit')

    def test_uom_abbreviation(self):
        self.assertEqual(self.uom.abbreviation, 'UN')


class ProductCategoryTest(TestCase):
    def setUp(self) -> None:
        self.category = ProductCategory.objects.create(
            name='Category',
            description='Description of category'
        )

    def test_product_category_name(self):
        self.assertEqual(self.category.name, 'Category')

    def test_product_category_description(self):
        self.assertEqual(self.category.description, 'Description of category')


class ProductTest(TestCase):
    def setUp(self) -> None:
        self.uom = UnitOfMeasure.objects.create(
            name='Unit',
            abbreviation='UN'
        )

        self.item_type = ItemTypeForSped.objects.create(
            code=1,
            description='Raw Material'
        )

        self.category = ProductCategory.objects.create(
            name='Category',
            description='Description of category'
        )

        self.product = Product.objects.create(
            sku_code='2435',
            name='Product Any',
            unit_of_measure=self.uom,
            item_type_for_sped=self.item_type,
            price_cost=78.90
        )

        self.product.categories.add(self.category)

    def test_product_uom(self):
        self.assertEqual(self.product.unit_of_measure, self.uom)
