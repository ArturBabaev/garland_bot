from model.user import User
from repository.db_helper import DBHelper


class UserRepository:
    def __init__(self) -> None:
        self.conn = DBHelper().get_connector()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UserRepository, cls).__new__(cls)
        return cls.instance

    def set_user(self, user: User) -> None:
        insert_user_query = 'INSERT OR REPLACE INTO users (user_id, ' \
                            'voltage,' \
                            'voltage_gost,' \
                            'degree_of_pollution,' \
                            'lambda_e,' \
                            'leakage_path_length,' \
                            'insulator_plate_diameter,' \
                            'insulator_utilization_factors,' \
                            'garland_utilization_factors,' \
                            'intermediate_result,' \
                            'final_result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        args = (user.user_id, user.voltage, user.voltage_gost, user.degree_of_pollution, user.lambda_e,
                user.leakage_path_length, user.insulator_plate_diameter, user.insulator_utilization_factors,
                user.garland_utilization_factors, user.intermediate_result, user.final_result)

        self.conn.execute(insert_user_query, args)
        self.conn.commit()

    def get_user(self, user_id: int) -> User:
        select_query = 'SELECT user_id,' \
                       'voltage,' \
                       'voltage_gost,' \
                       'degree_of_pollution,' \
                       'lambda_e,' \
                       'leakage_path_length,' \
                       'insulator_plate_diameter,' \
                       'insulator_utilization_factors,' \
                       'garland_utilization_factors,' \
                       'intermediate_result,' \
                       'final_result FROM users WHERE users.user_id = (?)'

        args = (user_id,)
        fetch = self.conn.execute(select_query, args).fetchone()

        user = User(fetch[0])
        user.voltage = fetch[1]
        user.voltage_gost = fetch[2]
        user.degree_of_pollution = fetch[3]
        user.lambda_e = fetch[4]
        user.leakage_path_length = fetch[5]
        user.insulator_plate_diameter = fetch[6]
        user.insulator_utilization_factors = fetch[7]
        user.garland_utilization_factors = fetch[8]
        user.intermediate_result = fetch[9]
        user.final_result = fetch[10]

        return user
