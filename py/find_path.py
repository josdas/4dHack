

def find_path(start, finish, duration, duration_on_food, money, temp_place, cafe, time, ):
    """
    :param start: --- position tuple(float, float)
    :param finish: --- position tuple(float, float)
    :param duration: --- float
    :param duration_on_food: --- float
    :param money: --- float
    :param temp_place: --- [position]
    :param wish_place: --- [(place_name, time), ...]
    :return: [positions, ...]
    """
    def calc(positions):

