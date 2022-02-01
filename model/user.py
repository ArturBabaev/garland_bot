class User:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.voltage = None
        self.voltage_gost =None
        self.degree_of_pollution = None
        self.lambda_e = None
        self.leakage_path_length = None
        self.insulator_plate_diameter = None
        self.insulator_utilization_factors = None
        self.garland_utilization_factors = None
        self.intermediate_result = None
        self.final_result = None
