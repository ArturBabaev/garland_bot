from telebot import types, TeleBot


class StartController:
    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot

    def process_start(self, message: types.Message) -> None:
        text = 'Привет, я бот "GarlandBot". Я помогу Вам найти количество подвесных тарельчатых изоляторов ' \
               'в поддерживающих и натяжных гирляндах для ВЛ.'

        self.bot.send_message(message.chat.id, text=text)
