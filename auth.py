from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, User
from parser import parserJournal
from os import getenv
import asyncio

engine = create_engine(
    url = f'mysql://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}:{getenv("DB_PORT")}/{getenv("DB_NAME")}',
    echo = False
)

session = Session(engine, future = True)
Base.metadata.create_all(engine)


async def registration(id: int, username:str, password:str):
    result = asyncio.create_task(parserJournal(username, password))
    await result
    result = result.result()
    if type(result) == dict:
        if session.query(User).filter(User.telegram_id == id).first():
            session.query(User).filter(User.telegram_id == id).update({'username': username, 'password': password})
            session.commit()
            return 'Данные успешно обновленны!'
        else:
            user = User(telegram_id = id, username = username, password = password)
            session.add(user)
            session.commit()

    else:
        return 'Некоректный логин или пароль!'
    
    
    return 'Регистрация прошла успешно!'


def authorization(id):
    return session.query(User.username, User.password).filter(User.telegram_id == id).first()