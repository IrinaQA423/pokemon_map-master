import folium
from django.utils.timezone import localtime, now
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.shortcuts import get_object_or_404

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
    
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

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

    previous_evolution = None
    if pokemon.previous_evolution:
        prev_evo = pokemon.previous_evolution
        previous_evolution = {
            'pokemon_id': prev_evo.id,
            'title_ru': prev_evo.title,
            'img_url': request.build_absolute_uri(prev_evo.photo.url) if prev_evo.photo else DEFAULT_IMAGE_URL
        }

    next_evolutions = []
    for next_evo in pokemon.next_evolutions.all():
        next_evolutions.append({
            'pokemon_id': next_evo.id,
            'title_ru': next_evo.title,
            'img_url': request.build_absolute_uri(next_evo.photo.url) if next_evo.photo else DEFAULT_IMAGE_URL
        })

    next_evolution = next_evolutions[0] if next_evolutions else None
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': {
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'img_url': request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else DEFAULT_IMAGE_URL,
            'description': pokemon.description,
            'previous_evolution': previous_evolution,
            'next_evolution': next_evolution
        }
    })
