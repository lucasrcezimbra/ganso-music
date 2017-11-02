from django import forms

from gansomusic.core.models import Music


class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['url', 'title', 'artist', 'genre']
