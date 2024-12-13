from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from vippacet.models import Vippacet


@admin.register(Vippacet)
class CustomUserAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'duration')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'price')
