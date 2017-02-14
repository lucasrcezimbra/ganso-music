from gansomusic.core.forms import MusicForm

import pafy
from django.http import HttpResponse
from django.shortcuts import render
from pydub import AudioSegment

def index(request):
    return render(request, 'index.html')

def download(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        url = form.data['url']
        audio = pafy.new(url).getbestaudio()
        filepath = audio.download()

        mp3_filepath = convert_to_mp3(audio.title, filepath, audio.extension)

        audio_file = open(mp3_filepath, 'rb')
        response = HttpResponse(content=audio_file)
        response['Content-Type'] = 'audio/mpeg3'
        response['Content-Disposition'] = 'attachment; filename={}'\
                                           .format(mp3_filepath)
        return response

def convert_to_mp3(newtitle, file, extension):
    mp3_filepath = slugify('{}.mp3'.format(newtitle))
    mp3_audio = AudioSegment.from_file(file, extension)
    mp3_audio.export(mp3_filepath, format='mp3')
    return mp3_filepath

def slugify(value):
    deletechars = '/'
    for c in deletechars:
        value = value.replace(c,'')
    return value;
