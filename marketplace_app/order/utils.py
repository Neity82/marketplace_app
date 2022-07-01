import logging
import typing
from inspect import signature

from django.db import connection
from django.utils.translation import gettext as _


CART_URL_NAME = "cart"
ADD_TO_CART_URL_NAME = "add-to-cart"
REMOVE_FROM_CART_URL_NAME = "remove-from-cart"

ADD_TO_CART_SHOP_URL_NAME = "add-to-cart-shop"
ADD_TO_CART_CNT_URL_NAME = "add-to-cart-cnt"

ERROR_RESPONSE_TYPE = "error"
SUCCESS_RESPONSE_TYPE = "success"
WARNING_RESPONSE_TYPE = "warning"

ADD_TO_CART_FAIL = _("failed to add")
ADD_TO_CART_SUCCESS = _("successfully added")

CHANGE_SHOP_CART_FAIL = _("failed to change shop")
CHANGE_SHOP_CART_SUCCESS = _("shop successfully changed")
CHANGE_SHOP_CART_SAME_SHOP = _("same shop")

REMOVE_FROM_CART_FAIL = _("failed to remove")
REMOVE_FROM_CART_SUCCESS = _("successfully removed")

UPDATE_CART_QUANTITY_FAIL = _("failed to change quantity")
UPDATE_CART_QUANTITY_SUCCESS = _("quantity changed to %s")
UPDATE_CART_QUANTITY_LIMIT_MERGED = _(
    "product's quantity limit is exceeded while merge \n quantity set to %s"
)

WRONG_REQUEST = _("wrong request")

logger = logging.getLogger(__name__)


def get_func_sign(func: typing.Callable) -> typing.Any:
    """Получаем тип возвращаемых данных из аннотаций функции"""
    try:
        sig = signature(func)
        return sig.return_annotation
    except Exception as exc:
        logger.error(f"check func's {func.__name__} annotation!", exc)


def db_table_exists(table_name: str) -> typing.Callable:
    """
    Хук для аннотации объектов еще несуществующих таблиц
    проверяем, существует ли таблица:
     - таблица существует: возвращаем вызов переданной функции
     - таблицы не существует: возвращаем пустой объект аннотации функции
    :param table_name:
    :return:
    """

    def decorator(func: typing.Callable) -> typing.Callable:
        def wrapper(*args, **kwargs) -> typing.Any:
            if table_name in connection.introspection.table_names():
                return func(*args, **kwargs)
            else:
                return_type = get_func_sign(func)
                if return_type is not None:
                    return return_type()

        return wrapper

    return decorator
