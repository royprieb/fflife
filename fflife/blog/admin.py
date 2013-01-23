from django.contrib import admin
#from imagekit.admin import AdminThumbnail
from blog.models import Journal, Car, Album, Post, Mod, Photo
from blog.models import FeaturedPhoto, FeaturedPost, HeroPhoto
from blog.models import UserProfile, Vote, Follow
from blog.models import CarMake, CarModel, Message
from blog.models import Event, Like, ModType
from blog.models import StaticPage,Feedback

#class PhotoAdmin(admin.ModelAdmin):
    #list_display = ('__str__', 'admin_thumbnail')
    #admin_thumbnail = AdminThumbnail(image_field='thumbnail')

admin.site.register(Journal)
admin.site.register(Car)
admin.site.register(Post)
admin.site.register(Mod)
admin.site.register(ModType)
admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(FeaturedPhoto)
admin.site.register(FeaturedPost)
admin.site.register(HeroPhoto)
admin.site.register(UserProfile)
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Vote)
admin.site.register(Follow)
admin.site.register(Message)
admin.site.register(Event)
admin.site.register(Like)
admin.site.register(StaticPage)
admin.site.register(Feedback)
#admin.site.register(PhotoAdmin)
