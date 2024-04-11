from DataBase import UserData
from Keyboards import inline_markup
from bot_init import bot
from telebot.types import Message


def bot_answer(message: Message):
    """
    Функция telegram-бота, которая отправляет ответ пользователю с информацией о том, сколько всего книг найдено
    :param message: сообщение от пользователя;
    """
    bot.reply_to(message, '\U0001F9FE <b>Всего найдено {} книг(и)!</b> \U0001F9FE\n\nЭто слишком много, попробуйте '
                      'ввести команду /search и снова ввести более <b><u>ПОЛНОЕ НАЗВАНИЕ</u></b> книги '
                      '\U0001F4A1\n\nЛибо вы можете получить необходимое вам количество <b><u>СТАРЫХ</u></b> или '
                      '<b><u>НОВЫХ</u></b> книг, удовлетворяющих результатам вашего поиска \U00002B07'.format(
                                            UserData.get(UserData.user_id == message.from_user.id).numFound),
                 reply_markup=inline_markup,
                 parse_mode='html')

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
