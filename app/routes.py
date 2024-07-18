from flask import render_template, session, request

from app import app
from app.logic_weather import main_func_logic_weather


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['city']:
            city = request.form['city']
            cur_temp, list_temp = main_func_logic_weather(city)
            return render_template('index.html', cur_temp=cur_temp, list_temp=list_temp, city=city)
        else:
            city = 'Город не указан'
            return render_template('index.html', city=city)
    return render_template('index.html')
