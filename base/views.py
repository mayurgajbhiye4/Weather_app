import requests
import datetime
from django.shortcuts import render
from django.contrib import messages
from decouple import config


# Create your views here.
def home(request):
    context = {}
    if request.method == "POST":
        city = request.POST.get('city')
        API_KEY = config('API_KEY')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        PARAMS = {'units': 'metric'}

        try:
            data = requests.get(url, PARAMS).json()
            description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temp = data['main']['temp']
            day = datetime.date.today()

            context = {
                'description': description,
                'icon': icon,
                'temp': temp,
                'day': day,
                'city': city,
            }

            return render(request, 'base/weather.html', context)
        except:
            exception_occured=True
            messages.error(request, f'Cannot fetch weather data for {city}')
            day = datetime.date.today()
            return render(request, 'base/weather.html', {'exception_occured':exception_occured})

    else:
        return render(request, 'base/weather.html')
    