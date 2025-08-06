from django.db import models  # noqa F401
from PIL import Image
from django.core.files import File
import os
from django.utils import timezone


class Pokemon(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='pokemon_photos')
    
    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(default=timezone.now)
    disappeared_at = models.DateTimeField(default=timezone.now)
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    defence = models.IntegerField(default=10)
    stamina = models.IntegerField(default=10)
    


    
# your models here
