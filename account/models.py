from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(_('Full Name'), max_length=255, blank=True)
    username = models.CharField(_('Username'), max_length=255, blank=True, null=True)
    user_lang = models.CharField(max_length=10, blank=True, null=True)
    telegram_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    tg_username = models.CharField(_('Telegram Username'), max_length=255, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    my_money = models.DecimalField(max_digits=20, decimal_places=7, default=0.0)
    image = models.ImageField(upload_to='staticfiles/account/images', null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    email = models.EmailField(_('Email Address'), unique=True)
    referral_link = models.CharField(max_length=255, blank=True, null=True)
    team = models.ManyToManyField('self', blank=True, symmetrical=False)
    generate_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    vip_packages = models.ManyToManyField(
        'account.VIPPackage', through='VIPPackagePurchase', related_name='users', blank=True
    )
    address_money = models.CharField(max_length=100, null=True, blank=True, unique=True)
    daily_income = models.DecimalField(max_digits=20, decimal_places=7, default=0.0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def get_referral_url(self):
        domain = ''
        return f"https://{domain}/register?ref={self.referral_link}"

    def save(self, *args, **kwargs):
        if not self.referral_link:
            self.referral_link = str(uuid4())
        super().save(*args, **kwargs)

    def calculate_daily_income(self):
        """
        Foydalanuvchining VIP paketlari asosida kunlik daromadini hisoblab qaytaradi va yangilaydi.
        """
        total_income = sum(
            purchase.package.daily_income_vip
            for purchase in VIPPackagePurchase.objects.filter(user=self)
        )
        self.daily_income = total_income
        self.save(update_fields=['daily_income'])
        return total_income

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email


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
    image = models.ImageField(upload_to='staticfiles/vippacet/images', verbose_name="Paket Rasm")
    name = models.CharField(_("name"), max_length=100)
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"))
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Umumiy Narx")
    duration = models.PositiveIntegerField(verbose_name="Davomiyligi (kun)")
    daily_income_vip = models.DecimalField(max_digits=20, decimal_places=15, verbose_name="Kunlik Daromad")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("VIP Paket")
        verbose_name_plural = _("VIP Paketlar")


class News(models.Model):
    image = models.ImageField(upload_to='staticfiles/news/images')
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"))
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_news", blank=True)
    daily_share = models.DecimalField(max_digits=20, decimal_places=15, default=0.0)

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

    def toggle_like(self, user):
        if self.likes.filter(id=user.id).exists():
            self.likes.remove(user)
        else:
            self.likes.add(user)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")


class OrderMinSum(models.Model):
    min_order_sum = models.DecimalField(max_digits=20, decimal_places=7, default=0.0)

    class Meta:
        verbose_name = "Order minimum sum"
        verbose_name_plural = "Order minimum sum"


class AddressMoney(models.Model):
    telegram_address_money = models.CharField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.telegram_address_money


class VIPPackagePurchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package = models.ForeignKey(VIPPackage, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=self.package.duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.package.name}"

    class Meta:
        verbose_name = _('VIP Paket Xaridi')
        verbose_name_plural = _('VIP Paket Xaridlari')
