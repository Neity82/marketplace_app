from order import models as order_models
from order.tests.test_cart import mixins as order_mixins
from order import utils as order_utils
from product import models as product_models
from shop import models as shop_models
from user import models as user_models


class CartModelTest(order_mixins.CartTestMixin):

    def test_get_anonymous_cart(self) -> None:
        user = self.response.wsgi_request.user
        cart = self.model.get_cart(user=user, device=self.device)
        self.assertTrue(cart.device == self.device)

    def test_get_user_cart(self) -> None:
        new_user = user_models.CustomUser.objects.create_user(**order_mixins.USER_DATA)
        self.client.login(**order_mixins.USER_DATA)
        response = self.client.get(self.base_url)
        self.assertTrue(response.status_code == 200)
        user = response.wsgi_request.user
        cart = self.model.get_cart(user=user, device=self.device)
        self.assertTrue(cart.device == self.device)
        self.assertTrue(cart.user_id == new_user)

    def test_add_to_cart(self) -> None:
        stock = self.get_random_stock()
        self.cart.add_to_cart(stock_id=stock.id)
        cart_stocks = product_models.Stock.objects.filter(cart_entity__cart=self.cart)
        self.assertTrue(stock in cart_stocks)

    def test_remove_from_cart(self) -> None:
        stock = self.get_random_stock()
        self.cart.remove_from_cart(stock_id=stock.id)
        cart_stocks = product_models.Stock.objects.filter(cart_entity__cart=self.cart)
        self.assertTrue(stock not in cart_stocks)

    def test_update_quantity_increase(self) -> None:
        increase_count = 2
        stock = product_models.Stock.objects.filter(count__gt=1).first()
        self.cart.add_to_cart(stock_id=stock.id)
        self.cart.update_quantity(stock_id=stock.id, quantity=increase_count)
        self.assertTrue(len(self.cart) == increase_count)
        cart_entity = order_models.CartEntity.objects.filter(
            cart=self.cart, stock=stock
        ).first()
        self.assertTrue(cart_entity.quantity == increase_count)

    def test_update_quantity_decrease(self) -> None:
        increase_count = 3
        decrease_count = 1
        stock = product_models.Stock.objects.filter(count__gt=1).first()
        self.cart.add_to_cart(stock_id=stock.id)
        self.cart.update_quantity(stock_id=stock.id, quantity=increase_count)
        self.cart.update_quantity(stock_id=stock.id, quantity=decrease_count)
        self.assertTrue(len(self.cart) == decrease_count)
        cart_entity = order_models.CartEntity.objects.filter(
            cart=self.cart, stock=stock
        ).first()
        self.assertTrue(cart_entity.quantity == decrease_count)

    def test_update_quantity_to_zero(self) -> None:
        increase_count = 3
        decrease_count = 0
        stock = product_models.Stock.objects.filter(count__gt=1).first()
        self.cart.add_to_cart(stock_id=stock.id)
        self.cart.update_quantity(stock_id=stock.id, quantity=increase_count)
        self.cart.update_quantity(stock_id=stock.id, quantity=decrease_count)
        self.assertTrue(len(self.cart) == decrease_count)
        cart_entity = order_models.CartEntity.objects.filter(
            cart=self.cart, stock=stock
        )
        self.assertTrue(not cart_entity)

    def test_change_shop_by_id_same_shop(self) -> None:
        stock = self.get_random_stock()
        shop = stock.shop
        self.cart.add_to_cart(stock_id=stock.id)
        result, message = self.cart.change_shop_by_id(
            stock_id=stock.id, shop_id=shop.id
        )
        self.assertTrue(result)
        self.assertTrue(message == order_utils.CHANGE_SHOP_CART_SAME_SHOP)

    def test_total_sums(self) -> None:
        old_sum = 0
        discount_sum = 0
        for _ in range(3):
            stock = self.get_random_stock()
            self.cart.add_to_cart(stock_id=stock.id)
            old_sum += stock.price
            if stock.product.discount:
                discount_sum += stock.product.discount.get("price")
            else:
                discount_sum += stock.price
        sums = self.cart.total_sums()
        self.assertTrue(old_sum == sums.get("old_sum"))

    def test_get_shops(self) -> None:
        for _ in range(5):
            stock = self.get_random_stock()
            self.cart.add_to_cart(stock_id=stock.id)
        shops_qs = shop_models.Shop.objects.filter(
            stock__cart_entity__cart=self.cart
        ).distinct()
        shops_set = self.cart.get_shops()
        self.assertTrue(len(shops_qs) == len(shops_set))
        for shop in shops_qs:
            self.assertTrue(shop in shops_set)
