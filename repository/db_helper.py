import sqlite3
from sqlite3 import Connection


class DBHelper:
    conn = sqlite3.connect('sqlite.db', check_same_thread=False)

    def get_connector(self) -> Connection:
        return self.conn

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBHelper, cls).__new__(cls)
            cls.instance.conn.enable_load_extension(True)
            cls.instance.setup()
        return cls.instance

    def setup(self):
        user_table_query = 'CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, ' \
                           'voltage INTEGER,' \
                           'voltage_gost REAL,' \
                           'degree_of_pollution INTEGER,' \
                           'lambda_e REAL,' \
                           'leakage_path_length INTEGER,' \
                           'insulator_plate_diameter INTEGER,' \
                           'insulator_utilization_factors REAL,' \
                           'garland_utilization_factors REAL)'

        self.conn.execute(user_table_query)
        self.conn.commit()
