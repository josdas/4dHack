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


@app.route('/get_path', methods=['GET', 'POST'])
def get_path():
    a = [
        (59.974597, 30.336504),
        (59.950367, 30.37593299999999),
        (59.9331299, 30.4108599),
        (59.9419364, 30.4614353),
        (59.9331299, 30.4108599),
        (59.93678509999999, 30.3612154),
        (59.922008, 30.355412),
        (59.974597, 30.336504)
    ]
    ret = []
    for i in a:
        ret += [{"lat": i[0], "lng": i[1], "type": "WALKING"}]
    return json.dumps(ret)
    return json.dumps([
        {"lat": 59.973180, "lng": 30.273461, "type": "TRANSIT",
         "href": "https://pp.userapi.com/c637718/v637718344/4285c/JL2lgOGK3ig.jpg"},
        {"lat": 59.938445, "lng": 30.367521, "type": "WALKING",
         "href": "https://www.gravatar.com/avatar/870c227ab02e5c61101a8265cdd14989?s=328&d=identicon&r=PG"},
        {"lat": 59.938612, "lng": 30.261119, "type": "TRANSIT"}
    ])


if __name__ == '__main__':
    app.run(debug=True)