import os
from django.db import models
from django.contrib.auth.models import User
# not sure if the below import is required leaving commented
#from django.conf import settings
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors.resize import ResizeToFit, SmartResize
from taggit.managers import TaggableManager

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    original_image = models.ImageField(upload_to='profiles', blank=True, null=True)
    display_image = ImageSpecField(
        [SmartResize(70,70)],
        image_field='original_image', format='JPEG', options={'quality':90})
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    motto = models.CharField(max_length=100, null=True, blank = True)
    
    def __unicode__(self):
        return self.user.username

class Journal(models.Model):
    owner = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.owner.username

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
    journal = models.ForeignKey(Journal)
    make = models.ForeignKey(CarMake, null=True, blank=True)
    model = models.ForeignKey(CarModel, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    tags = TaggableManager(blank=True)
    
    def __unicode__(self):
        return self.name

class Vote(models.Model):
    FAST = 'fast'
    FRESH = 'fresh'
    BOSS = 'boss'
    VOTE_TYPE_CHOICES = (
        (FAST, 'fast'),
        (FRESH, 'fresh'),
        (BOSS, 'boss'),
    )
    user = models.ForeignKey(User)
    car = models.ForeignKey(Car)
    type = models.CharField(max_length=10, choices=VOTE_TYPE_CHOICES)
    
    def __unicode__(self):
        return self.type

class Follow(models.Model):
    user = models.ForeignKey(User)
    car = models.ForeignKey(Car)
    
    def __unicode__(self):
        return self.car.name

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='user_message_sender')
    receiver = models.ForeignKey(User, related_name='user_message_receiver')
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    send_date = models.DateTimeField('date sent')
    
    def __unicode__(self):
        return self.title

class Event(models.Model):
    WELCOME = 'welcome'
    CAR = 'car'
    MSG = 'message'
    VOTE = 'vote'
    LIKE = 'like'
    FOLLOW = 'follow'
    EVENT_TYPE_CHOICES = (
        (WELCOME, 'welcome'),
        (CAR, 'car'),
        (MSG, 'message'),
        (VOTE, 'vote'),
        (LIKE, 'like'),
        (FOLLOW, 'follow'),
    )
    
    type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES)
    user = models.ForeignKey(User)
    viewed = models.BooleanField()
    pub_date = models.DateTimeField('date published')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    next = models.URLField(null=True, blank=True)
    
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

class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    
    def __unicode__(self):
        return self.post.title

class FeaturedPost(models.Model):
    original_image = models.ImageField(upload_to='features')
    display_image = ImageSpecField(
        [SmartResize(150,100)],
        image_field='original_image', format='JPEG', options={'quality':90})
    pub_date = models.DateTimeField('date published')
    title = models.CharField(max_length = 100)
    body = RichTextField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    
    def __unicode__(self):
        return self.title

class Album(models.Model):
    car = models.ForeignKey(Car)
    
    def __unicode__(self):
        return self.car.name

class HeroPhoto(models.Model):
    original_image = models.ImageField(upload_to='hero')
    display_image = ImageSpecField(
        [SmartResize(470,350)],
        image_field='original_image', format='JPEG', options={'quality':90})

def get_image_path(instance, filename):
    return os.path.join('gallery/',str(instance.id), filename)

class Photo(models.Model):
    album = models.ForeignKey(Album)
    caption = models.CharField(max_length=100, null=True, blank=True)
    original_image = models.ImageField(upload_to=get_image_path)
    thumb_image = ImageSpecField(
        [SmartResize(150,150)],
        image_field='original_image', format='JPEG', options={'quality':90})
    display_image = ImageSpecField(
        [ResizeToFit(1000,500)],
        image_field='original_image', format='JPEG', options={'quality':90})
    
    def __unicode__(self):
        return self.caption

class FeaturedPhoto(models.Model):
    photo = models.ForeignKey(Photo)
    
    def __unicode__(self):
        return self.photo.caption

class ModType(models.Model):
    category = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.category

class Mod(models.Model):
    car = models.ForeignKey(Car, related_name='mods')
    modType = models.ForeignKey(ModType)
    brand = models.CharField(max_length=100, null=True, blank=True)
    part = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.part

class StaticPage(models.Model):
    ABOUT = 'about'
    CONTACT = 'contact'
    ADVERTISE = 'advertise'
    TERMS = 'terms'
    PRIVACY = 'privacy'
    STATICPAGE_TYPE_CHOICES = (
        (ABOUT, 'about'),
        (CONTACT, 'contact'),
        (ADVERTISE, 'advertise'),
        (TERMS, 'terms'),
        (PRIVACY, 'privacy'),
    )
    type = models.CharField(max_length=12, choices=STATICPAGE_TYPE_CHOICES)
    body = RichTextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.type

class Feedback(models.Model):
    sender = models.EmailField()
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    submit_date = models.DateTimeField('date submitted')
    
    def __unicode__(self):
        return self.title