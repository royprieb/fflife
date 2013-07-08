from django.conf.urls import patterns, include, url
from blog import views
from haystack.forms import SearchForm
from haystack.views import SearchView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('blog.views',
    # Base views
    url(r'^$', 'index', name='index'),
    url(r'^home/$', 'index', name='home'),
    url(r'^filter/$', 'filter', name='filter'),
    url(r'^make/(?P<makeId>\d+)/all_json_models/$', 'all_json_models', name='all_json_models'),
    url(r'^rank/$', 'rank', name='rank'),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^about/$', 'about', name='about'),
    url(r'^advertise/$', 'advertise', name='advertise'),
    url(r'^terms/$', 'terms', name='terms'),
    url(r'^privacy/$', 'privacy', name='privacy'),
                       
    # Visit views
    url(r'^visit/car/(?P<carId>\d+)/$', 'carVisit', name='carVisit'),
    url(r'^visit/car/(?P<carId>\d+)/post/(?P<postId>\d+)/$', 'postVisit', name='postVisit'),
    url(r'^visit/car/(?P<carId>\d+)/post/(?P<postId>\d+)/like/$', 'like', name='like'),
    url(r'^visit/feature/(?P<featureId>\d+)/$', 'featureVisit', name='featureVisit'),
    url(r'^visit/car/(?P<carId>\d+)/vote/(?P<voteType>\w+)/$', 'vote', name='vote'),
    url(r'^visit/car/(?P<carId>\d+)/follow/$', 'follow', name='follow'),
    url(r'^visit/car/(?P<carId>\d+)/stopfollow/$', 'stopFollow', name='stopFollow'),
    url(r'^message/(?P<ownerId>\d+)/$', 'message', name='message'),
                       
    # Account views
    url(r'^account/new/$', 'newAccount', name='newAccount'),
    url(r'^account/edit/$', 'accountEdit', name='accountEdit'),
    url(r'^account/delete/$', 'accountDelete', name='accountDelete'),
    url(r'^logout/$', 'logoutuser', name='logout'),
    url(r'^login/$', 'loginuser', name='login'),
                       
    # Journal views
    url(r'^journal/view/$', 'journalView', name='journalView'),
    url(r'^journal/edit/$', 'journalEdit', name='journalEdit'),
    # Journal views: car
    url(r'^journal/car/new/$', 'carNew', name='carNew'),
    url(r'^journal/car/(?P<carId>\d+)/edit/$', 'carEdit', name='carEdit'),
    url(r'^journal/car/(?P<carId>\d+)/view/$', 'carView', name='carView'),
    url(r'^journal/car/(?P<carId>\d+)/delete/$', 'carDelete', name='carDelete'),
    # Journal views: posts
    url(r'^journal/car/(?P<carId>\d+)/post/new/$', 'postNew', name='postNew'),
    url(r'^journal/car/(?P<carId>\d+)/post/(?P<postId>\d+)/view/$', 'postView', name='postView'),
    url(r'^journal/car/(?P<carId>\d+)/post/(?P<postId>\d+)/edit/$', 'postEdit', name='postEdit'),
    url(r'^journal/post/(?P<postId>\d+)/delete/$', 'postDelete', name='postDelete'),
    url(r'^journal/car/(?P<carId>\d+)/post/(?P<postId>\d+)/like/$', 'like', name='like'),
    # Journal views: mods
    url(r'^journal/car/(?P<carId>\d+)/mod/add/$', 'modAdd', name='modAdd'),
    url(r'^journal/car/(?P<carId>\d+)/mod/view/$', 'modView', name='modView'),
    url(r'^journal/car/(?P<carId>\d+)/mod/(?P<modId>\d+)/edit/$', 'modEdit', name='modEdit'),
    url(r'^journal/mod/(?P<modId>\d+)/delete/$', 'modDelete', name='modDelete'),
    # Journal views: photos
    url(r'^journal/car/(?P<carId>\d+)/album/(?P<albumId>\d+)/add/$', 'albumAdd', name='albumAdd'),
    url(r'^journal/car/(?P<carId>\d+)/album/(?P<albumId>\d+)/view/$', 'albumView', name='albumView'),
    url(r'^journal/car/(?P<carId>\d+)/album/(?P<albumId>\d+)/edit/$', 'albumEdit', name='albumEdit'),
    url(r'^journal/photo/(?P<photoId>\d+)/delete/$', 'photoDelete', name='photoDelete'),
                       
    # tools
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^comments/delete/(?P<commentId>\d+)/$', 'commentDelete', name='commentDelete'),
    url(r'^comments/', include('django.contrib.comments.urls')),
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
