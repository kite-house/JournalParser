from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.models import Base, User
from parser.parser import parserJournal
from cryptography.fernet import Fernet
from os import getenv
from datetime import datetime
import asyncio

engine = create_engine(
    url = f'mysql+pymysql://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}:{getenv("DB_PORT")}/{getenv("DB_NAME")}',
    echo = False
)

session = Session(engine, future = True)
fernet = Fernet(getenv('CRYPTO_KEY'))

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


async def registration(id: int, username:str, password:str):
    response = await asyncio.create_task(parserJournal(username, password))

    if type(response) == dict:
        if session.query(User).filter(User.telegram_id == id).first():
            session.query(User).filter(User.telegram_id == id).update({
                    'username': username, 
                    'password': fernet.encrypt(bytes(password, 'utf-8'))
                    }
                )
            session.commit()
            return 'Данные успешно обновленны!'
        else:
            user = User(telegram_id = id, 
                        username = username, 
                        password = fernet.encrypt(bytes(password, 'utf-8')),
                        date_created = datetime.now().date()
                        )
            session.add(user)
            session.commit()

    else:
        return 'Некоректный логин или пароль!'
    
    return 'Регистрация прошла успешно!'


def authorization(id):
    username, password = session.query(User.username, User.password).filter(User.telegram_id == id).first()
    return username, str(fernet.decrypt(password), 'utf-8')