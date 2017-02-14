from django import forms

class MusicForm(forms.Form):
    url = forms.CharField(label='URL', required=True)
    title = forms.CharField(label='Título')
    artist = forms.CharField(label='Artista')
    gender = forms.CharField(label='Gênero')
