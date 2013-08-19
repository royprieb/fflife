from django import forms
from captcha.fields import CaptchaField
from blog.models import CarMake, CarModel
from blog.models import Car, Mod
from blog.models import Post, Message
from blog.models import Feedback
from ckeditor.widgets import CKEditorWidget
from taggit.forms import *

# form classes here
class loginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class':'input-large',
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class':'input-large',
        }))

class feedbackForm(forms.Form):
    sender_email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Sender Email',
        'class': 'input-xlarge',
        }))
    msg_title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Subject',
        'class':'input-xlarge',
        }))
    msg_body = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'input-xlarge',
        'placeholder':'Message',
        'rows':'4',
        }))

class accountForm(forms.Form):
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class':'input-xlarge',
        }))
    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={
        'placeholder': 'Email',
        'class': 'input-xlarge',
        }))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class':'input-xlarge',
        }))
    photo = forms.FileField(required=False, widget=forms.FileInput)
    motto = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Motto ("My Need For Speed")',
        'class':'input-xlarge',
        }))
    city = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'City',
        'class':'input-xlarge',
        }))
    state = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'State',
        'class':'input-xlarge',
        }))
    country = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Country',
        'class':'input-xlarge',
        }))
    captcha = CaptchaField()

class vendorAccountForm(forms.Form):
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class':'input-xlarge',
        }))
    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={
        'placeholder': 'Email',
        'class': 'input-xlarge',
        }))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class':'input-xlarge',
        }))
    photo = forms.FileField(required=False, widget=forms.FileInput)
    vendor_category = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Vendor Type',
        'class':'vendorCategoryTypeahead input-xlarge',
        'autocomplete':'off',
        }))
    website = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Website URL',
        'class':'input-xlarge',
        }))
    street_address = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Street Address',
        'class':'input-xlarge',
        }))
    city = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'City',
        'class':'input-xlarge',
        }))
    state = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'State',
        'class':'input-xlarge',
        }))
    country = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Country',
        'class':'input-xlarge',
        }))
    captcha = CaptchaField()

class carForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Choose A Name',
        'class': 'input-block-level',
        }))
    image = forms.FileField(required=False, widget=forms.FileInput)
    make = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Choose A Make',
        'class': 'carMakeTypeahead input-block-level',
        'autocomplete': 'off',
        }))
    model = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Choose A Model',
        'class': 'carModelTypeahead input-block-level',
        'autocomplete': 'off',
        }))
    year =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'placeholder':' Select Year',
        'class': 'input-block-level',
        }))
    c_tags = TagField(required=False, widget=forms.TextInput(attrs={
        'placeholder':' Add Tags',
        'class': 'input-block-level',
        }))

class modForm(forms.Form):
    modType = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Select Modification Type',
        'class': 'modTypeTypeahead input-block-level',
        }))
    brand = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Select Brand Type',
        'class': 'input-block-level',
        }))
    part = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Select Part Type',
        'class': 'input-block-level',
        }))
    # edit set
    modType_edit = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Select Modification Type',
        'class': 'modTypeTypeahead input-block-level',
        }))
    brand_edit = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Select Brand Type',
        'class': 'input-block-level',
        }))
    part_edit = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Select Part Type',
        'class': 'input-block-level',
        }))

class photoForm(forms.Form):
    caption = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Add A Caption',
        'class': 'input-block-level',
        }))
    photo = forms.FileField(required=False, widget=forms.FileInput)

class postForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Choose A Title',
        'class': 'input-block-level',
        }))
    body = forms.CharField(required=False, widget=CKEditorWidget(attrs={
        'class': 'input-block-level',
        'placeholder':'body',
        'rows':'20',
        }))
    p_tags = TagField(required=False, widget=forms.TextInput(attrs={
        'class': 'input-block-level',
        'placeholder':'Add Tags',
        }))

class newGroupForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your Group Title',
        'class': 'input-block-level',
        }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'input-block-level',
        'placeholder':'Describe Your Group Below',
        'rows':'4',
        }))
    
class messageForm(forms.Form):
    subject = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Subject',
        'class':'input-block-level',
        }))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'input-block-level',
        'placeholder':'Message',
        'rows':'4',
        }))

class topicForm(forms.Form):
    body = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'input-block-level',
        'placeholder':'Your Message Here',
        'rows':'4',
        }))

class commentForm(forms.Form):
    body = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'input-block-level',
        'placeholder':'Your Message Here',
        'rows':'2',
        }))