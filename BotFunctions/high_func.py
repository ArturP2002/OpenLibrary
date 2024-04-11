from telebot.types import Message
import peewee
from BotFunctions.method_high_func import high_history, update_data, books_type_high, high_answer
from DataBase import UserNewData


def high_books(bot, message: Message):
    """
    Метод сортировки книг от самых новых к самым старым
    :param message: принятое сообщение от пользователя
    """
    db_high_work(message)
    UserNewData.get(UserNewData.user_id == message.from_user.id).new_data = sorted(
                                        eval(UserNewData.get(UserNewData.user_id == message.from_user.id).new_data),
                                        key=lambda year: year['first_publish_year'], reverse=False)
    books = 'НОВЫХ'

    books_type_high(bot, message, books)
    high_history(bot, message)
    high_answer(bot, message)


def db_high_work(message: Message):
    """
    Функция бота для работы с базой данных, содержащей всю информацию о найденных новых книгах
    :param message: принятое сообщение от пользователя
    """
    try:
        UserNewData.create(
            user_id=message.from_user.id,
            new_data=update_data(message),
            command=message.text,
        )
    except peewee.IntegrityError:
        information = UserNewData.get(UserNewData.user_id == message.from_user.id)
        information.new_data = update_data(message)
        information.command = message.text
        information.save()
