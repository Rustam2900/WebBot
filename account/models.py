from django.db import models
from django.utils.translation import gettext_lazy as _

from bot.validators import phone_number_validator


class CustomUser(models.Model):
    full_name = models.CharField(_("Full Name"), max_length=255, blank=True)
    username = models.CharField(_("Username"), max_length=255, blank=True, null=True)
    user_lang = models.CharField(max_length=10, blank=True, null=True)
    telegram_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    tg_username = models.CharField(_("Telegram Username"), max_length=255, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    my_money = models.DecimalField(max_digits=20, decimal_places=7, default=0.0)
    image = models.ImageField(upload_to='static/account/images', null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    referral_link = models.CharField(max_length=255, blank=True, null=True)
    team = models.ManyToManyField("self", blank=True, symmetrical=False)
    generate_id = models.CharField(max_length=10, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.full_name


class UserPackage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="packages")
    package = models.ForeignKey('account.VIPPackage', on_delete=models.CASCADE)
    active_until = models.DateTimeField()
    daily_income = models.DecimalField(max_digits=20, decimal_places=15,
                                       default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("User Package")
        verbose_name_plural = _("User Packages")

    def __str__(self):
        return f"{self.user.full_name} - {self.package.name}"


class VIPPackage(models.Model):
    image = models.ImageField(upload_to='static/vippacet/images', verbose_name="Paket Rasm")
    name = models.CharField(_("name"), max_length=100)
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"))
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Umumiy Narx")
    duration = models.PositiveIntegerField(verbose_name="Davomiyligi (kun)")
    daily_income = models.DecimalField(max_digits=20, decimal_places=15, verbose_name="Kunlik Daromad")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("VIP Paket")
        verbose_name_plural = _("VIP Paketlar")


class News(models.Model):
    image = models.ImageField(upload_to='static/news/images')
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"))
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_news", blank=True)
    daily_share = models.DecimalField(max_digits=20, decimal_places=15, default=0.0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
