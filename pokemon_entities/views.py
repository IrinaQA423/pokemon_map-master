import folium


import datetime
from django.utils.timezone import localtime, now
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.conf import settings
from django.http import HttpRequest

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime(now())
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time
    )
    
    for entity in pokemon_entities:
        photo_url = DEFAULT_IMAGE_URL
        if entity.pokemon.photo:
            photo_url = request.build_absolute_uri(entity.pokemon.photo.url)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            photo_url 
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        photo_url = DEFAULT_IMAGE_URL
        if pokemon.photo:
            photo_url = request.build_absolute_uri(pokemon.photo.url)
        pokemons_on_page.append({
            'pokemon_id':  pokemon.id,
            'img_url': photo_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime(now())
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time
    )

    for entity in pokemon_entities:
        photo_url = DEFAULT_IMAGE_URL
        if pokemon.photo:
            photo_url = request.build_absolute_uri(pokemon.photo.url)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            photo_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': {
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title,
            'img_url': request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else DEFAULT_IMAGE_URL,

        }
    })