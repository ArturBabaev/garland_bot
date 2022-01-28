import telebot
from telebot import types
from decouple import config
from controllers.start_controller import StartController


TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)

start_controller = StartController(bot)


@bot.message_handler(commands=['start'])
def start_command(message: types.Message) -> None:
    start_controller.process_start(message)



bot.polling(none_stop=True, interval=0)