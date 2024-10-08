# Personal Diary — Web Application
___
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

---

**Personal Diary** — это веб-приложение для ведения личного дневника, выполненное в минималистичном скандинавском стиле. Основное внимание уделено простоте интерфейса и плавности взаимодействия, что позволяет пользователям легко создавать, редактировать и управлять своими записями. Приложение создано на базе современных технологий, таких как **Django** и **Bootstrap**, что обеспечивает его надежность и адаптивность.

## 🌟 Основные возможности:
- ✏️ **Создание личных записей** - возможность их опубликовать для всех пользователей,отображаются на главной странице
- 🔒 **Модерация записей** перед публикацией - отображается в статусе в деталях дневника
- 📈 **Отслеживание статистики** просмотров для каждой записи - при 100 просмотрах опубликованной записи отправляется уведомление пользователю на емейл
- 🔐 **Авторизация и регистрация пользователей**
- 🔄 **Восстановление пароля** - пароль генерируется и отправляется на почту
- 🛠 **Управление записями** -для модераторов: редактирование, удаление, публикация, отклонение

---

## ⚙️ Перед запуском
Чтобы приложение работало корректно, необходимо настроить почтовую службу **Yandex** по [этой инструкции](https://clck.ru/3BLEsg).

## 🚀 Запуск проекта:
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
- Для заполнения базы данных используйте команду (допишите емайл пользователя для которого создаются данные)
```ini
python manage.py faker your_email@example.com
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
- ### _Для модерации необходимо создать через админ панель группу moderator и присвоить группе права:_

```ini
diary|Дневник|Может модерировать записи
```

- Для остановки локального сервера используйте Сtrl+С в терминале

# В разработке: _реализация общения между пользователями_