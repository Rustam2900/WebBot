import logging

from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

from account.models import CustomUser, VIPPackage, AddressMoney
from bot.db import save_user_telegram_info, get_user_language, get_user_money_statistics
from bot.keyboards import get_languages, get_main_menu
from bot.states import UserStates, VIPPurchaseState

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


def update_user_language(user_id, user_lang):
    try:
        user_language = CustomUser.objects.get(telegram_id=user_id)
        user_language.user_lang = user_lang
        user_language.save()
        print(f"User language updated for {user_id} to {user_lang}")
    except CustomUser.DoesNotExist:
        CustomUser.objects.create(telegram_id=user_id, user_lang=user_lang)
        print(f"User created with language {user_lang} for {user_id}")


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


@router.message(F.text.in_(["Statistics", "Статистика"]))
async def show_statistics(message: Message):
    user_id = message.from_user.id
    user_lang = await get_user_language(user_id)
    user_stats = await get_user_money_statistics(user_id)

    statistics = (
        f"👤 <b>Statistika:</b>\n"
        f"💵 <b>{default_languages[user_lang]['user_balance_statistics']}:</b>\n"
        f"📅 {default_languages[user_lang]['earnings_24h']} <b>{user_stats['income_24h']} $</b>\n"
        f"📅 {default_languages[user_lang]['earnings_1_month']} <b>{user_stats['income_1_month']} $</b>\n"
        f"💰 {default_languages[user_lang]['total_earnings']} <b>{user_stats['total_income']} $</b>\n\n"

        f"🏦 <b>VIP packages:</b>\n"
        f"💎 {default_languages[user_lang]['total_spent_on_vip']}: <b>{user_stats['total_vip_spent']} $</b>\n"
    )

    try:
        await message.answer(text=statistics, parse_mode="HTML")
    except TelegramBadRequest as e:
        logging.error(f"Failed to send message to user {user_id}: {str(e)}")
        await message.answer("⚠️ Error.")


@router.message(F.text.in_(["deposit money", "вносить деньги"]))
async def show_vip_packages(message: Message):
    user_id = message.from_user.id
    user_lang = await get_user_language(user_id)

    vip_packages = await sync_to_async(list)(VIPPackage.objects.all())

    if not vip_packages:
        await message.answer(text=default_languages[user_lang]['not'])
        return

    inline_buttons = []
    for package in vip_packages:
        if user_lang == 'ru':
            button_text = f"{package.name_ru} - {package.price} $"
        else:
            button_text = f"{package.name_en} - {package.price} $"

        inline_buttons.append(
            [InlineKeyboardButton(text=button_text, callback_data=f"vip_{package.id}")]
        )
    inline_kb = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
    await message.answer(
        text=default_languages[user_lang]['vip_packege'],
        reply_markup=inline_kb
    )


@router.callback_query(F.data.startswith("vip_"))
async def show_vip_package_details(callback_query: CallbackQuery):
    package_id = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id
    user_lang = await get_user_language(user_id)

    try:
        package = await sync_to_async(VIPPackage.objects.get)(id=package_id)
    except VIPPackage.DoesNotExist:
        await callback_query.message.answer(text=default_languages[user_lang]['not'])
        return

    if user_lang == 'ru':
        caption_text = (
            f"<b>{package.name_ru}</b>\n\n"
            f"<b>{package.title_ru}</b>\n\n"
            f"{package.description_ru}\n\n"
            f"Цена: {package.price} $\n"
            f"Длительность: {package.duration} дней\n"
            f"Ежедневный доход: {package.daily_income} $"
        )
        button_text = "Купить пакет"
    else:
        caption_text = (
            f"<b>{package.name_en}</b>\n\n"
            f"<b>{package.title_en}</b>\n\n"
            f"{package.description_en}\n\n"
            f"price: {package.price} $\n"
            f"Duration: {package.duration} day\n"
            f"Daily income: {package.daily_income} $"
        )
        button_text = "Buy a package"

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=button_text, callback_data=f"buy_{package.id}")]]
    )

    await callback_query.message.answer(
        text=caption_text,
        reply_markup=inline_kb
    )
    await callback_query.answer()


@router.callback_query(F.data.startswith("buy_"))
async def start_vip_purchase(callback_query: CallbackQuery, state: FSMContext):
    package_id = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id
    user_lang = await get_user_language(user_id)
    await state.update_data(package_id=package_id)
    try:
        address = await sync_to_async(AddressMoney.objects.first)()
    except AddressMoney.DoesNotExist:
        await callback_query.message.answer(
            text=default_languages[user_lang]['not']
        )
        return

    if not address or not address.telegram_address_money:
        await callback_query.message.answer(
            text=default_languages[user_lang]['not']
        )
        return

    await callback_query.message.answer(
        text=
        f"{default_languages[user_lang]['wallet_address']}\n"
        f"{address.telegram_address_money}\n\n"
        f"{default_languages[user_lang]['receipt_request']}",

        parse_mode="Markdown"
    )

    await state.set_state(VIPPurchaseState.waiting_for_receipt)


@router.message(VIPPurchaseState.waiting_for_receipt)
async def handle_receipt_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = await get_user_language(user_id)
    data = await state.get_data()
    package_id = data.get('package_id')
    user = message.from_user
    package = await sync_to_async(VIPPackage.objects.get)(id=package_id)
    try:
        web_user = await sync_to_async(CustomUser.objects.get)(telegram_id=user.id)
    except CustomUser.DoesNotExist:
        await message.answer(text=default_languages[user_lang]['not'])
        return
    if not message.photo:
        await message.answer(text=default_languages[user_lang]['user_check_photo_error'])
        return

    photo = message.photo[-1]

    caption = (
        f"🆔 <b>User Telegram ID:</b> {user.id}\n"
        f"🆔 <b>User Web ID:</b> {web_user.generate_id}\n"
        f"👤 <b>User:</b> {user.full_name or user.username}\n"
        f"📦 <b>Paket ID:</b> {package_id}\n"
        f"📦 <b>Paket Name:</b> {package.name}\n"
        f"📦 <b>Paket price:</b> {package.price}\n"
        f"✅ <b>Chek yuborildi, iltimos tekshiring.</b>"
    )

    admin_channel_id = -1002330025759
    try:
        await message.bot.send_photo(
            chat_id=admin_channel_id,
            photo=photo.file_id,
            caption=caption,
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(text=default_languages[user_lang]['user_check_error'])
        print(f"Error sending photo to channel: {e}")
        return

    await message.answer(
        text=default_languages[user_lang]['user_check']
    )

    await state.clear()


@router.message(F.text.in_(["issuing money", "выпуск денег"]))
async def issuing_money(message: Message):
    pass
