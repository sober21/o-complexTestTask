from flask import render_template, session, request

from app import app
from app.logic_weather import main_func_logic_weather


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['city']:
            city = request.form['city']
            temperature = main_func_logic_weather(city)
            return render_template('index.html', res=temperature)
        else:
            res = 'Город не указан'
            return render_template('index.html', res=res)
    return render_template('index.html')
