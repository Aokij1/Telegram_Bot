import requests
import datetime


from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


bot = Bot(token ="6402243129:AAGhuer4__1z2ux0ijvkmXAjYUVqxbrkmeg")
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)


class Form(StatesGroup):
    day1 = State()
    day1_3h = State()
    day2 = State()


#После комманды старт появляются 3 кнопки, а также идёт приветсвие бота
@dp.message_handler(commands=["start"])
async def start_bot(message: types.Message):
    button_weather_today = KeyboardButton('Погода сегодня')
    greet_dx = ReplyKeyboardMarkup(resize_keyboard=True)
    button_3h = KeyboardButton("Через 3 часа")
    button_1day = KeyboardButton("Погода завтра")
    greet_dx.add(button_weather_today,button_3h, button_1day)
    await message.answer("Привет! \nЯ бот погоды!", reply_markup=greet_dx)

#Реагируем на кнопку "Погода сегодня", а также записывает сообщение пользователя
@dp.message_handler(lambda message: message.text == "Погода сегодня")
async def weather_today(message: types.Message):
    await message.answer('Скажи мне свой город')
    await Form.day1.set()

#После ввода города выполняется скрипт отправка и получение запроса, Данные которые нам нужны записываем в переменную, также идет фильтрация сообщений с выводом сообщения бота "Я вас не понимаю!"
@dp.message_handler(state=Form.day1)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer("Я вас не понимаю!")
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + message.text + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()
    info_weather = f"На данный момент в городе, {message.text}, {round(weather_data['main']['temp'])}°\n"
    info_weather += f"Ощущается как {round(weather_data['main']['feels_like'])}°\n"
    info_weather += f"В небе {weather_data['weather'][0]['description']}"
    await message.answer(info_weather)
    await state.finish()


#Реагируем на кнопку "Через 3 часа", а также записывает сообщение пользователя
@dp.message_handler(lambda message: message.text =="Через 3 часа")
async def weather_3h(message: types.Message):
    await message.answer('Скажи мне свой город')
    await Form.day1_3h.set()

#После ввода города выполняется скрипт отправка и получение запроса, Данные которые нам нужны записываем в переменную, также идет фильтрация сообщений с выводом сообщения бота "Я вас не понимаю!"
@dp.message_handler(state=Form.day1_3h)
async def weather_(message: types.Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer("Я вас не понимаю!")
    url_v2 = 'https://api.openweathermap.org/data/2.5/forecast?q=' + message.text + ',&units=metric&lang=ru&appid=afbcd143a2ff5250be99459f17a39a24'
    weather_data_v2 = requests.get(url_v2)
    data = weather_data_v2.json()
    time = datetime.datetime.now()
    number = (24 - time.hour - 1) // 3
    weather_data_3h = (data["list"][1])
    info_weather_3h = f"Через 3 часа в городе, {message.text}, {round(weather_data_3h['main']['temp'])}°\n"
    info_weather_3h += f"Ощущается как {round(weather_data_3h['main']['feels_like'])}°\n"
    info_weather_3h += f"В небе {weather_data_3h['weather'][0]['description']}"
    await message.answer(info_weather_3h)
    await state.finish()


#Реагируем на кнопку "Погода завтра", а также записывает сообщение пользователя
@dp.message_handler(lambda message: message.text == "Погода завтра")
async def weather_day2(message: types.Message):
    await message.answer('Скажи мне свой город')
    await Form.day2.set()

#После ввода города выполняется скрипт отправка и получение запроса, Данные которые нам нужны записываем в переменную, также идет фильтрация сообщений с выводом сообщения бота "Я вас не понимаю!"
@dp.message_handler(state=Form.day2)
async def weather_day2_2(message: types.Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer("Я вас не понимаю!")
    url_v2 = 'https://api.openweathermap.org/data/2.5/forecast?q=' + message.text + ',&units=metric&lang=ru&appid=afbcd143a2ff5250be99459f17a39a24'
    weather_data_v2 = requests.get(url_v2)
    data = weather_data_v2.json()
    time = datetime.datetime.now()
    number = (24 - time.hour - 1) // 3
    weather_data_2day = (data["list"][8])
    info_weather_2day = f"Завтра в городе, {message.text}, {round(weather_data_2day['main']['temp'])}°\n"
    info_weather_2day += f"Ощущается как {round(weather_data_2day['main']['feels_like'])}°\n"
    info_weather_2day += f"В небе {weather_data_2day['weather'][0]['description']}"
    await message.answer(info_weather_2day)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
