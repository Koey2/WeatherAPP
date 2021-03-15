from django.urls import path
from .views import index


app_name = 'weatherapp'

urlpatterns = [
    path('', index, name='index' ),
]
