from telebot import types, TeleBot
from repository.user_repository import UserRepository
from model.user import User


class StartController:
    def __init__(self, bot: TeleBot, user_repository: UserRepository) -> None:
        self.bot = bot
        self.user_repository = user_repository

    def process_start(self, message: types.Message) -> None:
        self.user_repository.set_user(User(user_id=message.chat.id))

        text = 'Привет, я бот "GarlandBot". Я помогу Вам найти количество подвесных тарельчатых изоляторов ' \
               'в поддерживающих и натяжных гирляндах для ВЛ.'

        self.bot.send_message(message.chat.id, text=text)

        self.choose_voltage(message)

    def choose_voltage(self, message: types.Message) -> None:
        text = 'Выберите напряжение ВЛ.'

        keyboard = types.InlineKeyboardMarkup()

        key_35 = types.InlineKeyboardButton(text='35 кВ', callback_data='35')
        key_110 = types.InlineKeyboardButton(text='110 кВ', callback_data='110')
        key_220 = types.InlineKeyboardButton(text='220 кВ', callback_data='220')
        key_330 = types.InlineKeyboardButton(text='330 кВ', callback_data='330')
        key_500 = types.InlineKeyboardButton(text='500 кВ', callback_data='500')
        key_750 = types.InlineKeyboardButton(text='750 кВ', callback_data='750')

        keyboard.add(key_35, key_110, key_220, key_330, key_500, key_750)

        self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    def voltage_callback(self, call: types.CallbackQuery) -> None:
        user = self.user_repository.get_user(call.message.chat.id)
        user.voltage = int(call.data)
        self.user_repository.set_user(user)

        self.choose_pollution(call.message)

    def choose_pollution(self, message: types.Message) -> None:
        user = self.user_repository.get_user(message.chat.id)

        text = 'Вы выбрали напряжение ВЛ {} кВ. Выберите степень загрязнения атмосферы.'.format(user.voltage)

        keyboard = types.InlineKeyboardMarkup(row_width=4)

        key_1 = types.InlineKeyboardButton(text='1', callback_data='1')
        key_2 = types.InlineKeyboardButton(text='2', callback_data='2')
        key_3 = types.InlineKeyboardButton(text='3', callback_data='3')
        key_4 = types.InlineKeyboardButton(text='4', callback_data='4')

        keyboard.add(key_1, key_2, key_3, key_4)

        self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    def pollution_callback(self, call: types.CallbackQuery) -> None:
        user = self.user_repository.get_user(call.message.chat.id)
        user.degree_of_pollution = int(call.data)
        self.user_repository.set_user(user)

        text = 'Вы выбрали {} степень загрязнения.'.format(user.degree_of_pollution)

        if user.degree_of_pollution == 1:
            if user.voltage == 35:
                user.lambda_e = 1.9
            else:
                user.lambda_e = 1.6
        elif user.degree_of_pollution == 2:
            if user.voltage == 35:
                user.lambda_e = 2.35
            else:
                user.lambda_e = 2
        elif user.degree_of_pollution == 3:
            if user.voltage == 35:
                user.lambda_e = 3
            else:
                user.lambda_e = 2.5
        elif user.degree_of_pollution == 4:
            if user.voltage == 35:
                user.lambda_e = 3.5
            else:
                user.lambda_e = 3.1

        self.user_repository.set_user(user)

        self.bot.send_message(call.message.chat.id, text=text)

        self.choose_leakage_path_length(call.message)

    def choose_leakage_path_length(self, message: types.Message) -> None:
        text = 'Введите длину пути утечки одного изолятора по стандарту или техническим условиям ' \
               'на изолятор конкретного типа в мм.'

        self.bot.send_message(message.chat.id, text=text)

        self.bot.register_next_step_handler(message, self.leakage_path_length_callback)

    def leakage_path_length_callback(self, message: types.Message) -> None:
        try:
            user = self.user_repository.get_user(message.chat.id)
            user.leakage_path_length = int(message.text)
            self.user_repository.set_user(user)

            self.choose_insulator_utilization_factors(message)

        except ValueError:
            self.bot.send_message(message.chat.id, 'Введите целое число в мм, пожалуйста!')
            self.choose_leakage_path_length(message)

    def choose_insulator_utilization_factors(self, message: types.Message) -> None:
        text_1_9_45 = 'ПУЭ-7 п.1.9.45. Коэффициенты использования kи подвесных тарельчатых изоляторов по ГОСТ 27661 ' \
                      'со слабо развитой нижней поверхностью изоляционной детали следует определять в зависимости ' \
                      'от отношения длины пути утечки изолятора Lи к диаметру его тарелки D.'
        text_1_9_46 = 'ПУЭ-7 п.1.9.46. Коэффициенты использования kи подвесных тарельчатых изоляторов специального ' \
                      'исполнения с сильно развитой поверхностью следует определять в зависимости от конфигурация изолятора.'
        text = 'Выберите пункт ПУЭ-7 в соответсвии с которым необходимо определить коэффициент kи.'

        keyboard = types.InlineKeyboardMarkup()

        key_1_9_45 = types.InlineKeyboardButton(text='п.1.9.45', callback_data='1.9.45')
        key_1_9_46 = types.InlineKeyboardButton(text='п.1.9.46', callback_data='1.9.46')

        keyboard.add(key_1_9_45, key_1_9_46)

        self.bot.send_message(message.chat.id, text=text_1_9_45)
        self.bot.send_message(message.chat.id, text=text_1_9_46)
        self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    def utilization_factors_1_9_45_callback(self, message: types.Message) -> None:
        text = 'Вы выбрали п.1.9.45. Введите диаметр тарелки изолятора в мм.'

        self.bot.send_message(message.chat.id, text=text)

        self.bot.register_next_step_handler(message, self.choose_insulators_diameter)

    def utilization_factors_1_9_46_callback(self, message: types.Message) -> None:
        text = 'Вы выбрали п.1.9.46. Выберите конфигурацию изолятора.'

        keyboard = types.InlineKeyboardMarkup(row_width=1)

        configuration_1 = types.InlineKeyboardButton(text='Двукрылая', callback_data='diptera')
        configuration_2 = types.InlineKeyboardButton(text='С увеличенным вылетом ребра на нижней поверхности',
                                                     callback_data='extended_rib')
        configuration_3 = types.InlineKeyboardButton(text='Аэродинамического профиля (конусная, полусферическая)',
                                                     callback_data='conical')
        configuration_4 = types.InlineKeyboardButton(text='Колоколообразная с гладкой внутренней и ребристой '
                                                          'наружной поверхностями', callback_data='bell_shaped')

        keyboard.add(configuration_1, configuration_2, configuration_3, configuration_4)

        self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        self.choose_garland_utilization_factors(message)

    def choose_insulators_diameter(self, message: types.Message) -> None:
        try:
            user = self.user_repository.get_user(message.chat.id)
            user.insulator_plate_diameter = int(message.text)

            koeff = round((user.leakage_path_length / user.insulator_plate_diameter), 2)

            if 0.9 < koeff <= 1.05:
                user.insulator_utilization_factors = 1
            elif 1.05 < koeff <= 1.1:
                user.insulator_utilization_factors = 1.05
            elif 1.1 < koeff <= 1.2:
                user.insulator_utilization_factors = 1.1
            elif 1.2 < koeff <= 1.3:
                user.insulator_utilization_factors = 1.15
            elif 1.3 < koeff <= 1.4:
                user.insulator_utilization_factors = 1.2

            self.user_repository.set_user(user)

            self.choose_garland_utilization_factors(message)

        except ValueError:
            self.bot.send_message(message.chat.id, 'Введите целое число в мм, пожалуйста!')
            self.utilization_factors_1_9_45_callback(message)

    def choose_garland_utilization_factors(self, message: types.Message) -> None:
        text_1_9_49 = 'ПУЭ-7 п.1.9.49. Коэффициенты использования kк одноцепных гирлянд и одиночных опорных колонок, ' \
                      'составленных из однотипных изоляторов, следует принимать равными 1,0.'
        text_1_9_50 = 'ПУЭ-7 п.1.9.50. Коэффициенты использования kк составных конструкций с параллельными ветвями ' \
                      '(без перемычек), составленных из однотипных элементов (двухцепных и многоцепных ' \
                      'поддерживающих и натяжных гирлянд, двух- и многостоечных колонок), следует определять ' \
                      'в соответсвии с количеством параллельных ветвей.'
        text_1_9_51 = 'ПУЭ-7 п.1.9.51. Коэффициенты использования kк А-образных и V-образных гирлянд с одноцепными ' \
                      'ветвями следует принимать равными 1,0.'
        text_1_9_52 = 'ПУЭ-7 п.1.9.52. Коэффициенты использования kк составных конструкций с ' \
                      'последовательно-параллельными ветвями, составленными из изоляторов одного типа ' \
                      '(гирлянд типа Y, опорных колонок с различным числом параллельных ветвей по высоте, ' \
                      'а также подстанционных аппаратов с растяжками), следует принимать равными 1,1.'

        text = 'Выберите пункт ПУЭ-7 в соответсвии с которым необходимо определить коэффициент kк.'
