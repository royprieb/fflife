from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from blog.models import UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
#from django.contrib.auth.views import password_change
from django.template import RequestContext
from blog.models import Journal, Car
from blog.models import CarMake, CarModel
from blog.models import Photo, Mod
from blog.models import Album, Post
from blog.models import FeaturedPhoto, FeaturedPost
from blog.models import HeroPhoto, Message
from blog.models import Vote, Follow
from blog.models import Event, Like
from blog.models import StaticPage, Feedback
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Count
from captcha.fields import CaptchaField
from django.contrib.auth.models import Group
# comment deletion imports
from django.contrib.comments.models import Comment
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.comments.views.moderation import perform_delete
# search form
from haystack.forms import SearchForm
# for ajax functions
from django.core import serializers

# form classes here
class newAccountForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    photo = forms.FileField(label="Profile Picture", required=False)
    motto = forms.CharField(max_length=100, label="Motto", required=False)
    city = forms.CharField(max_length=100, label="City", required=False)
    state = forms.CharField(max_length=100, label="State", required=False)
    country = forms.CharField(max_length=100, label="Country", required=False)
    captcha = CaptchaField()
    next = forms.CharField(widget=forms.HiddenInput)

class accountEditForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    email = forms.EmailField(label="Email Address")
    photo = forms.FileField(label="Profile Picture", required=False)
    motto = forms.CharField(max_length=100, label="Motto", required=False)
    city = forms.CharField(max_length=100, label="City", required=False)
    state = forms.CharField(max_length=100, label="State", required=False)
    country = forms.CharField(max_length=100, label="Country", required=False)
    next = forms.CharField(widget=forms.HiddenInput)

class loginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    next = forms.CharField(widget=forms.HiddenInput)

class journalEditForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title")
    description = forms.CharField(max_length=200, label="Description")

class carForm(forms.ModelForm):
    year =  forms.IntegerField(required=True)
    #    firstMake = CarMake.objects.get(pk=1)
    #make = forms.ModelChoiceField(queryset=CarMake.objects.all().order_by('name'), initial={'make':firstMake.pk}, required=True)
    make = forms.ModelChoiceField(queryset=CarMake.objects.all().order_by('name'), required=True)
    #model = forms.ModelChoiceField(queryset=CarModel.objects.filter(carmaker=firstMake).order_by('name'), required=True)
    model = forms.ModelChoiceField(queryset=CarModel.objects.all().order_by('name'), required=True)
    class Meta:
        fields =('year','make','model','tags')
        model = Car
        exclude = ('journal','name')

class carEditForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ('journal','make','model','year')

class modForm(forms.ModelForm):
    class Meta:
        model = Mod
        exclude = ('car',)

class albumForm(forms.Form):
    caption = forms.CharField(max_length=100, label="Caption")
    photo = forms.FileField()

class postForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('car','pub_date')

class messageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('send_date','sender','receiver')

class feedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('submit_date')

# function definitions
def all_json_models(request, makeId):
    if makeId == "0":
        models = CarModel.objects.all().order_by('name')
    else:
        current_make = CarMake.objects.get(pk=makeId)
        models = CarModel.objects.filter(carmaker=current_make).order_by('name')
    json_models = serializers.serialize("json", models)
    return HttpResponse(json_models, content_type="application/json")

def canBeInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def filter(request):
    #searchform
    navSearchForm = SearchForm()
    
    results = ''
    if request.method == 'POST':
        cars = Car.objects.all()
        
        make = request.POST['make']
        if make == '0':
            s1 = cars
        else:
            s1 = cars.filter(make=make)
        
        model = request.POST['model']
        if model == '0':
            s2 = cars
        else:
            s2 = cars.filter(model=model)
        
        startyear = request.POST['startyear']
        if startyear != '' and canBeInt(startyear):
            s3 = cars.filter(year__gte=int(float(startyear)))
        else:
            s3 = cars
        
        endyear = request.POST['endyear']
        if endyear != ''  and canBeInt(endyear):
            s4 = cars.filter(year__lte=int(endyear))
        else:
            s4 = cars
        
        r = s1 & s2 & s3 & s4
        
        results = r.annotate(num_votes=Count('vote'))
        
        return render(request,'filter.html',{
                      'navSearchForm':navSearchForm,
                      'results':results,
                      })
    
    else:
        
        return render(request,'filter.html', {
                      'navSearchForm':navSearchForm,
                      'results':results,
                      })

def rank(request):
    #searchform
    navSearchForm = SearchForm()
    
    fastList = Car.objects.filter(vote__type='fast').annotate(num_votes=Count('vote')).order_by('-num_votes')
    freshList= Car.objects.filter(vote__type='fresh').annotate(num_votes=Count('vote')).order_by('-num_votes')
    bossList = Car.objects.filter(vote__type='boss').annotate(num_votes=Count('vote')).order_by('-num_votes')
    
    return render(request,'rank.html', {
                  'fastList':fastList,
                  'freshList':freshList,
                  'bossList':bossList,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  })

def advertise(request):
    #searchform
    navSearchForm = SearchForm()
    #content
    content = StaticPage.objects.get(type='advertise')
    
    #contact form
    if request.method == 'POST':
        form = feedbackForm(request.POST)
        
        if form.is_valid():
            sender = form.cleaned_data['sender']
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            
            # create a new message
            feedback = Feedback(
                                sender = sender,
                                title = title,
                                body = body,
                                submit_date = datetime.now(),
                                )
            feedback.save()
            
            return render(request, 'advertisesubmit.html',{
                          'navSearchForm':navSearchForm,
                          'next': request.path,
                          })
        
        else:
            return HttpResponse('invalid data')
    else:
        form = feedbackForm()
        
        return render(request,'advertise.html',{
                      'navSearchForm':navSearchForm,
                      'content':content,
                      'form': form,
                      'next':request.path,
                      })

def terms(request):
    #searchform
    navSearchForm = SearchForm()
    #content
    content = StaticPage.objects.get(type='terms')
    
    return render(request,'terms.html',{
                  'navSearchForm':navSearchForm,
                  'content':content,
                  'next':request.path,
                  })

def privacy(request):
    #searchform
    navSearchForm = SearchForm()
    #content
    content = StaticPage.objects.get(type='privacy')
    
    return render(request,'privacy.html',{
                  'navSearchForm':navSearchForm,
                  'content':content,
                  'next':request.path,
                  })

def index(request):
    # hero feature randomly selected
    hero_photos = HeroPhoto.objects.order_by('?')
    hero_photo = ''
    if hero_photos.count() >= 1:
        hero_photo = hero_photos[0]
    
    featured_posts = FeaturedPost.objects.order_by('-pub_date')[:3]
    recent_posts = Post.objects.order_by('-pub_date')[:6]
    
    # featured photos randomly selected
    featured_photos = FeaturedPhoto.objects.order_by('?')[:9]
    
    # top5 lists
    fastList = Car.objects.filter(vote__type='fast').annotate(num_votes=Count('vote')).order_by('-num_votes')[:5]
    freshList= Car.objects.filter(vote__type='fresh').annotate(num_votes=Count('vote')).order_by('-num_votes')[:5]
    bossList = Car.objects.filter(vote__type='boss').annotate(num_votes=Count('vote')).order_by('-num_votes')[:5]
    
    # eventcounts if authenticated
    if request.user.is_authenticated():
        newEventCount = Event.objects.filter(user=request.user).filter(viewed=False).count() 
    else:
        newEventCount = ''
    
    #searchform
    navSearchForm = SearchForm()
    
    return render(request, 'index.html',{
                  'hero_photo': hero_photo,
                  'featured_posts': featured_posts,
                  'recent_posts': recent_posts,
                  'featured_photos': featured_photos,
                  'fastList': fastList,
                  'freshList': freshList,
                  'bossList': bossList,
                  'newEventCount': newEventCount,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  })

def featureVisit(request, featureId):
    #searchform
    navSearchForm = SearchForm()
    
    feature_post = FeaturedPost.objects.get(pk=featureId)
    tags = feature_post.tags.all()
    recent_features = FeaturedPost.objects.order_by('-pub_date').exclude(pk=featureId)[:5]
    
    return render(request, 'featureVisit.html',{
                  'feature_post':feature_post,
                  'tags': tags,
                  'recent_features': recent_features,
                  'navSearchForm': navSearchForm,
                  'next':request.path,
                  })

def postVisit(request, carId, postId):
    c = Car.objects.get(pk=carId)
    j = c.journal
    cars = Car.objects.filter(journal=j)
    a = Album.objects.get(car=c)
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car=c)
    photos = Photo.objects.filter(album=a)
    
    p = Post.objects.get(pk=postId)
    tags = p.tags.all()
    
    # previous and next
    newerposts = Post.objects.filter(car=c).filter(pub_date__gt=p.pub_date)
    if newerposts.count() == 0:
        next_p = ''
    else:
        next_p = newerposts.order_by('pub_date')[0]
    
    olderposts = Post.objects.filter(car=c).filter(pub_date__lt=p.pub_date)
    if olderposts.count() == 0:
        prev_p = ''
    else:
        prev_p = olderposts.order_by('-pub_date')[0]
    
    # like counts
    likecount = Like.objects.filter(post=p).count()
    
    #searchform
    navSearchForm = SearchForm()
    
    return render(request, 'postVisit.html',{
                  'car': c,
                  'journal': j,
                  'cars':cars,
                  'album': a,
                  'posts': recent_posts,
                  'mods': m,
                  'photos': photos,
                  'navSearchForm':navSearchForm,
                  'next': request.path,
                  'post': p,
                  'tags': tags,
                  'next_p':next_p,
                  'prev_p':prev_p,
                  'likecount': likecount,
                  'next': request.path,
                  })

@login_required
def like(request, carId, postId):
    u = request.user
    c = Car.objects.get(pk=carId)
    p = Post.objects.get(pk=postId)
    next = request.GET.get('next')
    
    # like status
    liketest = Like.objects.filter(user = u.pk).filter(post = p).exists()
    if not liketest:
        l = Like(
                 user = u,
                 post = p,
                 )
        l.save()
        
        #create events for post/car owner
        ev = Event(
                   type = 'like',
                   user = c.journal.owner,
                   viewed = False,
                   pub_date = datetime.now(),
                   title = '%s liked your post, "%s"!' % (u.username, p.title),
                   )
        ev.save()
    
    
    return HttpResponseRedirect(next)

def carVisit(request, carId):
    c = Car.objects.get(pk=carId)
    tags = c.tags.all()
    j = c.journal
    cars = Car.objects.filter(journal=j)
    a = Album.objects.get(car=c)
    sort = request.GET.get('sort')
    if sort == 'newest':
        posts = Post.objects.filter(car=c).order_by('-pub_date')
    else:
        posts = Post.objects.filter(car=c).order_by('pub_date')
    m = Mod.objects.filter(car=c)
    photos = Photo.objects.filter(album=a)
    
    # vote counts
    fastvotecount = Vote.objects.filter(car=c).filter(type='fast').count()
    freshvotecount = Vote.objects.filter(car=c).filter(type='fresh').count()
    bossvotecount = Vote.objects.filter(car=c).filter(type='boss').count()
    
    # check follow status
    if request.user.is_authenticated():
        if Follow.objects.filter(user = request.user.pk).filter(car = c).exists():
            followStatus = True
        else:
            followStatus = False
    else:
        followStatus = False
    
    #searchform
    navSearchForm = SearchForm()
    
    return render(request, 'carvisit.html',{
                  'car': c,
                  'tags':tags,
                  'journal': j,
                  'cars':cars,
                  'album': a,
                  'posts': posts,
                  'mods': m,
                  'photos': photos,
                  'fastvotecount':fastvotecount,
                  'freshvotecount':freshvotecount,
                  'bossvotecount':bossvotecount,
                  'followStatus':followStatus,
                  'navSearchForm':navSearchForm,
                  'next': request.path,
                  })

@login_required
def vote(request, carId, voteType):
    u = request.user
    c = Car.objects.get(pk=carId)
    t = voteType
    next = request.GET.get('next')
    
    # vote status
    votetest = Vote.objects.filter(user = u.pk).filter(car = c).exists()
    if not votetest:
        v = Vote(
                 user = u,
                 car = c,
                 type = t,
                 )
        v.save()
        
        #create events for post/car owner
        ev = Event(
                   type = 'vote',
                   user = c.journal.owner,
                   viewed = False,
                   pub_date = datetime.now(),
                   title = '%s gave your car, "%s", a %s vote!' % (u.username, c.name, t),
                   )
        ev.save()
    
    return HttpResponseRedirect(next)

@login_required
def follow(request, carId):
    u = request.user
    c = Car.objects.get(pk=carId)
    
    # follow status
    followtest = Follow.objects.filter(user = u.pk).filter(car = c).exists()
    if not followtest:
        f = Follow(
                   user = u,
                   car = c,
                   )
        f.save()
        
        #create events for post/car owner
        ev = Event(
                   type = 'follow',
                   user = c.journal.owner,
                   viewed = False,
                   pub_date = datetime.now(),
                   title = '%s is now following your car, "%s".' % (u.username, c.name),
                   )
        ev.save()
    
    url = '/visit/car/'
    url += str(c.pk)
    
    return HttpResponseRedirect(url)

@login_required
def stopFollow(request, carId):
    u = request.user
    c = Car.objects.get(pk=carId)
    follow = Follow.objects.get(user=u, car=c)
    follow.delete()
    
    url = '/visit/car/'
    url += str(c.pk)
    
    return HttpResponseRedirect(url)

@login_required
def message(request, ownerId):
    o = User.objects.get(pk=ownerId)
    j = Journal.objects.get(owner=o)
    cars = Car.objects.filter(journal=j)
    #searchform
    navSearchForm = SearchForm()
    
    if request.method =='POST':
        form = messageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            
            # create a new message
            msg = Message(
                          sender = request.user,
                          receiver = o,
                          title = title,
                          body = body,
                          send_date = datetime.now()
                          )
            msg.save()
            
            # create an event
            next = 'http://fastfreshlife.royprieb.webfactional.com/message/'
            next += str(request.user.pk)
            next += '/'
            
            ev = Event(
                       type = 'message',
                       user = o,
                       viewed = False,
                       title = 'Message from %s: %s' % (request.user, msg.title),
                       description = msg.body,
                       next = next,
                       pub_date = datetime.now(),
                       )
            ev.save()
            
            return render(request, 'messagesent.html',{
                          'journal':j,
                          'cars': cars,
                          'form': form,
                          'navSearchForm':navSearchForm,
                          'next': request.path,
                          })
        
        else:
            
            return HttpResponse('invalid data')
    
    else:
        form = messageForm()
        
        return render(request,'message.html',{
                      'journal':j,
                      'cars': cars,
                      'form': form,
                      'navSearchForm': navSearchForm,
                      'next': request.path,
                      })

def contact(request):
    #searchform
    navSearchForm = SearchForm()
    #content
    content = StaticPage.objects.get(type='contact')
    
    #contact form
    if request.method == 'POST':
        form = feedbackForm(request.POST)
        
        if form.is_valid():
            sender = form.cleaned_data['sender']
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            
            # create a new message
            feedback = Feedback(
                                sender = sender,
                                title = title,
                                body = body,
                                submit_date = datetime.now(),
                                )
            feedback.save()
            
            return render(request, 'contactsubmit.html',{
                          'navSearchForm':navSearchForm,
                          'next': request.path,
                          })
        
        else:
            return HttpResponse('invalid data')
    else:
        form = feedbackForm()
        
        return render(request,'contact.html',{
                      'navSearchForm':navSearchForm,
                      'content':content,
                      'form': form,
                      'next':request.path,
                      })

def about(request):
    #searchform
    navSearchForm = SearchForm()
    #content
    content = StaticPage.objects.get(type='about')
    
    return render(request,'about.html',{
                  'navSearchForm':navSearchForm,
                  'content':content,
                  'next':request.path,
                  })

def newAccount (request):
    #searchform
    navSearchForm = SearchForm()
    #next placeholder
    next = '/'
    
    if request.method == 'POST':
        form = newAccountForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            motto = form.cleaned_data['motto']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            next = form.cleaned_data['next']
            
            # create a new user
            owner = User.objects.create_user(
                                             username,
                                             email,
                                             pw,
                                             )
            
            # add user to comment_ready group
            g = Group.objects.get(name='comment_ready')
            g.user_set.add(owner)
            
            # login user
            user = authenticate(username=username, password=pw)
            login(request, user)
            
            # create user profile
            p = UserProfile(
                            user=owner,
                            motto=motto,
                            city=city,
                            state=state,
                            country=country,
                            )
            p.save()
            
            # save profile photo
            if request.FILES:
                image_file = request.FILES['photo']
                p.original_image.save(image_file.name, image_file)
                p.save()
            
            # create journal and welcome event
            j = Journal(
                        owner=owner,
                        )
            j.save()
            
            ev = Event(
                       type = 'welcome',
                       user = owner,
                       viewed = False,
                       pub_date = datetime.now(),
                       title = 'Welcome %s' % owner.username,
                       description = 'This is your FastFreshLife Journal. When you are ready, click "Add New Car" to start logging your latest ride.',
                       )
            ev.save()
            
            return render(request,'welcome.html',{
                          'navSearchForm':navSearchForm,
                          'next':next,
                          })
    
    else:
        next = request.GET.get('next','')
        form = newAccountForm()
        form = newAccountForm(initial={
                              'next':next,
                              })
    
    return render(request,'newaccount.html', {
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':next,
                  })

@login_required
def accountEdit(request):
    #searchform
    navSearchForm = SearchForm()
    #next placeholder
    next = '/'
    
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = accountEditForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            motto = form.cleaned_data['motto']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            next = form.cleaned_data['next']
            
            # update user information
            u = User.objects.get(pk=request.user.pk)
            u.username = username
            u.email = email
            u.save()
            
            # update profile information
            profile.motto = motto
            profile.city = city
            profile.state = state
            profile.country = country
            profile.save()
            
            # add profile image
            if request.FILES:
                image_file = request.FILES['photo']
                profile.original_image.save(image_file.name, image_file)
                profile.save()
            
            # redirect to next
            return HttpResponseRedirect(next)
    
    else:
        # provide the form for editing
        next = request.GET.get('next','')
        form = accountEditForm(initial={
                               'username': request.user.username,
                               'email': request.user.email,
                               'motto': profile.motto,
                               'city': profile.city,
                               'state': profile.state,
                               'country': profile.country,
                               'next': next,
                               })
    
    return render(request,'accountedit.html', {
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':next,
                  })

@login_required
def accountDelete(request):
    request.user.delete()
    return HttpResponseRedirect('/')

def logoutuser (request):
    logout(request)
    return HttpResponseRedirect('/')

def loginuser (request):
    #searchform
    navSearchForm = SearchForm()
    #next placeholder
    next = '/'
    
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            next = form.cleaned_data['next']
            user = authenticate(
                                username = username,
                                password = password,
                                )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next)
    
    else:
        next = request.GET.get('next','')
        form = loginForm(initial={
                         'next': next,
                         })
    
    return render(request, 'login.html', {
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':next,
                  })

@login_required
def journalView(request):
    #searchform
    navSearchForm = SearchForm()
    
    j = Journal.objects.get(owner=request.user)
    events = Event.objects.filter(user=request.user).order_by('-pub_date')
    for event in events:
        event.viewed = True
        event.save()
    cars = Car.objects.filter(journal=j)
    
    return render(request,'journalview.html',{
                  'journal':j,
                  'events': events,
                  'cars':cars,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  })

@login_required
def journalEdit(request):
    #searchform
    navSearchForm = SearchForm()
    
    journal = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=journal)
    if request.method == 'POST':
        form = journalEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            
            journal.title = title
            journal.description = description
            journal.save()
            
            return HttpResponseRedirect('/journal/view/')
        else:
            return HttpResponse('invalid form')
    
    else:
        form = journalEditForm(initial={
                               'title': journal.title,
                               'description': journal.description,
                               })
        
        return render(request, 'journaledit.html', {
                      'journal':journal,
                      'cars':cars,
                      'form':form,
                      'navSearchForm':navSearchForm,
                      'next':request.path,
                      })

@login_required
def carNew(request):
    #searchform
    navSearchForm = SearchForm()
    
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    if request.method == 'POST':
        form = carForm(request.POST)
        if form.is_valid():
            make = form.cleaned_data['make']
            model = form.cleaned_data['model']
            year = form.cleaned_data['year']
            tags = form.cleaned_data['tags']
            
            # create new car
            c = Car(
                    journal=Journal.objects.get(owner=request.user),
                    name="%s's car" % request.user.username,
                    make=make,
                    model=model,
                    year=year,
                    )
            c.save()
            
            #add tags to the post
            for tag in tags:
                c.tags.add(tag)
            
            # create gallery
            a = Album(
                      car = c,
                      )
            a.save()
            
            # set url for the car view
            u = '/journal/car/'
            u += str(c.pk)
            u += '/view/?sort=oldest'
            
            return HttpResponseRedirect(u)
    
    else:
        form = carForm()
    
    return render(request, 'carnew.html', {
                  'journal':j,
                  'cars':cars,
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  })

@login_required
def carView(request, carId):
    #searchform
    navSearchForm = SearchForm()
    
    # carview variables: journal, post, modlist, gallery
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    tags = c.tags.all()
    sort = request.GET.get('sort')
    if sort == 'newest':
        posts = Post.objects.filter(car=c).order_by('pub_date')
    else:
        posts = Post.objects.filter(car=c).order_by('-pub_date')
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(car=c)
    photos = Photo.objects.filter(album=a)
    
    # vote counts
    fastvotecount = Vote.objects.filter(car=c).filter(type='fast').count()
    freshvotecount = Vote.objects.filter(car=c).filter(type='fresh').count()
    bossvotecount = Vote.objects.filter(car=c).filter(type='boss').count()
    
    # vote status
    votetest = Vote.objects.filter(user = request.user).filter(car = c).exists()
    if votetest:
        votestatus = True
    else:
        votestatus = False
    
    # tab display
    posts_tab = 'checked'
    mods_tab = ''
    album_tab = ''
    
    return render(request, 'carview.html', {
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'tags':tags,
                  'posts':posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'fastvotecount':fastvotecount,
                  'freshvotecount':freshvotecount,
                  'bossvotecount':bossvotecount,
                  'votestatus':votestatus,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def carEdit(request, carId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(car=c)
    photos = Photo.objects.filter(album=a)
    
    # tab display
    posts_tab = 'checked'
    mods_tab = ''
    album_tab = ''
    
    if request.method == 'POST':
        form = carEditForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            tags = form.cleaned_data['tags']
            
            c.name = name
            c.save()
            
            #clear add tags to the post
            c.tags.clear()
            for tag in tags:
                c.tags.add(tag)
            
            # set url for the car Edit
            u = '/journal/car/'
            u += str(c.pk)
            u += '/view'
            
            return HttpResponseRedirect(u)
    
    else:
        ctags = c.tags.all()
        tagstr = ''
        for tag in ctags:
            tagstr += tag.name
            tagstr += ', '
        
        form = carEditForm(initial={
                           'name': c.name,
                           'tags': tagstr,
                           })
    
    return render(request,'caredit.html', {
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def carDelete(request, carId):
    c = Car.objects.get(pk=carId)
    u = '/journal/view/'
    c.delete()
    
    return HttpResponseRedirect(u)

@login_required
def postNew(request, carId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(car=c)
    photos = Photo.objects.filter(album=a)
    
    # tab display
    posts_tab = 'checked'
    mods_tab = ''
    album_tab = ''
    
    if request.method == 'POST':
        form = postForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            tags = form.cleaned_data['tags']
            
            # create post object
            p = Post(
                     car = c,
                     pub_date = datetime.now(),
                     title=title,
                     body=body,
                     )
            p.save()
            
            #add tags to the post
            for tag in tags:
                p.tags.add(tag)
            
            #create events for followers
            follows = Follow.objects.filter(car=c)
            next = 'http://fastfreshlife.royprieb.webfactional.com/visit/car/'
            next += str(c.pk)
            next += '/post/'
            next += str(p.pk)
            next += '/'
            
            for f in follows:
                ev = Event(
                           type = 'car',
                           user = f.user,
                           viewed = False,
                           pub_date = datetime.now(),
                           title = 'New post on %s' % c.name,
                           description = p.title,
                           next = next,
                           )
                ev.save()
            
            u = '/journal/car/'
            u += str(c.pk)
            u += '/post/'
            u += str(p.pk)
            u += '/view/'
            
            return HttpResponseRedirect(u)
    
    else:
        form = postForm()
    
    return render(request,'postNew.html',{
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def postView(request, carId, postId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(car=c)
    photos = Photo.objects.filter(album=a)
    
    p = Post.objects.get(pk = postId)
    tags = p.tags.all()
    
    # previous and next
    newerposts = Post.objects.filter(car=c).filter(pub_date__gt=p.pub_date)
    if newerposts.count() == 0:
        next_p = ''
    else:
        next_p = newerposts.order_by('pub_date')[0]
    
    olderposts = Post.objects.filter(car=c).filter(pub_date__lt=p.pub_date)
    if olderposts.count() == 0:
        prev_p = ''
    else:
        prev_p = olderposts.order_by('-pub_date')[0]
    
    # like counts
    likecount = Like.objects.filter(post=p).count()
    
    # tab display
    posts_tab = 'checked'
    mods_tab = ''
    album_tab = ''
    
    return render(request, 'postView.html', {
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'post':p,
                  'tags':tags,
                  'next_p':next_p,
                  'prev_p':prev_p,
                  'likecount':likecount,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def postEdit(request, carId, postId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    tags = c.tags.all()
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(car=c)
    photos = Photo.objects.filter(album=a)
    
    p = Post.objects.get(pk = postId)
    
    # tab display
    posts_tab = 'checked'
    mods_tab = ''
    album_tab = ''
    
    if request.method == 'POST':
        form = postForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            tags = form.cleaned_data['tags']
            
            # save changes to post object
            p.title = title
            p.body = body
            p.save()
            
            # set with new tags
            p.tags.clear()
            for tag in tags:
                p.tags.add(tag)
            
            #create events for followers
            follows = Follow.objects.filter(car=c)
            next = 'http://fastfreshlife.royprieb.webfactional.com/visit/car/'
            next += str(c.pk)
            next += '/post/'
            next += str(p.pk)
            next += '/'
            
            for f in follows:
                ev = Event(
                           type = 'car',
                           user = f.user,
                           viewed = False,
                           pub_date = datetime.now(),
                           title = 'Post updated on %s' % c.name,
                           description = p.title,
                           next = next,
                           )
                ev.save()
            
            u = '/journal/car/'
            u += str(c.pk)
            u += '/post/'
            u += str(p.pk)
            u += '/view/'
            
            return HttpResponseRedirect(u)
    
    else:
        ptags = p.tags.all()
        tagstr = ''
        for tag in ptags:
            tagstr += tag.name
            tagstr += ', '
        
        form = postForm(initial={
                        'title': p.title,
                        'body': p.body,
                        'tags': tagstr,
                        })
    
    return render(request, 'postEdit.html',{
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'tags': tags,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'post':p,
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def postDelete(request, postId):
    p = Post.objects.get(pk=postId)
    
    c = p.car
    u = '/journal/car/'
    u += str(c.pk)
    u += '/view/'
    
    p.delete()
    
    return HttpResponseRedirect(u)

@login_required
def commentDelete(request,commentId):
    next = request.GET.get('next')
    comment = get_object_or_404(Comment, pk=commentId)
    perform_delete(request, comment)
    
    return HttpResponseRedirect(next)

@login_required
def modView(request,carId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    tags = c.tags.all()
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(car=c)
    photos = Photo.objects.filter(album=a)
    
    # tab display
    posts_tab = ''
    mods_tab = 'checked'
    album_tab = ''
    
    return render(request, 'modView.html',{
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'tags':tags,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'navSearchForm': navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def modAdd(request, carId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    tags = c.tags.all()
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(car=c)
    photos = Photo.objects.filter(album=a)
    
    # tab display
    posts_tab = ''
    mods_tab = 'checked'
    album_tab = ''
    
    if request.method == 'POST':
        form = modForm(request.POST)
        if form.is_valid():
            brand = form.cleaned_data['brand']
            part = form.cleaned_data['part']
            modType = form.cleaned_data['modType']
            
            # create mod object
            m = Mod(
                    car = c,
                    brand = brand,
                    part = part,
                    modType = modType,
                    )
            m.save()
            
            #create events for followers
            follows = Follow.objects.filter(car=c)
            next = 'http://fastfreshlife.royprieb.webfactional.com/visit/car/'
            next += str(c.pk)
            next += '/'
            
            for f in follows:
                ev = Event(
                           type = 'car',
                           user = f.user,
                           viewed = False,
                           pub_date = datetime.now(),
                           title = 'Mod added on %s' % c.name,
                           description = '%s %s (%s)' % (m.brand,m.part,m.modType.category),
                           next = next,
                           )
                ev.save()
            
            u = '/journal/car/'
            u += str(c.pk)
            u += '/mod/view/'
            
            return HttpResponseRedirect(u)
    
    else:
        form = modForm()
    
    return render(request, 'modAdd.html',{
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'tags':tags,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def modEdit(request, carId, modId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    tags = c.tags.all()
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(car=c)
    photos = Photo.objects.filter(album=a)
    
    mod = Mod.objects.get(pk = modId)
    
    # tab display
    posts_tab = ''
    mods_tab = 'checked'
    album_tab = ''
    
    if request.method == 'POST':
        form = modForm(request.POST)
        if form.is_valid():
            brand = form.cleaned_data['brand']
            part = form.cleaned_data['part']
            modType = form.cleaned_data['modType']
            
            # modify mod object
            mod.brand = brand
            mod.part = part
            mod.modType = modType
            mod.save()
            
            #create events for followers
            follows = Follow.objects.filter(car=c)
            next = 'http://fastfreshlife.royprieb.webfactional.com/visit/car/'
            next += str(c.pk)
            next += '/'
            
            for f in follows:
                ev = Event(
                           type = 'car',
                           user = f.user,
                           viewed = False,
                           pub_date = datetime.now(),
                           title = 'Mod changed on %s' % c.name,
                           description = '%s %s (%s)' % (mod.brand,mod.part,mod.modType.category),
                           next = next,
                           )
                ev.save()
            
            u = '/journal/car/'
            u += str(c.pk)
            u += '/mod/view/'
            
            return HttpResponseRedirect(u)
    
    else:
        form = modForm(initial={
                       'brand':mod.brand,
                       'part':mod.part,
                       'modType':mod.modType,
                       })
    
    return render(request, 'modEdit.html',{
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'tags':tags,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'mod':mod,
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def modDelete(request, modId):
    m = Mod.objects.get(pk=modId)
    u = '/journal/car/'
    u += str(m.car.pk)
    u += '/mod/view/'
    m.delete()
    
    return HttpResponseRedirect(u)

@login_required
def albumView(request, carId, albumId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    tags = c.tags.all()
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(pk = albumId)
    photos = Photo.objects.filter(album=a)
    
    # tab display
    posts_tab = ''
    mods_tab = ''
    album_tab = 'checked'
    
    return render(request, 'albumView.html',{
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'tags':tags,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def albumAdd(request, carId, albumId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    tags = c.tags.all()
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(pk = albumId)
    photos = Photo.objects.filter(album=a)
    
    # tab display
    posts_tab = ''
    mods_tab = ''
    album_tab = 'checked'
    
    if request.method == 'POST':
        form = albumForm(request.POST, request.FILES)
        if form.is_valid():
            caption = form.cleaned_data['caption']
            # create photo instance and save image
            p = Photo(
                      album = a,
                      caption = caption,
                      )
            p.save() 
            image_file = request.FILES['photo']
            p.original_image.save(image_file.name, image_file)
            p.filename = image_file.name
            p.save()
            
            #create events for followers
            follows = Follow.objects.filter(car=c)
            next = 'http://fastfreshlife.royprieb.webfactional.com/visit/car/'
            next += str(c.pk)
            next += '/'
            
            for f in follows:
                ev = Event(
                           type = 'car',
                           user = f.user,
                           viewed = False,
                           pub_date = datetime.now(),
                           title = 'Photo added on %s' % c.name,
                           description = p.caption,
                           next = next,
                           )
                ev.save()
            
            # set url
            u = '/journal/car/'
            u += str(c.pk)
            u += '/album/'
            u += str(a.pk)
            u += '/view/'
            
            return HttpResponseRedirect(u)
    
    else:
        form = albumForm()
    
    return render(request, 'albumAdd.html',{
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'tags':tags,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'form':form,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

@login_required
def albumEdit(request, carId, albumId):
    #searchform
    navSearchForm = SearchForm()
    
    # journal variables
    j = Journal.objects.get(owner=request.user)
    cars = Car.objects.filter(journal=j)
    c = Car.objects.get(pk=carId)
    tags = c.tags.all()
    recent_posts = Post.objects.filter(car=c).order_by('-pub_date')[:5]
    m = Mod.objects.filter(car = c)
    a = Album.objects.get(pk = albumId)
    photos = Photo.objects.filter(album=a)
    
    # tab display
    posts_tab = ''
    mods_tab = ''
    album_tab = 'checked'
    
    return render(request, 'albumEdit.html',{
                  'journal':j,
                  'cars':cars,
                  'car':c,
                  'tags':tags,
                  'posts':recent_posts,
                  'mods':m,
                  'album':a,
                  'photos': photos,
                  'navSearchForm':navSearchForm,
                  'next':request.path,
                  'posts_tab':posts_tab,
                  'mods_tab':mods_tab,
                  'album_tab':album_tab,
                  })

def photoDelete(request, photoId):
    p = Photo.objects.get(pk=photoId)
    
    a = p.album
    u = '/journal/car/'
    u += str(a.car.pk)
    u += '/album/'
    u += str(a.pk)
    u += '/edit/'
    
    p.delete()
    
    return HttpResponseRedirect(u)

