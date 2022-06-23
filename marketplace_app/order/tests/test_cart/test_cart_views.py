import random
import typing

from django.urls import reverse

from order import models as order_models
from order import utils as order_utils
from order.tests.test_cart.mixins import CartTestMixin, USER_DATA
from product import models as product_models
from user import models as user_models


class CartViewTest(CartTestMixin):
    url = order_utils.CART_URL_NAME
    template_name = "order/cart.html"

    def test_get(self) -> None:
        self.assertTrue(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, self.template_name)

    def test_empty_post(self) -> None:
        response = self.client.post(reverse(f"{self.app_name}:{self.url}"))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            self.get_response_type(response) == order_utils.WARNING_RESPONSE_TYPE
        )


class AnonymousCartCreationTest(CartTestMixin):
    url = f"/{order_utils.CART_URL_NAME}/"

    def test_cart_page(self):
        self.assertTrue(self.response.status_code == 200)

    def test_cart_create(self) -> None:
        self.assertTrue(self.cart is not None)

    def test_cart_empty(self) -> None:
        self.assertTrue(len(self.cart) == 0)


class AuthenticatedCartCreationTest(CartTestMixin):
    anonymous_cart_pk = None
    anonymous_cart_device = None

    def setUp(self) -> None:
        super().setUp()
        self.anonymous_cart_pk = self.cart.pk
        self.anonymous_cart_device = self.cart.device
        user_models.CustomUser.objects.create_user(**USER_DATA)
        self.client.login(**USER_DATA)
        response = self.client.get(self.base_url)
        self.assertTrue(response.status_code == 200)

    def test_same_cart_after_login(self):
        self.assertTrue(self.cart.pk == self.anonymous_cart_pk)

    def test_same_device_after_login(self):
        self.assertTrue(self.cart.device == self.anonymous_cart_device)


class AddToCartViewTest(CartTestMixin):
    url = order_utils.ADD_TO_CART_URL_NAME
    cart_count = 0

    def test_add_stock_to_cart(self) -> None:
        stock_id = self.get_random_stock_id()
        kwargs = {"pk": stock_id}
        response = self.client.post(
            reverse(f"{self.app_name}:{self.url}", kwargs=kwargs)
        )
        self.assertTrue(response.status_code == 200)
        if self.get_response_type(response) == order_utils.SUCCESS_RESPONSE_TYPE:
            self.cart_count += 1
        self.assertTrue(len(self.cart) == self.cart_count)

    def test_add_product_to_cart(self) -> None:
        product_id = self.get_random_product_id()
        data = {"pk": product_id, "is_product": True}
        response = self.client.post(
            reverse(f"{self.app_name}:{self.url}", args=(product_id,)), data=data
        )
        self.assertTrue(response.status_code == 200)
        if self.get_response_type(response) == order_utils.SUCCESS_RESPONSE_TYPE:
            self.cart_count += 1
        self.assertTrue(len(self.cart) == self.cart_count)

    def test_add_shop_product(self) -> None:
        stock_id = self.get_random_stock_id()
        data = {"shop_id": stock_id}
        response = self.client.post(
            reverse(f"{self.app_name}:{self.url}", kwargs={"pk": stock_id}), data=data
        )
        self.assertTrue(response.status_code == 200)
        if self.get_response_type(response) == order_utils.SUCCESS_RESPONSE_TYPE:
            self.cart_count += 1
        self.assertTrue(len(self.cart) == self.cart_count)

    def test_add_few_products(self) -> None:
        for _ in range(random.randint(1, 10)):
            stock_id = self.get_random_stock_id()
            kwargs = {"pk": stock_id}
            response = self.client.post(
                reverse(f"{self.app_name}:{self.url}", kwargs=kwargs)
            )
            self.assertTrue(response.status_code == 200)
            if self.get_response_type(response) == order_utils.SUCCESS_RESPONSE_TYPE:
                self.cart_count += 1
        self.assertTrue(len(self.cart) == self.cart_count)


class RemoveFromCartViewTest(CartTestMixin):
    url = order_utils.REMOVE_FROM_CART_URL_NAME
    cart_count = 0
    stock_ids = list()

    min_cart_count = 4
    max_cart_count = 10

    def setUp(self) -> None:
        super().setUp()
        for _ in range(random.randint(self.min_cart_count, self.max_cart_count)):
            stock_id = self.get_random_stock_id()
            self.stock_ids.append(stock_id)
            kwargs = {"pk": stock_id}
            response = self.client.post(
                reverse(
                    f"{self.app_name}:{order_utils.ADD_TO_CART_URL_NAME}", kwargs=kwargs
                )
            )
            if self.get_response_type(response) == order_utils.SUCCESS_RESPONSE_TYPE:
                self.cart_count += 1
            self.assertTrue(response.status_code == 200)

    def test_remove_from_cart(self):
        random_stock = self.random_choice(self.stock_ids)
        kwargs = {"pk": random_stock}
        response = self.client.delete(
            reverse(f"{self.app_name}:{self.url}", kwargs=kwargs)
        )
        self.assertTrue(response.status_code == 200)
        response_count = self.get_response_content(response).get("cart_count", None)
        self.assertTrue(len(self.cart) == response_count)

    def test_remove_few_from_cart(self):
        for i in range(1, self.min_cart_count + 1):
            stock_id = self.stock_ids[i]
            kwargs = {"pk": stock_id}
            response = self.client.delete(
                reverse(f"{self.app_name}:{self.url}", kwargs=kwargs)
            )
            self.assertTrue(response.status_code == 200)
            response_count = self.get_response_content(response).get("cart_count", None)
            self.assertTrue(len(self.cart) == response_count)

    def test_clean_cart(self):
        for stock_id in self.stock_ids:
            kwargs = {"pk": stock_id}
            response = self.client.delete(
                reverse(f"{self.app_name}:{self.url}", kwargs=kwargs)
            )
            self.assertTrue(response.status_code == 200)
            response_count = self.get_response_content(response).get("cart_count", None)
            self.assertTrue(len(self.cart) == response_count)
        self.assertTrue(len(self.cart) == 0)


class ChangeQuantityCartTest(CartTestMixin):
    url = order_utils.CART_URL_NAME
    cart_count = 0

    def add_to_cart(self, stock_id: typing.Union[str, int], **kwargs) -> None:
        url = order_utils.ADD_TO_CART_URL_NAME
        data = kwargs
        data.update(pk=stock_id)
        response = self.client.post(
            reverse(f"{self.app_name}:{url}", args=(stock_id,)),
            data,
        )
        self.assertTrue(response.status_code == 200)
        if self.get_response_type(response) == order_utils.SUCCESS_RESPONSE_TYPE:
            self.cart_count += 1
        self.assertTrue(len(self.cart) == self.cart_count)

    def test_increase_quantity(self) -> None:
        increase_count = 2
        stock_id = self.random_choice(
            product_models.Stock.objects.filter(count__gt=1).values_list(
                "id", flat=True
            )
        )
        self.add_to_cart(stock_id)
        data = {"stock_id": stock_id, "quantity": increase_count}
        response = self.client.post(reverse(f"{self.app_name}:{self.url}"), data=data)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            self.get_response_type(response) == order_utils.SUCCESS_RESPONSE_TYPE
        )
        self.cart_count += 1
        self.assertTrue(len(self.cart) == self.cart_count)

    def test_decrease_quantity(self) -> None:
        increase_count = 1
        stock_id = self.random_choice(
            product_models.Stock.objects.filter(count__gt=1).values_list(
                "id", flat=True
            )
        )
        [self.add_to_cart(stock_id) for _ in range(2)]

        data = {"stock_id": stock_id, "quantity": increase_count}
        response = self.client.post(reverse(f"{self.app_name}:{self.url}"), data=data)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            self.get_response_type(response) == order_utils.SUCCESS_RESPONSE_TYPE
        )
        self.cart_count -= 1
        self.assertTrue(len(self.cart) == self.cart_count)

    def test_zero_stock_quantity(self):
        stock_id = self.random_choice(
            product_models.Stock.objects.filter(count__gt=1).values_list(
                "id", flat=True
            )
        )
        self.add_to_cart(stock_id)
        data = {"stock_id": stock_id, "quantity": 0}
        response = self.client.post(reverse(f"{self.app_name}:{self.url}"), data=data)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            self.get_response_type(response) == order_utils.SUCCESS_RESPONSE_TYPE
        )
        self.cart_count -= 1
        self.assertTrue(len(self.cart) == self.cart_count)
        cart_entities = order_models.CartEntity.objects.filter(cart=self.cart)
        self.assertTrue(not cart_entities)

    def test_overflow_stock_quantity(self):
        stock = self.get_random_stock()
        self.add_to_cart(stock.id)
        data = {"stock_id": stock.id, "quantity": stock.count + 1}
        response = self.client.post(reverse(f"{self.app_name}:{self.url}"), data=data)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            self.get_response_type(response) == order_utils.WARNING_RESPONSE_TYPE
        )
        self.assertTrue(len(self.cart) == 1)
