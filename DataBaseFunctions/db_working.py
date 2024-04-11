from telebot.types import Message
from DataBase import UserData, BooksCount, UserNewData, BooksName
import peewee
from BotFunctions.method_low_func import update_data_low


def db_information_work(message: Message, data):
    """
    Функция telegram-бота, создающая и использующая в дальнейшем базу данных с информацией о всех найденных книгах
    :param message: принятое сообщение от пользователя
    :param data: преобразованный json-файл в python-файл
    """
    try:  # Создаем базу данных с информацией о книгах
        UserData.create(
            user_id=message.from_user.id,
            numFound=data['numFound'],
            name=data['docs'][0]['title'],
            link=data['docs'][0]['key'],
            docs=data['docs'],
            user_text=message.text,
        )
    except peewee.IntegrityError:  # Если пользователь уже есть в базе данных, то обновляем информацию для него
        information = UserData.get(UserData.user_id == message.from_user.id)
        information.numFound = data['numFound']
        information.name = data['docs'][0]['title']
        information.link = data['docs'][0]['key']
        information.docs = data['docs']
        information.user_text = message.text
        information.save()


def db_count_work(message: Message, count):
    """
    Функция telegram-бота, которая создает и использует в дальнейшем базу данных с информацией о количестве книг
    :param message: принятое сообщение от пользователя
    :param count: число книг, необходимое найти в результате
    """
    try:
        BooksCount.create(
            user_id=message.from_user.id,
            count=count,
        )
    except peewee.IntegrityError:
        information = BooksCount.get(BooksCount.user_id == message.from_user.id)
        information.count = count
        information.save()


def db_low_work(message: Message):
    """
    Функция для создания и работы с базой данных, содержащей информацию о найденных старых книгах
    :param message: принятое сообщение от пользователя
    """
    try:
        UserNewData.create(
            user_id=message.from_user.id,
            new_data=update_data_low(message),
            command=message.text,
        )
    except peewee.IntegrityError:
        information = UserNewData.get(UserNewData.user_id == message.from_user.id)
        information.new_data = update_data_low(message)
        information.command = message.text
        information.save()


def db_book_high_work(message: Message, booktype):
    """
    Функция telegram-бота, необходимая для создания и дальнейшей работы с базой данных, содержащей информацию о новых
    книгах
    :param message: принятое сообщение от пользователя
    :param booktype: тип книжек по результатам поиска
    """
    try:
        BooksName.create(
            user_id=message.from_user.id,
            name=booktype,
        )
    except peewee.IntegrityError:
        information = BooksName.get(BooksName.user_id == message.from_user.id)
        information.name = booktype
        information.save()
