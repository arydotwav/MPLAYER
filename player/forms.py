from django import forms
from .models import Song, Album, Playlist, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-username', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-password1', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-password2', 'placeholder': 'Confirm Password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'usable_password' in self.fields:
            del self.fields['usable_password']