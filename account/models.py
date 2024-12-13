from django.db import models
from django.utils.translation import gettext_lazy as _

from bot.validators import phone_number_validator


class CustomUser(models.Model):
    full_name = models.CharField(_("full name"), blank=True, max_length=255)
    username = models.CharField(_("username"), blank=True, max_length=255, null=True)
    phone_number = models.CharField(blank=True, unique=True, validators=[phone_number_validator],
                                    max_length=20)
    user_lang = models.CharField(blank=True, null=True, max_length=10)
    telegram_id = models.CharField(blank=True, null=True, max_length=255, unique=True)
    tg_username = models.CharField(_("telegram username"), blank=True, null=True, max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    my_money = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True, max_length=50)
    image = models.ImageField(upload_to='static/account/images', null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.full_name
