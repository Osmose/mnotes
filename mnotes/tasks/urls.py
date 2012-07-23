from django.conf.urls.defaults import patterns, url

from mnotes.tasks import views

urlpatterns = patterns('',
    url(r'^/?$', views.task_list, name='mnotes.tasks.task_list'),
    url(r'^tasks/?$', views.tasks, name='mnotes.tasks.tasks'),
    url(r'^jsonp/create_task/?$', views.create_task, name='mnotes.tasks.create_task'),
)
