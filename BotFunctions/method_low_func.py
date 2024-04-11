from DataBase import BooksCount, UserNewData, UserData, BooksName, User
import peewee
from Keyboards import back_kb
from datetime import datetime
from API import BOOK_URL
from telebot.types import Message


def low_history(bot, message: Message):
    """
    Функция telegram-бота, которая отправляет пользователю определенное им ранее количество книг, отсортированных
    по возрастанию
    :param bot: telegram-бот
    :param message: принятое сообщение от пользователя
    """
    history_file = open('История поиска {name}.txt'.format(
        name=User.get(User.user_id == message.from_user.id).first_name), 'a', encoding='utf-8')

    for i_elem in range(BooksCount.get(BooksCount.user_id == message.from_user.id).count):
        bot.send_message(message.chat.id, '<b>{num}) Название</b>: {title}\n<b>Ссылка на книжку</b>: {link}\n\n'.format(
            num=i_elem + 1,
            title=eval(UserNewData.get(UserNewData.user_id == message.from_user.id).new_data)[i_elem]['title'],
            link=BOOK_URL + eval(UserNewData.get(UserNewData.user_id == message.from_user.id).new_data)[i_elem]['key']),
                         parse_mode='html')

        history_file.write('{date}\nНазвание: {title}\nСсылка на книжку: {link}\n\n'.format(
            date=datetime.now(),
            title=eval(UserNewData.get(UserNewData.user_id == message.from_user.id).new_data)[i_elem]['title'],
            link=BOOK_URL + eval(UserNewData.get(UserNewData.user_id == message.from_user.id).new_data)[i_elem]['key']))

    history_file.close()


def update_data_low(message: Message):
    """
    Функция telegram-бота, которая заполняет базу данных всеми найденными старыми книгами
    :param message: принятое сообщение от пользователя
    :return: new_data - список старых книг
    """
    new_data = []  # Список с полной информацией о книгах

    for i_elem in eval(UserData.get(UserData.user_id == message.from_user.id).docs):
        try:
            if isinstance(i_elem['first_publish_year'], int):
                new_data.insert(0, i_elem)
        except KeyError:
            print('Повреждение ключа!')

    return new_data


def books_type_low(bot, message: Message, booktype):
    """
    Функция telegram-бота, которая заносит в базу данных, какие именно книги были найдены в результате поиска
    :param bot: telegram-бот
    :param message: принятое сообщение от пользователя
    :param booktype: тип книг
    """
    db_book_low_work(message, booktype)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


def low_answer(bot, message: Message):
    """
    Функция telegram-бота, которая отправляет пользователю сообщение от бота о результатах поиска старых книг
    :param bot: telegram-бот
    :param message: принятое сообщение от пользователя
    """
    bot.send_message(message.chat.id, 'По результатам ваших запросов выше представлены <b>{count} САМЫХ {status} '
                          'КНИЖЕК</b> из открытой библиотеки \U00002705\n\n\U00002757 <b>ВНИМАНИЕ</b> \U00002757\n\n'
                          'Результат поиска будет <b><u>ПОСТОЯННО</u></b> находиться в чате! Однако Вы можете в любой '
                          'момент его очистить самостоятельно, а все ваши результаты поиска будут храниться в '
                          '<b><u>ИСТОРИИ</u></b>'.format(
                                    count=BooksCount.get(BooksCount.user_id == message.from_user.id).count,
                                    status=BooksName.get(BooksName.user_id == message.from_user.id).name),
                              reply_markup=back_kb,
                              parse_mode='html')


def db_book_low_work(message: Message, booktype):
    """
    Функция telegram-бота, необходимая для создания и дальнейшей работы с базой данных, содержащей информацию о старых
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
