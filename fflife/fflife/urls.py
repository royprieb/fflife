from django.conf.urls import patterns, include, url
from blog import views
from haystack.forms import SearchForm
from haystack.views import SearchView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('blog.views',
    # static views
    url(r'^$', 'index', name='index'),
    url(r'^about/$', 'about', name='about'),
    url(r'^terms/$', 'terms', name='terms'),
    url(r'^privacy/$', 'privacy', name='privacy'),
    url(r'^contact/$', 'contact', name='contact'),
    # account views
    url(r'^account/new/$', 'newAccount', name='newAccount'),
    url(r'^account/new/owner/$', 'newOwner', name='newOwner'),
    url(r'^account/new/vendor/$', 'newVendor', name='newVendor'),
    url(r'^account/edit/$', 'accountEdit', name='accountEdit'),
    url(r'^account/delete/$', 'accountDelete', name='accountDelete'),
    url(r'^logout/$', 'logoutuser', name='logout'),
    # nonJournal pages
    url(r'^home/$', 'home', name='home'),
    url(r'^message/(?P<messageId>\d+)/delete/$', 'messageDelete', name='messageDelete'),
    url(r'^explore/$', 'explore', name='explore'),
    url(r'^videos/$', 'videos', name='videos'),
    # Photoboard views
    url(r'^photoboard/$', 'photoboard', name='photoboard'),
    url(r'^photoboard/(?P<boardId>\d+)/upload/$', 'boardUpload', name='boardUpload'),
    url(r'^boardDetails/(?P<boardId>\d+)/$', 'boardDetails', name='boardDetails'),
    url(r'^photoboard/(?P<boardId>\d+)/photo/(?P<photoId>\d+)/$', 'boardPhotoView', name='boardPhotoView'),
    url(r'^photoboard/(?P<boardId>\d+)/photo/(?P<photoId>\d+)/like/$', 'boardPhotoLike', name='boardPhotoLike'),
    url(r'^photoboard/(?P<boardId>\d+)/photo/(?P<photoId>\d+)/delete/$', 'boardPhotoDelete', name='boardPhotoDelete'),
    url(r'^photoboard/(?P<boardId>\d+)/photo/(?P<photoId>\d+)/newcomment/$', 'boardPhotoComment', name='boardPhotoComment'),
    url(r'^photoboard/(?P<boardId>\d+)/photo/(?P<photoId>\d+)/comment/(?P<commentId>\d+)/delete/$', 'boardPhotoCommentDelete', name='boardPhotoCommentDelete'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/$', 'journal', name='journal'),
    # Group views
    url(r'^groups/$', 'groups', name='groups'),
    url(r'^groups/add/$', 'groupAdd', name='groupAdd'),
    url(r'^groups/(?P<groupId>\d+)/view/$', 'groupView', name='groupView'),
    url(r'^groups/(?P<groupId>\d+)/delete/$', 'groupDelete', name='groupDelete'),
    url(r'^groups/(?P<groupId>\d+)/join/$', 'groupJoin', name='groupJoin'),
    url(r'^groups/(?P<groupId>\d+)/leave/$', 'groupLeave', name='groupLeave'),
    url(r'^groups/(?P<groupId>\d+)/topic/add$', 'topicAdd', name='topicAdd'),
    url(r'^groups/(?P<groupId>\d+)/topic/(?P<topicId>\d+)/view/$', 'topicView', name='topicView'),
    url(r'^groups/(?P<groupId>\d+)/topic/(?P<topicId>\d+)/delete/$', 'topicDelete', name='topicDelete'),
    url(r'^groups/(?P<groupId>\d+)/topic/(?P<topicId>\d+)/respond/$', 'topicRespond', name='topicRespond'),
    url(r'^groups/(?P<groupId>\d+)/topic/(?P<topicId>\d+)/response/(?P<responseId>\d+)/delete/$', 'responseDelete', name='responseDelete'),
    # Journal views: vendor posts
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/vendorpost/add/$', 'vendorPostNew', name='vendorPostNew'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/post/(?P<postId>\d+)/$', 'vendorPostView', name='vendorPostView'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/post/(?P<postId>\d+)/edit/$', 'vendorPostEdit', name='vendorPostEdit'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/post/(?P<postId>\d+)/delete/$', 'vendorPostDelete', name='vendorPostDelete'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/post/(?P<postId>\d+)/newcomment/$', 'vendorPostComment', name='vendorPostComment'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/post/(?P<postId>\d+)/comment/(?P<commentId>\d+)/delete/$', 'vendorPostCommentDelete', name='vendorPostCommentDelete'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/post/(?P<postId>\d+)/next$', 'vendorPostNext', name='vendorPostNext'),
    # Journal views: cars
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/add/$', 'carNew', name='carNew'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/$', 'carView', name='carView'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/edit/$', 'carEdit', name='carEdit'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/delete/$', 'carDelete', name='carDelete'),
    # Journal views: posts
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/post/add/$', 'postNew', name='postNew'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/post/(?P<postId>\d+)/$', 'postView', name='postView'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/post/(?P<postId>\d+)/edit/$', 'postEdit', name='postEdit'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/post/(?P<postId>\d+)/delete/$', 'postDelete', name='postDelete'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/post/(?P<postId>\d+)/newcomment/$', 'postComment', name='postComment'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/post/(?P<postId>\d+)/comment/(?P<commentId>\d+)/delete/$', 'postCommentDelete', name='postCommentDelete'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/post/(?P<postId>\d+)/next$', 'postNext', name='postNext'),
    # Journal views: mods
    url(r'^details/mod/(?P<modId>\d+)/$', 'modDetails', name='modDetails'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/mod/add/$', 'modAdd', name='modAdd'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/mod/$', 'modView', name='modView'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/mod/(?P<modId>\d+)/edit/$', 'modEdit', name='modEdit'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/mod/(?P<modId>\d+)/delete/$', 'modDelete', name='modDelete'),
    # Journal views: photos
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/photo/add/$', 'photoAdd', name='photoAdd'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/photo/$', 'photoView', name='photoView'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/photo/(?P<photoId>\d+)/delete/$', 'photoDelete', name='photoDelete'),
    # Visitor views
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/follow/$', 'follow', name='follow'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/unfollow/$', 'unfollow', name='unfollow'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/vote/(?P<voteType>\w+)/$', 'vote', name='vote'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/car/(?P<carId>\d+)/post/(?P<postId>\d+)/like/$', 'like', name='like'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/post/(?P<postId>\d+)/like/$', 'vendorPostLike', name='vendorPostLike'),
    url(r'^journal/(?P<name>[-A-Za-z0-9_]+)/message/$', 'message', name='message'),
    # Typeahead views
    url(r'^carmake/$', 'carMake', name='carMake'),
    url(r'^carmodel/$', 'carModel', name='carModel'),
    url(r'^modtype/$', 'modType', name='modType'),
    url(r'^vendorcategory/$', 'vendorCategory', name='vendorCategory'),
    
    # tools
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^captcha/', include('captcha.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#url patterns for haystack views
urlpatterns += patterns('haystack.views',
    url(r'^search/', SearchView(form_class=SearchForm, results_per_page=10), name='haystack_search'),
)

# url patterns for user uploaded media files -- NOT PRODUCTION SETTING --
if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                    'document_root': settings.MEDIA_ROOT,
                                }),
                            )

#url patterns from django.contrib.auth.views pw reset and change
urlpatterns += patterns('',
    url(r'^account/password/change/$', 'django.contrib.auth.views.password_change', {'template_name':'pwchange.html','post_change_redirect': '/'}, name='changepw'),
    url(r'^account/password/reset/$', 'django.contrib.auth.views.password_reset', {
        'template_name':'fflife_pw_reset_form.html',
        'email_template_name':'fflife_pw_reset_email.html',
        'post_reset_redirect':'/account/password/reset/done/',
        }),
    url(r'^account/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {
        'template_name':'fflife_pw_reset_done.html',
        }),
    url(r'^account/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {
        'post_reset_redirect': '/account/password/done/',
        'template_name': 'fflife_pw_reset_confirm.html',
        }),
    url(r'^account/password/done/$', 'django.contrib.auth.views.password_reset_complete', {
        'template_name': 'fflife_pw_reset_complete.html',
        }),
)