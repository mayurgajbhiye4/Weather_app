import requests
import datetime
from django.shortcuts import render
from django.contrib import messages
from decouple import config


# Create your views here.
def home(request):
    context = {} 
    try:   
        if request.method == "POST":
            city = request.POST.get('city')
            API_KEY = config('API_KEY')
            weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
            forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
            
            weather_data, forecasts_data = fetch_weather_and_forecasts(city, API_KEY, weather_url, forecast_url)

            context = {
                'weather_data': weather_data,
                'forecasts_data': forecasts_data
            }
            return render(request, 'base/weather.html', context)
        
        else:
            return render(request, 'base/weather.html')

    except:
        exception_occured=True
        messages.error(request, f'Cannot fetch weather data for {city}')
        return render(request, 'base/weather.html', {'exception_occured':exception_occured})
        
    
def fetch_weather_and_forecasts(city, api_key, weather_url, forecast_url):
    PARAMS = {'units': 'metric'}
    weather_response = requests.get(weather_url, PARAMS).json()
    forecast_response = requests.get(forecast_url, PARAMS).json()

    description = weather_response['weather'][0]['description']
    icon = weather_response['weather'][0]['icon']
    temp = weather_response['main']['temp']
    day = datetime.date.today()

    weather_data = {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
    }

    daily_forecasts = []
    for daily_data in forecast_response['list'][:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%I:%M %p'),
            "min_temp": round(daily_data['main']['temp_min'], 2),
            "max_temp": round(daily_data['main']['temp_max'], 2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon']
        })

    return weather_data, daily_forecasts

 