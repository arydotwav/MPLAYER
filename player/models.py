from django.db import models
from django.contrib.auth.models import User

# Create your models here.   

class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    pic = models.ImageField(upload_to='artist_pic/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    
    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=100)
    dateofrelease = models.CharField(max_length=30)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    cover = models.ImageField(upload_to='album_photo/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}"
    

class Song(models.Model):
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE ,blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    songcover = models.ImageField(upload_to='song_photo/', blank=True, null=True)
    
    def __str__(self):
        return self.title
    def total_likes(self):
        return self.liked_by.count()

class Profile(models.Model):
    nickname = models.CharField(max_length=50, blank=True, null=True)
    pfp = models.ImageField(upload_to='profile_pics/', default='default_pfp.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='user_followers', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='user_following', blank=True)
    #el symmetrical=False dice que la relacion no necesariamente es simetrica, que si el user 1 sigue el 2, 
    #no significa que el 2 siga el 1
    followed_artists = models.ManyToManyField(Artist, related_name='followed_artists', blank=True)
    liked_albums = models.ManyToManyField(Album, related_name='liked_albums', blank=True)
    liked_songs = models.ManyToManyField(Song, related_name='liked_songs', blank=True)
    
    def __str__(self):
        return f"{self.user}"  

class Playlist(models.Model):
    title = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    artists = models.ManyToManyField(Artist, related_name='playlists')
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datecreated = models.DateField(null=True)
    photo = models.ImageField(upload_to='playlist_photo/', default='default-cover.png', blank=True, null=True)
    public = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.user}"

