import datetime
from haystack.indexes import *
from haystack import site
from blog.models import Car, Post
from blog.models import Mod

#class CarIndex(SearchIndex):
class CarIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    make = CharField(model_attr='make', faceted=True)
    model = CharField(model_attr='model', faceted=True)
    year = IntegerField(model_attr='year', faceted=True)
    
    def get_model(self):
        return Car

#class PostIndex(SearchIndex):
class PostIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)

    def get_model(self):
        return Post

#class ModIndex(SearchIndex):
class ModIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)

    def get_model(self):
        return Mod

site.register(Mod, ModIndex)
site.register(Post, PostIndex)
site.register(Car, CarIndex)
