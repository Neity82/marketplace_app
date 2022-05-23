from django.db import models
from django.utils.translation import gettext_lazy as _


class SEOItem(models.Model):
    path_name = models.CharField(_("path name"), max_length=512)
    meta_title = models.CharField(_("meta title"), max_length=512)
    meta_description = models.CharField(
        _("meta description"),
        max_length=512,
        blank=True,
    )
    title = models.CharField(
        _("meta description"),
        max_length=512,
        blank=True,
    )

    objects = models.Manager()

    class Meta:
        ordering = ('path_name',)
        verbose_name = _("SEO item")
        verbose_name_plural = _("SEO items")

    def __str__(self):
        return "{path_name}".format(
            path_name=self.path_name
        )
