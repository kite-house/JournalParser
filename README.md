# JournalParser #RU
[EN](https://github.com/kite-house/JournalParser?tab=readme-ov-file#JournalParser-eng)

> [!IMPORTANT]
> Парсер журнала колледжа, и отправка данных в телеграмм конкретному пользователю.

### Как установить?
> pip install requirements.txt

> Создайте .env

```
TELEGRAM_ACCESS_TOKEN = "Токен телеграмм бота"
DB_USER = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = ""
DB_NAME = ""
CRYPTO_KEY = "Ключ для шифрование"
```

### Описание

Парсер журнала, отправляющий зарегистририванным пользователем - статистику их обучение. 

### Как работает? 

> При вызове команды /stats, пользователя просят авторизоваться для получение доступа к его журналу.

> После перехода в личные сообщение и вызова /auth {username} {password}, мы проверяем корректны ли данные, если да то отправляем статус запроса, и сохраняем в базу данных.
 
> После регистрации, команда /stats становится доступной, при её вызове мы получаем нужные данные из БД, и парсер данные с сайта. 

### Доступные командыы

> [!TIP]
> /start - Вывод привественного сообщения.

> [!TIP]
> /auth {username} {password} - Регистрация польователя в боте, сохранение его авторизицонных данных от сайта в бд.

> [!TIP]
> /stats - Вывод статистики.



# JournalParser #ENG
[EN](https://github.com/kite-house/JournalParser?tab=readme-ov-file#JournalParser-ru)

> [!IMPORTANT]
> College journal parser, and sending data in telegrams to a specific user.

### How to install?
> pip install requirements.txt

> Create .env

```
TELEGRAM_ACCESS_TOKEN = "Bot telegram token"
DB_USER = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = ""
DB_NAME = ""
CRYPTO_KEY = ""Key for encryption"
```

### Description

A log parser that sends registered user statistics to their training. 

### How does it work? 

> When calling the /stats command, the user is asked to log in to access his log.

> After going to a private message and calling /auth {username} {password}, we check whether the data is correct, if so, we send the status of the request, and save it to the database.
 
> After registration, the /stats command becomes available, when we call it, we get the necessary data from the database, and the parser data from the site. 

### Available commands

> [!TIP]
> /start - Output of the original message.

> [!TIP]
> /auth {username} {password} - Registration of the user in the bot, saving his authorization data from the site in the database.

> [!TIP]
> /stats - Statistics output.

