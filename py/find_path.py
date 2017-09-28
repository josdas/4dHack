import map_api


def find_path(gmap, start, finish, duration, duration_on_foot, money, temp_place, cafe_type, time_cafe):
    """
    :param start: --- position tuple(float, float)
    :param finish: --- position tuple(float, float)
    :param duration: --- float
    :param duration_on_foot: --- float
    :param money: --- float
    :param temp_place: --- [position]
    :param cafe_type: --- str or None
    :param time_cafe: --- float or None
    :return: [positions, ...]
    """

    def calc_score(places):
        score = 0
        spent_money = 0
        visited = []
        spent_time = 0
        spent_time_on_foot = 0

        # если маршрут начинается пешком, то это неплохо
        if places[0].position == start:
            score += 10

        # если маршрут коначается пешком, то это неплохо
        if places[-1].position == finish:
            score += 10

        for place in places:
            place_type = place.info.get('type', None)
            # если мы хотим сходить в кафе и сходили
            if place_type == cafe_type and cafe_type is not None:
                score -= (spent_time - time_cafe) ** 2 * 0.05  #
                # посетил кафе? ты нереально крут
                score += 300

                # в среднем 20 минут сидишь, можно сделать разные времена для разных мест # todo
                spent_time += 20

                spent_money += place.info.get('money', 0)

                # рейтинг тоже может увеличить очки
                score += place.info.get('rating', 0) * 30
            if place_type in temp_place:
                visited.append(place_type)

                # гуляешь в каком-то месте 10 минут
                spent_time += 10

                # походили 10 минут
                spent_time_on_foot += 10

                # рейтинг влияет чуть хуже
                score += place.info.get('rating', 0) * 10
        # если мы не хотели тратить, но потратили, то это очень плохо
        if money == 0 and spent_money > 0:
            score -= 100
        # если мы потратили больше, чем планировали, то тоже плохо
        if money - spent_money < 0:
            score -= 10000

        # считаем очки за посещенные цели
        score += len(set(temp_place) & set(visited)) * 40

        # считаем время между точками пешком
        for i in range(len(places) - 1):
            time_to_next = gmap.get_duration(places[i].position, places[i + 1].position, transit_mode='walking')
            if time_to_next is not None:
                spent_time_on_foot += time_to_next
            else:
                score -= 100000

        # считаем штраф за время на ногах
        dif_time_on_foot = duration_on_foot - spent_time_on_foot
        if dif_time_on_foot < 0:
            score -= dif_time_on_foot ** 2 * 0.03
        else:
            score -= abs(dif_time_on_foot) ** 3 * 0.005

        # считаем штраф за время
        dif_time = duration - spent_time
        if dif_time < 0:
            score -= dif_time ** 2 * 0.03
        else:
            score -= abs(dif_time) ** 3 * 0.005
        return score

    walk_places = []
    for point in [start, finish]:
        for place in temp_place:
            walk_places += gmap.get_places(
                place,
                location=point,
                min_price=0,
                max_price=money
            )
        if cafe_type is not None:
            walk_places += gmap.get_places(
                cafe_type,
                location=point,
                min_price=0,
                max_price=money
            )
    walk_places = list(set(walk_places))
    print(walk_places)

    return calc_score(walk_places)

if __name__ == '__main__':
    gmap = map_api.GMap()
    start = (59.974597, 30.336504)
    finish = (59.964200, 30.357014)
    temp = find_path(
        gmap,
        start=start,
        finish=finish,
        duration=140,
        duration_on_foot=120,
        money=300,
        temp_place=['парк', 'магазин одежды'],
        cafe_type='кафе',
        time_cafe=30
    )
    print(temp)
