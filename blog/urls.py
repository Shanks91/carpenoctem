from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^list/$', views.article_list, name='article_list'),
    url(r'^draft/$', views.article_draft, name='article_draft'),
    url(r'^article/create/$', views.article_create, name='article_create'),
    url(r'^article/(?P<pk>\d+)/$', views.article_detail, name='article_detail'),
    url(r'^draft/(?P<pk>\d+)/publish/$', views.article_publish, name='article_publish'),
    url(r'^article/(?P<pk>\d+)/edit/$', views.article_edit, name='article_edit'),
    url(r'^article/(?P<pk>\d+)/delete/$', views.article_delete, name='article_delete'),
]
