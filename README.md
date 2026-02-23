
# FastAPI Blog Backend
Backend-приложение для блога с админскими CRUD-операциями, публичным API и системой управления пользователям

## Для запуска приложения
создаем виртуальное окружение
* MAC: python3 -m venv venv
* WIN: python -m venv venv

активируем
* MAC: source venv/bin/activate
* WIN: venv\Scripts\activate

устанавливаем необходимые пакеты
* pip install -r req.txt

запустить
* uvicorn main:app --reload

## Для запуска контейнера
в директории проекта запустить
docker-compose up -d --build

## Документация
Для проверки ендпоинтов и работы приложения \n
http://localhost:8000/docs

## Технологический стек

- Python 3.12
- Фреймворк: FastAPI + Uvicorn
- БД: SQLite 
- ORM sqlalchemy==2.0.23
- Миграции alembic
- Валидация pydantic==2.11.0
- Аутентификация: JWT (access/refresh), пароли — bcrypt

## БД
Логическая модель
![Логическая модель](https://raw.githubusercontent.com/MMoreon/BackendApp/refs/heads/main/image/логическаяМодель.png)
Физическая модель
![Физическая модель](https://raw.githubusercontent.com/MMoreon/BackendApp/refs/heads/main/image/Физ.модельБД.jpg)

## СRUD в swagger
http://127.0.0.1:8000/docs
![](https://raw.githubusercontent.com/MMoreon/BackendApp/refs/heads/main/image/Руты.jpg)
как и указано в ТЗ, основным функционалом умеет пользоваться только роль ADMIN, это можно понять по соотвествующему значку справа от эндпоинта

## Аутентификация и роли
Реализована регистрация с хешированием пароля
![](https://raw.githubusercontent.com/MMoreon/BackendApp/refs/heads/main/image/хешПароли.jpg)
так же реализованы токены и роли
