import json
import os
import random
import typing
import uuid

from http.cookies import SimpleCookie
from django.http import HttpResponse
from django.test import TestCase

from order import models as order_models
from order import utils as order_utils
from product import models as product_models

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_FIXTURE_DIR = os.path.join(CURRENT_DIR, "fixtures")

FIXTURES = [
    os.path.join(TEST_FIXTURE_DIR, "test_discount.json"),
    os.path.join(TEST_FIXTURE_DIR, "test_users.json"),
    os.path.join(TEST_FIXTURE_DIR, "test_shop.json"),
    os.path.join(TEST_FIXTURE_DIR, "test_product.json"),
    os.path.join(TEST_FIXTURE_DIR, "test_orders.json"),
    os.path.join(TEST_FIXTURE_DIR, "test_attribute.json"),
]

USER_DATA = {"email": "test_django@test.com", "password": "Zaq123456wsx"}


class CartTestMixin(TestCase):
    app_name = "order"
    base_url = f"/{order_utils.CART_URL_NAME}/"
    fixtures = FIXTURES

    model = order_models.Cart
    device = None
    template_name = None
    url = None

    def setUp(self) -> None:
        self.client.logout()
        self.set_device()
        self.add_device_cookie()
        self.init_cart(self.base_url)

    def add_device_cookie(self) -> None:
        self.client.cookies = SimpleCookie({"device": self.device})

    def init_cart(self, init_url: str) -> None:
        self.response = self.client.get(init_url)
        self.cart = self.model.objects.filter(device=self.device).first()

    def set_device(self) -> None:
        self.device = str(uuid.uuid4())

    @staticmethod
    def random_choice(values: list) -> typing.Any:
        return random.choice(values)

    def get_random_stock(self) -> product_models.Stock:
        return self.random_choice(product_models.Stock.objects.all())

    def get_random_stock_id(self) -> int:
        return self.random_choice(
            product_models.Stock.objects.all().values_list("id", flat=True)
        )

    def get_random_product_id(self) -> int:
        return self.random_choice(
            product_models.Product.objects.filter(stock__isnull=False).values_list(
                "id", flat=True
            )
        )

    @staticmethod
    def get_response_content(response: HttpResponse) -> dict:
        content_raw = getattr(response, "content", None)
        content = {}
        if content_raw:
            content = json.loads(content_raw)
        return content

    def get_response_type(self, response: HttpResponse) -> str:
        content = self.get_response_content(response)
        return content.get("type", None)
