import peewee
from telebot.types import Message
from DataBase import UserNewData, UserYears
from bot_init import bot
from BotFunctions.result_search import empty_searching, good_search
from BotFunctions.method_high_func import update_data


@bot.message_handler(commands=['custom_search'])
@bot.message_handler(commands=['custom'])
def custom_books(message: Message):
    """
    Метод пользовательской сортировки(по датам публикации) результата поиска
    :param message: принятое сообщение от пользователя
    """
    db_custom_work(message)

    years_msg = bot.reply_to(message, '<b>Введите <u>ДИАПОЗОН</u> лет</b>:\n\n\U00002757 <b>НАПРИМЕР</b> '
                                      '\U00002757\n\n1976 1988',
                             parse_mode='html')

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.register_next_step_handler(years_msg, custom_search)


@bot.message_handler(func=lambda message: message.text == '<b>Введите <u>ДИАПОЗОН</u> лет</b>:\n\n\U00002757 '
                                                          '<b>НАПРИМЕР</b> \U00002757\n\n1976 1988')
def custom_search(message: Message):
    """
    Функция telegram-бота, которая получает на вход диапозон дат первой публикации книг, а затем выдает результат поиска
    :param message: принятое сообщение от пользователя
    """
    db_years_range_work(message)

    years = message.text.split()
    count_of_books = good_search(bot, message, years)

    if count_of_books == 0:
        empty_searching(bot, message)
    else:
        bot.reply_to(message, 'По результатам ваших запросов выше представлены <b>{count} книжек в диапозоне '
                          'от {left_board} до {right_board} годов публикаций</b> из '
                          'открытой библиотеки \U00002705\n\n\U00002757 <b>ВНИМАНИЕ</b> \U00002757\n\n'
                          'Как только вы вернетесь в главное меню, переписка с ботом будет <b><u>АВТОМАТИЧЕСКИ '
                          'УДАЛЕНА!</u></b>'.format(
                                            count=count_of_books,
                                            left_board=int(years[0]),
                                            right_board=int(years[1])),
                     parse_mode='html')

        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


def db_custom_work(message: Message):
    """
    Функция для создания и работы с базой данных, содержащей информацию о найденных пользовательским методом сортировки
    книгах
    :param message: принятое сообщение от пользователя
    """
    try:  # Создаем базу данных с новыми данными поиска для пользователя
        UserNewData.create(
            user_id=message.from_user.id,
            new_data=update_data(message),
            command=message.text,
        )
    except peewee.IntegrityError:  # Если пользователь уже есть в базе данных, обновляем информацию
        information = UserNewData.get(UserNewData.user_id == message.from_user.id)
        information.new_data = update_data(message)
        information.command = message.text
        information.save()


def db_years_range_work(message: Message):
    """
    Функция telegram-бота, которая создает и использует в дальнейшем базу данных с информацией о введенном пользователем
    диапазона годов первой публикации книг при получении команды /custom
    :param message: принятое сообщение от пользователя
    """
    try:
        UserYears.create(
            user_id=message.from_user.id,
            years_range=message.text,
        )
    except peewee.IntegrityError:
        information = UserYears.get(UserYears.user_id == message.from_user.id)
        information.years_range = message.text
        information.save()
