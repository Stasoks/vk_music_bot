import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from yoomoney import Quickpay
from yoomoney import Client
import uuid
from config import *
import sqlite3
from utils import *
import requests
from aiogram.enums.parse_mode import ParseMode

connection = sqlite3.connect('Users.db')

client = Client(YOOMONEY_TOKEN)
BOT_TOKEN = ''
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
cursor = connection.cursor()

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота


# Инициализация бота и диспетчера\
dp = Dispatcher()

# Приветственное сообщение
START_MESSAGE = (
    "Приветствую, мы занимаемся подключением официальной подписки на сервис «Музыка Вконтакте» по очень низкой цене.\n"
    "Наш канал: @subscribevkmusic\n"
    "Поддержка: @subscribevkmusicsupport"
)

# Описание услуги
DESCRIPTION = (
    "Важно!!!\n"
    "Подключение подписки происходит без входа в ваш аккаунт, логин и пароль не нужен.\n\n"
    "Наша подписка работает только на номерах Российской Федерации ( +7 )\n\n"
    "Никаких списаний, деактиваций, и прочих манипуляций ожидать не стоит, мы работаем уже достаточно долго.\n\n"
    "Гарантия на продукт - 12 месяцев с даты покупки подписки.\n\n"
    "<a href=\"https://t.me/+FXM61kjzGpUwYTg1\">Инструкция</a>\n"
    "<a href=\"https://t.me/subscribevkmusicsupport\">Поддержка</a>"
)

# Главное меню
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Купить подписку")],
        [KeyboardButton(text="Инструкция, Вопрос/Ответ")],
        [KeyboardButton(text="Поддержка")]
    ],
    resize_keyboard=True
)

check_payment_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Проверить оплату")],
              [KeyboardButton(text="Назад в меню")]],
    resize_keyboard=True
)
# Меню оплаты
payment_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оплата Банковской картой")],
        [KeyboardButton(text="Оплата по СБП")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@dp.message(CommandStart())
async def send_welcome(message: types.Message):

    user_id = message.from_user.id
    username = message.from_user.username

    if user_exist(user_id) == False:
        cursor.execute("INSERT INTO Users (Id, Username, Transactions) VALUES (?, ?, ?)",(user_id, username, 0))
        connection.commit()
        await bot.send_message(chat_id=ADMIN_ID, text=f'{username} присоединился к боту')

    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://sun1-83.userapi.com/impg/v-uP8GBS10j9-dw2Uw6zUrnYLQOFN_5wDpy6FA/zqYeeemOphc.jpg?size=1280x695&quality=96&sign=896bfaeb97cd36c4047c6125484d8279&type=album",
        caption=START_MESSAGE,
        reply_markup=menu_keyboard
    )

# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: types.Message):
    text = message.text

    if text == "Купить подписку":
        await message.answer(DESCRIPTION, reply_markup=payment_keyboard)
    elif text == "Инструкция, Вопрос/Ответ":
        await message.answer("Пожалуйста, ознакомьтесь с инструкцией по ссылке: https://t.me/+FXM61kjzGpUwYTg1")
    elif text == "Поддержка":
        await message.answer("Свяжитесь с нашей поддержкой: @subscribevkmusicsupport")
    elif text in ["Оплата по СБП"]:
        userid = message.from_user.id
        cursor.execute("SELECT Transactions FROM Users WHERE Id = ?", (userid,))
        transactions = cursor.fetchone()[0]

        order_id = str(userid) + '_' + str(transactions)
        payment_url = create_payment_link(order_id)
        click_to_pay_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить", url=f"{payment_url}")] 
    ])
        await message.answer('Оплатите подписку, нажав на кнопку ниже', reply_markup=click_to_pay_keyboard)
        await message.answer('Когда совершите оплату, проверьте ее, нажав кнопку в нижней панели действий.\r\nЕсли оплата была проведена успешно - бот отправит вам ссылку на товар.', reply_markup=check_payment_keyboard)


    elif text == "Оплата Банковской картой":
        userid = message.from_user.id
        cursor.execute("SELECT Transactions FROM Users WHERE Id = ?", (userid,))
        transactions = cursor.fetchone()[0]

        payment = Quickpay(receiver=YOOMONEY_WALLET, 
                   quickpay_form='shop',
                   targets='ВК', 
                   paymentType='SB', 
                   sum = AMOUNT, 
                   label = f"{str(message.from_user.id) + '_' + str(transactions)}")
        
        click_to_pay_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить", url=f"{payment.base_url}")] 
    ])
        await message.answer('Оплатите подписку, нажав на кнопку ниже', reply_markup=click_to_pay_keyboard)
        await message.answer('Когда совершите оплату, проверьте ее, нажав кнопку в нижней панели действий.\r\nЕсли оплата была проведена успешно - бот отправит вам ссылку на товар.', reply_markup=check_payment_keyboard)

    elif text == "Проверить оплату":

        userid = message.from_user.id
        cursor.execute("SELECT Transactions FROM Users WHERE Id = ?", (userid,))
        transactions = cursor.fetchone()[0]
        label = str(userid) + '_' + str(transactions)

        if check_payment(label) or check_payment_status(label) == 'paid':
            await message.answer(f'Отлично, оплата прошла, вот ваша ссылка на товар: <a href="{LINK}">ссылка на товар</a>', parse_mode=ParseMode.HTML)
            await bot.send_message(chat_id=ADMIN_ID, text = f'{message.from_user.username} приобрел подписку')

            cursor.execute("UPDATE Users SET Transactions = ? WHERE id = ?",(transactions+1, userid))
            connection.commit()
        else:    
            await message.answer("Пожалуйста, иди нахуй")
            
    elif text == "Назад в меню":
        await message.answer("Меню", reply_markup=menu_keyboard)

    else:
        await message.answer("Пожалуйста, выберите одну из доступных опций.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
