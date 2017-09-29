# -*- coding: utf-8 -*-
from flask import Flask, render_template, json, request, jsonify
from find_path import find_path


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_len', methods=['GET', 'POST'])
def get_len():
    name = request.form['name'];
    return json.dumps({'len': len(name)})

#192.100.00.00:5000?start=59.974597,30.336504&end=59.974597,30.336504&
@app.route('/get_path', methods=['GET', 'POST'])
def get_path():
    args = request.args

    """
        :param start: --- position tuple(float, float)
        :param finish: --- position tuple(float, float)
        :param duration: --- float
        :param duration_on_foot: --- float
        :param money: --- float
        :param temp_place: --- [name, ...]
        :param cafe_type: --- str or None
        :param time_cafe: --- float or None
        :return: [place, ...]
    """
    #kek = request.args
    #print(kek['huy'])
    if "huy" in args.keys():
        kek = args['huy'].split(',')
        path = []
        for i in range(len(kek)//2):
            path += [(float(kek[2*i]), float(kek[2*i+1]))]
        """
        path = [
            (59.974597, 30.336504),
            (59.9635111, 30.3084668),
            (59.9845707, 30.2995708),
            (60.05290139999999, 30.3061451),
            (60.032444, 30.37410689999999),
            (59.994406, 30.420843),
            (59.9642, 30.357014)
        ]
        """
    else:
        start = tuple(map(float, args['start'].split(',')))
        finish = tuple(map(float, args['finish'].split(',')))
        duration = float(args['duration'])
        duration_on_foot = float(args['duration_on_foot'])
        money = float(args['money'])
        temp_place = tuple(args['temp_place'].split(','))
        cafe_type = args['cafe_type'] if 'cafe_type' in args.keys() else None
        time_cafe = float(args['time_cafe']) if 'time_cafe' in args.keys() else None
        path = find_path(start, finish, duration, duration_on_foot, money, temp_place, cafe_type, time_cafe)

    ret = []
    for step in path:
        ret += [{"lat": step[0], "lng": step[1], "type": "WALKING"}]
    return json.dumps(ret)
    return json.dumps([
        {"lat": 59.973180, "lng": 30.273461, "type": "TRANSIT",
         "href": "https://pp.userapi.com/c637718/v637718344/4285c/JL2lgOGK3ig.jpg"},
        {"lat": 59.938445, "lng": 30.367521, "type": "WALKING",
         "href": "https://www.gravatar.com/avatar/870c227ab02e5c61101a8265cdd14989?s=328&d=identicon&r=PG"},
        {"lat": 59.938612, "lng": 30.261119, "type": "TRANSIT"}
    ])


if __name__ == '__main__':
    app.run(host="0.0.0.0");