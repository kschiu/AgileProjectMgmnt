from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agility.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'agility.views.index', name='index'),
    url(r'^index$', 'agility.views.index', name='index'),
    url(r'^register$', 'agility.views.register', name='register'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'agility/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),
    #Project
    url(r'^create_project$', 'agility.views.create_project', name='create_project'),
    url(r'^edit_project/(?P<id>\d+)$', 'agility.views.edit_project', name='edit_project'),
    url(r'^view_project/(?P<id>\d+)$', 'agility.views.view_project', name='view_project'),
    url(r'^delete_project/(?P<id>\d+)$', 'agility.views.delete_project', name='delete_project'),
    #Tasks
    url(r'^create_task$', 'agility.views.create_task', name='create_task'),
    url(r'^edit_task/(?P<id>\d+)$', 'agility.views.edit_task', name='edit_task'),
    url(r'^view_task/(?P<id>\d+)$', 'agility.views.view_task', name='view_task'),
    url(r'^delete_task/(?P<id>\d+)$', 'agility.views.delete_task', name='delete_task'),
    #Sprint
    url(r'^create_sprint$', 'agility.views.create_sprint', name='create_sprint'),
    url(r'^edit_sprint/(?P<id>\d+)$', 'agility.views.edit_sprint', name='edit_sprint'),
    url(r'^view_sprint/(?P<id>\d+)$', 'agility.views.view_sprint', name='view_sprint'),
    url(r'^delete_sprint/(?P<id>\d+)$', 'agility.views.delete_sprint', name='delete_sprint'),

    url(r'^add_comment/(?P<id>\d+)$', 'agility.views.add_comment', name='add_comment'),
    url(r'^delete_comment/(?P<id>\d+)$', 'agility.views.delete_comment', name='delete_comment'),

)