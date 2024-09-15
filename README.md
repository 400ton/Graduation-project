# Personal Diary — Web Application
___
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

**Personal Diary** — это веб-приложение для ведения личного дневника с возможностью публикации записей, просмотра статистики, модерации контента и управления записями. Приложение выполнено в минималистичном, скандинавском стиле с использованием современных технологий, таких как Django и Bootstrap, для создания адаптивного и приятного интерфейса.

## Основные возможности:

- Создание личных записей.
- Модерация записей перед публикацией.
- Ведение статистики просмотров для записей.
- Поддержка авторизации и регистрации пользователей.
- Возможность восстановления пароля.
- Управление записями: редактирование, удаление, публикация и отклонение.

## Перед запуском программы необходимо:

> Настроить почту yandex.ru, [по инструкции](https://clck.ru/3BLEsg)

### Для запуска программы необходимо:
- Клонировать проект
```ini
https://github.com/400ton/mailing-service.git
```
- В корне проекта переименовать и заполнить файл .env
- Создать виртуальное окружение:

```ini
python -m venv venv
```
- Активировать виртуальное окружение:
```ini
venv/Scripts/activate # Для Windows
source venv/bin/activate  # Для Linux/Mac
```
- Установить зависимости командой:
```ini
pip install -r requirements.txt
```
- Для работы с базой данных используйте PostgresSQL или другую базу данных по вашему выбору. 
- Примените миграции для инициализации базы данных
```ini
python manage.py migrate
```
- В терминале перейти в корень проекта, выполнить команду и перейти по доменному адресу:
```ini
python manage.py runserver
```
- Для регистрации админа выполнить команду
```ini
python manage.py csu
```
- Для входа в админ панель используйте емайл и пароль:
```ini
admin@localhost
12345
```
- Для остановки локального сервера используйте Сtrl+С в терминале
