from django.conf.urls.defaults import patterns, url

from mnotes.users import views

urlpatterns = patterns('',
    url(r'^user/?$', views.get_user, name='mnotes.users.get_user'),
    url(r'^login/?$', views.login, name='mnotes.users.login'),
    url(r'^logout/?$', views.logout, name='mnotes.users.logout'),
)
