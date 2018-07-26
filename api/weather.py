import json
import requests
import store
from datetime import datetime

appid = store.openweatherapi
city_id = 0


def weatherapp(text):
    place_query = ""
    place_query = text
    place_apikey = store.google_place_api
    lat = "lat"
    lon = "lot"

    # Находим место по названию города с пощью Google Place API
    try:
        place_res = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json',
                                 params={'query': place_query, 'language': 'ru', 'key': place_apikey})
        place_data = place_res.json()

        lon = json.dumps(place_data['results'][0]['geometry']['location']['lng'])
        lat = json.dumps(place_data['results'][0]['geometry']['location']['lat'])
        place_name = place_data['results'][0]['name']

    except Exception as e:
        print("Error requests: ", e)
    pass

    # По широте и долготе определям погоду местности с  помощью OpenWeatherMap API
    try:
        now = datetime.now()
        t = 0
        res = requests.get("https://api.openweathermap.org/data/2.5/forecast",
                           params={'lat': lat, 'lon': lon, 'units': 'metric',
                                   'lang': 'ru', 'appid': appid})
        data = res.json()
        day = "послезавтра"
        if (day == "сегодня"):
            t = 0
        elif (day == "завтра"):
            t = 1
        elif (day == "послезавтра"):
            t = 2
        list = data['list']
        for daily in list:
            name = str(data['city']['name'])
            conditions = str(daily['weather'][0]['description'])
            clouds = str(daily['clouds']['all'])
            wind_speed = str(daily['wind']['speed'])
            temp = daily['main']['temp']
            humi = str(daily['main']['humidity'])
            icon = str(daily['weather'][0]['icon'])
            date = str(daily['dt_txt'])
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            # солнце и снег => https://i.pinimg.com/originals/97/1b/02/971b02d5aacc22155dd10202c918cd16.gif
            # дождь и молния => https://i.pinimg.com/originals/49/b8/94/49b894d42ec5fae7a8531b9f29bf4649.gif
            # снег => https://i.pinimg.com/originals/63/76/47/6376471219dbbd746ebe5fbd81e9dc4b.gif
            # дождь  => https://i.pinimg.com/originals/37/8c/11/378c1143e77f70582a1d316647c923f6.gif
            # солнце и дождь => https://i.pinimg.com/originals/eb/b1/f6/ebb1f6930e3fe59e4ed399ca4f5fb0b0.gif
            # солнце => https://i.pinimg.com/originals/12/05/1f/12051f635e87316a758c126151690519.gif
            # солнце и облако => https://i.pinimg.com/originals/7d/cb/5b/7dcb5be30b0594b7c45e285ebb01b2bf.gif
            # облако => https://i.pinimg.com/originals/4d/94/5f/4d945fdce719f03a255b5270f39546db.gif

            gifs = {
                '01d': 'https://i.pinimg.com/originals/12/05/1f/12051f635e87316a758c126151690519.gif',
                '02d': 'https://i.pinimg.com/originals/7d/cb/5b/7dcb5be30b0594b7c45e285ebb01b2bf.gif',
                '03d': 'https://i.pinimg.com/originals/4d/94/5f/4d945fdce719f03a255b5270f39546db.gif',
                '04d': 'https://i.pinimg.com/originals/4d/94/5f/4d945fdce719f03a255b5270f39546db.gif',
                '09d': 'https://i.pinimg.com/originals/37/8c/11/378c1143e77f70582a1d316647c923f6.gif',
                '10d': 'https://i.pinimg.com/originals/eb/b1/f6/ebb1f6930e3fe59e4ed399ca4f5fb0b0.gif',
                '11d': 'https://i.pinimg.com/originals/49/b8/94/49b894d42ec5fae7a8531b9f29bf4649.gif',
                '13d': 'https://i.pinimg.com/originals/63/76/47/6376471219dbbd746ebe5fbd81e9dc4b.gif',
                '50d': 'https://i.pinimg.com/originals/4d/94/5f/4d945fdce719f03a255b5270f39546db.gif'
            }
            for key, val in gifs.items():
                if (key == icon):
                    im = val
                    break

            if (temp > 0):
                temp = "+" + str(temp)
            weather = "Error 007"
            if date.hour == 12 and date.day == now.day + t:
                weather = str(
                    date.date()) + " в  " + place_name + "\n" + conditions.capitalize() + "\nТемпература: " + str(
                    temp) + " \xb0C \nВлажность: " + humi + " %\nОблачность: " + clouds + " %\nСкорость ветра: " + wind_speed + " м/с\n<a href = '" + im + "'>.</a>\n\n"
                break
        return weather

    except Exception as e:
        print(e)
        pass
