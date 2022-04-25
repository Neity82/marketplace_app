from django.db import models
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    name = models.CharField(_("name"), max_length=150)
    description = models.TextField(_("description"))
    image = models.ImageField(_("image"))
    address = models.CharField(_("address"), max_length=150)
    phone = models.CharField(_("phone"), max_length=12)
    mobile = models.CharField(_("mobile"), max_length=12)
    email_general = models.EmailField(_("general email"))
    email_editor = models.EmailField(_("editor email"))

    class Meta:
        ordering = ('name',)
        verbose_name = _("shop")
        verbose_name_plural = _("shops")

    def __str__(self):
        return "{name}".format(
            name=self.name
        )
