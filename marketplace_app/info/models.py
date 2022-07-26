from typing import List
from django.db import models
from django.utils.translation import gettext_lazy as _

from info.utils import banner_image_path


class Banner(models.Model):
    """Модель баннер"""

    title = models.CharField(
        verbose_name=_("title"), max_length=150, help_text=_("banner title")
    )

    text = models.TextField(verbose_name=_("text"), help_text=_("banner text"))

    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=banner_image_path,
        help_text=_("banner image"),
    )

    url = models.URLField(verbose_name=_("URL"), help_text=_("banner url"))

    is_active = models.BooleanField(
        verbose_name=_("active"), help_text=_("banner is active")
    )

    class Meta:
        ordering = ("is_active",)
        verbose_name = _("banner")
        verbose_name_plural = _("banners")

    objects = models.Manager()

    def __str__(self) -> str:
        return "{title}".format(title=self.title)

    @classmethod
    def get_banners(cls, limit: int = 3) -> List["Banner"]:
        """
        Получаем список случайных активных баннеров в размере limit

        :param limit: Необходимое колличество
        :type limit: int
        :return: Список баннеров
        :rtype: List[Banner]
        """
        queryset: List[Banner] = Banner.objects.filter(is_active=True).order_by("?")
        return queryset[:limit]


class SEOItem(models.Model):
    """Модель переопределения обозначений url"""

    path_name = models.CharField(verbose_name=_("path name"), max_length=512)

    meta_title = models.CharField(
        verbose_name=_("meta title"),
        max_length=512,
        help_text=_(
            "for detail pages (products, shop etc) after meta title"
            "auto adding name (title) field of detail page"
        ),
    )

    meta_description = models.CharField(
        _("meta description"),
        max_length=512,
        blank=True,
        help_text=_(
            "for detail pages (products, shop etc)"
            "after meta description"
            "auto adding description field of detail page"
        ),
    )

    title = models.CharField(
        _("meta description"),
        max_length=512,
        blank=True,
    )

    objects = models.Manager()

    class Meta:
        ordering = ("path_name",)
        verbose_name = _("SEO item")
        verbose_name_plural = _("SEO items")

    def __str__(self):
        return "{path_name}".format(path_name=self.path_name)


class Settings(models.Model):
    """Модель хранения настроек проекта"""

    name = models.CharField(verbose_name=_("name"), max_length=50, unique=True)

    description = models.CharField(verbose_name=_("description"), max_length=250)

    value = models.CharField(verbose_name=_("value"), max_length=150)

    class Meta:
        ordering = ("description",)
        verbose_name = _("settings")
        verbose_name_plural = _("settings")

    def __str__(self):
        return "{descr} ({name})".format(name=self.name, descr=self.description)
