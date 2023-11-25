# myapp/views.py
from django.shortcuts import render
from .forms import SearchForm
from .models import SearchHistory
from django.conf import settings
import requests
import googlemaps

def search_places(request):
    form = SearchForm(request.GET)
    places = []

    if form.is_valid():
        query = form.cleaned_data['query']
        api_key_places = settings.GOOGLE_MAPS_API_KEY
        api_key_distance_matrix = settings.GOOGLE_MAPS_API_KEY

        # Search for places using the Places API
        places_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key_places}"
        places_response = requests.get(places_url)
        places_data = places_response.json()
        places = places_data.get('results', [])

        # Save the top result to the database
        if places:
            top_result = places[0]
            SearchHistory.objects.create(
                query=query,
                place_name=top_result.get('name', ''),
                formatted_address=top_result.get('formatted_address', ''),
                place_id=top_result.get('place_id', ''),
            )

            # Retrieve search history
            search_history = SearchHistory.objects.all()

            # Initialize the Google Maps client
            gmaps = googlemaps.Client(key=api_key_distance_matrix)

            # Calculate distances using the Distance Matrix API
            origin = top_result['formatted_address']
            destinations = [history.formatted_address for history in search_history]
            
            # Specify units as kilometers in the Distance Matrix API request
            distance_matrix = gmaps.distance_matrix(origin, destinations, units='metric')

            if 'rows' in distance_matrix and 'elements' in distance_matrix['rows'][0]:
                elements = distance_matrix['rows'][0]['elements']
                for i, history in enumerate(search_history):
                    distance_info = elements[i].get('distance', {})
                    # Convert the distance from meters to kilometers
                    history.distance = distance_info.get('value', float('inf')) / 1000

                # Sort search history based on distance
                search_history = sorted(search_history, key=lambda x: x.distance)

    return render(request, 'myapp/search_results.html', {'form': form, 'places': places, 'search_history': search_history})
