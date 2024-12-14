from modeltranslation.translator import TranslationOptions, register
from account import models


@register(models.CustomUser)
class CustomUserTranslation(TranslationOptions):
    fields = ('full_name', 'username', 'bio')


@register(models.VIPPackage)
class VIPPackageTranslation(TranslationOptions):
    fields = ('name', 'title', 'description')


@register(models.News)
class NewsTranslation(TranslationOptions):
    fields = ('title', 'description')
