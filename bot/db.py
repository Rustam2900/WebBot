from datetime import timedelta

from aiogram.types import Message
from django.utils import timezone

from asgiref.sync import sync_to_async

from account.models import CustomUser


@sync_to_async
def get_user_statistics():
    total_users = CustomUser.objects.count()

    time_24_hours_ago = timezone.now() - timedelta(days=1)
    new_users_24h = CustomUser.objects.filter(create_at__gte=time_24_hours_ago).count()

    time_1_month_ago = timezone.now() - timedelta(days=30)
    new_users_1_month = CustomUser.objects.filter(create_at__gte=time_1_month_ago).count()

    return {
        "total_users": total_users,
        "new_users_24h": new_users_24h,
        "new_users_1_month": new_users_1_month
    }


@sync_to_async
def get_all_users():
    return list(CustomUser.objects.all())


@sync_to_async
def save_user_telegram_info(user, message: Message, user_lang: str):
    if not user.telegram_id:
        user.telegram_id = message.from_user.id
        user.tg_username = message.from_user.username or "null"
        user.full_name = message.from_user.full_name or "null"
        user.user_lang = user_lang
        user.save()


@sync_to_async
def get_user_language(user_id):
    try:
        user = CustomUser.objects.get(telegram_id=user_id)
        return user.user_lang
    except CustomUser.DoesNotExist:
        return 'en'
