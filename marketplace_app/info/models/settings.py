from django.db import models
from django.utils.translation import gettext_lazy as _


class Settings(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    description = models.CharField(_("description"), max_length=250)
    value = models.CharField(_("value"), max_length=150)

    class Meta:
        ordering = ('description',)
        verbose_name = _("settings")
        verbose_name_plural = _("settings")

    def __str__(self):
        return "{descr} ({name})".format(
            name=self.name,
            descr=self.description
        )
