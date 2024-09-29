from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('sign_up/', views.signup, name='signup'),
    path('sign_in/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('library/', views.playlists, name='library'),
    path('playlist/<int:playlist_id>', views.showplaylist, name='showplaylist'),
    path('upload_song/', views.uploadsong, name='uploadsong'),
    path('upload_album/', views.uploadalbum, name='uploadalbum'),
    path('album/<int:album_id>', views.album, name='album'),
    path('album/<int:album_id>/like', views.likeAlbum, name='like'),
    path('album/<int:album_id>/unlike', views.unlikeAlbum, name='unlike'),
    path('songs/<int:song_id>', views.songView, name='song'),
    path('songs/<int:song_id>/like/', views.likeSong, name='likeSong'),
    path('songs/<int:song_id>/unlike/', views.unlikeSong, name='unlikeSong'),
    path('saved/', views.library, name='saved'),
    path('create_playlist/', views.createplaylist, name='createplaylist'),
    path('playlist/<int:playlist_id>/update/', views.update_playlist, name='update_playlist'),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist'),
    path('artist/<int:artist_id>/unfollow', views.unfollow_artist, name='unfollow'),
    path('artist/<int:artist_id>/follow', views.follow_artist, name='follow'),
    path('artist/<int:artist_id>/songs', views.artist_songs, name='artist_songs'),
    path('results/', views.search, name='results'),
    path('profile/<int:profile_id>/following/', views.followingView, name='following'),
    path('playlist/<int:playlist_id>/delete', views.deleteplaylist, name='deleteplaylist'),
    path('profile/<int:user_id>/', views.profile, name='profile'),  # Muestra el perfil basado en el user_id
    path('profile/<int:profile_id>/update/', views.update_profile, name='updateprofile'),  # Actualiza el perfil basado en el profile_id
]
