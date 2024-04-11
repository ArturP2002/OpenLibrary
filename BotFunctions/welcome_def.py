import peewee
from Keyboards import start_kb
from DataBase import User
from telebot.types import Message


def welcome(bot, message: Message):
    """
    Метод приветствия OpenLibraryBot, вызывается вводом команды /start
    :param message: полученное от пользователя сообщение
    """
    try:
        User.create(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )

        # Приветствуем нового пользователя
        bot.reply_to(message, '<b>{name}, добро пожаловать в OpenLibraryBot!</b>\n\nЗдесь вы можете найти любую '
                          'интересующую вас книгу, попробовать узнать для себя новых авторов и их самые '
                          'популярные произведения.\n\nЧтобы начать работу, нажмите на кнопку '
                          'ниже ⬇️'.format(name=message.from_user.first_name),
                     reply_markup=start_kb,
                     parse_mode='html')

        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except peewee.IntegrityError:  # Приветствуем пользователя, если он уже есть в базе данных
        bot.reply_to(message, '<b>С возвращением, {name}!</b>\n\nЧтобы начать работу, нажмите на кнопку ниже ⬇️'.format(
                                                                                    name=message.from_user.first_name),
                                                                             reply_markup=start_kb,
                                                                             parse_mode='html')

        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
