import math

def quantity_insulators(lambda_e: float, U: int, L_i: int, k_i: float, k_k: float) -> int:
    """
    Функция для поиска количества изоляторов в гирлянде изоляторов

    :param lambda_e: (см/кВ) Удельная эффективная длина пути утечки
    :param U: (кВ) Наибольшее рабочее междуфазное напряжение по ГОСТ 721
    :param L_i: (мм) Длинна пути утечки одного изолятора по ТУ на изолятор
    :param k_i: Коэффициент использования изолятора
    :param k_k: Коэффициент использования состаной конструкции с паралельными или последовательно-паралельными ветвями
    :return: (шт.) Количество подвесных тарельчатых изоляторов
    """

    k = k_i * k_k
    L = lambda_e * 10 * U * k
    m = math.ceil(L / L_i)

    return m



# print(quantity_insulators(2, 363, 545, 1.25, 1.05))
