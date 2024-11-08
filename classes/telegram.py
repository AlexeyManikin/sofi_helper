__author__ = 'Alexey Y Manikin'

import telebot
import config.config
import re
import classes.llm_parser
import datetime
import classes.read_pdf
import classes.bill_parser
import traceback

botTelegram = telebot.TeleBot(config.config.TELEGRAM_BOT_KEY)

@botTelegram.message_handler(commands=['start'])
def start_bot(message: telebot.types.Message):
    botTelegram.reply_to(message, config.config.TELEGRAM_BOT_HELP)

@botTelegram.message_handler(commands=['print_group'])
def print_group(message: telebot.types.Message):
    model = classes.llm_parser.LLMParser()
    result = ""
    for item in model.get_list_of_category():
        result += " - " + str(model.get_list_of_category()[item]) + "\n"
    botTelegram.reply_to(message, result)

@botTelegram.message_handler(commands=['summary'])
def summary(message: telebot.types.Message):
    model = classes.llm_parser.LLMParser()
    result = "Суммарные траты за последние 30 дней - %i" % model.get_summary_row(30)
    botTelegram.reply_to(message, result)

@botTelegram.message_handler(commands=['last'])
def last(message: telebot.types.Message):
    model = classes.llm_parser.LLMParser()
    result =  model.get_list_spending(30)
    str_result = ""
    for item in result:
        str_result += " - " + str(item['date'])[0:10] + " - " + \
                      str(model.get_list_of_category()[item['group_type']]) + " - " + str(item['description']) + \
                      " - " + str(item['summ']) + "\n"

    botTelegram.reply_to(message, str_result)

@botTelegram.message_handler(content_types=['text'])
def parce_message(message: telebot.types.Message):
    try:
        if not re.findall(r'\d+', message.text):
            return

        model = classes.llm_parser.LLMParser()
        result = model.parse_date(message.text, message.date, message.from_user.full_name)

        if result != {}:
            d = model.get_list_of_category()
            try:
                group = d[result['group']]
            except KeyError:
                group = result['group']

            return_text = "Данные добавлены: \n" + \
                   "  - сумма: %s\n" % result['summ'] + \
                   "  - группа: %s\n" % group + \
                   "  - описание: %s\n" % result['description'] + \
                   "  - дата: %s\n" % result['date'] + \
                   "  - обоснование: %s\n" % result['reasoning']
            botTelegram.reply_to(message, return_text)
    except Exception as e:
        botTelegram.reply_to(message, e)

@botTelegram.message_handler(content_types=['document'])
def handle_docs_pdf(message: telebot.types.Message):
    try:
        # пока не особо работает надо сидеть править regexp - это где-то на 2 дня занятие
        file_info = botTelegram.get_file(message.document.file_id)
        downloaded_file = botTelegram.download_file(file_info.file_path)

        new_file_name = (config.config.CURRENT_PATH + '/pdf_data/txt/' +
                         datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S') +
                         "_" + str(message.chat.id) + ".txt")

        with open(new_file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        parser = classes.bill_parser.BillParser()
        result = parser.run(new_file_name)

        return_message = "Я сохранил этот файл: : %s\n" % new_file_name + \
                        " - вставлено новых чеков: %s\n" % result["count_bills"] + \
                        " - вставлено новых блюд: %s\n" % result["count_dish"] + \
                        " - найденно существующих записей: %s\n" % result["count_bills_already_insert"]

        botTelegram.reply_to(message, return_message)
    except Exception as e:
        print((traceback.format_exc()))
        botTelegram.reply_to(message, e)

def run():
    botTelegram.infinity_polling()