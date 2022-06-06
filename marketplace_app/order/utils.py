from django.utils.translation import gettext as _

ERROR_RESPONSE_TYPE = 'error'
SUCCESS_RESPONSE_TYPE = 'success'
WARNING_RESPONSE_TYPE = 'warning'

ADD_TO_CART_FAIL = _('failed to add')
ADD_TO_CART_SUCCESS = _('successfully added')

CHANGE_SHOP_CART_FAIL = _('failed to change shop')
CHANGE_SHOP_CART_SUCCESS = _('shop successfully changed')
CHANGE_SHOP_CART_SAME_SHOP = _('same shop')

REMOVE_FROM_CART_FAIL = _('failed to remove')
REMOVE_FROM_CART_SUCCESS = _('successfully removed')

UPDATE_CART_QUANTITY_FAIL = _('failed to change quantity')
UPDATE_CART_QUANTITY_SUCCESS = _('quantity changed to %s')
UPDATE_CART_QUANTITY_LIMIT_MERGED = _('product\'s quantity limit is exceeded while merge \n quantity set to %s')

WRONG_REQUEST = _('wrong request')
