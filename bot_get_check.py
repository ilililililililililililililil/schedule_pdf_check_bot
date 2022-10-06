import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import outcome
from config_bot import TOKEN
from utils import (get_html_source,
                   get_pdf_link,
                   get_pdf_and_save,
                   pdf_content_check,
                   get_datetime_now)

from settings import (CHROME_DRIVER_PATH,
                      WORD_TO_FIND,
                      SEARCH_PHRASE_FOR_PDF_LINK,
                      URL_PAGE,
                      PIC_PATH,
                      PDF_PATH,
                      HTML_PATH
                      )

def main():
    output: str = ''
    stop_working = 0
    delay = 60
    iterations = 0
    # print('Program starts at:', get_datetime_now('full'))
    # print('Delay between requests is: ', delay, 'seconds')
    # print('_________________________________________________')

    output += '\n' + 'Program starts at: ' + str(get_datetime_now('full'))
    output += '\n' + '___________________________'

    while stop_working != 1:
        stop_working = 1
        iterations += 1
        html_page_source = get_html_source(URL_PAGE, CHROME_DRIVER_PATH)
        # html_page_source = '' # manual file for
        pdf_link = get_pdf_link(html_page_source, SEARCH_PHRASE_FOR_PDF_LINK)

        pdf_fname = get_datetime_now('full') + '.pdf'
        pdf_file_name = PDF_PATH + '/' + pdf_fname
        get_pdf_and_save(pdf_link, pdf_file_name)
        result = pdf_content_check(pdf_file_name, WORD_TO_FIND, PIC_PATH)

        for key, value in result.items():
            # print('one more try at:', get_datetime_now('small'))
            # print('Key: ', key, ', result: ', value)
            # print('_________________________________________________')
            #output += '\n' + 'one more try at:' + str(get_datetime_now('small'))
            output += '\n' + str('Key: ') + str(key) + str(', result: ') + str(value)
            #output += '\n' + '___________________________'
            #output += '\n' 

            if key == WORD_TO_FIND.upper():
                stop_working = 1

        #time.sleep(delay)
        #if iterations > 1:
        #    stop_working = 1
    return output


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.bot.send_message(message.from_user.id, 
    """Добрый день! \n
    Этот бот предназначен для регулярной автоматической проверки 
    графика продажи билетов на спектакль в Большой театр. \n
    Это означает, что Бот будет проверять раздел ПРАВИЛА ПРОДАЖИ БИЛЕТОВ 
    а именно
    График предварительной продажи билетов на ДЕКАБРЬ 2022 г. 

    По умолчанию бот ждет появления в графике продаж спектакля "Щелкунчик"
    проверка происходит после получения любого сообщения
    Напишите любое сообщение и бот проверит есть ли щелкунчик в расписании

    """)
# При желании эти настройки можно поменять. 
#    Как их поменять? - Введите команду help

#@dp.message_handler(commands=['help'])
#async def process_help_command(message: types.Message):
#    await message.reply("""Доступные настройки:
#    - Команда : описание
#    - delay : задержка между проверками данных на сайте, 
#    указывается в минутах
#    (минимальный интервал 30 минут, максимальный 1 раз в день)
#
#    - show : название спектакля, рекомендуется указывать 1, наиболее характерное слово
#    (даже если название спектакля состоит из нескольких слов)
#
#    Примеры использования команд(без кавычек и доп. символов):
#    delay 30
#    delay 180
#    show каренина
#    show озеро """)

@dp.message_handler() #commands = ("stock", "s"),commands_prefix = "/!"
async def record(message: types.message):
    result = main()
    await message.bot.send_message(message.from_user.id, result)


if __name__ == '__main__':
    executor.start_polling(dp)