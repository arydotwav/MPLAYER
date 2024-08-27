from django.contrib import admin
from .models import Song, Artist, Album, Playlist, Profile
# Register your models here.
    
class PlaylistAdmin(admin.ModelAdmin):
    readonly_fields = ['datecreated']
    list_display = ('title', 'user')
    search_fields = ('title',)
    filter_horizontal = ('songs',) 

admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Profile)