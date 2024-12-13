from modeltranslation.translator import TranslationOptions, register
from account import models


@register(models.CustomUser)
class CustomUserTranslation(TranslationOptions):
    fields = ('full_name', 'username', 'bio')
