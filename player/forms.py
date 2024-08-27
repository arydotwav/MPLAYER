from django import forms
from .models import Song, Album, Playlist, Profile

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album', 'audio_file']
        
class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'cover', 'dateofrelease']
        
class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'description', 'photo', 'songs', 'public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-title', 'placeholder': 'ENTER TITLE'}),
            'description': forms.TextInput(attrs={'class': 'form-description', 'placeholder': 'ENTER DESCRIPTION'}),
            'photo': forms.FileInput(attrs={'class': 'form-photo', 'placeholder': 'upload photo'}),
            'public': forms.CheckboxInput(attrs={'class': 'form-public', 'placeholder': 'public'}),
            'songs': forms.SelectMultiple(attrs={'class': 'form-songs', 'placeholder': 'choose songs'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'pfp']