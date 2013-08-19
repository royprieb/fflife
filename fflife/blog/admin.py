from django.contrib import admin
#from imagekit.admin import AdminThumbnail
from blog.models import UserProfile
from blog.models import CarMake
from blog.models import CarModel
from blog.models import Car
from blog.models import Vote
from blog.models import Follow
from blog.models import Message
from blog.models import Post
from blog.models import PostComment
from blog.models import Like
from blog.models import Photo
from blog.models import ModType
from blog.models import Mod
from blog.models import Circle
from blog.models import Join
from blog.models import Topic
from blog.models import Response
from blog.models import Feedback
from blog.models import Video
from blog.models import Board
from blog.models import BoardPhoto
from blog.models import PhotoLike
from blog.models import PhotoComment
from blog.models import VendorCategory
from blog.models import VendorPost
from blog.models import VendorPostComment
from blog.models import VendorPostLike

#class PhotoAdmin(admin.ModelAdmin):
    #list_display = ('__str__', 'admin_thumbnail')
    #admin_thumbnail = AdminThumbnail(image_field='thumbnail')

admin.site.register(UserProfile)
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Car)
admin.site.register(Vote)
admin.site.register(Follow)
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Like)
admin.site.register(Photo)
admin.site.register(ModType)
admin.site.register(Mod)
admin.site.register(Circle)
admin.site.register(Join)
admin.site.register(Topic)
admin.site.register(Response)
admin.site.register(Feedback)
admin.site.register(Video)
admin.site.register(Board)
admin.site.register(BoardPhoto)
admin.site.register(PhotoLike)
admin.site.register(PhotoComment)
admin.site.register(VendorCategory)
admin.site.register(VendorPost)
admin.site.register(VendorPostComment)
admin.site.register(VendorPostLike)
