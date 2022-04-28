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
        regex=r"^\+?1?\d{8,15}$",
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
        help_text=_('User first name')
    )
    middle_name = models.CharField(
        verbose_name=_('middle name'),
        max_length=150,
        help_text=_('User middle name')
    )
    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=150,
        help_text=_('User last name')
    )
    phone = models.CharField(
        verbose_name=_('phone'),
        validators=[phone_regex],
        help_text=_('User phone'),
        max_length=16,
        unique=True)
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
        verbose_name = _('view')
        verbose_name_plural = _('views')
        ordering = ['-datetime']

    def __str__(self) -> str:
        return f'{self.product_id}'


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

    def __str__(self) -> str:
        return f'{self.product_id}'
