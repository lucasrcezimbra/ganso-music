from gansomusic.core.forms import MusicForm

import os
import pafy
from django.http import HttpResponse
from django.shortcuts import render
from pydub import AudioSegment
from vagalume import lyrics
from urllib.parse import quote

def index(request):
    return render(request, 'index.html')

def download(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        url = form.data['url']
        title = form.data.get('title')
        artist = form.data.get('artist')
        genre = form.data.get('genre')
        audio = pafy.new(url).getbestaudio()
        filepath = audio.download()

        new_name = get_filename(title, artist, audio.title)
        mp3_filepath = convert_to_mp3_with_tags(filepath, new_name,
                                                audio.extension, title,
                                                artist, genre)

        audio_file = open(mp3_filepath, 'rb')
        response = HttpResponse(content=audio_file)
        response['Content-Type'] = 'audio/mpeg3'
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}"\
                                           .format(quote(mp3_filepath))
        os.remove(filepath)
        os.remove(mp3_filepath)
        return response

def convert_to_mp3_with_tags(file, new_name, extension, title, artist, genre):
    tags = {'artist': artist,
            'title': title,
            'genre': genre,
            'lyrics': get_lyric(artist, title)}
    mp3_filepath = slugify(new_name)
    mp3_audio = AudioSegment.from_file(file, extension)
    mp3_audio.export(mp3_filepath, format='mp3', tags=tags)
    return mp3_filepath

def get_filename(title, artist, youtube_title):
    if title and artist:
        return '{} - {}.mp3'.format(artist, title)
    return youtube_title

def get_lyric(artist, title):
    # try:
    result = lyrics.find(artist, title)
    if result.is_not_found():
        return ''
    else:
        return result.song.lyric
    # except:
    #     return ''

def slugify(value):
    deletechars = '/'
    for c in deletechars:
        value = value.replace(c,'')
    return value;
