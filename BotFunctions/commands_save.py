from telebot.types import Message
from datetime import datetime
from DataBase import UserNewData, UserYears, UserData, BooksCount, User


def save_commands(message: Message):
    """
    Функция telegram-бота для сохранения введенных команд пользователем
    :param message: принятое сообщение от пользователя
    """
    commands_file = open('История команд {name}.txt'.format(
        name=User.get(User.user_id == message.from_user.id).first_name), 'a', encoding='utf-8')

    if UserNewData.get(UserNewData.user_id == message.from_user.id).command == '/custom':
        commands_file.write('{date}\n{book_title} - {command} - {years} - {count};\n\n'.format(
                                        date=datetime.now(),
                                        book_title=UserData.get(UserData.user_id == message.from_user.id).user_text,
                                        command=UserNewData.get(UserNewData.user_id == message.from_user.id).command,
                                        years=UserYears.get(UserYears.user_id == message.from_user.id).years_range,
                                        count=BooksCount.get(BooksCount.user_id == message.from_user.id).count))
    else:
        commands_file.write('{date}\n{book_title} - {command} - {count};\n\n'.format(
                                        date=datetime.now(),
                                        book_title=UserData.get(UserData.user_id == message.from_user.id).user_text,
                                        command=UserNewData.get(UserNewData.user_id == message.from_user.id).command,
                                        count=BooksCount.get(BooksCount.user_id == message.from_user.id).count))

    commands_file.close()
