# Application Marketplace (в разработке)

## Основные зависимости:

1. python3.8
2. django 3.2.13
3. postgresql12+

## Первичная настройка:

### 1) установить postgresql на Вашу машину
Для каждой ОС способы могут немного отличаться
для Linux алгоритм такой:
1. установка пользователю postgres пароля и переключение на него
2. инициация БД (initdb)
3. создание пользователя БД и БД
4. установка пароля пользователю БД (в оболочке psql)

### 2) установть зависимоти
pip install -r /path/to/requirements.txt  
P.S. для установки в docker заменить psycopg2 на psycopg2-binary

### 3) Заполнить файл с настройками
для удобства локальной разработки предлагается использовать личыне (именованные) файлы настроек в директории marketplace_app/dev_settings  

по умолчанию в settings в качестве БД указана SQLITE3  
в файле со своими настройками переопределяем словарь DATABASES с настройками для подключения к postgres

### 4) Использование django-environ

при желании можно определить некоторые переменные в файле .env (файл должен располагаться в одной директории с файлом настроек
)  
![env location](https://ltdfoto.ru/images/2022/04/12/env.png "env location")
пример содержания файла .env
```text
DEBUG=1
SECRET_KEY='6_qz=qb*)5#p6*5)g3iip-107y&&7cf2!-0=lc$%h)o%%=li*g'
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=db_name
DB_USER=db_user_name
DB_PASSWORD=db_user_password
DB_HOST=127.0.0.1
DB_PORT=5432
```
Инициализация django-environ в файле с настройками:
```python
env = environ.Env()
environ.Env.read_env()
```
Пример получения переменной из env:
```python
SECRET_KEY=env.get_value('SECRET_KEY')
```

### 5) Использование личного файла с настройками проекта:

для переопредения файла настроек нужно указать переменную окружения DJANGO_SETTINGS_MODULE  
пример:
```shell
DJANGO_SETTINGS_MODULE=marketplace_app.dev_settings.dev_aleksandr
```

пример установки для команды Pycharm:

1. Run-> Edit Configurations
2. Создаем новую конфигурацию или редактируем старую
3. в поле Environment variables добавляем нашу переменную как в примере выше
4. не забываем устнанавливать переменную для runserver, makemigrations, migrate итд
![run config](https://ltdfoto.ru/images/2022/04/12/run_config.png "run config")
