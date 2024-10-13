from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from os import getenv
import asyncio
from aiogram.utils.formatting import Bold, as_list, as_marked_section, as_key_value
from parser import parserJournal
from auth import registration, authorization

bot = Bot(token=getenv('TELEGRAM_ACCESS_TOKEN'))
dp = Dispatcher()


@dp.message(Command('start'))
async def startMessage(message: types.Message):
    await message.reply("че хотел?")

@dp.message(Command('stats'))
async def stats(message: types.Message):
    data = authorization(message.from_user.id)
    if data == None:
        await message.reply("Вы не зарегестрированы! Используйте команду /auth {username} {password}")
        return 
    result = asyncio.create_task(parserJournal(data[0], data[1]))
    await result
    result = result.result()
    try: 
        content = as_list(
            Bold(f'Статистика - {result["name"]}'),
            as_key_value('Группа', result['group']),
            as_marked_section(
                Bold('Успеваемость'),
                as_key_value('Средный балл', result['avg_rating']),
                as_key_value('Посещаемость', result['avg_attendance']),
            ),
            as_marked_section(
                Bold('Домашнее задание'),
                as_key_value("Выполнено", result['homework']['done']),
                as_key_value("Просроченно", result['homework']['overdue']),
                as_key_value("Текущие", result['homework']['current']),
                as_key_value("На проверке", result['homework']['verification'])
            ),

            as_marked_section(
            Bold('Рейтинг'),
            as_key_value('Место в группе', result['place_group']),
            as_key_value('Место в потоке', result['place_flow']),
            ),
            Bold('Данные получены с https://journal.top-academy.ru/'),
            sep="\n\n",
        )
    except Exception as error:
        await message.reply("Возникла ошибка :(")
    else:
        await message.reply(**content.as_kwargs())

@dp.message(Command('auth'))
async def auth(message: types.Message):
    if message.chat.type != "private":
        await message.reply("Для прохождение регистрации, перейдите в личные сообщение со мной!")
        return
    try:
        response = await registration(message.from_user.id, message.text.split(' ')[1], message.text.split(' ')[2])
    except Exception as error:
        print(error)
        if type(error) == IndexError:
            await message.reply("Используйте команду как /auth {username} {password}\n\nusername - ваш логин от журнала\npassword - ваш пароль от журнала\n\nМы сохраняем политику кондефициальности")
        else:
            await message.reply("Неизвестная ошибка!")
    else:
        await message.reply(response)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))