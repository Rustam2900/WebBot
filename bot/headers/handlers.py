from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async

from account.models import CustomUser
from bot.db import save_user_telegram_info, get_user_language
from bot.keyboards import get_languages, get_main_menu
from bot.states import UserStates

from bot.utils import default_languages, introduction_template, user_languages
from django.conf import settings
from aiogram.client.default import DefaultBotProperties

router = Router()
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message(CommandStart())
async def welcome(message: Message):
    user_id = message.from_user.id

    user = await CustomUser.objects.filter(telegram_id=user_id).afirst()

    if user and user.user_lang:
        main_menu_markup = get_main_menu(user.user_lang)
        await message.answer(
            text=introduction_template[user.user_lang],
            reply_markup=main_menu_markup,
            parse_mode="HTML"
        )
    else:
        msg = default_languages['welcome_message']
        await message.answer(text=msg, reply_markup=get_languages(), parse_mode="HTML")


@router.callback_query(lambda call: call.data.startswith("lang"))
async def get_query_languages(call: CallbackQuery, state: FSMContext):
    user_lang = call.data.split("_")[1]
    await state.update_data(user_lang=user_lang)

    await bot.answer_callback_query(call.id)
    await state.set_state(UserStates.ID)

    text = default_languages[user_lang]['ID']
    await call.message.answer(text, reply_markup=None)


@router.message(UserStates.ID)
async def reg_user_contact(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data()
    user_lang = user_data.get("user_lang")

    input_id = message.text.strip()
    user = await CustomUser.objects.filter(generate_id=input_id).afirst()
    if user:
        if user.telegram_id:
            if user.telegram_id == user_id:
                full_name = user.full_name if user.full_name else message.from_user.username
                text = f"Hello or Привет, {full_name}!"
                await message.answer(text=text, reply_markup=get_main_menu(user_lang), parse_mode="HTML")
                await state.clear()
            else:
                error_text = default_languages[user_lang]['already_linked']
                await message.answer(text=error_text, reply_markup=None, parse_mode="HTML")
        else:
            await save_user_telegram_info(user, message, user_lang)
            full_name = user.full_name if user.full_name else message.from_user.username
            text = f"Hello or Привет, {full_name}!"
            await message.answer(text=text, reply_markup=get_main_menu(user_lang), parse_mode="HTML")
            await state.clear()
    else:
        error_text = default_languages[user_lang]['invalid_id']
        await message.answer(text=error_text, reply_markup=None, parse_mode="HTML")


@router.message(F.text.in_(["⚙️ Настройки", "⚙️ Settings"]))
async def settings(message: Message):
    user_id = message.from_user.id
    user_lang = await get_user_language(user_id)
    await message.answer(text=default_languages[user_lang]['select_language'], reply_markup=get_languages("setLang"))


@router.callback_query(F.data.startswith("setLang"))
async def change_language(call: CallbackQuery):
    user_id = call.from_user.id
    user_lang = call.data.split("_")[1]
    user_languages[call.from_user.id] = user_lang

    await sync_to_async(update_user_language)(user_id, user_lang)

    await call.message.answer(
        text=default_languages[user_lang]['successful_changed'],
        reply_markup=get_main_menu(user_lang)
    )


def update_user_language(user_id, user_lang):
    try:
        user_language = CustomUser.objects.get(telegram_id=user_id)

        if user_lang == 'ru':
            user_language.user_lang = 'en'
        else:
            user_language.user_lang = user_lang

        user_language.save()
    except CustomUser.DoesNotExist:
        CustomUser.objects.create(telegram_id=user_id, user_lang=user_lang)
