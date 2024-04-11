from peewee import SqliteDatabase, Model, IntegerField, CharField

# База данных всех пользователей
db = SqliteDatabase('users.db')

# Делаем базу данных для хранения данных
database = SqliteDatabase('user_data.db')  # Создаем базу данных


class BaseModelData(Model):
    """
    Базовый класс для поисковых моделей пользователей
    """
    class Meta:
        database = database


class UserData(BaseModelData):
    user_id = IntegerField(primary_key=True)
    numFound = IntegerField()
    name = CharField()
    link = CharField()
    docs = CharField()
    user_text = CharField()

    class Meta:
        db_table = 'data'


class UserYears(BaseModelData):  # База данных для сохранения диапазона годов публикации при команде /custom
    user_id = IntegerField(primary_key=True)
    years_range = CharField()

    class Meta:
        db_table = 'years_range'


class BooksCount(BaseModelData):
    user_id = IntegerField(primary_key=True)
    count = IntegerField()

    class Meta:
        db_table = 'count'


class BooksName(BaseModelData):
    user_id = IntegerField(primary_key=True)
    name = CharField()

    class Meta:
        db_table = 'books_name'


class UserNewData(BaseModelData):
    user_id = IntegerField(primary_key=True)
    new_data = CharField()
    command = CharField()

    class Meta:
        db_table = 'new_data'


class BaseModelUser(Model):
    """
    Базовый класс для базы данных модели пользователя
    """
    class Meta:
        database = db


class User(BaseModelUser):
    """
    Модель пользователя
    :arg user_id: ID пользователя,
         first_name: имя пользователя в Telegram
         last_name: фамилия пользователя(если есть) в Telegram
         username: никнейм пользователя в Telegram

    """
    user_id = IntegerField(primary_key=True)
    first_name = CharField()
    last_name = CharField(null=True)
    username = CharField()
