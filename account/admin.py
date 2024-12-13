from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from account.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(TranslationAdmin):
    list_display = ('id', 'username', 'phone_number')
    list_display_links = ('id', 'username')
    search_fields = ('id', 'username', 'email')
