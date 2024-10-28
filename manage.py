from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from os import getenv
import asyncio
from aiogram.utils.formatting import Bold, as_list, as_marked_section, as_key_value
from parser.parser import parserJournal
from db.auth import registration, authorization

bot = Bot(token=getenv('TELEGRAM_ACCESS_TOKEN'))
dp = Dispatcher()


@dp.message(Command('start'))
async def startMessage(message: types.Message):
    await message.reply("Слушаю вас...")

@dp.message(Command('stats'))
async def stats(message: types.Message):
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
        Bold('Данные получены с https://journal.top-academy.ru/'),
        sep="\n\n",
    )

    await message.edit_text(**content.as_kwargs())

@dp.message(Command('auth'))
async def auth(message: types.Message):
    bot_message = await message.reply("Идёт регистрация..")
    if message.chat.type != "private":
        return await bot_message.edit_text("Для прохождение регистрации, перейдите в личные сообщение со мной!")

    try:
        response = await registration(message.from_user.id, message.text.split(' ')[1], message.text.split(' ')[2])
    except IndexError:
        return await bot_message.edit_text("Используйте команду как /auth {username} {password}"
                                   "\n\n"
                                   "username - ваш логин от журнала\npassword - ваш пароль от журнала"
                                   "\n\n"
                                   "Мы сохраняем политику кондефициальности")

    await bot_message.edit_text(response)

if __name__ == "__main__":
    print('System launch')
    asyncio.run(dp.start_polling(bot))