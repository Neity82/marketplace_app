import datetime
from typing import List, Dict

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractUser
from django.core.handlers.wsgi import WSGIRequest
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q, QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from product.models import Product, Category
from user.manager import CustomUserManager
from user.utils import avatar_directory_path


class CustomUser(AbstractUser):
    """
    Абстрактный базовый пользователь.

    Это в основном копия AbstractUser, но без поля username и расширено полями:
    - middle_name - отчество
    - phone - телефон
    - avatar - аватар пользователя
    """

    phone_regex = RegexValidator(
        regex=r"^\d{10}$",
        message=_('Invalid format')
    )

    username = None

    email = models.EmailField(
        verbose_name=_('email'),
        unique=True,
        help_text=_('User email')
    )
    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=150,
        blank=True,
        help_text=_('User first name')
    )
    middle_name = models.CharField(
        verbose_name=_('middle name'),
        max_length=150,
        blank=True,
        help_text=_('User middle name')
    )
    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=150,
        blank=True,
        help_text=_('User last name')
    )
    phone = models.CharField(
        verbose_name=_('phone'),
        validators=[phone_regex],
        help_text=_('User phone'),
        max_length=16,
        blank=True
    )
    avatar = models.ImageField(
        verbose_name=_('avatar'),
        help_text=_('User avatar'),
        blank=True,
        upload_to=avatar_directory_path
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def get_full_name(self) -> str:
        """Возвращает first_name, middle_name и last_name с пробелом между ними."""

        full_name = f'{self.last_name} {self.first_name} {self.middle_name}'
        return full_name.strip()

    @property
    def full_name(self) -> str:
        return self.get_full_name

    def __str__(self) -> str:
        first_name = getattr(self, "first_name")
        first_name = first_name[0] + '.' if first_name else ''
        middle_name = getattr(self, "middle_name")
        middle_name = middle_name[0] + '.' if middle_name else ''
        short_name = f'{getattr(self, "last_name")} {first_name}{middle_name}'
        return short_name

    @classmethod
    def login_new_user(cls, request: WSGIRequest, email: str, password: str) -> None:
        """
        аутентификация и авторизация пользователя
        :param request: реквест из вью
        :param email: электронная почта пользователя
        :param password: пароль пользователя
        :return: None
        """
        new_user = authenticate(
            email=email,
            password=password,
        )
        login(request, new_user)

    @staticmethod
    def parse_user_name(full_name: str) -> dict:
        """
        разделяем ФИО на части:
        ФИО -> last_name, first_name, middle_name
        ФИ -> last_name, first_name
        И -> first_name
        """
        user_name_data = {}
        if full_name:
            user_name_data_raw = full_name.split()
            user_name_data_raw_len = len(user_name_data_raw)
            if user_name_data_raw_len == 3:
                user_name_data.update(first_name=user_name_data_raw[1])
                user_name_data.update(last_name=user_name_data_raw[0])
                user_name_data.update(middle_name=user_name_data_raw[2])

            elif user_name_data_raw_len == 2:
                user_name_data.update(first_name=user_name_data_raw[1])
                user_name_data.update(last_name=user_name_data_raw[0])

            elif user_name_data_raw_len == 1:
                user_name_data.update(first_name=user_name_data_raw[0])

            elif user_name_data_raw_len > 3:
                user_name_data.update(last_name=user_name_data_raw[0])
                user_name_data.update(middle_name=user_name_data_raw[-1])
                user_name_data.update(first_name=" ".join(user_name_data_raw[1:-1]))
        else:
            user_name_data = full_name
        return user_name_data


class UserProductView(models.Model):
    """Модель просмотренных пользователем товаров"""

    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='user_view',
        help_text=_('The user who viewed the product')
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='product_view',
        help_text=_('Viewed product')
    )
    datetime = models.DateTimeField(
        auto_created=True,
        verbose_name=_('datetime of addition'),
        help_text=_('Viewing datetime')
    )

    class Meta:
        verbose_name = _('viewed product')
        verbose_name_plural = _('viewed products')
        ordering = ['-datetime']

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{self.product_id}'

    @classmethod
    def get_product_view(cls, user: CustomUser, limit: int = None) -> List['UserProductView']:
        """
        Метод получения списка просмотренных товаров

        :param user: Пользователь
        :type user: CustomUser
        :param limit: Необходимое количество просмотренных товаров
        :type limit: int
        :return: Список просмотренных товаров
        :rtype: List[UserProductView]
        """

        queryset: List[UserProductView] = UserProductView.objects.filter(
            user_id=user
        ).select_related(
            'product_id',
            'product_id__category'
        )
        return queryset[:limit]

    @classmethod
    def add_object(cls, user: CustomUser, product: int) -> (bool, str):
        """
        Добавляем товар в просмотренные если его там нет или
        обновляем дату просмотра

        :param user: Пользователь
        :type user: CustomUser
        :param product: id Товара
        :type product: int
        :return: результат добавления и сообщение
        :rtype: (bool, str)
        """

        result: bool = True
        message: str = _('successfully added')

        if user.is_authenticated:
            if UserProductView.objects.filter(
                    user_id=user, product_id=product
            ).exists():
                UserProductView.objects.filter(
                    user_id=user,
                    product_id=product
                ).update(
                    datetime=timezone.now()
                )

            else:
                UserProductView.objects.create(
                    user_id=user,
                    product_id=Product.objects.get(id=product),
                    datetime=timezone.now()
                )
        return result, message


class CompareEntity(models.Model):
    """Модель товара в сравнении"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='product_compare',
        help_text=_('Product for comparison')
    )

    compare = models.ForeignKey(
        'Compare',
        on_delete=models.CASCADE,
        related_name='compare_entity',
        verbose_name=_('compare\'s')
    )

    class Meta:
        verbose_name = _('compare entity')
        verbose_name_plural = _('compare entities')

    objects = models.Manager()

    def __str__(self) -> str:
        user = getattr(self.compare, 'user_id') if getattr(self.compare, 'user_id') else 'Unknown'
        return f'Compare entity: user {user}, product: {self.product}'


class Compare(models.Model):
    """Модель сравнения"""

    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='compare_user',
        help_text=_('Compare user'),
        blank=True,
        null=True
    )

    device = models.CharField(
        max_length=255,
        verbose_name=_('device'),
        help_text=_('cookie device value'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('compare')
        verbose_name_plural = _('compares')

    def __str__(self) -> str:
        user = getattr(self, 'user_id') if getattr(self, 'user_id') else 'Unknown'
        return f'Compare: user: {user}, device: {self.device}'

    objects = models.Manager()

    @classmethod
    def get_compare_list(cls, compare_id: 'Compare') -> QuerySet['CompareEntity']:
        """
        Список товаров для сравнения

        :param compare_id: Объект сравнения
        :type compare_id: Compare
        :return: Список товаров
        :rtype: List['CompareEntity']
        """

        result: QuerySet[CompareEntity] = CompareEntity.objects.filter(
            compare=compare_id
        )
        return result

    @classmethod
    def get_compare(cls, request: WSGIRequest) -> 'Compare':
        """
        Получаем объект сравнения из реквеста пользователя, проверяя cookie
        :param request: django wsgi реквест
        :type request: WSGIRequest
        :return: объект Сравнения
        :rtype: Compare
        """
        user = getattr(request, 'user', None)
        device = request.COOKIES.get('device', None)

        assert user, 'can\'t get user from request!'
        # assert device, 'no "device", check static!'

        if user.is_anonymous:
            instance = cls._get_anonymous_compare(device=device)
        else:
            instance = cls._get_user_compare(user=user, device=device)
        return instance

    @classmethod
    def _get_anonymous_compare(cls, device: str) -> 'Compare':
        """
        Получаем или создаем сравнение для анонимного пользователя

        :param device: Девайс пользователя
        :type device: str
        :return: объект Сравнения
        :rtype: Compare
        """

        instance = Compare.objects.filter(device=device).first()
        if instance is None:
            instance = Compare.objects.create(device=device)
        return instance

    @classmethod
    def _get_user_compare(cls, user: CustomUser, device: str) -> 'Compare':
        """
        Получаем или создаем сравнение для авторизованного пользователя

        :param user: Пользователь
        :type user: CustomUser
        :param device: Девайс пользователя
        :type device: str
        :return: объект Сравнения
        :rtype: Compare
        """
        instance = Compare.objects.filter(Q(user_id=user) | Q(device=device)).first()
        if instance is None:
            instance = Compare.objects.create(device=device, user_id=user)
        else:
            cls.update_instance(instance, device=device, user_id=user)
        return instance

    @staticmethod
    def update_instance(instance: 'Compare', **kwargs) -> None:
        """
        Обновляем объект сравнения из kwargs

        :param instance: объект Сравнения
        :type instance: Compare
        """

        updated: bool = False
        for attr, value in kwargs.items():
            if getattr(instance, attr) != value:
                setattr(instance, attr, value)
                updated = True
        if updated:
            instance.save()

    def add_to_compare(self, product_id: int) -> (bool, str):
        """
        Добавляем товар в сравнение если его там нет

        :param product_id: id Товара
        :type product_id: int
        :return: результат добавления и сообщение
        :rtype: (bool, str)
        """
        result: bool = True
        message: str = _('successfully added')

        count: int = CompareEntity.objects.filter(
                    compare_id=self.pk
                ).count()

        if count < 4:
            compare_entity = CompareEntity.objects.filter(
                compare=self.pk,
                product=product_id
            ).exists()

            if compare_entity is False:
                CompareEntity.objects.create(
                    compare_id=self.pk,
                    product_id=product_id
                )
            else:
                result: bool = False
                message: str = _('has already been added before')
        else:
            result = False
            message = _('maximum of products for comparison')

        return result, message

    def remove_from_compare(self, product_id: int) -> (bool, str):
        """
        Удаляем элемент сравнения

        :param product_id: id товара
        :return: - успех удаления, сообщение
        """

        result: bool = False
        message: str = _('failed to remove')

        compare_entity = CompareEntity.objects.filter(
            compare=self.pk,
            product=product_id
        )

        if compare_entity.exists():
            compare_entity.delete()
            result = True
            message = _('successfully removed')

        return result, message

    @classmethod
    def count(cls, compare_id: 'Compare') -> int:
        """
        Считаем количество товаров для сравнения

        :param compare_id: Сравнение
        :type compare_id: Compare
        :return: Количество товаров
        :rtype: int
        """

        result: int = CompareEntity.objects.filter(compare=compare_id).count()
        return result

    @classmethod
    def get_categories(cls, compare_id: 'Compare') -> Dict[Category, int]:
        """
        Получаем словарь, где ключ - объект Категория,
        значение - количество товаров в этой категории

        :param compare_id: Объект сhавнение
        :type compare_id: Compare
        :return: Словарь из объекта Категории и количества товаров в категории
        :rtype: Dict[Category, int]
        """
        compare_list: QuerySet[CompareEntity] = cls.get_compare_list(compare_id=compare_id)

        category_list = [Category.objects.get(pk=item.product.category_id)
                         for item in compare_list]
        categories = {}
        for item in set(category_list):
            categories[item] = compare_list.filter(product__category=item).count()
        return categories


