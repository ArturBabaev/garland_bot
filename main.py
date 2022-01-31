import telebot
from telebot import types
from decouple import config
from controllers.start_controller import StartController
from repository.user_repository import UserRepository


TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)

user_repository = UserRepository()
start_controller = StartController(bot, user_repository)


@bot.message_handler(commands=['start'])
def start_command(message: types.Message) -> None:
    start_controller.process_start(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user = user_repository.get_user(call.message.chat.id)

    if call.data == '35':
        user.voltage_gost = 40.5
        user_repository.set_user(user)
        start_controller.voltage_callback(call)
    elif call.data == '110':
        user.voltage_gost = 126
        user_repository.set_user(user)
        start_controller.voltage_callback(call)
    elif call.data == '220':
        user.voltage_gost = 252
        user_repository.set_user(user)
        start_controller.voltage_callback(call)
    elif call.data == '330':
        user.voltage_gost = 363
        user_repository.set_user(user)
        start_controller.voltage_callback(call)
    elif call.data == '500':
        user.voltage_gost = 525
        user_repository.set_user(user)
        start_controller.voltage_callback(call)
    elif call.data == '750':
        user.voltage_gost = 787
        user_repository.set_user(user)
        start_controller.voltage_callback(call)
    elif call.data == '1' or call.data == '2' or call.data == '3' or call.data == '4':
        start_controller.pollution_callback(call)
    elif call.data == '1.9.45':
        start_controller.utilization_factors_1_9_45_callback(call.message)
    elif call.data == '1.9.46':
        start_controller.utilization_factors_1_9_46_callback(call.message)
    elif call.data == 'diptera':
        user.insulator_utilization_factors = 1.2
        user_repository.set_user(user)
    elif call.data == 'extended_rib':
        user.insulator_utilization_factors = 1.25
        user_repository.set_user(user)
    elif call.data == 'conical':
        user.insulator_utilization_factors = 1
        user_repository.set_user(user)
    elif call.data == 'bell_shaped':
        user.insulator_utilization_factors = 1.15
        user_repository.set_user(user)


bot.polling(none_stop=True, interval=0)
