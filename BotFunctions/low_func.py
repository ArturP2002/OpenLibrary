from BotFunctions.method_low_func import low_history, books_type_low, low_answer
from telebot.types import Message
from DataBase import UserNewData
from DataBaseFunctions.db_working import db_low_work


def low_books(bot, message: Message):
    """
    Метод сортировки книг от самых старых к самым новым
    :param message: принятое сообщение от пользователя
    """
    db_low_work(message)
    UserNewData.get(UserNewData.user_id == message.from_user.id).new_data = sorted(
                                        eval(UserNewData.get(UserNewData.user_id == message.from_user.id).new_data),
                                        key=lambda year: year['first_publish_year'])
    books = 'СТАРЫХ'

    books_type_low(bot, message, books)
    low_history(bot, message)
    low_answer(bot, message)
