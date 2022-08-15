from django.db.models import ManyToManyField, Model
from product.models import Product, AttributeValue, Stock, Category, Tag
from product.tests.test_detail.mixins import (
    ProductDetailMixin,
    PRODUCT_DATA,
    USER_DATA,
    REVIEW_CNT,
)
from user.models import CustomUser


class ProductListTest(ProductDetailMixin):
    def test_get(self) -> None:
        for product_num in PRODUCT_DATA.keys():
            url = self.base_url + f"{product_num}/"
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, self.template_name)

    def test_info_content(self) -> None:
        for product_num, product_data in PRODUCT_DATA.items():
            url = self.base_url + f"{product_num}/"
            response = self.client.get(url)
            for attr, value in product_data["info"].items():
                if attr == "category":
                    category = Category.objects.get(id=value)
                    self.assertContains(response, category.title)
                elif attr == "tags":
                    for tag_id in value:
                        tag = Tag.objects.get(id=tag_id)
                        self.assertContains(response, tag.title)
                else:
                    self.assertContains(response, value)

    def test_attributes_content(self) -> None:
        for product_num, product_data in PRODUCT_DATA.items():
            url = self.base_url + f"{product_num}/"
            response = self.client.get(url)
            for attr, value in product_data["attributes"].items():
                self.assertContains(response, attr)
                self.assertContains(response, value)

    def _add_review(self, product, user, text="Test text for review", rating=4):
        url = self.base_url + f"{product.id}/"
        data_for_review = {
            "product": product,
            "user": user,
            "text": text,
            "rating": rating,
        }
        self.client.post(url, data=data_for_review)

    def test_review_add(self) -> None:
        new_user = CustomUser.objects.create_user(**USER_DATA)
        self.client.login(**USER_DATA)
        for product_id in PRODUCT_DATA.keys():
            product = Product.objects.get(id=product_id)
            for _ in range(REVIEW_CNT):
                self._add_review(product, new_user)

        for product_id in PRODUCT_DATA.keys():
            url = self.base_url + f"{product_id}/"
            response = self.client.get(url)
            self.assertContains(response, "Test text for review", count=REVIEW_CNT)
            self.assertContains(
                response,
                f"{USER_DATA['first_name']} {USER_DATA['last_name']}",
                count=REVIEW_CNT,
            )
            product = Product.objects.get(id=1)
            self.assertEqual(product.rating, 4)
