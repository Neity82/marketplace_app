from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from product.models import Product
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

    def get_full_name(self) -> str:
        """Возвращает first_name, middle_name и last_name с пробелом между ними."""

        full_name = f'{self.last_name} {self.first_name} {self.middle_name}'
        return full_name.strip()

    def __str__(self) -> str:
        first_name = getattr(self, "first_name")
        first_name = first_name[0] + '.' if first_name else ''
        middle_name = getattr(self, "middle_name")
        middle_name = middle_name[0] if middle_name else ''
        short_name = f'{getattr(self, "last_name")} {first_name}{middle_name}'
        return short_name


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
        auto_now_add=True,
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
    def get_product_view(cls, user, limit: int = None):
        """Метод получения списка просмотренных товаров"""

        queryset = UserProductView.objects.filter(
            user_id=user
        ).select_related(
            'product_id',
            'product_id__category'
        )
        return queryset[:limit]


class Compare(models.Model):
    """Модель товаров для сравнения"""

    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='user_compare',
        help_text=_('A user who compares products')
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='product_compare',
        help_text=_('Product for comparison')
    )

    class Meta:
        verbose_name = _('Compare')
        verbose_name_plural = _('Compares')

    def __str__(self):
        return f'{self.product_id}'

    objects = models.Manager()
