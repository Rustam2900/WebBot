from django.core.exceptions import ValidationError


def validate_gmail_email(value):
    """
    Email adresining oxiri @gmail.com bilan tugashini tekshiradi.
    """
    if not value.endswith('@gmail.com'):
        raise ValidationError(
            "Email manzili faqat @gmail.com bilan tugashi kerak.",
            params={'value': value},
        )
