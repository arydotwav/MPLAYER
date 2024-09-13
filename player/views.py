from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import SongForm, AlbumForm, PlaylistForm, ProfileForm, CustomUserCreationForm
from .models import Playlist, Song, Album, Artist, Profile
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q, Count
from thefuzz import process

def index(request):
    artist = Artist.objects.all()
    rec_albums = Album.objects.order_by('?')[:3]
        
    #checkeo si esta loggeado el usuario   
    if request.user.is_authenticated:
        #si lo esta va a agarrar el objeto aleatorio de la tabla playlist
        rec_playlist = Playlist.objects.filter(user=request.user).order_by('?').first()
        rec_albums = rec_albums[:2]
    else:
        #se pone el none para que no tire error, ya q en el inicio yo puse para que se muestren recomendaciones
        #del user q esta logeado
        rec_playlist = None
        rec_albums = rec_albums[:3]
    rec_artist = Artist.objects.order_by('?').first()
    profile = Profile.objects.all()
    return render(request, 'layout/home.html', {
        'profile': profile,
        'rec_artist': rec_artist,
        'rec_albums': rec_albums,
        'rec_playlist': rec_playlist,
        'artist': artist
    })

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'invalid data')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {
        'form': form,
    })

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'users/signin.html', {
        'form': form
    })

def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile, created = Profile.objects.get_or_create(user=user)
    playlist = Playlist.objects.filter(user=user)
    is_owner = request.user == user

    if created:
        profile.nickname = user.username
        profile.pfp = 'default_pfp.jpg'
        profile.save()
    else:
        return render(request, 'users/profile.html', {
            'playlist': playlist,
            'profile': profile,
            'is_owner': is_owner
        })

   
@login_required
def update_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=profile.user.id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/update_profile.html', {
        'profile': profile,
        'form': form
    })

def search(request):
    query = request.POST.get('q')
    songs = Song.objects.all()
    albums = Album.objects.all()
    artists = Artist.objects.all()
    
    if query:
        song_titles = [song.title for song in songs]
        artist_names = [artist.name for artist in artists]
        album_titles = [album.title for album in albums]
        
        song_matches = process.extract(query, song_titles, limit=len(song_titles))
        matched_song_titles = [match[0] for match in song_matches if match[1] > 70]
        
        artist_matches = process.extract(query, artist_names, limit=len(artist_names))
        matched_artist_names = [match[0] for match in artist_matches if match[1] > 70]
        
        album_matches = process.extract(query,album_titles, limit=len(album_titles))
        matched_album_titles = [match[0] for match in album_matches if match[1] > 70]
        
        songs = songs.filter(Q(title__in=matched_song_titles)|Q(artist__name__in=matched_artist_names))
        artists = artists.filter(Q(name__in=matched_artist_names))
        albums = albums.filter(Q(title__in=matched_album_titles)|Q(artist__name__in=matched_artist_names))
        
        
    return render(request, 'search/results.html', {
        'songs': songs,
        'artists': artists,
        'albums': albums
    })
    
@login_required
def playlists(request):
    
    albums = Album.objects.all()
    user_playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'songs/playlists_display.html', {
        'playlist': user_playlists,
        'albums': albums
    })
    
def showplaylist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    songs =  playlist.songs.all()
    artist = songs.first().artist if songs.exists() and songs.first().artist else None
    return render(request, 'songs/show_playlist.html', {
        'playlist': playlist,
        'songs': songs,
        'artist': artist,
    })

@login_required
def update_playlist(request, playlist_id):
        
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            form.save()
            return redirect('showplaylist', playlist_id=playlist.id)
    else:
        form = PlaylistForm(instance=playlist)

    return render(request, 'songs/update_playlist.html', {'form': form, 'playlist': playlist})

@login_required
def deleteplaylist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
    if request.method == 'POST':
        messages.success(request, 'Playlist deleted successfully')
        playlist.delete()
        return redirect('library')
    
    return render(request, 'songs/confirm_delete.html', {'playlist': playlist})

def album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    user = request.user
    
    if user.is_authenticated:
        liked_albums = request.user.profile.liked_albums.all()
        return render(request, 'artist/album.html', {
            'album': album,
            'liked_albums': liked_albums
        })
    else:
        return render(request, 'artist/album.html', {
            'album': album,
        })



def songView(request, song_id):
    songs = get_object_or_404(Song, pk=song_id)
    user = request.user
    
    if user.is_authenticated:
        liked_songs = request.user.profile.liked_songs.all()
        return render(request, 'songs/song.html', {
            'songs': songs,
            'liked_songs': liked_songs
        })
    else:
        return render(request, 'songs/song.html', {
            'songs': songs
        })

def uploadsong(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('You are not allowed to access this page')

    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('songlist')  # Redirect to the song list page
    else:
        form = SongForm()

    return render(request, 'songs/upload_song.html', {
        'form': form
    })
            
def uploadalbum(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('songs/album_list')
    else:
        form = AlbumForm()
    return render(request, 'create_album.html', {'form': form})

def createplaylist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            return redirect('library')
    else:
        form = PlaylistForm()
    return render(request, 'songs/create_playlist.html', {
        'form': form
    })

def artist_detail(request, artist_id):    
    artist = get_object_or_404(Artist, id=artist_id)
    album = Album.objects.filter(artist=artist)
    songs = Song.objects.filter(artist=artist).annotate(total_likes=Count('liked_songs')).order_by('-total_likes')
    
    if request.user.is_authenticated:
        user = request.user
        is_following = artist.followers.filter(id=request.user.id).exists()
        liked_artists_count = Artist.objects.filter(followers=user).count()
        return render(request, 'artist/artist.html', {
            'songs': songs,
            'artist': artist,
            'is_following': is_following,
            'liked_artists_count': liked_artists_count,
            'album': album
        })
         
    else:
        return render(request, 'artist/artist.html', {
            'songs': songs,
            'artist': artist,
            'album': album
        })
    
def followingView(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    
    return render(request, 'users/see_following.html', {
        'profile': profile
    })  
 
def follow_artist(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    user = request.user
    artist.followers.add(user)
    user.profile.followed_artists.add(artist)
    
    return redirect('artist', artist_id=artist.id)

def unfollow_artist(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    user = request.user
    artist.followers.remove(user)
    user.profile.followed_artists.remove(artist)
    
    return redirect('artist', artist_id=artist.id)



def likeSong(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    profile = request.user.profile
    profile.liked_songs.add(song)

    return redirect('song', song_id=song.id)

def unlikeSong(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    profile = request.user.profile
    if song in profile.liked_songs.all():
        profile.liked_songs.remove(song)
    return redirect('song', song_id=song.id)

@login_required
def library(request):
    profile = request.user.profile
    liked_songs = profile.liked_songs.all()  # Get all songs liked by the current user
    return render(request, 'songs/library.html', {'liked_songs': liked_songs})

@login_required
def userplaylist(request, playlist_id, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    songs = playlist.songs.all()
    return render(request, 'songs/playlists_display.html', {
        'playlist': playlist,
        'songs': songs,
        'artist': artist
    })


def likeAlbum(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    profile = request.user.profile
    profile.liked_albums.add(album)
    return redirect('album', album_id=album.id)
    
def unlikeAlbum(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    profile = request.user.profile
    
    if album in profile.liked_albums.all():
        profile.liked_albums.remove(album)
    
    return redirect('album', album_id=album.id)
