from aiogram import Dispatcher, types
from aiogram.filters.command import Command
import asyncio
from aiogram.utils.formatting import Bold, as_list, as_marked_section, as_key_value
from parser.parser import parserJournal, parserSchedule, URL
from db.auth import registration, authorization
from src.anti_spam import timeout

dp = Dispatcher()


@dp.message(Command('start'))
async def startMessage(message: types.Message):
    await message.reply("Слушаю вас...")


@dp.message(Command('stats'))
async def stats(message: types.Message):
    if timeout(message.from_user.id) == False:
        return await message.reply('Слишком часто!')
    
    try:
        username, password = authorization(message.from_user.id)
    except TypeError:
        return await message.reply("Вы не зарегестрированы! Используйте команду /auth {username} {password}")

    message = await message.reply("Формируем данные...")
    response = await asyncio.create_task(parserJournal(username, password))

    if type(response) != dict:
        return await message.edit_text(f"Возникла ошибка\n> {response}")

    content = as_list(
        Bold(f'Статистика - {response["name"]}'),
        as_key_value('Группа', response['group']),
        as_marked_section(
            Bold('Успеваемость'),
            as_key_value('Средный балл', response['avg_rating']),
            as_key_value('Посещаемость', response['avg_attendance']),
        ),
        as_marked_section(
            Bold('Домашнее задание'),
            as_key_value("Выполнено", response['homework_done']),
            as_key_value("Просроченно", response['homework_overdue']),
            as_key_value("Текущие", response['homework_current']),
            as_key_value("На проверке", response['homework_verification'])
        ),

        as_marked_section(
            Bold('Рейтинг'),
            as_key_value('Место в группе', response['place_group']),
            as_key_value('Место в потоке', response['place_flow']),
        ),
        Bold(f'Данные получены с {URL}'),
        sep="\n\n",
    )

    await message.edit_text(**content.as_kwargs())


@dp.message(Command('schedule'))
async def schedule(message: types.Message):
    if timeout(message.from_user.id) == False:
        return await message.reply('Слишком часто!')

    try:
        username, password = authorization(message.from_user.id)
    except TypeError:
        return await message.reply("Вы не зарегестрированы! Используйте команду /auth {username} {password}")

    message = await message.reply("Формируем данные...")

    response = await asyncio.create_task(parserSchedule(username, password))

    if not response:
        return await message.reply("На сегодня расписание пустое!") 

    content = as_list(
        as_marked_section(
            Bold('Расписание'),
            f'{"\n".join(f'\n{str(key)}\n • {"\n • ".join(list(value.values()))}' for key, value in response.items())}',
            marker=''
        ),
        Bold(f'Данные получены с {URL}'),
        sep="\n\n",
    )
    await message.edit_text(**content.as_kwargs())

@dp.message(Command('auth'))
async def auth(message: types.Message):
    if message.chat.type != "private":
        return await message.reply("Для прохождение регистрации, перейдите в личные сообщение со мной!")

    id, username, password = message.from_user.id, *message.text.split(' ')[1:3]
    message = await message.reply("Идёт регистрация..")

    try:
        response = await registration(id, username, password)
    except IndexError:
        return await message.edit_text("Используйте команду как /auth {username} {password}"
                                       "\n\n"
                                       "username - ваш логин от журнала\npassword - ваш пароль от журнала"
                                       "\n\n"
                                       "Мы сохраняем политику кондефициальности")

    await message.edit_text(response)
