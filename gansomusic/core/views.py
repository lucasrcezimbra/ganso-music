import pafy
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def download(request):
    if request.method == 'POST':
        url = request.POST['url']
        audio = pafy.new(url).getbestaudio()
        file = audio.download()
        return render(request, 'index.html')
