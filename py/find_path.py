import map_api
import random
import place as place_


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
            visited.append(place_type)
            # если мы хотим сходить в кафе и сходили
            if place_type == cafe_type and cafe_type is not None:
                score -= (spent_time - time_cafe) ** 2 * 0.05

                # посетил кафе? ты нереально крут
                score += 300

                # в среднем 20 минут сидишь, можно сделать разные времена для разных мест # todo
                spent_time += 20

                spent_money += place.info.get('money', 250)

                # рейтинг тоже может увеличить очки
                score += place.info.get('rating', 0) * 30
            if place_type in temp_place:
                # гуляешь в каком-то месте 10 минут
                spent_time += 10

                # походили 10 минут
                spent_time_on_foot += 10

                # рейтинг влияет чуть хуже
                score += place.info.get('rating', 0) * 10

        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        def sca(A, B, C):
            return (C[0] - A[0]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[1] - A[1])

        # Return true if line segments AB and CD intersect
        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

        # считаем время между точками пешком
        for i in range(len(places) - 1):
            transit_mode = 'walking'
            if i == 0 or i == len(places) - 2:
                transit_mode = 'transit'
            time_to_next = gmap.get_duration(places[i].position, places[i + 1].position, transit_mode=transit_mode)
            if time_to_next is not None:
                spent_time_on_foot += time_to_next
            else:
                score -= 100000

        for i in range(1, len(places) - 1):
            for j in range(i - 1):
                if intersect(places[i].position, places[i + 1].position,
                             places[j].position, places[j + 1].position):
                    score -= 100
            if sca(places[i - 1].position, places[i].position, places[i + 1].position):
                score -= 100

        # если мы не хотели тратить, но потратили, то это очень плохо
        if money == 0 and spent_money > 0:
            score -= 100
        # если мы потратили больше, чем планировали, то тоже плохо
        if money - spent_money < 0:
            score -= 10000

        # считаем очки за посещенные цели
        score += len(set(temp_place) & set(visited)) * 40

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

    if False:
        walk_places = []
        for place_type in temp_place:
            walk_places.append([])
            walk_places[-1] += gmap.get_places(
                place_type,
                location=start,
                min_price=0,
                max_price=money
            )
        if cafe_type is not None:
            walk_places.append([])
            walk_places[-1] += gmap.get_places(
                cafe_type,
                location=start,
                min_price=0,
                max_price=money
            )

        # walk_places = list(set(walk_places))

        if False:
            import pickle
            for i in range(len(walk_places)):
                for j in range(len(walk_places[i])):
                    walk_places[i][j] = walk_places[i][j].to_dick()

            with open('H', 'wb') as file:
                pickle.dump(walk_places, file=file)

    if True:
        import pickle
        with open('H', 'rb') as file:
            walk_places = pickle.load(file=file)

        for i in range(len(walk_places)):
            for j in range(len(walk_places[i])):
                walk_places[i][j] = place_.Place(**walk_places[i][j])
    best_path = []
    best_score = -10 ** 10
    random.seed(228)
    for iteration in range(50):
        size = random.randint(1, len(walk_places) * 2)
        if cafe_type is not None:
            cafe_index = random.randint(0, size)
        else:
            cafe_index = None
        places = []
        for i in range(size):
            if i == cafe_index:
                places.append(walk_places[-1])
            else:
                if cafe_type is not None:
                    index = random.randint(0, len(walk_places) - 2)
                else:
                    index = random.randint(0, len(walk_places) - 1)
                places.append(walk_places[index])
        average_distance = max(5, (duration_on_foot - 10 * size) / size)
        mid_path = [place_.Place('start', start, {})]
        fail = False
        for place_type in places:
            best_place = None
            for j in range(30):
                place = random.choice(place_type)
                distance = gmap.get_duration(place.position, mid_path[-1].position)
                if distance is not None and 0.5 < distance / average_distance < 3:
                    best_place = place
                    break

            if best_place is None:
                fail = True
                break
            else:
                mid_path.append(best_place)
        if not fail:
            mid_path += [place_.Place('finish', finish, {})]
            score = calc_score(mid_path)
            print(str(score) + ' ' + str(iteration))
            if best_score < score:
                best_score = score
                best_path = mid_path
        else:
            print('fail ' + str(iteration))
    return best_score, best_path


if __name__ == '__main__':
    gmap = map_api.GMap()
    start = (59.974597, 30.336504)
    finish = (59.964200, 30.357014)
    temp = find_path(
        gmap,
        start=start,
        finish=finish,
        duration=30,
        duration_on_foot=30,
        money=300,
        temp_place=['парк', 'магазин одежды'],
        cafe_type='кафе',
        time_cafe=30
    )
    for x in temp[1]:
        print(x.position)
    print(temp)
