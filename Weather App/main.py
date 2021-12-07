from flask import Flask, render_template, request, flash
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from requests.sessions import Session


app = Flask(__name__)
db = SQLAlchemy(app)



app.config['SECRET_KEY'] = "thisissomethingsecrect"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///weather.db"

class cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form['city']
        if city:
            if not cities.query.filter(func.lower(cities.name) == func.lower(city)).first():
                new_city = cities(name=city)
                db.session.add(new_city)
                db.session.commit()
                flash(message='City Added', category='success')
            else:
                flash(message='City Already Exists', category='danger')
                
    API_key = "d809c01efeeb879d2ca5ea3ff7e3ec89"
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
    
    all_cities = cities.query.all()

    weather_data = []

    for city in all_cities:
        r = requests.get(url.format(city.name,API_key)).json()
        

        if r['cod'] == 200:
            weather = {
                'city' : r['name'],
                'icon' : r['weather'][0]['icon'],
                'temp' : r['main']['temp'],
                'desc' : r['weather'][0]['description']
            }
            weather_data.append(weather)
        elif r['cod'] == '404':
            flash(message='City Not found', category='danger')
    return render_template('home.html', weather_data=weather_data)



if __name__ == '__main__':
    app.run(debug=True)    