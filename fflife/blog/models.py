import os
from django.db import models
from django.contrib.auth.models import User
# not sure if the below import is required leaving commented
#from django.conf import settings
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors.resize import ResizeToFit, SmartResize
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse
from django.dispatch import receiver
import django.dispatch 
from datetime import datetime

def get_gallery_image_path(instance, filename):
    return os.path.join('gallery/',str(instance.car.id), filename)

#def get_car_profile_cache_path(instance, filename):
#    return os.path.join('car_profile/',str(instance.id), filename)

# owner signals
profile_created = django.dispatch.Signal(providing_args=[])
follow_created = django.dispatch.Signal(providing_args=[])
like_created = django.dispatch.Signal(providing_args=[])
vote_created = django.dispatch.Signal(providing_args=[])
# follower signals
car_created = django.dispatch.Signal(providing_args=[])
post_created = django.dispatch.Signal(providing_args=[])
mod_created = django.dispatch.Signal(providing_args=[])
photo_created = django.dispatch.Signal(providing_args=[])
# group signals
topic_created = django.dispatch.Signal(providing_args=[])
response_created = django.dispatch.Signal(providing_args=[])
# post comment signal
post_comment_created = django.dispatch.Signal(providing_args=[])
photo_comment_created = django.dispatch.Signal(providing_args=[])

# models below
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    display_name = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    motto = models.CharField(max_length=50, null=True, blank = True)
    original_image = models.ImageField(upload_to='user_profiles', blank=True, null=True)
    display_image = ImageSpecField(
        processors = [SmartResize(100,100)],
        image_field='original_image',
        format='JPEG',
        options={'quality':90}
        )
    
    def __unicode__(self):
        return self.display_name
    
    def send_profile(self):
        profile_created.send(sender=self)

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class CarModel(models.Model):
    carmaker = models.ForeignKey(CarMake)
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class Car(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100, null=True, blank=True)
    make = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    original_image = models.ImageField(upload_to='car_profiles', blank=True, null=True)
    display_image = ImageSpecField(
        image_field = 'original_image',
        processors = [SmartResize(678,248)],
        format='JPEG',
        options={'quality':90},
        )

    def __unicode__(self):
        return self.name

    def send_car(self):
        car_created.send(sender=self)

class Vote(models.Model):
    FAST = 'fast'
    FRESH = 'fresh'
    VOTE_TYPE_CHOICES = (
        (FAST, 'fast'),
        (FRESH, 'fresh'),
    )
    user = models.ForeignKey(User)
    car = models.ForeignKey(Car)
    type = models.CharField(max_length=10, choices=VOTE_TYPE_CHOICES)
    
    def __unicode__(self):
        return self.type

    def send_vote(self):
        vote_created.send(sender=self)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='user_following_party')
    followed = models.ForeignKey(User, related_name='user_followed_party')
    
    def __unicode__(self):
        return self.followed.username

    def send_follow(self):
        follow_created.send(sender=self)

class Message(models.Model):
    recipient = models.ForeignKey(User)
    sender = models.CharField(max_length=100)
    viewed = models.BooleanField()
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True) 
    pub_date = models.DateTimeField('date published')
    label = models.CharField(max_length=50)
    action = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.title

class Post(models.Model):
    car = models.ForeignKey(Car)
    pub_date = models.DateTimeField('date published')
    title = models.CharField(max_length=100)
    body = RichTextField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    
    def __unicode__(self):
        return self.title

    def send_post(self):
        post_created.send(sender=self)

class PostComment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    body = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.post.title

    def send_post_comment(self):
        post_comment_created.send(sender=self)

class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    
    def __unicode__(self):
        return self.post.title

    def send_like(self):
        like_created.send(sender=self)

class Photo(models.Model):
    car = models.ForeignKey(Car)
    caption = models.CharField(max_length=100, null=True, blank=True)
    original_image = models.ImageField(upload_to=get_gallery_image_path)
    thumb_image = ImageSpecField(
        processors=[SmartResize(150,150)],
        image_field='original_image',
        format='JPEG',
        options={'quality':90}
        )
    display_image = ImageSpecField(
        processors=[ResizeToFit(1000,500)],
        image_field='original_image',
        format='JPEG',
        options={'quality':90}
        )
    
    def __unicode__(self):
        return self.caption

    def send_photo(self):
        photo_created.send(sender=self)

class ModType(models.Model):
    category = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.category

class Mod(models.Model):
    car = models.ForeignKey(Car, related_name='mods')
    modType = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    part = models.CharField(max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return self.part

    def send_mod(self):
        mod_created.send(sender=self)

class Circle(models.Model):
    moderator = models.ForeignKey(User)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.title

class Join(models.Model):
    group = models.ForeignKey(Circle)
    member = models.ForeignKey(User)

    def __unicode__(self):
        return self.group.title
    
class Topic(models.Model):
    group = models.ForeignKey(Circle)
    owner = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    body = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.body

    def send_topic(self):
        topic_created.send(sender=self)


class Response(models.Model):
    topic = models.ForeignKey(Topic)
    responder = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    body = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.body

    def send_response(self):
        response_created.send(sender=self)

class Feedback(models.Model):
    sender = models.EmailField()
    title = models.CharField(max_length=30)
    body = models.TextField(null=True, blank=True)
    submit_date = models.DateTimeField('date submitted')
    
    def __unicode__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=30)
    embedCode = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title

class Board(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.title

class BoardPhoto(models.Model):
    uploader = models.ForeignKey(User)
    board = models.ForeignKey(Board)
    post_date = models.DateTimeField('date posted')
    caption = models.CharField(max_length=100, null=True, blank=True)
    original_image = models.ImageField(upload_to='board_photo_profiles', blank=True, null=True)
    thumbnail_image = ImageSpecField(
        image_field = 'original_image',
        processors = [SmartResize(300,300)],
        format='JPEG',
        options={'quality':90},
        )
    display_image = ImageSpecField(
        image_field = 'original_image',
        processors = [ResizeToFit(900,600)],
        format='JPEG',
        options={'quality':90},
        )

    def __unicode__(self):
        return self.board.title

class PhotoLike(models.Model):
    user = models.ForeignKey(User)
    photo = models.ForeignKey(BoardPhoto)

    def __unicode__(self):
        return self.user.username

class PhotoComment(models.Model):
    photo = models.ForeignKey(BoardPhoto)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    body = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def send_photo_comment(self):
        photo_comment_created.send(sender=self)

# define signal handlers
@receiver(profile_created)
def SignalHandler_UserProfile(sender, **kwargs):
    userprofile = UserProfile.objects.get(user=sender.user)
    m = Message(
        recipient=sender.user,
        sender='FastFreshLife',
        viewed=False,
        title='Welcome %s!' % userprofile.display_name,
        body='<p>This is your FastFreshLife! Click <strong>"Add New Car"</strong> to start logging your latest ride.</p>',
        pub_date = datetime.now()
    )
    m.save()

@receiver(follow_created)
def SignalHandler_Follow(sender, **kwargs):
    userprofile_follower = UserProfile.objects.get(user=sender.follower)
    m = Message(
        recipient=sender.followed,
        sender='FastFreshLife',
        viewed=False,
        title='%s is now following you!' % userprofile_follower.display_name,
        body='<p><strong>Congratulations!</strong> Your fame is spreading far and wide.</p>',
        pub_date = datetime.now(),
        label = 'View Profile',
        action = '/journal/%s/' % sender.follower.username
    )
    m.save()

@receiver(like_created)
def SignalHandler_Like(sender, **kwargs):
    userprofile = UserProfile.objects.get(user=sender.user)
    m = Message(
        recipient=sender.post.car.owner,
        sender='FastFreshLife',
        viewed=False,
        title='%s liked your post!' % userprofile.display_name,
        body='<p><strong>Congratulations!</strong> %s liked your post titled "%s".</p>' % (sender.user.username, sender.post.title),
        pub_date = datetime.now(),
        label = 'View Profile',
        action = '/journal/%s/' % sender.user.username
    )
    m.save()

@receiver(vote_created)
def SignalHandler_Vote(sender, **kwargs):
    userprofile = UserProfile.objects.get(user=sender.user)
    m = Message(
        recipient=sender.car.owner,
        sender='FastFreshLife',
        viewed=False,
        title='%s gave your car a %s vote!' % (userprofile.display_name, sender.type),
        body='<p><strong>Congratulations!</strong> %s gave your car, %s, a %s vote.</p>' % (userprofile.display_name, sender.car.name, sender.type),
        pub_date = datetime.now(),
        label = 'View Profile',
        action = '/journal/%s/' % sender.user.username
    )
    m.save()
    
@receiver(car_created)
def SignalHandler_Car(sender, **kwargs):
    userprofile_owner = UserProfile.objects.get(user=sender.owner)
    followers = Follow.objects.filter(followed=sender.owner)
    for f in followers:
        m = Message(
            recipient=f.follower,
            sender='FastFreshLife',
            viewed=False,
            title='%s added a new car!' % userprofile_owner.display_name,
            body='<p><strong>Check it out!</strong> %s added a new car, %s, a %s %s %s</p>' % (userprofile_owner.display_name, sender.name, sender.make, sender.model, sender.year),
            pub_date = datetime.now(),
            label = 'View Car',
            action = '/journal/%s/car/%s' % (sender.owner.username, sender.pk)
            )
        m.save()

@receiver(post_created)
def SignalHandler_Post(sender, **kwargs):
    userprofile_owner = UserProfile.objects.get(user=sender.car.owner)
    followers = Follow.objects.filter(followed=sender.car.owner)
    for f in followers:
        m = Message(
            recipient=f.follower,
            sender='FastFreshLife',
            viewed=False,
            title='%s added a new post!' % userprofile_owner.display_name,
            body='<p><strong>Take a look!</strong> %s added a new post, %s.</p>' % (userprofile_owner.display_name, sender.title),
            pub_date = datetime.now(),
            label = 'View Post',
            action = '/journal/%s/car/%s/post/%s' % (sender.car.owner.username, sender.car.pk, sender.pk)
            )
        m.save()

@receiver(mod_created)
def SignalHandler_Mod(sender, **kwargs):
    userprofile_owner = UserProfile.objects.get(user=sender.car.owner)
    followers = Follow.objects.filter(followed=sender.car.owner)
    for f in followers:
        m = Message(
            recipient=f.follower,
            sender='FastFreshLife',
            viewed=False,
            title='%s added a new mod!' % userprofile_owner.display_name,
            body='<p><strong>Neat!</strong> %s added a new %s modification.</p>' % (userprofile_owner.display_name, sender.modType),
            pub_date = datetime.now(),
            label = 'View Mod',
            action = '/journal/%s/car/%s/mod/%s' % (sender.car.owner.username, sender.car.pk, sender.pk)
            )
        m.save()

@receiver(photo_created)
def SignalHandler_Photo(sender, **kwargs):
    userprofile_owner = UserProfile.objects.get(user=sender.car.owner)
    followers = Follow.objects.filter(followed=sender.car.owner)
    for f in followers:
        m = Message(
            recipient=f.follower,
            sender='FastFreshLife',
            viewed=False,
            title='%s added a new photo!' % userprofile_owner.display_name,
            body='<p><strong>Nice pic!</strong> %s added a new photo for %s.</p>' % (userprofile_owner.display_name, sender.car.name),
            pub_date = datetime.now(),
            label = 'View Photos',
            action = '/journal/%s/car/%s/photo' % (sender.car.owner.username, sender.car.pk)
            )
        m.save()

@receiver(topic_created)
def SignalHandler_Topic(sender, **kwargs):
    joins = Join.objects.filter(group=sender.group)
    for j in joins:
        m = Message(
            recipient=j.member,
            sender='FastFreshLife',
            viewed=False,
            title='New topic addded to %s!' % sender.group.title,
            body='<p><strong>%s</strong></p>' % sender.body,
            pub_date = datetime.now(),
            label = 'View Topic',
            action = '/groups/%s/topic/%s/view' % (sender.group.pk, sender.pk)
            )
        m.save()

@receiver(response_created)
def SignalHandler_Response(sender, **kwargs):
    topic_owner = sender.topic.owner
    responses = Response.objects.filter(topic=sender.topic)
    responders = []
    for response in responses:
        if response.responder != topic_owner and response.responder not in responders:
            responders.append(response.responder)
            
    # send message to topic owner
    m = Message(
        recipient=topic_owner,
        sender='FastFreshLife',
        viewed=False,
        title='New response to your topic: %s' % sender.topic.body,
        body='<p><strong>%s</strong></p>' % sender.body,
        pub_date = datetime.now(),
        label = 'View Topic',
        action = '/groups/%s/topic/%s/view' % (sender.topic.group.pk, sender.topic.pk)        
    )
    m.save()
    
    # send message to responders
    for r in responders:
        m = Message(
            recipient=r,
            sender='FastFreshLife',
            viewed=False,
            title='New response to the topic: %s!' % sender.topic.title,
            body='<p><strong>%s</strong></p>' % sender.body,
            pub_date = datetime.now(),
            label = 'View Topic',
            action = '/groups/%s/topic/%s/view' % (sender.topic.group.pk, sender.topic.pk)
            )
        m.save()
        
@receiver(post_comment_created)
def SignalHandler_PostComment(sender, **kwargs):
    current_post = sender.post
    
    # get commenters, exclude post author and comment author
    current_post_comments = PostComment.objects.filter(post=current_post)
    commenters = []
    for c in current_post_comments:
        if c.user != current_post.car.owner and c.user != sender.user and c.user not in commenters:
            commenters.append(c.user)

    for commenter in commenters:
        m = Message(
            recipient=commmenter,
            sender='FastFreshLife',
            viewed = False,
            title = 'New comment on: %s' % current_post.title,
            body='<p><strong>%s</strong></p>' % sender.body,
            pub_date = datetime.now(),
            label = 'View Post',
            action = '/journal/%s/car/%s/post/%s' % (current_post.car.owner.username, current_post.car.pk, current_post.pk)
        )
        m.save()
    
    # send message to post author
    m = Message(
        recipient = current_post.car.owner,
        sender='FastFreshLife',
        viewed = False,
        title = 'New comment on: %s' % current_post.title,
        body='<p><strong>%s</strong></p>' % sender.body,
        pub_date = datetime.now(),
        label = 'View Post',
        action = '/journal/%s/car/%s/post/%s' % (current_post.car.owner.username, current_post.car.pk, current_post.pk)        
    )
    m.save()

@receiver(photo_comment_created)
def SignalHandler_PhotoComment(sender, **kwargs):
    current_photo = sender.photo
    
    # get commenters
    current_photo_comments = PhotoComment.objects.filter(photo=current_photo)
    commenters = []
    for c in current_photo_comments:
        if c.user != current_photo.uploader and c.user != sender.user and c.user not in commenters:
            commenters.append(c.user)
    
    for commenter in commenters:
        m = Message(
            recipient=commenter,
            sender='FastFreshLife',
            viewed = False,
            title = 'New photo comment',
            body='<p><strong>%s</strong></p>' % sender.body,
            pub_date = datetime.now(),
            label = 'View Photo',
            action = '/photoboard/%s/photo/%s' % (current_photo.board.pk, current_photo.pk)
        )
        m.save()
        
    # send message to photo uploader
    m = Message(
        recipient = current_photo.uploader,
        sender='FastFreshLife',
        viewed = False,
        title = 'New photo comment',
        body='<p><strong>%s</strong></p>' % sender.body,
        pub_date = datetime.now(),
        label = 'View Photo',
        action = '/photoboard/%s/photo/%s' % (current_photo.board.pk, current_photo.pk)
    )
    m.save()    