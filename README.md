##ДЗ: https://github.com/netology-code/py-homeworks-web/tree/new/2.3-aiohttp<br/>
Для запуска требуется:
1. docker-compose up
запуск контейнеров

2. передавать запросы к апи (можно запустить файл client.py)
Описание
Код
Описание БД в файле db.py - по сравнению с дз по Flask используется AsyncSession, и другая строка подключения (через асинхронный провайдер) Описание таблиц осталось без изменений.
Логика записана в файле server.py
Валидация осталась без изменений, записана в файле schema.py
Докеризация
Сделан докер контейнер с python и запуском файла server.py, с прокидыванием порта 8080 на 8080
В файле docker-compose два контейнера: постгре и свой, постгре прокинут с 5432 на 5431
после запуска docker-compose можно либо отправлять запросы, описанные в client.py, либо потом посмотреть по адресу: http://localhost:8080/users/1/
