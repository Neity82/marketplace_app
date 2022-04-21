from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

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

    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$",
                                 message=_('Invalid format'))

    username = None
    email = models.EmailField(verbose_name=_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    middle_name = models.CharField(_('middle name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    phone = models.CharField(verbose_name=_('phone'),
                             validators=[phone_regex],
                             max_length=16,
                             unique=True)
    avatar = models.ImageField(verbose_name=_('avatar'), blank=True, upload_to=avatar_directory_path)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        """
        Возвращает first_name, middle_name и last_name с пробелом между ними.
        """
        full_name = f'{self.last_name} {self.first_name} {self.middle_name}'
        return full_name.strip()




