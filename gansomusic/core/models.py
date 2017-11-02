from django.db import models


class Music(models.Model):
    url = models.CharField('URL', max_length=255)
    title = models.CharField('título', max_length=200, blank=True)
    artist = models.CharField('artista', max_length=200, blank=True)
    genre = models.CharField('gênero', max_length=100, blank=True)
    file = models.FileField(upload_to='')
