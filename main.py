from telegram.ext import Updater
from telegram.ext import InlineQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler
from telegram import ReplyKeyboardRemove

import telegram
import requests
import re
import logging

import tokenconfig

#logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)
logger = logging.getLogger(__name__)

TOKEN = tokenconfig.TOKEN

def start_reply(bot, update):
    chat_id = update.message.chat_id
    button_yes = telegram.KeyboardButton(text="Да, я знаю, что такое Forex")
    button_no = telegram.KeyboardButton(text="Нет, расскажи про Forex")
    buttons = [button_yes, button_no]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id, 
                  text="Ты знаешь, что такое Forex?", 
                  reply_markup=reply_markup)


def forex_yes_handler(bot, update):
    chat_id = update.message.chat_id
    button_forex_pamm = telegram.KeyboardButton(text="Расскажи про ПАММ")
    button_forex_manual = telegram.KeyboardButton(text="Расскажи про ручную торговлю")
    button_forex_robot = telegram.KeyboardButton(text="Расскажи про роботизированную торговлю")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_forex_pamm], [button_forex_manual], [button_forex_robot]])
    bot.send_message(chat_id=chat_id, 
                  text="На форексе есть 3 типа заработка: ПАММ счет (доверительное управление), ручная торговля и робототизированная торговля", 
                  reply_markup=reply_markup)

def forex_no_handler(bot, update):
    chat_id = update.message.chat_id
    button_forex_moreinfo = telegram.KeyboardButton(text="Хочу узнать больше про Форекс")
    button_forex_gotit = telegram.KeyboardButton(text="Теперь понятно, давай дальше")
    
    buttons = [button_forex_moreinfo, button_forex_gotit]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id, 
                  text="Тут инфа про форекс, инфографики, объем рынка и т.д.", 
                  reply_markup=reply_markup)

def forex_moreinfo_handler(bot, update):
    chat_id = update.message.chat_id
    button_forex_gotit = telegram.KeyboardButton(text="Теперь понятно, давай дальше")
    
    buttons = [button_forex_gotit]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id, 
                  text="Тут еще больше инфы про форекс, ссылки на вики или еще куда-то для новичков и т.д.", 
                  reply_markup=reply_markup)

def forex_pamm_handler(bot, update):
    chat_id = update.message.chat_id
    button_forex_manual = telegram.KeyboardButton(text="Расскажи про ручную торговлю")
    button_forex_robot = telegram.KeyboardButton(text="Расскажи про роботизированную торговлю")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_forex_manual], [button_forex_robot]])
    bot.send_message(chat_id=chat_id, 
                  text="ПАММ счета - доверительное управление... инфа про ПАММы", 
                  reply_markup=reply_markup)

def forex_manual_handler(bot, update):
    chat_id = update.message.chat_id
    button_forex_pamm = telegram.KeyboardButton(text="Расскажи про ПАММ")
    button_forex_robot = telegram.KeyboardButton(text="Расскажи про роботизированную торговлю")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_forex_pamm], [button_forex_robot]])
    bot.send_message(chat_id=chat_id, 
                  text="Инфа по ручной торговле на форекс...", 
                  reply_markup=reply_markup)

def forex_robot_handler(bot, update):
    chat_id = update.message.chat_id
    button_ai = telegram.KeyboardButton(text="Что за искусственный интеллект?")
    button_davinci = telegram.KeyboardButton(text="Подробнее про робота DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_ai], [button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text="Роботизированная торговля - с помощью так называемых советников. Наш советник, мы его назвали робот DaVinci, не просто программа, а искусственный интеллект, который обучается и тд и тп.", 
                  reply_markup=reply_markup)

def forex_ai_handler(bot, update):
    chat_id = update.message.chat_id
    button_ai_more = telegram.KeyboardButton(text="Хочу знать больше про искусственный интеллект и нейросети")
    button_davinci = telegram.KeyboardButton(text="Подробнее про робота DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_ai_more], [button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text="Искусственный интеллект, нейросети и т.д. Основные принципы и информация.", 
                  reply_markup=reply_markup)

def forex_davinci_handler(bot, update):
    chat_id = update.message.chat_id
    button_brokers = telegram.KeyboardButton(text="Про брокеров")
    button_stats = telegram.KeyboardButton(text="Статистика реальных счетов")
    button_davinci_more = telegram.KeyboardButton(text="Еще детальней про DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_brokers], [button_stats], [button_davinci_more]])
    bot.send_message(chat_id=chat_id, 
                  text="Инфа про робота давинчи, про брокеров, на которых он работает, про статистику реальных счетов и про гибкость выбора стратегии и стоимости самого робота...", 
                  reply_markup=reply_markup)

def forex_brokers_handler(bot, update):
    chat_id = update.message.chat_id
    button_whoisbrokers = telegram.KeyboardButton(text="Кто такие брокеры?")
    button_whythese = telegram.KeyboardButton(text="Почему именно на этих брокерах?")
    button_davinci = telegram.KeyboardButton(text="Подробнее про робота DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_whoisbrokers], [button_whythese], [button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text="DaVinci работает на двух брокерах: Roboforex, Forex4You...", 
                  reply_markup=reply_markup)

def forex_whoisbrokers_handler(bot, update):
    chat_id = update.message.chat_id
    button_whythese = telegram.KeyboardButton(text="Почему именно на этих брокерах?")
    button_davinci = telegram.KeyboardButton(text="Подробнее про робота DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_whythese], [button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text="Брокер - это ...", 
                  reply_markup=reply_markup)

def forex_whythesebrokers_handler(bot, update):
    chat_id = update.message.chat_id
    button_whoisbrokers = telegram.KeyboardButton(text="Кто такие брокеры?")
    button_davinci = telegram.KeyboardButton(text="Подробнее про робота DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_whoisbrokers], [button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text="Команда DaVinci тщательно выбирает брокеров, с которыми работает. Используется много критериев, таких как: ... Эти брокеры удовлетворяют всем условиям и входят в ТОП-10 брокеров в мире по версии ...", 
                  reply_markup=reply_markup)

def forex_stats_handler(bot, update):
    chat_id = update.message.chat_id
    button_myfxbook = telegram.KeyboardButton(text="Что за myfxbook? Можно ему доверять?")
    button_stats_more = telegram.KeyboardButton(text="Хочу больше аналитики реальных счетов!")
    button_davinci = telegram.KeyboardButton(text="Подробнее про робота DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_myfxbook], [button_stats_more], [button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text="Большинство наших партнеров завели счет на сервисе myfxbook...Вот скрины нескоторых реальных счетов:...тут фотки", 
                  reply_markup=reply_markup)

def forex_myfxbook_handler(bot, update):
    chat_id = update.message.chat_id
    button_stats_more = telegram.KeyboardButton(text="Хочу больше аналитики реальных счетов!")
    button_davinci = telegram.KeyboardButton(text="Подробнее про робота DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_stats_more], [button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text="MyFxBook - это независимый сервис статистики, который работает с любыми брокерскими счетами форекс...Инфа про myfxbook и почему ему можно доверять...", 
                  reply_markup=reply_markup)

def forex_stats_more_handler(bot, update):
    chat_id = update.message.chat_id
    button_myfxbook = telegram.KeyboardButton(text="Что за myfxbook? Можно ему доверять?")
    button_davinci = telegram.KeyboardButton(text="Подробнее про робота DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_myfxbook], [button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text="Больше аналитики, скрины, фотки, ссылки на myfxbook...", 
                  reply_markup=reply_markup)

def forex_davinci_more_handler(bot, update):
    chat_id = update.message.chat_id
    button_strategies = telegram.KeyboardButton(text="Стратегии заработка с DaVinci")
    button_developers = telegram.KeyboardButton(text="Про разработчиков")
    button_community = telegram.KeyboardButton(text="Про поддержку и сообщество")
    button_howmuch = telegram.KeyboardButton(text="Сколько стоит робот?")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_strategies], [button_developers], [button_community], [button_howmuch]])
    bot.send_message(chat_id=chat_id, 
                  text="Больше инфы про давинчи, про стратегии, стоимости, команду, поддержку, сообщество и т.д.", 
                  reply_markup=reply_markup)

def forex_davinci_strategies_handler(bot, update):
    chat_id = update.message.chat_id
    button_light = telegram.KeyboardButton(text="Про ЛАЙТ")
    button_optima = telegram.KeyboardButton(text="Про ОПТИМУ")
    button_maximum = telegram.KeyboardButton(text="Про МАКСИМУМ")
    button_turbo = telegram.KeyboardButton(text="Про ТУРБО")
    button_davinci_more = telegram.KeyboardButton(text="Еще детальней про DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_light, button_optima, button_maximum, button_turbo], [button_davinci_more]])
    bot.send_message(chat_id=chat_id, 
                  text="Есть лайт (3-5% прибыли), оптима 5-10%, максимум 10-20%, турбо 20-30% в месяц.", 
                  reply_markup=reply_markup)

def forex_davinci_light_handler(bot, update):
    chat_id = update.message.chat_id
    button_optima = telegram.KeyboardButton(text="Про ОПТИМУ")
    button_maximum = telegram.KeyboardButton(text="Про МАКСИМУМ")
    button_turbo = telegram.KeyboardButton(text="Про ТУРБО")
    button_davinci_more = telegram.KeyboardButton(text="Еще детальней про DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_optima, button_maximum, button_turbo], [button_davinci_more]])
    bot.send_message(chat_id=chat_id, 
                  text="Инфа про лайт (3-5% прибыли).", 
                  reply_markup=reply_markup)

def forex_davinci_optima_handler(bot, update):
    chat_id = update.message.chat_id
    button_light = telegram.KeyboardButton(text="Про ЛАЙТ")
    button_maximum = telegram.KeyboardButton(text="Про МАКСИМУМ")
    button_turbo = telegram.KeyboardButton(text="Про ТУРБО")
    button_davinci_more = telegram.KeyboardButton(text="Еще детальней про DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_light, button_maximum, button_turbo], [button_davinci_more]])
    bot.send_message(chat_id=chat_id, 
                  text="Инфа про оптиму 5-10%.", 
                  reply_markup=reply_markup)

def forex_davinci_maximum_handler(bot, update):
    chat_id = update.message.chat_id
    button_light = telegram.KeyboardButton(text="Про ЛАЙТ")
    button_optima = telegram.KeyboardButton(text="Про ОПТИМУ")
    button_turbo = telegram.KeyboardButton(text="Про ТУРБО")
    button_davinci_more = telegram.KeyboardButton(text="Еще детальней про DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_light, button_optima, button_turbo], [button_davinci_more]])
    bot.send_message(chat_id=chat_id, 
                  text="Инфа про максимум: 10-20%", 
                  reply_markup=reply_markup)

def forex_davinci_turbo_handler(bot, update):
    chat_id = update.message.chat_id
    button_light = telegram.KeyboardButton(text="Про ЛАЙТ")
    button_optima = telegram.KeyboardButton(text="Про ОПТИМУ")
    button_maximum = telegram.KeyboardButton(text="Про МАКСИМУМ")
    button_davinci_more = telegram.KeyboardButton(text="Еще детальней про DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_light, button_optima, button_maximum], [button_davinci_more]])
    bot.send_message(chat_id=chat_id, 
                  text="Инфа про турбо 20-30% в месяц.", 
                  reply_markup=reply_markup)

def forex_davinci_developers_handler(bot, update):
    chat_id = update.message.chat_id
    button_strategies = telegram.KeyboardButton(text="Стратегии заработка с DaVinci")
    button_community = telegram.KeyboardButton(text="Про поддержку и сообщество")
    button_howmuch = telegram.KeyboardButton(text="Сколько стоит робот?")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_strategies], [button_community], [button_howmuch]])
    bot.send_message(chat_id=chat_id, 
                  text="3 основателя/разработчика с командой из 10 человек - с огромным опытом трейдинга, обработки информации, bigdata, data science и т.д.", 
                  reply_markup=reply_markup)

def forex_davinci_community_handler(bot, update):
    chat_id = update.message.chat_id
    button_strategies = telegram.KeyboardButton(text="Стратегии заработка с DaVinci")
    button_developers = telegram.KeyboardButton(text="Про разработчиков")
    button_howmuch = telegram.KeyboardButton(text="Сколько стоит робот?")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_strategies], [button_developers], [button_howmuch]])
    bot.send_message(chat_id=chat_id, 
                  text="Поддержка 24/7 от всех участников сообщества и от разработчиков и их команды. Есть офисы, представительства, телефоны и т.д.", 
                  reply_markup=reply_markup)

def forex_davinci_howmuch_handler(bot, update):
    chat_id = update.message.chat_id
    button_letsbuy = telegram.KeyboardButton(text="Я согласен! Что дальше?")
    button_davinci_more = telegram.KeyboardButton(text="Еще детальней про DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_letsbuy], [button_davinci_more]])
    bot.send_message(chat_id=chat_id, 
                  text="Стоимость отличается суммой, которой торгует робот, а соответственно и максимальным заработком. Стоимость за год: $250 - до $2000, $500 - до $5000, $1000 - до $15000 (2 робота), $2000 - до $100000 (2 робота)", 
                  reply_markup=reply_markup)

def forex_davinci_letsbuy_handler(bot, update):
    chat_id = update.message.chat_id
    button_letsbuy = telegram.KeyboardButton(text="Я согласен! Что дальше?")
    button_davinci_more = telegram.KeyboardButton(text="Еще детальней про DaVinci")

    reply_markup = telegram.ReplyKeyboardMarkup([[button_letsbuy], [button_davinci_more]])
    bot.send_message(chat_id=chat_id, 
                  text="Регистрируйся по этой ссылке: ... - обращайся по любым вопросам по следующим контактам: ...", 
                  reply_markup=reply_markup)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    # Commands
    dp.add_handler(CommandHandler('start', start_reply))

    # CallbackQueryHandler

    # Messages
    dp.add_handler(MessageHandler(Filters.regex(r'Да, я знаю, что такое Forex'), forex_yes_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Нет, расскажи про Forex'), forex_no_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Хочу узнать больше про Форекс'), forex_moreinfo_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Теперь понятно, давай дальше'), forex_yes_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Расскажи про ПАММ'), forex_pamm_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Расскажи про ручную торговлю'), forex_manual_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Расскажи про роботизированную торговлю'), forex_robot_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Что за искусственный интеллект?'), forex_ai_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Подробнее про робота DaVinci'), forex_davinci_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Про брокеров'), forex_brokers_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Кто такие брокеры?'), forex_whoisbrokers_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Почему именно на этих брокерах?'), forex_whythesebrokers_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Статистика реальных счетов'), forex_stats_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Что за myfxbook? Можно ему доверять?'), forex_myfxbook_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Хочу больше аналитики реальных счетов!'), forex_stats_more_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Еще детальней про DaVinci'), forex_davinci_more_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Стратегии заработка с DaVinci'), forex_davinci_strategies_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Про разработчиков'), forex_davinci_developers_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Про поддержку и сообщество'), forex_davinci_community_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Сколько стоит робот?'), forex_davinci_howmuch_handler))

    dp.add_handler(MessageHandler(Filters.regex(r'Про ЛАЙТ'), forex_davinci_light_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Про ОПТИМУ'), forex_davinci_optima_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Про МАКСИМУМ'), forex_davinci_maximum_handler))
    dp.add_handler(MessageHandler(Filters.regex(r'Про ТУРБО'), forex_davinci_turbo_handler))

    dp.add_handler(MessageHandler(Filters.regex(r'Я согласен! Что дальше?'), forex_davinci_letsbuy_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()