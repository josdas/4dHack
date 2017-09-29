import map_api
import random
import place as Place
import geometry
from geometry import rel_error


def get_score_function(start, finish, duration, duration_on_foot, money, temp_place, cafe_type, time_cafe):
    gmap = map_api.GMap()

    def calc_score(places):
        score = 0
        spent_money = 0
        visited = []
        spent_time = 0
        spent_time_on_foot = 0

        # если маршрут начинается пешком, то это неплохо
        if places[0].position == start:
            score += 50

        # если маршрут коначается пешком, то это неплохо
        if places[-1].position == finish:
            score += 50

        for place in places:
            place_type = place.info.get('type', None)
            visited.append(place_type)
            # если мы хотим сходить в кафе и сходили
            if place_type == cafe_type and cafe_type is not None:
                score -= rel_error(spent_time, time_cafe) ** 2 * 1000

                # посетил кафе? ты нереально крут
                score += 300

                # в среднем 20 минут сидишь, можно сделать разные времена для разных мест # todo
                spent_time += 20

                spent_money += place.info.get('money', 250)

                # рейтинг тоже может увеличить очки
                score += place.info.get('rating', 0) * 300
            if place_type in temp_place:
                # гуляешь в каком-то месте 10 минут
                spent_time += 10

                # походили 10 минут
                spent_time_on_foot += 10

                # рейтинг влияет чуть хуже
                score += place.info.get('rating', 0) * 100
        if cafe_type is not None and cafe_type not in visited:
            score -= 10 ** 4

        # считаем время между точками пешком
        for i in range(len(places) - 1):
            transit_mode = 'walking'
            if (i == 0 and start != places[i].position) or \
                    (i == len(places) - 2 and finish != places[i + 1].position):
                transit_mode = 'transit'
            time_to_next = gmap.get_duration(places[i].position, places[i + 1].position, transit_mode=transit_mode)
            if time_to_next is not None:
                if transit_mode == 'walking':
                    spent_time_on_foot += time_to_next
                spent_time += time_to_next
            else:
                score -= 10 ** 10

        # Самопересечения пути и острые углы - это плохо
        for i in range(1, len(places) - 1):
            for j in range(i - 1):
                if geometry.intersect(places[i].position, places[i + 1].position,
                                      places[j].position, places[j + 1].position):
                    score -= 1000
            if geometry.sca(places[i - 1].position, places[i].position, places[i + 1].position):
                score -= 300

        # если мы потратили больше, чем планировали, то очень плохо
        if money < spent_money:
            score -= 10 ** 5

        # считаем очки за посещенные цели
        score += len(set(temp_place) & set(visited)) * 40
        for visited_place in set(visited):
            if visited_place in temp_place:
                index = temp_place.index(visited_place)
                score += 1 / (5 + index) * 1000

        # считаем штраф за время на ногах
        dif_time_on_foot = rel_error(duration_on_foot, spent_time_on_foot)
        if dif_time_on_foot < 0:
            score -= dif_time_on_foot ** 2 * 300
        else:
            score -= abs(dif_time_on_foot) ** 4 * 10000

        # считаем штраф за время
        dif_time = rel_error(duration, spent_time)
        if dif_time < 0:
            score -= dif_time ** 2 * 300
        else:
            score -= abs(dif_time) ** 3 * 6000
        if abs(duration - spent_time) > 60:
            score -= 10 ** 4
        print(spent_time, spent_time_on_foot)
        return score

    return calc_score


def score_decorate(find):
    def temp_function(*args, **keys):
        fun = get_score_function(*args, **keys)
        return find(*args, **keys, calc_score=fun)

    return temp_function


SPB_POSITION = (59.974597, 30.336504)

@score_decorate
def find_path(start, finish, duration, duration_on_foot, money, temp_place, cafe_type, time_cafe, calc_score):
    """
    :param start: --- position tuple(float, float) or str
    :param finish: --- position tuple(float, float) or str
    :param duration: --- float
    :param duration_on_foot: --- float
    :param money: --- float
    :param temp_place: --- [name, ...]
    :param cafe_type: --- str or None
    :param time_cafe: --- float or None
    :return: [place, ...]
    """
    gmap = map_api.GMap()
    if isinstance(start, str):
        start = gmap.get_position_from_name(start, SPB_POSITION)
    if isinstance(finish, str):
        finish = gmap.get_position_from_name(finish, SPB_POSITION)
    print(start)
    if True:
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

        if False:
            import pickle
            for i in range(len(walk_places)):
                for j in range(len(walk_places[i])):
                    walk_places[i][j] = walk_places[i][j].to_dick()

            with open('H', 'wb') as file:
                pickle.dump(walk_places, file=file)
    else:
        import pickle
        with open('H', 'rb') as file:
            walk_places = pickle.load(file=file)

        for i in range(len(walk_places)):
            for j in range(len(walk_places[i])):
                walk_places[i][j] = Place.Place(**walk_places[i][j])

    best_path = []
    best_score = -10 ** 30

    for iteration in range(30):
        random.seed(iteration + 228)

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
        mid_path = [Place.Place('start', start, {})]
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
            mid_path += [Place.Place('finish', finish, {})]
            score = calc_score(mid_path)
            print(score, iteration)
            if best_score < score:
                best_score = score
                best_path = mid_path
        else:
            print('fail', iteration)
    return best_path


if __name__ == '__main__':
    random.seed(3124)
    start = 'Исаакиевский собор'  # (59.974597, 30.336504)
    finish = (59.964200, 30.357014)
    temp = find_path(
        start=start,
        finish=finish,
        duration=120,
        duration_on_foot=120,
        money=400,
        temp_place=['парк', 'кладбище'],
        cafe_type='бар',
        time_cafe=60
    )
    for x in temp[1]:
        print(x.position)
    print(temp)
