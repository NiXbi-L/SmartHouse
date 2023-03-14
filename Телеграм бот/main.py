import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.send_media_group import SendMediaGroup

import cfg

form_router = Router()
bot = Bot(token=cfg.telegramAPI_TOKEN, parse_mode="HTML")
timers = {}
class Form(StatesGroup):
    main = State()
    tea = State()
    tea_time = State()
    tea_time_set = State()
    cloth = State()
@form_router.message(Command("start"))
async def command_start(message: types.message, state: FSMContext) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
        text="Чаеварка",
        callback_data="tea"),
        types.InlineKeyboardButton(
            text="Шторы",
            callback_data="cloth")
    )
    await state.set_state(Form.main)
    await message.answer('Выберите устройство',reply_markup= builder.as_markup())
@form_router.message(Form.tea_time)
async def City(message: Message, state: FSMContext) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Назад",
            callback_data="Back1"),
        types.InlineKeyboardButton(
            text="Добавить таймер",
            callback_data="Set" )
    )
    await bot.delete_message(message_id=message.message_id - 1,
                                chat_id=message.chat.id)
    await bot.delete_message(message_id=message.message_id,
                                chat_id=message.chat.id)
    await bot.edit_message_text(message_id=message.message_id-2,
                                chat_id=message.chat.id,
                                text="Отложеная заварка:\nдд-мм-гг чч:мм",
                                reply_markup=builder.as_markup())
    await state.set_state(Form.tea)
@form_router.callback_query(Form.tea)
async def callback_query_handler(call: types.CallbackQuery, state: FSMContext) -> any:
    if call.data == 'time':
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="Back1"),
            types.InlineKeyboardButton(
                text="Добавить таймер",
                callback_data="Set")
        )
        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text="Отложеная заварка:\nдд-мм-гг чч:мм",
                                    reply_markup=builder.as_markup())
    elif call.data == 'Back1':
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Заварить чай",
                callback_data="tea"),
            types.InlineKeyboardButton(
                text="Отложеная заварка",
                callback_data="time")
        )
        builder.row(
            types.InlineKeyboardButton(
                text="Настроить",
                callback_data="setings"),
            types.InlineKeyboardButton(
                text="Вернуться назад",
                callback_data="back")
        )
        await state.set_state(Form.tea)
        await bot.edit_message_text(message_id=call.message.message_id
                                    , chat_id=call.message.chat.id
                                    , text="Чаеварка:\n"
                                           "ID: XXXXXXXX\n"
                                           "Состояние: Готов к работе/Нет воды/нет сахара/Нет заварки"
                                           "/Нет кружки/Работает/Заберите кружку\n"
                                           "Сахар: X г.\n"
                                           "Заварка: X г.\n"
                                           "Вода: X л.\n"
                                    , reply_markup=builder.as_markup())
    elif call.data == 'back':
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Чаеварка",
                callback_data="tea"),
            types.InlineKeyboardButton(
                text="Шторы",
                callback_data="cloth")
        )
        await state.set_state(Form.main)
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Чаеварка",
                callback_data="tea"),
            types.InlineKeyboardButton(
                text="Шторы",
                callback_data="cloth")
        )
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text='Выберите устройство',
                                    reply_markup=builder.as_markup())
@form_router.callback_query(Form.main)
async def callback_query_handler(call: types.CallbackQuery, state: FSMContext) -> any:
    if call.data == 'tea':
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
            text="Заварить чай",
            callback_data="tea"),
            types.InlineKeyboardButton(
                text="Отложеная заварка",
                callback_data="time")
        )
        builder.row(
            types.InlineKeyboardButton(
                text="Настроить",
                callback_data="setings"),
            types.InlineKeyboardButton(
                text="Вернуться назад",
                callback_data="back")
        )
        await state.set_state(Form.tea)
        await bot.edit_message_text(message_id=call.message.message_id
                                    ,chat_id=call.message.chat.id
                                    ,text="Чаеварка:\n"
                                          "ID: XXXXXXXX\n"
                                          "Состояние: Готов к работе/Нет воды/нет сахара/Нет заварки"
                                          "/Нет кружки/Работает/Заберите кружку\n"
                                          "Сахар: X г.\n"
                                          "Заварка: X г.\n"
                                          "Вода: X л.\n"
                                    ,reply_markup=builder.as_markup())
    elif call.data == "cloth":
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Задвинуть/Раздвинуть",
                callback_data="tea"),
            types.InlineKeyboardButton(
                text="Настройка",
                callback_data="time")
        )
        builder.row(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="back")
        )
        await state.set_state(Form.cloth)
        await bot.edit_message_text(message_id=call.message.message_id
                                    ,chat_id=call.message.chat.id
                                    ,text="Автошторы:\n"
                                          "ID: XXXXXXXX\n"
                                          "Состояние: Готов к работе/Ошибка работы"
                                    ,reply_markup=builder.as_markup())
@form_router.callback_query(Form.cloth)
async def callback_query_handler(call: types.CallbackQuery, state: FSMContext) -> any:
        if call.data == "back":
            builder = InlineKeyboardBuilder()
            builder.add(
                types.InlineKeyboardButton(
                    text="Чаеварка",
                    callback_data="tea"),
                types.InlineKeyboardButton(
                    text="Шторы",
                    callback_data="cloth")
            )
            await state.set_state(Form.main)
            builder = InlineKeyboardBuilder()
            builder.add(
                types.InlineKeyboardButton(
                    text="Чаеварка",
                    callback_data="tea"),
                types.InlineKeyboardButton(
                    text="Шторы",
                    callback_data="cloth")
            )
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text='Выберите устройство',
                                        reply_markup=builder.as_markup())
async def main():
    bot = Bot(token=cfg.telegramAPI_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())