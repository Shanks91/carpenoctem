from django.conf.urls import url
from ordinem import views


urlpatterns = [
    url(r'^ngo/$', views.ngolist, name='ngo_list'),
    url(r'^ngo/search/$', views.ngolist_search, name='ngo_list_search'),
    url(r'^ngo/signup/$', views.createngo, name='ngo_signup'),
    url(r'^ngo/detail/(?P<pk>\d+)/$', views.ngoprofile, name='ngo_profile'),
    url(r'^ngo/detail/(?P<pk>\d+)/gallery/$', views.gallery_view, name='gallery'),
    url(r'^ngo/detail/(?P<pk>\d+)/like/$', views.ngo_like, name='ngo_like'),
    url(r'^ngo/detail/(?P<pk>\d+)/rate/$', views.rate_ngo, name='ngo_rate'),
    url(r'^ngo/detail/(?P<pk>\d+)/create/event/$', views.post_happening, name='post_happening'),
    url(r'^ngo/happening/(?P<pk>\d+)/edit/$', views.edit_happening, name='edit_happening'),
    url(r'^ngo/happening/(?P<pk>\d+)/delete/$', views.delete_happening, name='delete_happening'),
    url(r'^ngo/happening/(?P<pk>\d+)/like/$', views.happening_post_like, name='like_happening'),
    url(r'^ngo/detail/(?P<npk>\d+)/follow/(?P<upk>\d+)/$', views.follow_ngo, name='follow_ngo'),
    url(r'^ngo/detail/(?P<pk>\d+)/create/gallery/$', views.post_gallery, name='post_gallery'),
    url(r'^ngo/detail/(?P<pk>\d+)/comment/$', views.post_comment, name='post_comment'),
]
