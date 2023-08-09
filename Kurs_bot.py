import telebot
import configparser
from extensions import CurrencyConverter


config = configparser.ConfigParser()
config.read('config.ini')
bot = telebot.TeleBot(config.get('Secret_data', 'API_key_bot'))


@bot.message_handler(commands=['start', 'help'])
def com_start_help(message):
    if message.text == '/start':# если команада start вывод сообщения с приветствием
        bot.send_message(message.chat.id, f"Привет {message.chat.username}, это бот конвертирования валют\n"
                                          f"---------------------------------------\n"
                                          f"Команды бота:\n/start - запуск бота, вывод основной информации\n"
                                          f"/help - вывод информации по использованию\n"
                                          f"/values - вывод доступных валют для конвертирования\n"
                                          f"---------------------------------------\n"
                                          f"Для корректного конвертирования отправь сообщение в таком виде:"
                                          f"\nUSD - название валюты, из которой нужно перевести\nEUR - название валюты, "
                                          f"в которую нужно перевести\nКоличество валюты\nПример сообщения:\n"
                                          f"USD AED 15")
    elif message.text == '/help':# если команада help вывод сообщения с объяснением формата отправки сообщения
        bot.send_message(message.chat.id, f"Для корректного конвертирования отправь сообщение в таком виде:"
                                          f"\nUSD - название валюты, из которой нужно перевести\nEUR - название валюты, "
                                          f"в которую нужно перевести\nКоличество валюты\nПример сообщения:\n"
                                          f"USD AED 15")


@bot.message_handler(commands=['values'])
def com_values(message):# вывод доступных валют
    del_list = ['{', '}', '"']# список символов для удаления из строк
    list_currency = CurrencyConverter.get_all_currency()# получение списка доступных валют
    list_currency = list_currency.replace(', ', "\n")
    for i in del_list:
        list_currency = list_currency.replace(i, "")# удаление из строк символов
    list_currency = "".join(["Доступные валюты для конвертирования:\n", list_currency])
    if list_currency:# проверка есть ли доступные валюты для конвертирования
        for k in range(0, len(list_currency), 4086):# цикл отправки сообщений, если список слишком большой и
            # колиество символов больше допустимых в сообщении
            bot.send_message(message.chat.id, text=f'{list_currency}')
    else:
        bot.send_message(message.chat.id, f'Бот в данный момент не конвертирует валюту')


@bot.message_handler(content_types =['text', ])
def currency_txt(message):# обработка текстового сообщения пользователя
    try:
        text_list = message.text.split()
        base = text_list[0]# базовая валюта
        quote = text_list[1]# конвертируемая валюта
        amount = text_list[2]# количество валюты
        amount = int(amount)
        if amount < 1:# проверка на допустимое количество
            raise ValueError
        currency = CurrencyConverter.get_price(base, quote, int(amount))# получение сконвертированной валюты
        if currency[0]:# проверка отработки запроса
            bot.send_message(message.chat.id, f'{int(amount)} {base} к {quote} = {currency[0]}')# отправка пользователю валюты
        elif not (currency[0]) and currency[1] == 1:# проверка на корректность введеной валюты
            bot.send_message(message.chat.id, f'Вы некорректно ввели валюты')
        else:
            bot.send_message(message.chat.id, f'Бот в данный момент не конвертирует валюту')

    except IndexError:
        bot.send_message(message.chat.id,f'Вы некорректно ввели данные')
    except ValueError:
        bot.send_message(message.chat.id,f'Вы ввели недопустимое количество')



if __name__ == "__main__":
    bot.polling(none_stop=True)
