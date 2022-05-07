from django.db import models
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    name = models.CharField(_("name"), max_length=150)
    description = models.TextField(_("description"), blank=True)
    image = models.ImageField(_("image"), null=True, upload_to='shop_images/')
    address = models.CharField(_("address"), max_length=150, blank=True)
    phone = models.CharField(_("phone"), max_length=12, blank=True)
    mobile = models.CharField(_("mobile"), max_length=12, blank=True)
    email_general = models.EmailField(_("general email"), blank=True)
    email_editor = models.EmailField(_("editor email"), blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _("shop")
        verbose_name_plural = _("shops")

    def __str__(self):
        return "{name}".format(
            name=self.name
        )
