import functools
from telebot.types import Message
from API import BASE_URL
import requests
import json
from Keyboards import quantity_kb, main_menu_kb, back_kb
from BotFunctions.welcome_def import welcome
from BotFunctions.high_func import high_books
from BotFunctions.low_func import low_books
from BotFunctions.custom_func import custom_books
from BotFunctions.searching_answ import bot_answer
from BotFunctions.history_save import history_answer
from BotFunctions.commands_save import save_commands
from DataBase import db, UserData, BooksCount, BooksName, UserNewData, User
from bot_init import bot
from DataBaseFunctions.db_working import db_information_work, db_count_work


with db:  # Создаем таблицы для всех баз данных бота
    db.create_tables([UserData, BooksCount, BooksName, UserNewData, User])


@bot.message_handler(func=lambda message: message.text == 'Начать поиск \U0001F680')
def main_menu(message: Message):
    """
    Функция telegram-бота для вывода главного меню бота, также вызывается командой /search
    :param message: принятое сообщение(команда) от пользователя
    """
    bot.reply_to(message, text='<b>Выбери одну из предложенных ниже команд:</b>\n\n\U00002757 '
                             'Чтобы узнать о каждой из них поподробнее, а также о работе бота, нажми на '
                             'кнопку "Помощь" \U00002757',
                     reply_markup=main_menu_kb,
                     parse_mode='html')

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(func=lambda message: message.text == 'Поиск книги по ее названию \U0001F50E')
@bot.message_handler(commands=['search'])
def searching_title(message: Message):
    """
    Функция telegram-бота для поиска книг согласно запросам пользователя
    :param message: принятое сообщение от пользователя
    """
    book_title = bot.reply_to(message, text='<b>Введите название книги на <u>АНГЛИЙСКОМ</u> языке!</b>\n\n\U00002757 '
                                    'Чем более полным будет ваше введенное название, тем более точный результат Вы '
                                    'получите! \U00002757',
                                       parse_mode='html')

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.register_next_step_handler(book_title, title)


@bot.message_handler(func=lambda message: message.text == 'История поиска \U0001F4D6')
def searching_story(message: Message):
    """
    Функция telegram-бота, при выполнении которой бот отправляет пользователю файл(история поиска), где указаны
    названия всех книг, отправленные когда-либо раньше
    :param message: принятое сообщение от пользователя
    """
    with open('История поиска {name}.txt'.format(
            name=User.get(User.user_id == message.from_user.id).first_name), 'r', encoding='utf-8') as history_file:
        bot.send_document(message.chat.id, history_file, reply_markup=back_kb)

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(func=lambda message: message.text == 'История команд \U0001F6E0')
def sending_commands(message: Message):
    """
    Функция telegram-бота, при выполнении которой бот отправляет пользователю файл(история команд), где перечислены все
    ранее введенные команды пользователя в том случае, когда слишком большой объем результатов поиска
    :param message: принятое сообщение от пользователя
    """
    save_commands(message)
    with open('История команд {name}.txt'.format(
                name=User.get(User.user_id == message.from_user.id).first_name), 'r', encoding='utf-8') as saving_data:
        bot.send_document(message.chat.id, saving_data, reply_markup=back_kb)

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(func=lambda message: message.text == 'Что можно добавить? \U0001F4DD')
def searching_new(message: Message):
    """
    Функция telegram-бота, при выполнении которой бот отправляет сообщение с информацией о дальнейших перспективах
    развития
    :param message: принятое сообщение от пользователя
    """
    bot.reply_to(message, 'Данный бот находится на этапе раннего доступа с готовой реализацией поиска книг по их '
                          'названиям. Однако в дальнейшем будут реализованы следующие команды поиска книг:\n\n1) '
                          'Поиск всех книг введенных пользователем автора;\n\n2) Поиск книг по жанрам(тематике), '
                          'например: поиск всех книг про теннис;\n\n3) Поиск книг на различных языках мира.',
                 reply_markup=back_kb)

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(func=lambda message: message.text == 'Помощь \U00002049')
def searching_help(message: Message):
    """
    Функция telegram-бота, при выполнении которой бот отправляет пользователю сообщение с информацией о том, что умеет
    бот
    :param message: принятое сообщение от пользователя
    :return:
    """
    bot.reply_to(message, '<b>Что умеет OpenLibraryBot?</b>\n\nДля начала работы с ботом нажмите на кнопку '
                         '<b><u>"НАЧАТЬ"</u></b>.\n\nЕсли же вы уже пользовались данным ботом и снова вернулись для '
                         'поиска еще одних(ой) книг(и), то введите команду /start.\n\nПосле того как бот с '
                         'вами поздоровался и вы перешли в основное меню, вам будут предложены следующие '
                         'команды:\n\n1) <b>"Поиск книги по ее названию"</b> - по данной команде бот выдаст вам '
                         'книгу в соответствие с вашим введенным название.\n\n\U00002757 <b>ОБРАТИТЕ ВНИМАНИЕ</b> '
                         '\U00002757\nНазвания необходимо вводить <b><u>АНГЛИЙСКИМИ</u></b> буквами. Далее следуйте '
                         'согласно указаниям бота.\n\n\U00002757 ВАЖНО \U00002757\nБот является <b><u>ранней '
                         'версией</u></b>, еще множество других функций будут добавлены позже!',
                     reply_markup=back_kb,
                     parse_mode='html')
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(func=lambda message: message.text == '<b>Введите название книги на <u>АНГЛИЙСКОМ</u> языке!</b>'
                                              '\n\n\U00002757 Чем более полным будет ваше введенное '
                                              'название, тем более точный результат Вы получите! \U00002757',
                                          parse_mode='html')
def title(message: Message):
    """
    Функция telegram-бота, выводящая пользователю окончательный результат поиска. Если книг с таким названием слишком
     много, то бот выполняет функцию bot_answer();
     Если пользователь ввел правильное и точное название книги, то бот выполняет функцию history
    :param message: принятое сообщение от пользователя
    """
    URL = BASE_URL + 'title={title}'.format(title=message.text)

    response = requests.get(URL)
    data_resp = json.loads(response.text)

    with open('titles.json', 'w') as file:
        json.dump(data_resp, file, indent=4)

    with open('titles.json', 'r') as file:
        data = json.load(file)

    db_information_work(message, data)
    appeal_to_bd = UserData.get(UserData.user_id == message.from_user.id).numFound  # Обращение бота к базе данных

    if appeal_to_bd >= 10:
        bot_answer(message)
    else:
        history_answer(message)


@bot.message_handler(func=lambda message: message.text == '5')
@bot.message_handler(func=lambda message: message.text == '10')
@bot.message_handler(func=lambda message: message.text == '15')
def sorting(message: Message):
    """
    Функция telegram-бота для выбора конкретной сортировки полученного результата поиска;
    При получении команды /high переходит к методу сортировки книг от самых новых к самым старым;
    Команда /low переходит к методу сортировки книг от самых старых к самым новым;
    Команда /custom - переходит к пользовательскому методу сортировки книг по годам публикации
    :param message: принятое сообщение от пользователя
    """
    count = int(message.text)  # Преобразуем текстовое сообщение от пользователя в целое число для поиска книг
    db_count_work(message, count)

    bot.send_message(message.chat.id, '<b>ОТЛИЧНО!</b>\n\n\U0001F50E Если вы хотите получить <b><u>{num1} САМЫХ '
                            'НОВЫХ КНИГ</u></b>, то введите команду /high\n\nЕсли же вы хотите увидеть <b><u>{num2} '
                            'САМЫХ СТАРЫХ КНИГ</u></b>, то введите команду /low\n\nТакже вы можете выбрать книги '
                            'согласно <b>ГОДУ ИХ ПЕРВОЙ ПУБЛИКАЦИИ</b>, для этого введите команду /custom '
                            '\U0001F50D'.format(
                                    num1=BooksCount.get(
                                        BooksCount.user_id == message.from_user.id).count,
                                    num2=BooksCount.get(
                                        BooksCount.user_id == message.from_user.id).count),
                                     parse_mode='html')

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(func=lambda message: message.text == 'Главное меню \U0001F4A1')
def go_main_menu(message: Message):
    """
    Функция для перехода в главное меню
    :param message: принятое сообщение от пользователя
    """
    bot.reply_to(message, '<b>Вы вернулись в главное меню!</b>\n\nДля продолжения работы выберите одну из '
                          'предложенных ниже команд \U00002B07',
                     reply_markup=main_menu_kb,
                     parse_mode='html')

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def how_many(call):
    """
    Функция telegram-бота, которая запрашивает у пользователя сколько именно книг необходимо ему вывести в случае
    большого результата поиска
    :param call: данные функции обратного вызова(inline-кнопка клавиатуры)
    """
    if call.message:
        if call.data == 'count':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            msg = bot.send_message(call.message.chat.id, 'Сколько книг вы хотите получить?', reply_markup=quantity_kb)
            bot.register_next_step_handler(msg, sorting)


functions_for_register = [(welcome, {"commands": ['start']}),
                          (high_books, {"commands": ['high']}),
                          (low_books, {"commands": ['low']}),
                          (custom_books, {"commands": ['custom']})]


def register_func(bot, func, *args, **kwargs):
    """
    Функция регистрации функций telegram-бота
    :param bot: параметр telegram-бота
    :param func: метод функционирования бота
    :param args:  параметры, передающиеся по позиции
    :param kwargs: параметры, передающиеся по имени
    """
    @bot.message_handler(*args, **kwargs)
    @functools.wraps(func)
    def wrapper(message: Message):
        return func(bot, message)

    return wrapper


for func, kwargs in functions_for_register:
    new_func = register_func(bot, func, **kwargs)


@bot.message_handler(func=lambda message: True)
def echo_all(message: Message) -> None:
    """
    Обработчик сообщений echo_all
    :param message: принятое сообщение от пользователя
    """
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    bot.infinity_polling()  # Запуск бесконечного цикла работы telegram-бота
