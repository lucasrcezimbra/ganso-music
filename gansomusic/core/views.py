from gansomusic.core.forms import MusicForm

import pafy
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def download(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        url = form.data['url']
        audio = pafy.new(url).getbestaudio()
        filepath = audio.download()
        file = open(filepath, 'rb')
        response = HttpResponse(content=file)
        response['Content-Type'] = 'audio/mpeg3'
        response['Content-Disposition'] = ('attachment; filename={}'.format(filepath))
        return response
