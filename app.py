from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class CityDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(159), nullable=False)



@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        city = request.form["content"]


        new_city =CityDb(city_name=city)

        db.session.add(new_city)
        db.session.commit()


    cities = CityDb.query.order_by(-CityDb.id).first().city_name

    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=0ebb730f01e81a6e41ece925c3e7785c"
    response = requests.get(url.format(cities)).json()

    weather = {
        'city': response['name'],
        'temperature': response['main']['temp'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }








    return render_template("weather.html",weather=weather)










if __name__ == "__main__":
    app.run(debug=True)