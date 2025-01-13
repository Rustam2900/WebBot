from datetime import timedelta

from aiogram.types import Message
from django.utils import timezone

from asgiref.sync import sync_to_async
from django.db.models import Sum

from account.models import CustomUser, VIPPackage


@sync_to_async
def get_user_statistics():
    total_users = CustomUser.objects.count()

    time_24_hours_ago = timezone.now() - timedelta(days=1)
    new_users_24h = CustomUser.objects.filter(created_at__gte=time_24_hours_ago).count()

    time_1_month_ago = timezone.now() - timedelta(days=30)
    new_users_1_month = CustomUser.objects.filter(created_at__gte=time_1_month_ago).count()

    return {
        "total_users": total_users,
        "new_users_24h": new_users_24h,
        "new_users_1_month": new_users_1_month
    }


@sync_to_async
def get_user_money_statistics(user_id):
    time_24_hours_ago = timezone.now() - timedelta(days=1)

    time_1_month_ago = timezone.now() - timedelta(days=30)

    income_24h = \
        CustomUser.objects.filter(telegram_id=user_id, created_at__gte=time_24_hours_ago).aggregate(
            total_income=Sum('my_money'))[
            'total_income'] or 0
    income_1_month = \
        CustomUser.objects.filter(telegram_id=user_id, created_at__gte=time_1_month_ago).aggregate(
            total_income=Sum('my_money'))[
            'total_income'] or 0

    total_income = CustomUser.objects.filter(
        telegram_id=user_id
    ).aggregate(total_income=Sum('my_money'))['total_income'] or 0

    # total_vip_spent = VIPPackage.objects.filter(
    #     customuser__telegram_id=user_id
    # ).aggregate(total_spent=Sum('price'))['total_spent'] or 0

    return {
        "income_24h": income_24h,
        "income_1_month": income_1_month,
        "total_income": total_income,
        # "total_vip_spent": total_vip_spent,
    }


@sync_to_async
def get_all_users():
    return list(
        CustomUser.objects.filter(
            telegram_id__isnull=False,
        ).exclude(telegram_id='').exclude(telegram_id='0')
    )



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
