from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def download(request):
    if request.method == 'POST':
        filepath = '/home/lucas/Downloads/audio.mp3'
        file = open(filepath, 'rb')
        response = HttpResponse(content=file)
        response['Content-Type'] = 'audio/mpeg3'
        response['Content-Disposition'] = 'attachment; filename=audio.mp3'
        return response
