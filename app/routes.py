from flask import render_template, session, request

from app import app
from app.weather import main_logic


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['city']:
            city = request.form['city']
            temperature = main_logic(city)
            return render_template('index.html', res=temperature)
        else:
            res = 'Город не указан'
            return render_template('index.html', res=res)
    return render_template('index.html')
