def load_path_url(points):
    url = "https://www.google.ru/maps/dir/"
    for i in range(len(points) - 1):
        url += str(points[i][0]) + ',' + str(points[i][1]) + '//'
    url += "data=!3m1!4b1!4m2!4m1!3e2?hl=ru"
    return url
