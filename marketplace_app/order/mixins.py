from django.core.handlers.wsgi import WSGIRequest
from django.views import View

from order.models import Cart
from order.utils import SUCCESS_RESPONSE_TYPE, WARNING_RESPONSE_TYPE
from product.models import Stock
from user.models import CustomUser


def cart_init_data(request: WSGIRequest) -> dict:
    """
    Обертка для получения пользователя и устройства из реквеста
    :param request: wsgi реквест django
    :return: dict[user, device]
    """
    user = getattr(request, "user", None)
    device = request.COOKIES.get("device", None)
    assert user, "can't get user from request!"
    return {
        'user': user,
        'device': device
    }


class CartMixin(View):
    """Миксин корзины"""

    cart = None
    model = Cart

    user_model = CustomUser
    cart_model = Cart
    stock_model = Stock

    template_name = "order/cart.html"

    def get_cart(self) -> Cart:
        """Получение объекта корзины из реквеста пользователя"""
        return self.cart_model.get_cart(**cart_init_data(self.request))

    def get_cart_pk(self) -> int:
        """Получение id объекта корзины"""
        cart = self.get_cart()
        return getattr(cart, "id", None)

    def get_stock(self, pk: int) -> Stock:
        """Получение объекта 'Складской единицы' по id"""
        return self.stock_model.objects.filter(id=pk).first()

    @staticmethod
    def success_type_mapping(success: bool) -> str:
        """Отдаем нужный тип ответа, исходя из переменной success"""
        return SUCCESS_RESPONSE_TYPE if success else WARNING_RESPONSE_TYPE

    def prepare_response_data(self, success: bool, message: str, **kwargs) -> dict:
        """Подготавливаем данные респонса для фронта"""
        response_type = self.success_type_mapping(success=success)
        response_data = {
            "type": response_type,
            "message": message,
        }
        for k, v in kwargs.items():
            response_data.update({k: v})
        return response_data
