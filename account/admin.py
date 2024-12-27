from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from account.models import CustomUser, VIPPackage, News, UserPackage, OrderMinSum, AddressMoney


@admin.register(CustomUser)
class CustomUserAdmin(TranslationAdmin):
    list_display = ('id', 'username', 'my_money', 'user_lang', 'generate_id')
    list_display_links = ('id', 'username', 'generate_id')
    search_fields = ('id', 'username', 'email', 'generate_id')


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
