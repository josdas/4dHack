
def find_path(gmap, start, finish, duration, duration_on_foot, money, temp_place, cafe_type, time_cafe):
    """
    :param start: --- position tuple(float, float)
    :param finish: --- position tuple(float, float)
    :param duration: --- float
    :param duration_on_foot: --- float
    :param money: --- float
    :param temp_place: --- [position]
    :param cafe_type: --- str
    :param time_cafe: --- float or None
    :return: [positions, ...]
    """

    def calc_score(places):
        score = 0
        spent_money = 0
        visited = []
        spent_time = 0
        spent_time_on_foot = 0

        if places[0].position == start:  # если маршрут начинается пешком, то это неплохо
            score += 10
        if places[-1].position == finish:  # если маршрут коначается пешком, то это неплохо
            score += 10

        for place in places:
            place_type = place.info.get('type', None)
            if place_type == cafe_type and cafe_type is not None:  # если мы хотим сходить в кафе и сходили
                score -= (spent_time - time_cafe) ** 2 * 0.05  #
                score += 300  # посетил кафе? ты нереально крут
                spent_time += 20  # в среднем 20 минут сидишь, можно сделать разные времена для разных мест # todo
                spent_money += place.info.get('money', 0)
                score += place.info.get('rating', 0) * 30  # рейтинг тоже может увеличить очки
            if place_type in temp_place:
                visited.append(place_type)
                spent_time += 10  # гуляешь в каком-то месте 10 минут
                spent_time_on_foot += 10  # походили 10 минут
                score += place.info.get('rating', 0) * 10  # рейтинг влияет чуть хуже
        if money == 0 and spent_money > 0:  # если мы не хотели тратить, но потратили, то это очень плохо
            score -= 100
        if money - spent_money < 0:  # если мы потратили больше, чем планировали, то тоже плохо
            score -= 10000

        score += len(set(temp_place) & set(visited)) * 40  # считаем очки за посещенные цели

        spent_time_on_foot += gmap.get_duration_way(places[1:-1])  # считаем время между точками пешком

        dif_time_on_foot = duration_on_foot - spent_time_on_foot  # считаем штраф за время на ногах
        if dif_time_on_foot < 0:
            score -= dif_time_on_foot ** 2 * 0.03
        else:
            score -= abs(dif_time_on_foot) ** 3 * 0.005

        dif_time = duration - spent_time  # считаем штраф за время
        if dif_time < 0:
            score -= dif_time ** 2 * 0.03
        else:
            score -= abs(dif_time) ** 3 * 0.005
        return score

    
