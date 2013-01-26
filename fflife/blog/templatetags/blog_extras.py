# additional template tags for blog
from blog.models import CarMake
from blog.models import CarModel

from django import template

register = template.Library()

@register.inclusion_tag("make_model_year_select.html")
def make_model_year_select():
    make_list = CarMake.objects.all().order_by('name')
    model_list = CarModel.objects.all().order_by('name')
    return {
        'make_list':make_list,
        'model_list':model_list,
    }

#@register.inclusion_tag("add_car_select.html")
#def add_car_select():
#    make_list = CarMake.objects.all().order_by('name')
#    model_list = CarModel.objects.all().order_by('name')
#    return{
#        'make_list':make_list,
#        'model_list':model_list,
#    }
