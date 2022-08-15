from django.db.models import Q, ManyToManyField, Model
from product.models import Product, AttributeValue, Stock
from product.tests.test_detail.mixins import ProductDetailMixin, PRODUCT_DATA


class ProductListTest(ProductDetailMixin):
    def test_product_info(self) -> None:
        for product_num, product_data in PRODUCT_DATA.items():
            product_data_db = Product.objects.get(id=product_num)
            for attr, value in product_data["info"].items():
                data_for_check = getattr(product_data_db, attr)
                if isinstance(data_for_check, str):
                    self.assertEqual(data_for_check, value)
                elif isinstance(data_for_check, Model):
                    self.assertEqual(data_for_check.id, value)
                elif isinstance(data_for_check, ManyToManyField):
                    list_of_tags = [tag.id for tag in data_for_check.tags.all()]
                    self.assertEqual(list_of_tags, [1, 2, 3])

    def test_product_attributes(self) -> None:
        for product_num, product_data in PRODUCT_DATA.items():
            attribute_data = AttributeValue.objects.filter(product__id=product_num)
            self.assertEqual(len(attribute_data), 24)

            attributes_list = [
                (item.attribute.title.capitalize(), str(item.value))
                for item in attribute_data
            ]
            for attr_title, attr_value in product_data["attributes"].items():
                self.assertTrue(
                    (attr_title.capitalize(), str(attr_value)) in attributes_list
                )

    def test_product_in_shop(self) -> None:
        for product_num, product_data in PRODUCT_DATA.items():
            stocks = Stock.objects.filter(product__id=product_num)

            self.assertEqual(len(stocks), len(product_data["shop"]))
            stock_list = [(stock.shop.name, str(stock.price)) for stock in stocks]
            for shop_data in product_data["shop"]:
                self.assertTrue(shop_data in stock_list)
