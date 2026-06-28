from django.db import models


class SiteSetting(models.Model):

    company_name = models.CharField(
        max_length=100,
        default="YURÉA"
    )

    logo = models.ImageField(
        upload_to="settings/",
        blank=True,
        null=True
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30
    )

    address = models.TextField()

    facebook = models.URLField(
        blank=True
    )

    instagram = models.URLField(
        blank=True
    )

    telegram = models.URLField(
        blank=True
    )

    about = models.TextField()

    def __str__(self):
        return self.company_name