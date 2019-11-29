from django.shortcuts import render
import googlemaps
import requests
from datetime import datetime
from mapapp.form import SearchForm
from newsproject.settings import GOOGLE_API_KEY


def map_detail(request):
    google_json = None
    place_id = request.GET.get('place', None)
    if place_id:
        url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(place_id, GOOGLE_API_KEY)
        google_json = requests.get(url).json()

    form = SearchForm(data=request.POST or None)
    formatted_address = None
    place_id = None
    if form.is_valid():
        cd = form.cleaned_data
        search_address = cd.get('search', None)
        google_maps = googlemaps.Client(key=GOOGLE_API_KEY)
        geocode_result = google_maps.geocode(search_address)
        if geocode_result:
            formatted_address = geocode_result[0].get('formatted_address', None)
            place_id = geocode_result[0].get('place_id', None)

    return render(
        request, 'mapapp/map_detail.html',
        {
            'place_id': place_id,
            'google_json': google_json,
            'formatted_address': formatted_address,
        }
    )
