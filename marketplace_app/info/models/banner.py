from django.db import models
from django.utils.translation import gettext_lazy as _


class Banner(models.Model):
    title = models.CharField(_("title"), max_length=150)
    text = models.TextField(_("text"))
    image = models.ImageField(_("image"))
    url = models.URLField(_("URL"))
    is_active = models.BooleanField(_("active"))

    class Meta:
        ordering = ('is_active', 'title')
        verbose_name = _("banner")
        verbose_name_plural = _("banners")

    def __str__(self):
        return "{title}".format(
            title=self.title
        )
