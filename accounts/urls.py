from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^accounts/signup/', views.signup, name='signup'),
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^accounts/profile/$', views.profile_view, name='profile'),
    url(r'^accounts/profile/(?P<pk>[\-\w]+)/$', views.profile_detail, name='profile_detail'),
    url(r'^accounts/profile/(?P<pk>[\-\w]+)/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^accounts/feeds/$', views.feeds_view, name='user_feeds'),

]
