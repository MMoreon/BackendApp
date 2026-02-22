# FastAPI Blog Backend
Backend-приложение для блога с админскими CRUD-операциями, публичным API и системой управления пользователям

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
как и указано в ТЗ, основным фенкционалом умеет пользоваться только роль ADMIN, это можно понять по соотвествующему значку справа от эндпоинта

## Аутентификация и роли
Реализована регистрация с хешированием пароля
![](https://raw.githubusercontent.com/MMoreon/BackendApp/refs/heads/main/image/хешПароли.jpg)
так же реализованы токены и роли
