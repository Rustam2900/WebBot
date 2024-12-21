from datetime import timedelta
from django.utils import timezone

from asgiref.sync import sync_to_async
from django.db import IntegrityError

from account.models import CustomUser


@sync_to_async
def sync_save_user_language(user_id, user_lang):
    try:
        user, created = CustomUser.objects.get_or_create(
            telegram_id=user_id,
            defaults={'user_lang': user_lang}
        )

        if not created:
            if user.user_lang != user_lang:
                user.user_lang = user_lang
                user.save()

    except IntegrityError as e:
        print(f"IntegrityError: {e}")


async def save_user_language(user_id, user_lang):
    await sync_save_user_language(user_id, user_lang)


@sync_to_async
def save_user_info_to_db(user_data):
    try:
        new_user, created = CustomUser.objects.update_or_create(
            telegram_id=user_data['telegram_id'],
            defaults={
                "full_name": user_data['full_name'],
                "phone_number": user_data['phone_number'],
                "tg_username": user_data['tg_username'],
                "username": user_data['username']
            }
        )
        return new_user
    except IntegrityError:
        raise Exception("User already exists")


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
