from django.shortcuts import render
# from django.views.generic import TemplateView
import requests
from .models import City
from .forms import CityForm
from django.contrib import messages

# Create your views here.

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ff5ac4104ce1147b5d1e13992397f133'

    cities = City.objects.all()
    data = []
    error_msg = ''
    message = ''
    message_class = ''

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error_msg = 'City doesnt exist'
            else:
                error_msg = 'City already exists in database'
        if error_msg:
            message = error_msg
            message_class = 'warning'
        else:
            message = 'City has been added'
            message_class = 'success'

    form = CityForm()

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {    
            'city': city.name,
            'country': r['sys']['country'],
            'temperature': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        data.append(city_weather)

   


    print(data)
    return render(request,
     'assets/weather.html',
      {'data': data,
      'form': form,
      'message': message,
      'message_class': message_class})