from modeltranslation.translator import TranslationOptions, register
from vippacet import models


@register(models.Vippacet)
class CustomUserTranslation(TranslationOptions):
    fields = ('name', 'title', 'description')
