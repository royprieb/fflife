# initial imports
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.db import IntegrityError
# imports from forms.py
from blog.forms import accountForm
from blog.forms import vendorAccountForm
from blog.forms import loginForm
from blog.forms import carForm
from blog.forms import modForm
from blog.forms import photoForm
from blog.forms import postForm
from blog.forms import messageForm
from blog.forms import topicForm
from blog.forms import feedbackForm
from blog.forms import newGroupForm
from blog.forms import commentForm
# imports from django.contrib.auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# comment imports
#from django.contrib.comments.models import Comment
#from django.contrib.comments.views.moderation import perform_delete
#from django.contrib.auth.views import password_change
from blog.models import UserProfile
from blog.models import Car
from blog.models import CarMake
from blog.models import CarModel
from blog.models import ModType
from blog.models import Vote
from blog.models import Follow
from blog.models import Post
from blog.models import PostComment
from blog.models import Like
from blog.models import Photo
from blog.models import Message
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
from blog.models import VendorPostLike
from blog.models import VendorPostComment
# other
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Count
# search form
from haystack.forms import SearchForm
# for ajax functions
from django.core import serializers
from django.utils import simplejson

def index(request):
    if request.user.is_authenticated():
        owner = request.user
        return HttpResponseRedirect('/home/')
    
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            lower_username = username.lower()
            password = form.cleaned_data['password']
            user = authenticate(
                                username = lower_username,
                                password = password,
                                )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home/')
    else:
        form = loginForm()
        
    return render(request, 'index.html',{
        'form':form,
        })

def about(request):    
    return render(request,'about.html',{})

def terms(request):    
    return render(request,'terms.html',{})

def privacy(request):    
    return render(request,'privacy.html',{})

def contact(request):
    action = request.GET.get('action')
    msgAlert = 'hide'
    if action == 'msg':
        msgAlert = ''
        
    if request.method == 'POST':
        form = feedbackForm(request.POST)
        if form.is_valid():
            sender_email = form.cleaned_data['sender_email']
            msg_title = form.cleaned_data['msg_title']
            msg_body = form.cleaned_data['msg_body']
            # create a new message -- set up to email message?
            feedback = Feedback(
                                sender = sender_email,
                                title = msg_title,
                                body = msg_body,
                                submit_date = datetime.now(),
                                )
            feedback.save()
            return HttpResponseRedirect('/contact?action=msg')
    else:
        form = feedbackForm()
        
    return render(request,'contact.html',{
        'form': form,
        'msgAlert': msgAlert,
        })

def newAccount (request):
    return render(request,'accounttype.html', {})

def newOwner (request):
    if request.method == 'POST':
        form = accountForm(request.POST, request.FILES)
        if form.is_valid():
            display_username = form.cleaned_data['username']
            username = display_username.lower()
            email = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            motto = form.cleaned_data['motto']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            
            # create a new user
            try:
                owner = User.objects.create_user(
                                                 username,
                                                 email,
                                                 pw,
                                                 )
            except IntegrityError, e:
                 return render(request,'newaccount.html', {
                      'form':form,
                      'msg':'Username or email already in use. Please try again.',
                      })
            
            # login user
            user = authenticate(username=username, password=pw)
            login(request, user)
            
            # create user profile
            p = UserProfile(
                            user=owner,
                            account_type='owner',
                            display_name = display_username,
                            motto=motto,
                            city=city,
                            state=state,
                            country=country,
                            )
            p.save()
            p.send_profile()
            
            # save profile photo
            if request.FILES:
                image_file = request.FILES['photo']
                p.original_image.save(image_file.name, image_file)
                p.save()
            else:
                p.original_image = 'user_profiles/default_profile.jpg'
                p.save()
                        
            return HttpResponseRedirect('/home/')
    
    else:
        form = accountForm()
    
    return render(request,'newaccount.html', {
                  'form':form,
                  'msg':'',
                  })

# new vendor
def newVendor (request):
    if request.method == 'POST':
        form = vendorAccountForm(request.POST, request.FILES)
        if form.is_valid():
            display_username = form.cleaned_data['username']
            username = display_username.lower()
            email = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            vendor_category = form.cleaned_data['vendor_category']
            website = form.cleaned_data['website']
            street_address = form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            
            # create a new user
            try:
                owner = User.objects.create_user(
                                                 username,
                                                 email,
                                                 pw,
                                                 )
            except IntegrityError, e:
                 return render(request,'newvendor.html', {
                      'form':form,
                      'msg':'Username or email already in use. Please try again.',
                      })
            
            # login user
            user = authenticate(username=username, password=pw)
            login(request, user)
            
            # create user profile
            p = UserProfile(
                            user=owner,
                            account_type='vendor',
                            display_name = display_username,
                            vendor_category=vendor_category,
                            website=website,
                            street_address=street_address,
                            city=city,
                            state=state,
                            country=country,
                            )
            p.save()
            p.send_profile()
            
            # save profile photo
            if request.FILES:
                image_file = request.FILES['photo']
                p.original_image.save(image_file.name, image_file)
                p.save()
            else:
                p.original_image = 'user_profiles/default_profile.jpg'
                p.save()
                        
            return HttpResponseRedirect('/home/')
    
    else:
        form = vendorAccountForm()
    
    return render(request,'newvendor.html', {
                  'form':form,
                  'msg':'',
                  })

def home(request):
    owner = request.user
    isOwner = True
    profile = UserProfile.objects.get(user=owner)
    isVendor = False
    if profile.account_type == 'vendor':
        isVendor = True

    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    if Follow.objects.filter(followed=owner, follower=request.user).exists():
        isFollower = True
    followed = Follow.objects.filter(follower=owner)

    messages = Message.objects.filter(recipient=owner).order_by('-pub_date')
    for message in messages:
        message.viewed = True
        message.save()
    cars = Car.objects.filter(owner=owner)
    memberships = Join.objects.filter(member=owner)
    carform = carForm()

    return render(request,'home.html',{
        'owner':owner,
        'isOwner':isOwner,
        'isVendor': isVendor,
        'followCount': followCount,
        'isFollower': isFollower,
        'followed': followed,
        'messages': messages,
        'cars':cars,
        'memberships': memberships,
        'carform': carform,
        })

def messageDelete(request, messageId):
    message = Message.objects.get(id=messageId)
    message.delete()
    return HttpResponseRedirect('/home/')

def logoutuser (request):
    logout(request)
    return HttpResponseRedirect('/')

def explore(request):
    owner = request.user    
    results = ''
    topBlogs = User.objects.annotate(num_followers=Count('user_followed_party')).order_by('-num_followers')[:10]
    topPosts = Post.objects.all().order_by('-pub_date')[:10]

    if request.method == 'POST':
        searchDone = True
        cars = Car.objects.all()
        
        make = request.POST['make']
        if make == '':
            s1 = cars
        else:
            s1 = cars.filter(make=make)
        
        model = request.POST['model']
        if model == '':
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
            s4 = cars.filter(year__lte=int(float(endyear)))
        else:
            s4 = cars
        
        r = s1 & s2 & s3 & s4
        
        results = r.annotate(num_votes=Count('vote'))
        
        return render(request,'explore.html',{
            'searchDone': searchDone,
            'owner':owner,
            'results':results,
            'topBlogs':topBlogs,
            'topPosts':topPosts,
            })
    
    else:
        searchDone = False
        return render(request,'explore.html',{
            'searchDone': searchDone,
            'owner':owner,
            'results':results,
            'topBlogs':topBlogs,
            'topPosts':topPosts,
            })

def groups(request):
    owner = request.user
    newgroupform = newGroupForm()
    popularGroups = Circle.objects.annotate(num_members=Count('join')).order_by('-num_members')[:10]
    recentGroups = Circle.objects.annotate(num_members=Count('join')).order_by('-pub_date')[:10]

    return render(request,'groups.html',{
        'owner': owner,
        'newgroupform': newgroupform,
        'popularGroups': popularGroups,
        'recentGroups': recentGroups,
        })

def groupAdd(request):
    user = request.user
    if request.method == 'POST':
        form = newGroupForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            circle = Circle(
                moderator = user,
                title = title,
                description = description,
                pub_date = datetime.now(),
            )
            circle.save()
            m = Join(
                group = circle,
                member = user,
            )
            m.save()
            # redirect to next
            return HttpResponseRedirect('/groups/%s/view/' % circle.id)
    else:
        return HttpResponseRedirect('/groups/')

def groupView(request, groupId):
    user = request.user
    currentGroup = Circle.objects.get(id=groupId)
    isModerator = False
    if user == currentGroup.moderator:
        isModerator = True
    isMember = False
    if Join.objects.filter(group=currentGroup, member=user).exists():
        isMember = True
    groupMembers = Join.objects.filter(group=currentGroup)
    memberCount = groupMembers.count()
    topics = Topic.objects.filter(group=currentGroup).annotate(num_responses=Count('response')).order_by('-pub_date')
    topicCount = topics.count()
    topicform = topicForm()
    
    return render(request, 'groupView.html', {
        'currentGroup': currentGroup,
        'isModerator': isModerator,
        'isMember': isMember,
        'groupMembers': groupMembers,
        'memberCount': memberCount,
        'topics':topics,
        'topicCount': topicCount,
        'topicform':topicform,
        })

def groupDelete(request, groupId):
    user = request.user
    currentGroup = Circle.objects.get(id=groupId)
    if request.user != currentGroup.moderator:
        return HttpResponseRedirect('/groups/%s/view/' % groupId)
    currentGroup.delete()
    return HttpResponseRedirect('/groups/')

def groupJoin(request, groupId):
    user = request.user
    currentGroup = Circle.objects.get(id=groupId)
    if not Join.objects.filter(group=currentGroup, member=user).exists():
        member = Join(
            group = currentGroup,
            member = user,
            )
        member.save()
    return HttpResponseRedirect('/groups/%s/view/' % groupId)

def groupLeave(request, groupId):
    user = request.user
    currentGroup = Circle.objects.get(id=groupId)
    if Join.objects.filter(group=currentGroup, member=user).exists():
        member = Join.objects.get(group=currentGroup, member= user)
        member.delete()
        # remove any topics and comments attached to user
        group_topics = Topic.objects.filter(group=currentGroup)
        user_responses = Response.objects.filter(topic__in=group_topics, responder=user)
        user_responses.delete()
        user_topics = group_topics.filter(owner=user)
        user_topics.delete()
        
    return HttpResponseRedirect('/groups/%s/view/' % groupId)

def topicAdd(request, groupId):
    user = request.user
    currentGroup = Circle.objects.get(id=groupId)
    if request.method == 'POST':
        form = topicForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            
            # join non-member
            if not Join.objects.filter(group=currentGroup, member=user).exists():
                j = Join(
                    group = currentGroup,
                    member = user,
                )
                j.save()
                
            # create the topic
            t = Topic(
                group = currentGroup,
                owner = user,
                pub_date = datetime.now(),
                body = body,
            )
            t.save()

            # redirect to next
            return HttpResponseRedirect('/groups/%s/topic/%s/view/' % (currentGroup.id, t.id))
    else:
        return HttpResponseRedirect('/groups/%s/view/' % currentGroup.id)

def topicView(request, groupId, topicId):
    user = request.user
    currentGroup = Circle.objects.get(id=groupId)
    currentTopic = Topic.objects.get(id=topicId)
    isModerator = False
    if user == currentGroup.moderator:
        isModerator = True
    isOwner = False
    if user == currentTopic.owner:
        isOwner = True
    isMember = False
    if Join.objects.filter(member=user).exists():
        isMember = True
    groupMembers = Join.objects.filter(group=currentGroup)
    memberCount = groupMembers.count()
    topicCount = Topic.objects.filter(group=currentGroup).count()
    topicform = topicForm()
    responses = Response.objects.filter(topic=currentTopic).order_by('-pub_date')

    return render(request, 'topicView.html',{
        'currentGroup': currentGroup,
        'isModerator': isModerator,
        'isOwner': isOwner,
        'isMember': isMember,
        'groupMembers': groupMembers,
        'memberCount': memberCount,
        'topicCount': topicCount,
        'topicform':topicform,
        'currentTopic': currentTopic,
        'responses': responses,
        })

def topicDelete(request, groupId,topicId):
    user = request.user
    currentGroup = Circle.objects.get(id=groupId)
    currentTopic = Topic.objects.get(id=topicId)
    if user == currentGroup.moderator or user == currentTopic.owner:
        currentTopic.delete()
    return HttpResponseRedirect('/groups/%s/view/' % groupId)

def topicRespond(request, groupId, topicId):
    user = request.user
    currentGroup = Circle.objects.get(id=groupId)
    currentTopic = Topic.objects.get(id=topicId)

    if request.method == 'POST':
        form = topicForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            
            # join non-member
            if not Join.objects.filter(group=currentGroup, member=user).exists():
                j = Join(
                    group = currentGroup,
                    member = user,
                )
                j.save()
                
            # create the response
            t = Response(
                topic = currentTopic,
                responder = user,
                pub_date = datetime.now(),
                body = body,
            )
            t.save()

            # redirect to next
            return HttpResponseRedirect('/groups/%s/topic/%s/view/' % (currentGroup.id, currentTopic.id))
    else:
        return HttpResponseRedirect('/groups/%s/topic/%s/view/' % (currentGroup.id,currentTopic.id))

def responseDelete(request, groupId, topicId, responseId):
    user = request.user
    currentGroup = Circle.objects.get(id=groupId)
    currentTopic = Topic.objects.get(id=topicId)
    currentResponse = Response.objects.get(id=responseId)
    if user == currentGroup.moderator or user == currentTopic.owner:
        currentResponse.delete()
    return HttpResponseRedirect('/groups/%s/topic/%s/view/' % (groupId, topicId))
    
def videos(request):
    videos = Video.objects.order_by('-submit_date').all()
    return render(request,'videos.html',{
        'videos':videos,
        })

def photoboard(request):
    boards = Board.objects.all()
    current_board = ''
    boardphotos = []
    photoform = photoForm()
    b = request.GET.get('b')
    if boards:
        if b:
            current_board = Board.objects.get(id=b)
        else:
            current_board = boards[0]
        boardphotos = BoardPhoto.objects.filter(board=current_board).annotate(num_likes=Count('photolike')).order_by('-num_likes')
            
    return render(request,'photoboard.html',{
        'boards':boards,
        'current_board': current_board,
        'boardphotos': boardphotos,
        'photoform': photoform,
        })

def boardUpload(request, boardId):
    user = request.user
    current_board = Board.objects.get(id=boardId)
    if request.method == 'POST':
        form = photoForm(request.POST, request.FILES)
        if form.is_valid():
            caption = form.cleaned_data['caption']
            # create photo instance and save image
            p = BoardPhoto(
                uploader = user,
                board = current_board,
                caption = caption,
                post_date = datetime.now(),
                )
            p.save() 
            image_file = request.FILES['photo']
            p.original_image.save(image_file.name, image_file)
            p.filename = image_file.name
            p.save()
            
        return HttpResponseRedirect('/photoboard/%s/photo/%s/' % (current_board.id, p.id))
    else:
        return HttpResponseRedirect('/photoboard/')

def boardDetails(request, boardId):
    current_board = Board.objects.get(id=boardId)
    boardphotos = BoardPhoto.objects.filter(board=current_board).annotate(num_likes=Count('photolike')).order_by('-num_likes')
    photos = []
    for boardphoto in boardphotos:
        photo = {}
        photo["href"] = '/photoboard/%s/photo/%s/' % (boardphoto.board.pk, boardphoto.pk)
        photo["image"] = boardphoto.thumbnail_image.url
        photo["likes"] = boardphoto.num_likes
        photos.append(photo)
    json_photos = simplejson.dumps(photos)
    return HttpResponse(json_photos)

def boardPhotoView(request, boardId, photoId):
    user = request.user
    board = Board.objects.get(id=boardId)
    photo = BoardPhoto.objects.get(id=photoId)
    likescount = PhotoLike.objects.filter(photo=photo).count()
    comments = PhotoComment.objects.filter(photo=photo).order_by('-pub_date')
    form = commentForm()

    isUploader = False
    if photo.uploader == user:
        isUploader = True
        
    return render(request,'boardphotoview.html',{
        'user': user,
        'board':board,
        'photo':photo,
        'likescount':likescount,
        'comments': comments,
        'form':form,
        'isUploader':isUploader,
        })

def boardPhotoLike(request, boardId, photoId):
    u = request.user
    photo = BoardPhoto.objects.get(pk=photoId)
    if not PhotoLike.objects.filter(user = u.pk, photo=photo).exists():
        l = PhotoLike(
            user = u,
            photo = photo,
            )
        l.save()
        
    likecount = PhotoLike.objects.filter(photo=photo).count()
    c = {}
    c['likecount'] = str(likecount)
    like_json = simplejson.dumps(c)
    return HttpResponse(like_json)

def boardPhotoDelete(request, boardId, photoId):
    user = request.user
    photo = BoardPhoto.objects.get(id=photoId)
    board = Board.objects.get(id=boardId)
    if user == photo.uploader:
        photo.delete()
        return HttpResponseRedirect('/photoboard?b=%s' % board.id)
    else:
        return HttpResponseRedirect('/photoboard/%s/photo/%s/' % (board.id, photo.id))

def boardPhotoComment(request, boardId, photoId):
    user = request.user
    board = Board.objects.get(id=boardId)
    photo = BoardPhoto.objects.get(id=photoId)
    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
                            
            # create the comment
            c = PhotoComment(
                user = user,
                photo = photo,
                pub_date = datetime.now(),
                body = body,
            )
            c.save()
            c.send_photo_comment()
            
        return HttpResponseRedirect('/photoboard/%s/photo/%s/' % (board.id, photo.id))
    else:
        return HttpResponseRedirect('/photoboard/%s/photo/%s/' % (board.id, photo.id))

def boardPhotoCommentDelete(request, boardId, photoId, commentId):
    user = request.user
    board = Board.objects.get(id=boardId)
    photo = BoardPhoto.objects.get(id=photoId)
    comment = PhotoComment.objects.get(id=commentId)
    if user == photo.uploader:
        comment.delete()
    return HttpResponseRedirect('/photoboard/%s/photo/%s/' % (board.id, photo.id))
                
def journal(request, name):
    messageSent = False
    if request.GET.get('action') == 'message':
        messageSent = True
    owner = User.objects.get(username=name)
    profile = UserProfile.objects.get(user=owner)
    isVendor = False
    if profile.account_type == 'vendor':
        isVendor = True
    isOwner = False
    if request.user.username == name:
        isOwner = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    if Follow.objects.filter(followed=owner, follower=request.user).exists():
        isFollower = True
    followed = Follow.objects.filter(follower=owner)
    cars = Car.objects.filter(owner=owner)
    memberships = Join.objects.filter(member=owner)
    carform = carForm()
    messageform = messageForm()

    # vendorpost data
    posts = []
    last_post= ''
    all_posts = VendorPost.objects.filter(vendor=owner).order_by('-pub_date')
    if all_posts:
        select_posts = all_posts
        if all_posts.count() > 3:
            select_posts = all_posts[:3]
        last_post = select_posts[(len(select_posts) - 1)]
        for p in select_posts:
            post = {}
            post['id'] = p.id
            post['pub_date'] = p.pub_date
            post['author'] = profile.display_name
            post['username'] = owner.username
            post['title'] = p.title
            post['body'] = p.body
            post['likecount'] = VendorPostLike.objects.filter(vendorpost=p).count()
            post['tags'] = p.tags.all()
            post['comments'] = VendorPostComment.objects.filter(vendorpost=p).order_by('-pub_date')
            posts.append(post)

    postcommentform = commentForm()
        
    return render(request,'journal.html',{
        'owner':owner,
        'isOwner':isOwner,
        'isVendor':isVendor,
        'followCount':followCount,
        'isFollower': isFollower,
        'followed': followed,
        'cars':cars,
        'memberships':memberships,
        'carform':carform,
        'messageform':messageform,
        'messageSent':messageSent,
        'posts':posts,
        'last_post': last_post,
        'postcommentform':postcommentform,
        })

@login_required
def vendorPostNew(request, name):
    owner = User.objects.get(username=name)
    if request.user.username != name:
        return HttpResponseRedirect('/journal/%s/')
    isOwner = True
    profile = UserProfile.objects.get(user=owner)
    isVendor = False
    if profile.account_type == 'vendor':
        isVendor = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    followed = Follow.objects.filter(follower=owner)
    memberships = Join.objects.filter(member=owner)
    cancelUrl = "/journal/%s/" % owner.username
    if VendorPost.objects.filter(vendor=owner).exists():
        most_recent_post = VendorPost.objects.filter(vendor=owner).order_by('-pub_date')[0]
        cancelUrl = "/journal/%s/post/%s" % (owner.username, most_recent_post.id)

    if request.method == 'POST':
        form = postForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            p_tags = form.cleaned_data['p_tags']
            
            # create vendor post object
            p = VendorPost(
                vendor = owner,
                pub_date = datetime.now(),
                title=title,
                body=body,
                )
            p.save()
            p.send_vendorpost()

            #add tags to the post
            for tag in p_tags:
                p.tags.add(tag)

        return HttpResponseRedirect('/journal/%s/post/%s/' % (owner.username, p.id))

    else:
        postform = postForm()
        
        return render(request, 'newpostform.html', {
            'owner':owner,
            'isVendor': isVendor,
            'isOwner': isOwner,
            'followCount': followCount,
            'isFollower':isFollower,
            'followed': followed,
            'memberships': memberships,
            'cancelUrl': cancelUrl,
            'postform': postform,
            })

@login_required
def vendorPostView(request, name, postId):
    owner = User.objects.get(username=name)
    profile = UserProfile.objects.get(user=owner)
    isVendor = False
    if profile.account_type == 'vendor':
        isVendor = True
    owner_display_name = UserProfile.objects.get(user=owner).display_name
    isOwner = False
    if request.user.username == name:
        isOwner = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    if Follow.objects.filter(followed=owner, follower=request.user).exists():
        isFollower = True
    followed = Follow.objects.filter(follower=owner)
    memberships = Join.objects.filter(member=owner)
    # vendor post data
    posts = []
    last_post = ''
    current_post = VendorPost.objects.get(id=postId)
    all_posts = VendorPost.objects.filter(vendor=owner).filter(pub_date__lte=current_post.pub_date).order_by('-pub_date')
    if all_posts:
        select_posts = all_posts
        if all_posts.count() > 3:
            select_posts = all_posts[:3]
        last_post = select_posts[(len(select_posts)-1)]
        for p in select_posts:
            post = {}
            post['id'] = p.id
            post['pub_date'] = p.pub_date
            post['author'] = owner_display_name
            post['username'] = owner.username
            post['title'] = p.title
            post['body'] = p.body
            post['likecount'] = VendorPostLike.objects.filter(vendorpost=p).count()
            post['tags'] = p.tags.all()
            post['comments'] = VendorPostComment.objects.filter(vendorpost=p).order_by('-pub_date')
            posts.append(post)
        
    messageform = messageForm()
    postcommentform = commentForm()

    return render(request, 'journalView.html', {
        'owner':owner,
        'isVendor':isVendor,
        'isOwner':isOwner,
        'followCount':followCount,
        'isFollower': isFollower,
        'followed': followed,
        'memberships': memberships,
        'current_post':current_post,
        'posts':posts,
        'last_post':last_post,
        'messageform': messageform,
        'postcommentform':postcommentform,
    })

@login_required
def vendorPostEdit(request, name, postId):
    owner = User.objects.get(username=name)
    if request.user.username != name:
        return HttpResponseRedirect('/journal/%s/car/%s/')
    isOwner = True
    profile = UserProfile.objects.get(user=owner)
    isVendor = False
    if profile.account_type == 'vendor':
        isVendor = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    followed = Follow.objects.filter(follower=owner)
    memberships = Join.objects.filter(member=owner)
    p = VendorPost.objects.get(pk=postId)
    p_tags = p.tags.all()
    p_taglist = []
    for tag in p_tags:
        p_taglist.append(tag.name)
    p_tags_string = ', '.join(p_taglist)

    if request.method == 'POST':
        form = postForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            tags = form.cleaned_data['p_tags']
            
            # save changes to post object
            p.title = title
            p.body = body
            p.save()
            
            # set with new tags
            p.tags.clear()
            for tag in tags:
                p.tags.add(tag)
                
            return HttpResponseRedirect('/journal/%s/post/%s' % (owner.username, p.pk))
        
    else:
        editpostform = postForm(
            initial = {
                'title': p.title,
                'p_tags': p_tags_string,
                'body': p.body,
                }            
        )
        
        return render(request, 'editpostform.html', {
            'owner':owner,
            'isOwner': isOwner,
            'isVendor': isVendor,
            'followCount': followCount,
            'isFollower':isFollower,
            'followed': followed,
            'memberships': memberships,
            'post':p,
            'editpostform': editpostform,
            })

@login_required
def vendorPostDelete(request, name, postId):
    owner = request.user
    p = VendorPost.objects.get(pk=postId)
    p.delete()
    # find most recent post to go to
    posts = VendorPost.objects.filter(vendor=owner).order_by('-pub_date')
    if len(posts) > 0:
        u = '/journal/%s/post/%s' % (owner.username, posts[0].pk)
    else:
        u = '/journal/%s/' % (owner.username) 
    return HttpResponseRedirect(u)

def vendorPostComment(request, name, postId):
    user = request.user
    owner = User.objects.get(username=name)
    post = VendorPost.objects.get(pk=postId)
    isOwner = False
    if user == owner:
        isOwner=True
    postcommentform = commentForm()
    
    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']

            # create post comment object
            c = VendorPostComment(
                vendorpost = post,
                user = user,
                pub_date = datetime.now(),
                body = body,
                )
            c.save()
            c.send_vendorpost_comment()

            comments = VendorPostComment.objects.filter(vendorpost=post).order_by('-pub_date')

            return render(request, 'vendorpostcomments.html', {
                'isOwner': isOwner,
                'post':post,
                'postcommentform':postcommentform,
                'comments':comments,
            })
            
    else:
        return HttpResponseRedirect('/journal/%s/post/%s/' % (owner.username, post.id))

def vendorPostCommentDelete(request, name, postId, commentId):
    owner = User.objects.get(username=name)
    post = VendorPost.objects.get(pk=postId)
    isOwner = False
    if request.user.username == name:
        isOwner=True
    if not isOwner:
        return HttpResponseRedirect('/journal/%s/post/%s/' % (owner.username, post.id))
    comment = VendorPostComment.objects.get(id=commentId)
    comment.delete()
    
    postcommentform = commentForm()
    comments = VendorPostComment.objects.filter(vendorpost=post).order_by('-pub_date')

    return render(request, 'vendorpostcomments.html', {
        'isOwner': isOwner,
        'post':post,
        'postcommentform':postcommentform,
        'comments':comments,
        })

@login_required
def vendorPostLike(request, name, postId):
    u = request.user
    p = VendorPost.objects.get(pk=postId)
    if not VendorPostLike.objects.filter(user = u.pk, vendorpost=p).exists():
        l = VendorPostLike(
                 user = u,
                 vendorpost = p,
                 )
        l.save()
        l.send_vendorpost_like()
        
    likecount = len(VendorPostLike.objects.filter(vendorpost=p))
    c = {}
    c['likecount'] = str(likecount)
    like_json = simplejson.dumps(c)
    return HttpResponse(like_json)

def vendorPostNext(request, name, postId):
    owner = User.objects.get(username=name)
    owner_display_name = UserProfile.objects.get(user=owner).display_name
    isOwner = False
    if request.user.username == name:
        isOwner = True
    page = request.GET.get('p')
    posts_per_page = 3
    lower_bound = posts_per_page * (int(page)-1) 
    upper_bound = lower_bound + posts_per_page
#    car = Car.objects.get(id=carId)
    index_post = VendorPost.objects.get(id=postId)
    prev_posts = VendorPost.objects.filter(vendor=owner).filter(pub_date__lt=index_post.pub_date).order_by('-pub_date')
    posts = []
    if prev_posts.count() > lower_bound:
        if prev_posts.count() > upper_bound:
            select_posts = prev_posts[lower_bound:upper_bound]
        else:
            select_posts = prev_posts[lower_bound:prev_posts.count()]
        # set up the data dictionary
        for p in select_posts:
            post = {}
            post['id'] = p.id
#            post['carid'] = p.car.id
            post['pub_date'] = p.pub_date
            post['author'] = owner_display_name
            post['username'] = owner.username
            post['title'] = p.title
            post['body'] = p.body
            post['likecount'] = VendorPostLike.objects.filter(vendorpost=p).count()
            post['tags'] = p.tags.all()
            post['comments'] = VendorPostComment.objects.filter(vendorpost=p)
            posts.append(post)
    
        postcommentform = commentForm()

        return render(request, 'nextvendorposts.html', {
            'owner': owner,
            'isOwner': isOwner,
            'posts':posts,
            'postcommentform': postcommentform,
            });
    else:
        return HttpResponse('')

@login_required
def accountEdit(request):
    owner = request.user
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = accountForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            motto = form.cleaned_data['motto']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            
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
            return HttpResponseRedirect('/journal/%s/' % owner.username)
        else:
            return HttpResponse('form is invalid')
    else:
        # provide the form for editing
        form = accountForm(initial={
                               'username': owner.username,
                               'email': owner.email,
                               'motto': profile.motto,
                               'city': profile.city,
                               'state': profile.state,
                               'country': profile.country,
                               })
    
    return render(request,'accountedit.html', {
                  'form':form,
                  })

@login_required
def accountDelete(request):
    request.user.delete()
    return HttpResponseRedirect('/')

@login_required
def modType(request):
    modtypes = ModType.objects.all()
    options = []
    for modtype in modtypes:
        options.append(modtype.category)
    data = simplejson.dumps(options) 
    return HttpResponse(data, content_type='application/json')

@login_required
def carModel(request):
    make = request.GET.get('make')
    if make == 'all':
        models = CarModel.objects.all()
    else:
        if CarMake.objects.filter(name=make).exists():
            makeObject = CarMake.objects.get(name=make)
            models = CarModel.objects.filter(carmaker=makeObject)
        else:
            models = CarModel.objects.all()
    options = []
    for model in models:
        options.append(model.name)
    data = simplejson.dumps(options) 
    return HttpResponse(data, content_type='application/json')

@login_required
def carMake(request):
    makes = CarMake.objects.all()
    options = []
    for make in makes:
        options.append(make.name)
    data = simplejson.dumps(options) 
    return HttpResponse(data, content_type='application/json')

@login_required
def carNew(request, name):
    owner = User.objects.get(username=name)
    if request.method == 'POST':
        form = carForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            make = form.cleaned_data['make']
            model = form.cleaned_data['model']
            year = form.cleaned_data['year']
            c_tags = form.cleaned_data['c_tags']
            
            # create a car
            c = Car(
                    owner=owner,
                    name=name,
                    make=make,
                    model=model,
                    year=year,
                    )
            c.save()
            c.send_car()
            
            #add tags to the post
            for c_tag in c_tags:
                c.tags.add(c_tag)

            # add profile image
            if request.FILES:
                image_file = request.FILES['image']
                c.original_image.save(image_file.name, image_file)
                c.filename = image_file.name
                c.save()
                            
            # set redirect to the journal
            u = '/journal/%s/car/%s' % (owner.username, c.pk)

            return HttpResponseRedirect(u)
    
    else:
        return HttpResponseRedirect('/journal/%s/' % owner.username)

@login_required
def carEdit(request, name, carId):
    owner = User.objects.get(username=name)
    c = Car.objects.get(pk=carId) 
    if request.method == 'POST':
        form = carForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            make = form.cleaned_data['make']
            model = form.cleaned_data['model']
            year = form.cleaned_data['year']
            tags = form.cleaned_data['c_tags']
            
            # edit a car
            c.name = name
            c.make = make
            c.model= model
            c.year = year
            c.save()
            
            #clear and add new tags to the car
            c.tags.clear()
            for tag in tags:
                c.tags.add(tag)

            # add profile image
            if request.FILES:
                image_file = request.FILES['image']
                c.original_image.save(image_file.name, image_file)
                c.filename = image_file.name
                c.save()
            
            # set redirect to the journal
            u = '/journal/%s/car/%s' % (owner.username, c.pk)
            
            return HttpResponseRedirect(u)
    else:
        return HttpResponseRedirect('/journal/%s/' % owner.username)

@login_required
def carDelete(request, name, carId):
    owner = User.objects.get(username=name)
    c = Car.objects.get(pk=carId)
    u = '/journal/%s/' % owner.username
    c.delete()
    
    return HttpResponseRedirect(u)

@login_required
def carView(request, name, carId):
    owner = User.objects.get(username=name)
    owner_display_name = UserProfile.objects.get(user=owner).display_name
    isOwner = False
    if request.user.username == name:
        isOwner = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    if Follow.objects.filter(followed=owner, follower=request.user).exists():
        isFollower = True
    followed = Follow.objects.filter(follower=owner)
    cars = Car.objects.filter(owner=owner)
    memberships = Join.objects.filter(member=owner)
    c = Car.objects.get(pk=carId)
    c_tags = c.tags.all()
    c_taglist = []
    for tag in c_tags:
        c_taglist.append(tag.name)
    c_tags_string = ', '.join(c_taglist)
    # post data
    posts = []
    last_post= ''
    all_posts = Post.objects.filter(car=c).order_by('-pub_date')
    if all_posts:
        select_posts = all_posts
        if all_posts.count() > 3:
            select_posts = all_posts[:3]
        last_post = select_posts[(len(select_posts) - 1)]
        for p in select_posts:
            post = {}
            post['id'] = p.id
            post['carid'] = p.car.id
            post['pub_date'] = p.pub_date
            post['author'] = owner_display_name
            post['username'] = p.car.owner.username
            post['title'] = p.title
            post['body'] = p.body
            post['likecount'] = Like.objects.filter(post=p).count()
            post['tags'] = p.tags.all()
            post['comments'] = PostComment.objects.filter(post=p).order_by('-pub_date')
            posts.append(post)
        
    # mod data
    mods = Mod.objects.filter(car = c).order_by('modType')
    # photo data
    photos = Photo.objects.filter(car=c)

    # tab status
    carTabActive = True
    postsTabActive = False
    modTabActive = False
    galleryTabActive = False
    
    # vote counts
    fastvotecount = Vote.objects.filter(car=c).filter(type='fast').count()
    freshvotecount = Vote.objects.filter(car=c).filter(type='fresh').count()

    carform = carForm()
    editcarform = carForm(
        initial = {
            'name': c.name,
            'make': c.make,
            'model': c.model,
            'year': c.year,
            'c_tags': c_tags_string,
        }
    )
    modform = modForm()
    photoform = photoForm()
    messageform = messageForm()
    postcommentform = commentForm()

    return render(request, 'journalview.html', {
        'owner':owner,
        'isOwner': isOwner,
        'followCount': followCount,
        'isFollower':isFollower,
        'followed': followed,
        'cars':cars,
        'memberships': memberships,
        'car':c,
        'c_tags':c_tags,
        'posts':posts,
        'last_post':last_post,
        'mods':mods,
        'photos': photos,
        'carTabActive': carTabActive,
        'postsTabActive': postsTabActive,
        'modTabActive': modTabActive,
        'galleryTabActive': galleryTabActive,
        'fastvotecount':fastvotecount,
        'freshvotecount':freshvotecount,
        'carform': carform,
        'editcarform': editcarform,
        'modform': modform,
        'photoform': photoform,
        'messageform': messageform,
        'postcommentform': postcommentform,
    })

@login_required
def postNew(request, name, carId):
    owner = User.objects.get(username=name)
    if request.user.username != name:
        return HttpResponseRedirect('/journal/%s/car/%s/')
    isOwner = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    followed = Follow.objects.filter(follower=owner)
    cars = Car.objects.filter(owner=owner)
    memberships = Join.objects.filter(member=owner)
    c = Car.objects.get(pk=carId)
    cancelUrl = "/journal/%s/car/%s/" % (owner.username, c.id)
    if Post.objects.filter(car=c).exists():
        most_recent_post = Post.objects.filter(car=c).order_by('-pub_date')[0]
        cancelUrl = "/journal/%s/car/%s/post/%s" % (owner.username, c.id, most_recent_post.id)

    if request.method == 'POST':
        form = postForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            p_tags = form.cleaned_data['p_tags']
            
            # create post object
            p = Post(
                car = c,
                pub_date = datetime.now(),
                title=title,
                body=body,
                )
            p.save()
            p.send_post()

            #add tags to the post
            for tag in p_tags:
                p.tags.add(tag)

        return HttpResponseRedirect('/journal/%s/car/%s/post/%s' % (owner.username, c.id, p.id))

    else:
        postform = postForm()
        
        return render(request, 'newpostform.html', {
            'owner':owner,
            'isOwner': isOwner,
            'followCount': followCount,
            'isFollower':isFollower,
            'followed': followed,
            'cars':cars,
            'memberships': memberships,
            'car':c,
            'cancelUrl': cancelUrl,
            'postform': postform,
            })
    
@login_required
def postView(request, name, carId, postId):
    owner = User.objects.get(username=name)
    owner_display_name = UserProfile.objects.get(user=owner).display_name
    isOwner = False
    if request.user.username == name:
        isOwner = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    if Follow.objects.filter(followed=owner, follower=request.user).exists():
        isFollower = True
    followed = Follow.objects.filter(follower=owner)
    cars = Car.objects.filter(owner=owner)
    memberships = Join.objects.filter(member=owner)
    c = Car.objects.get(pk=carId)
    c_tags = c.tags.all()
    c_taglist = []
    for tag in c_tags:
        c_taglist.append(tag.name)
    c_tags_string = ', '.join(c_taglist)
    # post data
    posts = []
    last_post = ''
    current_post = Post.objects.get(id=postId)
    all_posts = Post.objects.filter(car=c).filter(pub_date__lte=current_post.pub_date).order_by('-pub_date')
    if all_posts:
        select_posts = all_posts
        if all_posts.count() > 3:
            select_posts = all_posts[:3]
        last_post = select_posts[(len(select_posts)-1)]
        for p in select_posts:
            post = {}
            post['id'] = p.id
            post['carid'] = p.car.id
            post['pub_date'] = p.pub_date
            post['author'] = owner_display_name
            post['username'] = p.car.owner.username
            post['title'] = p.title
            post['body'] = p.body
            post['likecount'] = Like.objects.filter(post=p).count()
            post['tags'] = p.tags.all()
            post['comments'] = PostComment.objects.filter(post=p).order_by('-pub_date')
            posts.append(post)

    # mod data
    mods = Mod.objects.filter(car = c).order_by('modType')
    # photo data
    photos = Photo.objects.filter(car=c)

    # tab status
    carTabActive = False
    postsTabActive = True
    modTabActive = False
    galleryTabActive = False

    # vote counts
    fastvotecount = Vote.objects.filter(car=c).filter(type='fast').count()
    freshvotecount = Vote.objects.filter(car=c).filter(type='fresh').count()
        
    carform = carForm()
    editcarform = carForm(
        initial = {
            'name': c.name,
            'make': c.make,
            'model': c.model,
            'year': c.year,
            'c_tags':c_tags_string,
        }
    )
    modform = modForm()
    photoform = photoForm()
    messageform = messageForm()
    postcommentform = commentForm()

    return render(request, 'journalview.html', {
        'owner':owner,
        'isOwner':isOwner,
        'followCount':followCount,
        'isFollower': isFollower,
        'followed': followed,
        'cars':cars,
        'memberships': memberships,
        'car':c,
        'c_tags':c_tags,
        'current_post':current_post,
        'posts':posts,
        'last_post':last_post,
        'mods':mods,
        'photos': photos,
        'carTabActive': carTabActive,
        'postsTabActive': postsTabActive,
        'modTabActive': modTabActive,
        'galleryTabActive': galleryTabActive,
        'fastvotecount':fastvotecount,
        'freshvotecount':freshvotecount,
        'carform': carform,
        'editcarform': editcarform,
        'modform': modform,
        'photoform': photoform,
        'messageform': messageform,
        'postcommentform':postcommentform,
    })

@login_required
def postEdit(request, name, carId, postId):
    owner = User.objects.get(username=name)
    if request.user.username != name:
        return HttpResponseRedirect('/journal/%s/car/%s/')
    isOwner = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    followed = Follow.objects.filter(follower=owner)
    cars = Car.objects.filter(owner=owner)
    memberships = Join.objects.filter(member=owner)
    c = Car.objects.get(pk=carId)
    p = Post.objects.get(pk=postId)
    p_tags = p.tags.all()
    p_taglist = []
    for tag in p_tags:
        p_taglist.append(tag.name)
    p_tags_string = ', '.join(p_taglist)

    if request.method == 'POST':
        form = postForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            tags = form.cleaned_data['p_tags']
            
            # save changes to post object
            p.title = title
            p.body = body
            p.save()
            
            # set with new tags
            p.tags.clear()
            for tag in tags:
                p.tags.add(tag)
                
            return HttpResponseRedirect('/journal/%s/car/%s/post/%s' % (owner.username,c.pk, p.pk))
        
    else:
        editpostform = postForm(
            initial = {
                'title': p.title,
                'p_tags': p_tags_string,
                'body': p.body,
                }            
        )
        
        return render(request, 'editpostform.html', {
            'owner':owner,
            'isOwner': isOwner,
            'followCount': followCount,
            'isFollower':isFollower,
            'followed': followed,
            'cars':cars,
            'memberships': memberships,
            'car':c,
            'post':p,
            'editpostform': editpostform,
            })

@login_required
def postDelete(request, name, carId, postId):
    owner = request.user
    c = Car.objects.get(pk=carId)
    p = Post.objects.get(pk=postId)
    p.delete()
    # find most recent post to go to
    posts = Post.objects.filter(car=c).order_by('-pub_date')
    if len(posts) > 0:
        u = '/journal/%s/car/%s/post/%s' % (owner.username, c.pk, posts[0].pk)
    else:
        u = '/journal/%s/car/%s/' % (owner.username, c.pk) 
    return HttpResponseRedirect(u)

def postComment(request, name, carId, postId):
    user = request.user
    owner = User.objects.get(username=name)
    car = Car.objects.get(pk=carId)
    post = Post.objects.get(pk=postId)
    isOwner = False
    if user == owner:
        isOwner=True
    postcommentform = commentForm()
    
    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']

            # create post comment object
            c = PostComment(
                post = post,
                user = user,
                pub_date = datetime.now(),
                body = body,
                )
            c.save()
            c.send_post_comment()

            comments = PostComment.objects.filter(post=post).order_by('-pub_date')

            return render(request, 'postcomments.html', {
                'isOwner': isOwner,
                'post':post,
                'postcommentform':postcommentform,
                'comments':comments,
            })
            
    else:
        return HttpResponseRedirect('/journal/%s/car/%s/post/%s/' % (owner.username, car.pk, post.id))

def postCommentDelete(request, name, carId, postId, commentId):
    owner = User.objects.get(username=name)
    car = Car.objects.get(pk=carId)
    post = Post.objects.get(pk=postId)
    isOwner = False
    if request.user.username == name:
        isOwner=True
    if not isOwner:
        return HttpResponse()
    comment = PostComment.objects.get(id=commentId)
    comment.delete()
    
    postcommentform = commentForm()
    comments = PostComment.objects.filter(post=post).order_by('-pub_date')

    return render(request, 'postcomments.html', {
        'isOwner': isOwner,
        'post':post,
        'postcommentform':postcommentform,
        'comments':comments,
        })
 
def postNext(request, name, carId, postId):
    owner = User.objects.get(username=name)
    owner_display_name = UserProfile.objects.get(user=owner).display_name
    isOwner = False
    if request.user.username == name:
        isOwner = True
    page = request.GET.get('p')
    posts_per_page = 3
    lower_bound = posts_per_page * (int(page)-1) 
    upper_bound = lower_bound + posts_per_page
    car = Car.objects.get(id=carId)
    index_post = Post.objects.get(id=postId)
    prev_posts = Post.objects.filter(car=car).filter(pub_date__lt=index_post.pub_date).order_by('-pub_date')
    posts = []
    if prev_posts.count() > lower_bound:
        if prev_posts.count() > upper_bound:
            select_posts = prev_posts[lower_bound:upper_bound]
        else:
            select_posts = prev_posts[lower_bound:prev_posts.count()]
        # set up the data dictionary
        for p in select_posts:
            post = {}
            post['id'] = p.id
            post['carid'] = p.car.id
            post['pub_date'] = p.pub_date
            post['author'] = owner_display_name
            post['username'] = p.car.owner.username
            post['title'] = p.title
            post['body'] = p.body
            post['likecount'] = Like.objects.filter(post=p).count()
            post['tags'] = p.tags.all()
            post['comments'] = PostComment.objects.filter(post=p)
            posts.append(post)
    
        postcommentform = commentForm()

        return render(request, 'nextposts.html', {
            'isOwner': isOwner,
            'posts':posts,
            'postcommentform': postcommentform,
            });
    else:
        return HttpResponse('')

@login_required
def modAdd(request, name, carId):
    owner = request.user
    c = Car.objects.get(pk=carId)
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
            
            return HttpResponseRedirect('/journal/%s/car/%s/mod/' % (owner.username, c.pk))
    else:
        return HttpResponseRedirect('/journal/%s/car/%s/mod/' % (owner.username, c.pk))
            
@login_required
def modView(request, name, carId):
    owner = User.objects.get(username=name)
    owner_display_name = UserProfile.objects.get(user=owner).display_name
    isOwner = False
    if request.user.username == name:
        isOwner = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    if Follow.objects.filter(followed=owner, follower=request.user).exists():
        isFollower = True
    followed = Follow.objects.filter(follower=owner)
    cars = Car.objects.filter(owner=owner)
    memberships = Join.objects.filter(member=owner)
    c = Car.objects.get(pk=carId)
    c_tags = c.tags.all()
    c_taglist = []
    for tag in c_tags:
        c_taglist.append(tag.name)
    c_tags_string = ', '.join(c_taglist)

    # post data    
    posts = []
    last_post = ''
    all_posts = Post.objects.filter(car=c).order_by('-pub_date')
    if all_posts:
        select_posts = all_posts
        if all_posts.count() > 3:
            select_posts = all_posts[:3]
        last_post = select_posts[(len(select_posts)-1)]
        for p in select_posts:
            post = {}
            post['id'] = p.id
            post['carid'] = p.car.id
            post['pub_date'] = p.pub_date
            post['author'] = owner_display_name
            post['username'] = p.car.owner.username
            post['title'] = p.title
            post['body'] = p.body
            post['likecount'] = Like.objects.filter(post=p).count()
            post['tags'] = p.tags.all()
            post['comments'] = PostComment.objects.filter(post=p).order_by('-pub_date')
            posts.append(post)

    # mod data
    mods = Mod.objects.filter(car = c).order_by('modType')
    # photo data
    photos = Photo.objects.filter(car=c)

    # tab status
    carTabActive = False
    postsTabActive = False
    modTabActive = True
    galleryTabActive = False
    
    # vote counts
    fastvotecount = Vote.objects.filter(car=c).filter(type='fast').count()
    freshvotecount = Vote.objects.filter(car=c).filter(type='fresh').count()
        
    carform = carForm()
    editcarform = carForm(
        initial = {
            'name': c.name,
            'make': c.make,
            'model': c.model,
            'year': c.year,
            'c_tags': c_tags_string,
        }
    )
    modform = modForm()
    photoform = photoForm()
    messageform = messageForm()
    postcommentform = commentForm()

    return render(request, 'journalview.html', {
        'owner':owner,
        'isOwner':isOwner,
        'followCount':followCount,
        'isFollower': isFollower,
        'followed':followed,
        'cars':cars,
        'car':c,
        'c_tags':c_tags,
        'posts':posts,
        'last_post': last_post,
        'mods':mods,
        'photos': photos,
        'carTabActive': carTabActive,
        'postsTabActive': postsTabActive,
        'modTabActive': modTabActive,
        'galleryTabActive': galleryTabActive,
        'fastvotecount':fastvotecount,
        'freshvotecount':freshvotecount,
        'carform': carform,
        'editcarform': editcarform,
        'modform': modform,
        'photoform': photoform,
        'messageform': messageform,
        'postcommentform':postcommentform,
    })

@login_required
def modEdit(request, name, carId, modId):
    owner = request.user
    car = Car.objects.get(pk=carId)
    if request.user.username != name:
        return HttpResponseRedirect('/journal/%s/car/%s/mod/' % (owner.username, car.id))
    mod = Mod.objects.get(pk=modId)    
    if request.method == 'POST':
        form = modForm(request.POST)
        if form.is_valid():
            brand = form.cleaned_data['brand_edit']
            part = form.cleaned_data['part_edit']
            modType = form.cleaned_data['modType_edit']
            
            # modify mod object
            mod.brand = brand
            mod.part = part
            mod.modType = modType
            mod.save()
            
            return HttpResponseRedirect('/journal/%s/car/%s/mod/' % (owner.username, car.id)) 
    else:
        return HttpResponseRedirect('/journal/%s/car/%s/mod/' % (owner.username, car.id))

@login_required
def modDelete(request, name, carId, modId):
    owner = request.user
    m = Mod.objects.get(pk=modId)
    c = Car.objects.get(pk=carId)
    m.delete()
    return HttpResponseRedirect('/journal/%s/car/%s/mod' % (owner.username, c.id))

@login_required
def modDetails(request, modId):
    mod = Mod.objects.get(pk=modId)
    car = mod.car
    owner = car.owner 
    m = {}
    m['target'] = '/journal/%s/car/%s/mod/%s/edit/' % (owner.username, car.pk, mod.pk)
    m['modType'] = mod.modType
    m['brand'] = mod.brand
    m['part'] = mod.part
    mod_json = simplejson.dumps(m)
    return HttpResponse(mod_json)

@login_required
def photoAdd(request, name, carId):
    owner = request.user
    car = Car.objects.get(pk=carId)
            
    if request.method == 'POST':
        form = photoForm(request.POST, request.FILES)
        if form.is_valid():
            caption = form.cleaned_data['caption']
            # create photo instance and save image
            p = Photo(
                car = car,
                caption = caption,
                )
            p.save() 
            image_file = request.FILES['photo']
            p.original_image.save(image_file.name, image_file)
            p.filename = image_file.name
            p.save()
            p.send_photo()
            
            return HttpResponseRedirect('/journal/%s/car/%s/photo/' % (owner.username, car.pk))
    else:
        return HttpResponseRedirect('/journal/%s/car/%s/photo/' % (owner.username, car.pk))
            
@login_required
def photoView(request, name, carId):
    owner = User.objects.get(username=name)
    owner_display_name = UserProfile.objects.get(user=owner).display_name
    isOwner = False
    if request.user.username == name:
        isOwner = True
    followCount = len(Follow.objects.filter(followed=owner))
    isFollower = False
    if Follow.objects.filter(followed=owner, follower=request.user).exists():
        isFollower = True
    followed = Follow.objects.filter(follower=owner)
    cars = Car.objects.filter(owner=owner)
    memberships = Join.objects.filter(member=owner)
    c = Car.objects.get(pk=carId)
    c_tags = c.tags.all()
    c_taglist = []
    for tag in c_tags:
        c_taglist.append(tag.name)
    c_tags_string = ', '.join(c_taglist)

    # post data
    posts = []
    last_post= ''
    all_posts = Post.objects.filter(car=c).order_by('-pub_date')
    if all_posts:
        select_posts = all_posts
        if all_posts.count() > 3:
            select_posts = all_posts[:3]
        last_post = select_posts[(len(select_posts) - 1)]
        for p in select_posts:
            post = {}
            post['id'] = p.id
            post['carid'] = p.car.id
            post['pub_date'] = p.pub_date
            post['author'] = owner_display_name
            post['username'] = p.car.owner.username
            post['title'] = p.title
            post['body'] = p.body
            post['likecount'] = Like.objects.filter(post=p).count()
            post['tags'] = p.tags.all()
            post['comments'] = PostComment.objects.filter(post=p).order_by('-pub_date')
            posts.append(post)

    # mod data
    mods = Mod.objects.filter(car = c).order_by('modType')
    # photo data
    photos = Photo.objects.filter(car=c)

    # tab status
    carTabActive = False
    postsTabActive = False
    modTabActive = False
    galleryTabActive = True
    
    # vote counts
    fastvotecount = Vote.objects.filter(car=c).filter(type='fast').count()
    freshvotecount = Vote.objects.filter(car=c).filter(type='fresh').count()
        
    carform = carForm()
    editcarform = carForm(
        initial = {
            'name': c.name,
            'make': c.make,
            'model': c.model,
            'year': c.year,
            'c_tags': c_tags_string,
        }
    )
    modform = modForm()
    photoform = photoForm()
    messageform = messageForm()
    postcommentform = commentForm()

    return render(request, 'journalview.html', {
        'owner':owner,
        'isOwner':isOwner,
        'followCount':followCount,
        'isFollower': isFollower,
        'followed': followed,
        'cars':cars,
        'memberships': memberships,
        'car':c,
        'c_tags':c_tags,
        'posts':posts,
        'last_post':last_post,
        'mods':mods,
        'photos': photos,
        'carTabActive': carTabActive,
        'postsTabActive': postsTabActive,
        'modTabActive': modTabActive,
        'galleryTabActive': galleryTabActive,
        'fastvotecount':fastvotecount,
        'freshvotecount':freshvotecount,
        'carform': carform,
        'editcarform': editcarform,
        'modform': modform,
        'photoform': photoform,
        'messageform': messageform,
        'postcommentform': postcommentform,
    })

def photoDelete(request, name, carId, photoId):
    owner = request.user
    car = Car.objects.get(pk=carId)
    photo = Photo.objects.get(pk=photoId)    
    photo.delete()
    
    return HttpResponseRedirect('/journal/%s/car/%s/photo' % (owner.username, car.pk))

def canBeInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@login_required
def follow(request, name):
    follower = request.user
    followed = User.objects.get(username=name)
    try:
        f = Follow.objects.get(follower=follower, followed=followed)
    except Follow.DoesNotExist:        
        f = Follow(
                   follower = follower,
                   followed = followed,
                   )
        f.save()
        f.send_follow()

    count = len(Follow.objects.filter(followed=followed))    
    c = {}
    c['count'] = count
    follow_json = simplejson.dumps(c)
    return HttpResponse(follow_json)

@login_required
def unfollow(request, name):
    follower = request.user
    followed = User.objects.get(username=name)
    try:
        f = Follow.objects.get(follower=follower, followed=followed)
        f.delete()
    except Follow.DoesNotExist:
        pass
    count = len(Follow.objects.filter(followed=followed))    
    c = {}
    c['count'] = str(count)
    follow_json = simplejson.dumps(c)
    return HttpResponse(follow_json)

@login_required
def vote(request, name, carId, voteType):
    u = request.user
    c = Car.objects.get(pk=carId)
    t = voteType
    if not Vote.objects.filter(user = u.pk, car=c).exists():
        v = Vote(
                 user = u,
                 car = c,
                 type = t,
                 )
        v.save()
        v.send_vote()
    fastcount = len(Vote.objects.filter(car=c, type='fast'))
    freshcount = len(Vote.objects.filter(car=c, type='fresh'))
    c = {}
    c['fastcount'] = str(fastcount)
    c['freshcount'] = str(freshcount)
    vote_json = simplejson.dumps(c)
    return HttpResponse(vote_json)

@login_required
def like(request, name, carId, postId):
    u = request.user
    p = Post.objects.get(pk=postId)
    if not Like.objects.filter(user = u.pk, post=p).exists():
        l = Like(
                 user = u,
                 post = p,
                 )
        l.save()
        l.send_like()
        
    likecount = len(Like.objects.filter(post=p))
    c = {}
    c['likecount'] = str(likecount)
    like_json = simplejson.dumps(c)
    return HttpResponse(like_json)

@login_required
def message(request, name):
    recipient = User.objects.get(username=name)
    if request.method =='POST':
        form = messageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            msg = Message(
                recipient = recipient,
                sender = request.user.username,
                viewed = False,
                title = subject,
                body = message,
                pub_date = datetime.now(),
                label = 'Visit sender',
                action = '/journal/%s/' % request.user.username,
            )
            msg.save()
            return HttpResponseRedirect('/journal/%s?action=message' % recipient.username)
    else:
        return HttpResponseRedirect('/journal/%s/' % recipient.username)
            
