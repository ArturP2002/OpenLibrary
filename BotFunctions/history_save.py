from bot_init import bot
from telebot.types import Message
from datetime import datetime
from DataBase import UserData, User
from API import BOOK_URL
from Keyboards import back_kb


def history_answer(message: Message):
    """
    Функция бота для сохранения результата поиска в историю, а так же выдачи результата поиска
    :param message: сообщение от пользователя
    """
    history_file = open('История поиска {name}.txt'.format(
        name=User.get(User.user_id == message.from_user.id).first_name), 'a', encoding='utf-8')

    history_file.write('{date}\nНазвание: {name}\nСсылка: {link}\n\n'.format(
        date=datetime.now(),
        name=UserData.get(UserData.user_id == message.from_user.id).name,
        link=BOOK_URL + UserData.get(UserData.user_id == message.from_user.id).link
    ))
    history_file.close()
    bot.reply_to(message, '<b>Книга успешно найдена!</b> \U00002705\n\n<b>Переходите по ссылке:</b> {}'.format(
        BOOK_URL + UserData.get(UserData.user_id == message.from_user.id).link),
                 reply_markup=back_kb,
                 parse_mode='html')

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
