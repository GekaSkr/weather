from django.shortcuts import render
from geopy import GoogleV3


def index(request):

    place = 'Київ'
    location = GoogleV3(api_key='AIzaSyDi_HeAAJ9AfpJns9PLZdJsfGhOeNx7e9c').geocode(place)

    context = {'location': location}
    return render(request, 'weather/index.html', context)

