from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from account.models import CustomUser, VIPPackage, News, UserPackage, OrderMinSum, AddressMoney, VIPPackagePurchase


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'full_name', 'username', 'user_lang', 'telegram_id', 'tg_username', 'image', 'bio', 'referral_link',
            'team', 'generate_id', 'address_money', 'daily_income', 'created_at')}),  # 'vip_packages' olib tashlandi
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    readonly_fields = ('last_login', 'created_at', 'display_vip_packages')

    def display_vip_packages(self, obj):
        return ", ".join([str(package) for package in obj.vip_packages.all()])

    display_vip_packages.short_description = "VIP Packages"


@admin.register(VIPPackage)
class VIPPackageAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'duration')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'price')


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'daily_share', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'daily_share')


@admin.register(UserPackage)
class UserPackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'active_until', 'daily_income', 'created_at')
    list_display_links = ('id', 'daily_income')
    search_fields = ('id',)


@admin.register(OrderMinSum)
class OrderMinSumAdmin(admin.ModelAdmin):
    list_display = ('id', 'min_order_sum')
    list_display_links = ('id', 'min_order_sum')
    search_fields = ('id',)


@admin.register(AddressMoney)
class AddressMoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_address_money')
    list_display_links = ('id', 'telegram_address_money')
    search_fields = ('id',)


@admin.register(VIPPackagePurchase)
class VIPPackagePurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'package', 'start_date', 'end_date')  # To'g'ri atribut nomlari ishlatildi
    list_filter = ('start_date', 'end_date')  # To'g'ri atribut nomlari ishlatildi
    search_fields = ('user__email', 'package__name')  # To'g'ri atribut nomlari ishlatildi

