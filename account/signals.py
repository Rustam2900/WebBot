import random

from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.models import CustomUser


def generate_unique_id(instance):
    random_prefix = f"{random.randint(100, 999)}"
    if instance.pk:
        return f"{random_prefix}{instance.pk}"
    return random_prefix


@receiver(pre_save, sender=CustomUser)
def set_generate_id(sender, instance, **kwargs):
    if not instance.generate_id:
        instance.generate_id = generate_unique_id(instance)
