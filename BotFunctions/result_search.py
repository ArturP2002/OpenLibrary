from telebot.types import Message
from DataBase import UserNewData, BooksCount, User
from datetime import datetime
from API import BOOK_URL
from Keyboards import back_kb


def empty_searching(bot, message: Message):
    """
    Функция telegram-бота, которая отправляет пользователю сообщение в случае, когда результат поиска книг по датам
    первой публикации равен нулю
    :param bot: telegram-бот
    :param message: принятое сообщение от пользователя
    """
    bot.send_message(message.chat.id, 'К сожалению <b>НЕТ</b> книжек, удовлетворяющих результатам вашего '
                                      'поиска...\U0001F61F\n\nПопробуйте ввести команду /custom_search и еще раз '
                                      'ввести <b><u>ДАТЫ ПУБЛИКАЦИЙ</u></b>',
                     parse_mode='html')

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


def good_search(bot, message: Message, years):
    """
    Функция telegram-бота, при выполнении которой бот отправляет пользователю информацию о книгах, удовлетворяющих
    результатам его поиска по датам первой публикации
    :param bot: telegram-бот
    :param message: принятое сообщение от пользователя
    :param years: даты первых публикаций, введенные пользователем
    :return: max_count - количество книг, найденное ботом согласно условиям пользователя
    """
    max_count = 0
    history_file = open('История поиска {name}.txt'.format(
        name=User.get(User.user_id == message.from_user.id).first_name), 'a', encoding='utf-8')

    for i_key in eval(UserNewData.get(UserNewData.user_id == message.from_user.id).new_data):
        if int(years[0]) <= int(i_key['first_publish_year']) <= int(years[1]):
            if max_count == BooksCount.get(BooksCount.user_id == message.from_user.id).count:
                break
            else:
                max_count += 1
                bot.send_message(message.chat.id, '<b>{num}) Название:</b> {title};\n<b>Год публикации:</b> '
                                      '{publish_year};\n<b>Ссылка на книжку:</b> {link}\n\n'.format(
                                        num=max_count,
                                        title=i_key['title'],
                                        publish_year=i_key['first_publish_year'],
                                        link=BOOK_URL + i_key['key']),
                                 reply_markup=back_kb,
                                 parse_mode='html')

                history_file.write('{date}\nНазвание: {title}\nСсылка на книжку: {link}\n\n'.format(
                    date=datetime.now(),
                    title=i_key['title'],
                    link=BOOK_URL + i_key['key']))

    history_file.close()

    return max_count
