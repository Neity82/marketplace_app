from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _

from info.utils import banner_image_path


class Banner(models.Model):
    """Модель баннер"""

    title = models.CharField(
        verbose_name=_("title"),
        max_length=150,
        help_text=_('Banner title')
    )
    text = models.TextField(
        verbose_name=_("text"),
        help_text=_('Banner text')
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=banner_image_path,
        help_text=_('Banner image')
    )
    url = models.URLField(
        verbose_name=_("URL"),
        help_text=_('Banner url')
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        help_text=_('Banner is active')
    )

    class Meta:
        ordering = ('is_active',)
        verbose_name = _("banner")
        verbose_name_plural = _("banners")

    objects = models.Manager()

    def __str__(self) -> str:
        return "{title}".format(
            title=self.title
        )

    @classmethod
    def get_banners(cls, limit: int = 3) -> List['Banner']:
        """
        Получаем список случайных активных баннеров в размере limit

        :param limit: Необходимое колличество
        :type limit: int
        :return: Список баннеров
        :rtype: List[Banner]
        """
        queryset: List[Banner] = Banner.objects.filter(
            is_active=True
        ).order_by('?')
        return queryset[:limit]
