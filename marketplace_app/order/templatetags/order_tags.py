from django import template

register = template.Library()


@register.simple_tag
def phone_normalize(phone: int) -> str:
    """
    Функция преобразует номер телефона
    Пример: 9991112233(int) -> +7(999) 111-22-33(str)

    :param phone: Номер телефона
    :type phone: int
    :return: Преобразованный номер телефона
    :rtype: str
    """

    phone: str = f"+7({phone[:3]}) {phone[3:6]}-{phone[6:8]}-{phone[8:]}"
    return phone
