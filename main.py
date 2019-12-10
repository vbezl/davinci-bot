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
import locales
from locales import _t

#logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)
logger = logging.getLogger(__name__)

TOKEN = tokenconfig.TOKEN
texts = locales.texts

def start_reply(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_yes = telegram.KeyboardButton(text=_t("Да, я знаю, что такое Forex", lang))
    button_no = telegram.KeyboardButton(text=_t("Нет, расскажи про Forex", lang))
    buttons = [button_yes, button_no]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Ты знаешь, что такое Forex?", lang), 
                  reply_markup=reply_markup)


def forex_yes_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_forex_pamm = telegram.KeyboardButton(text=_t("Расскажи про ПАММ", lang))
    button_forex_manual = telegram.KeyboardButton(text=_t("Расскажи про ручную торговлю", lang))
    button_forex_robot = telegram.KeyboardButton(text=_t("Расскажи про роботизированную торговлю", lang))
    button_straight_to_davinci = telegram.KeyboardButton(text=_t("Всё знаю, давай дальше", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_forex_pamm], [button_forex_manual], [button_forex_robot], [button_straight_to_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("На форексе есть 3 типа заработка...", lang), 
                  reply_markup=reply_markup)

def forex_no_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_forex_moreinfo = telegram.KeyboardButton(text=_t("Хочу узнать больше про Форекс", lang))
    button_forex_gotit = telegram.KeyboardButton(text=_t("Теперь понятно, давай дальше", lang))
    
    buttons = [button_forex_moreinfo, button_forex_gotit]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Тут инфа про форекс, инфографики, объем рынка и т.д.", lang), 
                  reply_markup=reply_markup)

def forex_moreinfo_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_forex_gotit = telegram.KeyboardButton(text=_t("Теперь понятно, давай дальше", lang))
    
    buttons = [button_forex_gotit]
    reply_markup = telegram.ReplyKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Тут еще больше инфы про форекс, ссылки на вики или еще куда-то для новичков и т.д.", lang), 
                  reply_markup=reply_markup)

def forex_pamm_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_forex_manual = telegram.KeyboardButton(text=_t("Расскажи про ручную торговлю", lang))
    button_forex_robot = telegram.KeyboardButton(text=_t("Расскажи про роботизированную торговлю", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_forex_manual], [button_forex_robot]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("ПАММ счета - доверительное управление... инфа про ПАММы", lang), 
                  reply_markup=reply_markup)

def forex_manual_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_forex_pamm = telegram.KeyboardButton(text=_t("Расскажи про ПАММ", lang))
    button_forex_robot = telegram.KeyboardButton(text=_t("Расскажи про роботизированную торговлю", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_forex_pamm], [button_forex_robot]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Инфа по ручной торговле на форекс...", lang), 
                  reply_markup=reply_markup)

def forex_robot_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_ai = telegram.KeyboardButton(text=_t("Что за искусственный интеллект?", lang))
    button_davinci = telegram.KeyboardButton(text=_t("Подробнее про робота DaVinci", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_ai], [button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Роботизированная торговля - это...", lang), 
                  reply_markup=reply_markup)

def forex_ai_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    #button_ai_more = telegram.KeyboardButton(text=_t("Хочу знать больше про искусственный интеллект и нейросети", lang))
    button_davinci = telegram.KeyboardButton(text=_t("Подробнее про робота DaVinci", lang))

    #reply_markup = telegram.ReplyKeyboardMarkup([[button_ai_more], [button_davinci]])
    reply_markup = telegram.ReplyKeyboardMarkup([[button_davinci]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Искусственный интеллект, нейросети и т.д. Основные принципы и информация.", lang), 
                  reply_markup=reply_markup)

def forex_davinci_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_brokers = telegram.KeyboardButton(text=_t("Про брокеров", lang))
    button_stats = telegram.KeyboardButton(text=_t("Статистика реальных счетов", lang))
    button_davinci_more = telegram.KeyboardButton(text=_t("Еще детальней про DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_davinci_more], [button_stats], [button_brokers], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Инфа про робота давинчи, про брокеров...", lang), 
                  reply_markup=reply_markup)

def forex_brokers_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_whoisbrokers = telegram.KeyboardButton(text=_t("Кто такие брокеры?", lang))
    button_whythese = telegram.KeyboardButton(text=_t("Почему именно на этих брокерах?", lang))
    button_davinci = telegram.KeyboardButton(text=_t("Подробнее про робота DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_whoisbrokers], [button_whythese], [button_davinci], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("DaVinci работает на двух брокерах: Roboforex, Forex4You...", lang), 
                  reply_markup=reply_markup)

def forex_whoisbrokers_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_whythese = telegram.KeyboardButton(text=_t("Почему именно на этих брокерах?", lang))
    button_davinci = telegram.KeyboardButton(text=_t("Подробнее про робота DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_whythese], [button_davinci], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Брокер - это ...", lang), 
                  reply_markup=reply_markup)

def forex_whythesebrokers_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_whoisbrokers = telegram.KeyboardButton(text=_t("Кто такие брокеры?", lang))
    button_davinci = telegram.KeyboardButton(text=_t("Подробнее про робота DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_whoisbrokers], [button_davinci], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Команда DaVinci тщательно выбирает брокеров...", lang), 
                  reply_markup=reply_markup)

def forex_stats_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_myfxbook = telegram.KeyboardButton(text=_t("Что за myfxbook? Можно ему доверять?", lang))
    button_stats_more = telegram.KeyboardButton(text=_t("Хочу больше аналитики реальных счетов!", lang))
    button_davinci = telegram.KeyboardButton(text=_t("Подробнее про робота DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_myfxbook], [button_stats_more], [button_davinci], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Большинство наших партнеров завели счет на сервисе myfxbook...", lang), 
                  reply_markup=reply_markup)

def forex_myfxbook_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_stats_more = telegram.KeyboardButton(text=_t("Хочу больше аналитики реальных счетов!", lang))
    button_davinci = telegram.KeyboardButton(text=_t("Подробнее про робота DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_stats_more], [button_davinci], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("MyFxBook - это независимый сервис статистики...", lang), 
                  reply_markup=reply_markup)

def forex_stats_more_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_myfxbook = telegram.KeyboardButton(text=_t("Что за myfxbook? Можно ему доверять?", lang))
    button_davinci = telegram.KeyboardButton(text=_t("Подробнее про робота DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_myfxbook], [button_davinci], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Больше аналитики, скрины, фотки, ссылки на myfxbook...", lang), 
                  reply_markup=reply_markup)

def forex_davinci_more_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_strategies = telegram.KeyboardButton(text=_t("Стратегии заработка с DaVinci", lang))
    button_developers = telegram.KeyboardButton(text=_t("Про разработчиков", lang))
    button_community = telegram.KeyboardButton(text=_t("Про поддержку и сообщество", lang))
    button_howmuch = telegram.KeyboardButton(text=_t("Сколько стоит робот?", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_strategies], [button_developers], [button_community], [button_howmuch], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Больше инфы про давинчи, про стратегии, стоимости, команду, поддержку, сообщество и т.д.", lang), 
                  reply_markup=reply_markup)

def forex_davinci_strategies_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_light = telegram.KeyboardButton(text=_t("Про ЛАЙТ", lang))
    button_optima = telegram.KeyboardButton(text=_t("Про ОПТИМУ", lang))
    button_maximum = telegram.KeyboardButton(text=_t("Про МАКСИМУМ", lang))
    button_turbo = telegram.KeyboardButton(text=_t("Про ТУРБО", lang))
    button_davinci_more = telegram.KeyboardButton(text=_t("Еще детальней про DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_light, button_optima, button_maximum, button_turbo], [button_davinci_more], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Есть лайт, оптима, максимум, турбо...", lang), 
                  reply_markup=reply_markup)

def forex_davinci_light_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_optima = telegram.KeyboardButton(text=_t("Про ОПТИМУ", lang))
    button_maximum = telegram.KeyboardButton(text=_t("Про МАКСИМУМ", lang))
    button_turbo = telegram.KeyboardButton(text=_t("Про ТУРБО", lang))
    button_davinci_more = telegram.KeyboardButton(text=_t("Еще детальней про DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_optima, button_maximum, button_turbo], [button_davinci_more], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Инфа про лайт (3-5% прибыли).", lang), 
                  reply_markup=reply_markup)

def forex_davinci_optima_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_light = telegram.KeyboardButton(text=_t("Про ЛАЙТ", lang))
    button_maximum = telegram.KeyboardButton(text=_t("Про МАКСИМУМ", lang))
    button_turbo = telegram.KeyboardButton(text=_t("Про ТУРБО", lang))
    button_davinci_more = telegram.KeyboardButton(text=_t("Еще детальней про DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_light, button_maximum, button_turbo], [button_davinci_more], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Инфа про оптиму 5-10%.", lang), 
                  reply_markup=reply_markup)

def forex_davinci_maximum_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_light = telegram.KeyboardButton(text=_t("Про ЛАЙТ", lang))
    button_optima = telegram.KeyboardButton(text=_t("Про ОПТИМУ", lang))
    button_turbo = telegram.KeyboardButton(text=_t("Про ТУРБО", lang))
    button_davinci_more = telegram.KeyboardButton(text=_t("Еще детальней про DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_light, button_optima, button_turbo], [button_davinci_more], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Инфа про максимум: 10-20%", lang), 
                  reply_markup=reply_markup)

def forex_davinci_turbo_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_light = telegram.KeyboardButton(text=_t("Про ЛАЙТ", lang))
    button_optima = telegram.KeyboardButton(text=_t("Про ОПТИМУ", lang))
    button_maximum = telegram.KeyboardButton(text=_t("Про МАКСИМУМ", lang))
    button_davinci_more = telegram.KeyboardButton(text=_t("Еще детальней про DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_light, button_optima, button_maximum], [button_davinci_more], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Инфа про турбо 20-30% в месяц.", lang), 
                  reply_markup=reply_markup)

def forex_davinci_developers_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_strategies = telegram.KeyboardButton(text=_t("Стратегии заработка с DaVinci", lang))
    button_community = telegram.KeyboardButton(text=_t("Про поддержку и сообщество", lang))
    button_howmuch = telegram.KeyboardButton(text=_t("Сколько стоит робот?", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_strategies], [button_community], [button_howmuch], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("3 основателя/разработчика с командой из 10 человек...", lang), 
                  reply_markup=reply_markup)

def forex_davinci_community_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_strategies = telegram.KeyboardButton(text=_t("Стратегии заработка с DaVinci", lang))
    button_developers = telegram.KeyboardButton(text=_t("Про разработчиков", lang))
    button_howmuch = telegram.KeyboardButton(text=_t("Сколько стоит робот?", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_strategies], [button_developers], [button_howmuch], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Поддержка 24/7 от всех участников сообщества и от разработчиков и их команды...", lang), 
                  reply_markup=reply_markup)

def forex_davinci_howmuch_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_letsbuy = telegram.KeyboardButton(text=_t("Я согласен! Что дальше?", lang))
    button_davinci_more = telegram.KeyboardButton(text=_t("Еще детальней про DaVinci", lang))
    button_contact_human = telegram.KeyboardButton(text=_t("Хочу поговорить с человеком", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_letsbuy], [button_davinci_more], [button_contact_human]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Стоимость отличается суммой, которой торгует робот...", lang), 
                  reply_markup=reply_markup)

def forex_davinci_letsbuy_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code
    button_letsbuy = telegram.KeyboardButton(text=_t("Я согласен! Что дальше?", lang))
    button_davinci_more = telegram.KeyboardButton(text=_t("Еще детальней про DaVinci", lang))

    reply_markup = telegram.ReplyKeyboardMarkup([[button_letsbuy], [button_davinci_more]])
    bot.send_message(chat_id=chat_id, 
                  text=_t("Регистрируйся по этой ссылке...", lang), 
                  reply_markup=reply_markup)

def forex_other_text_handler(bot, update):
    chat_id = update.message.chat_id
    lang = update.message.from_user.language_code

    bot.send_message(chat_id=chat_id, 
                  text=_t("Это бот, пожалуйста используйте меню ниже...", lang))


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    # Commands
    dp.add_handler(CommandHandler('start', start_reply))

    # CallbackQueryHandler

    # Messages
    dp.add_handler(MessageHandler(Filters.regex(texts['Да, я знаю, что такое Forex']['ru']), forex_yes_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Да, я знаю, что такое Forex']['en']), forex_yes_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Нет, расскажи про Forex']['ru']), forex_no_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Нет, расскажи про Forex']['en']), forex_no_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Хочу узнать больше про Форекс']['ru']), forex_moreinfo_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Хочу узнать больше про Форекс']['en']), forex_moreinfo_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Теперь понятно, давай дальше']['ru']), forex_yes_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Теперь понятно, давай дальше']['en']), forex_yes_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Расскажи про ПАММ']['ru']), forex_pamm_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Расскажи про ПАММ']['en']), forex_pamm_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Расскажи про ручную торговлю']['ru']), forex_manual_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Расскажи про ручную торговлю']['en']), forex_manual_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Расскажи про роботизированную торговлю']['ru']), forex_robot_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Расскажи про роботизированную торговлю']['en']), forex_robot_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Всё знаю, давай дальше']['ru']), forex_robot_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Всё знаю, давай дальше']['en']), forex_robot_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Что за искусственный интеллект?']['ru']), forex_ai_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Что за искусственный интеллект?']['en']), forex_ai_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Подробнее про робота DaVinci']['ru']), forex_davinci_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Подробнее про робота DaVinci']['en']), forex_davinci_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про брокеров']['ru']), forex_brokers_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про брокеров']['en']), forex_brokers_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Кто такие брокеры?']['ru']), forex_whoisbrokers_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Кто такие брокеры?']['en']), forex_whoisbrokers_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Почему именно на этих брокерах?']['ru']), forex_whythesebrokers_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Почему именно на этих брокерах?']['en']), forex_whythesebrokers_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Статистика реальных счетов']['ru']), forex_stats_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Статистика реальных счетов']['en']), forex_stats_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Что за myfxbook? Можно ему доверять?']['ru']), forex_myfxbook_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Что за myfxbook? Можно ему доверять?']['en']), forex_myfxbook_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Хочу больше аналитики реальных счетов!']['ru']), forex_stats_more_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Хочу больше аналитики реальных счетов!']['en']), forex_stats_more_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Еще детальней про DaVinci']['ru']), forex_davinci_more_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Еще детальней про DaVinci']['en']), forex_davinci_more_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Стратегии заработка с DaVinci']['ru']), forex_davinci_strategies_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Стратегии заработка с DaVinci']['en']), forex_davinci_strategies_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про разработчиков']['ru']), forex_davinci_developers_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про разработчиков']['en']), forex_davinci_developers_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про поддержку и сообщество']['ru']), forex_davinci_community_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про поддержку и сообщество']['en']), forex_davinci_community_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Сколько стоит робот?']['ru']), forex_davinci_howmuch_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Сколько стоит робот?']['en']), forex_davinci_howmuch_handler))

    dp.add_handler(MessageHandler(Filters.regex(texts['Про ЛАЙТ']['ru']), forex_davinci_light_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про ЛАЙТ']['en']), forex_davinci_light_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про ОПТИМУ']['ru']), forex_davinci_optima_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про ОПТИМУ']['en']), forex_davinci_optima_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про МАКСИМУМ']['ru']), forex_davinci_maximum_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про МАКСИМУМ']['en']), forex_davinci_maximum_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про ТУРБО']['ru']), forex_davinci_turbo_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Про ТУРБО']['en']), forex_davinci_turbo_handler))

    dp.add_handler(MessageHandler(Filters.regex(texts['Я согласен! Что дальше?']['ru']), forex_davinci_letsbuy_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Я согласен! Что дальше?']['en']), forex_davinci_letsbuy_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Хочу поговорить с человеком']['ru']), forex_davinci_letsbuy_handler))
    dp.add_handler(MessageHandler(Filters.regex(texts['Хочу поговорить с человеком']['en']), forex_davinci_letsbuy_handler))

    dp.add_handler(MessageHandler(Filters.regex(".*"), forex_other_text_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()