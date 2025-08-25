from django.utils import timezone
from django.db import models


class Pokemon(models.Model):
    """Модель покемона с основными характеристиками и эволюциями"""
    title = models.CharField(max_length=200, verbose_name="Название(рус.)")
    photo = models.ImageField(upload_to='pokemon_photos', verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Описание")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Название(англ.)")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="Название(яп.)")
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционировал'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"


class PokemonEntity(models.Model):
    """Модель для хранения информации о появлении покемона на карте."""
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name="Покемон")
    appeared_at = models.DateTimeField(default=timezone.now, verbose_name="Время появления")
    disappeared_at = models.DateTimeField(default=timezone.now, verbose_name="Время исчезновения")
    level = models.IntegerField(default=1, verbose_name="Уровень")
    health = models.IntegerField(default=100, verbose_name="Здоровье")
    strength = models.IntegerField(default=10, verbose_name="Сила")
    defence = models.IntegerField(default=10, verbose_name="Защита")
    stamina = models.IntegerField(default=10, verbose_name="Выносливость")

    def __str__(self):
        return f"{self.pokemon.title} (уровень: {self.level})"

    class Meta:
        verbose_name = "Сущность покемона"
        verbose_name_plural = "Сущности покемонов"
