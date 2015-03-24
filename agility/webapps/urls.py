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
    url(r'^create_task$', 'agility.views.create_task', name='create_task'),
	url(r'^create_project$', 'agility.views.create_project', name='create_project'),
	url(r'^create_sprint$', 'agility.views.create_sprint', name='create_sprint'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'agility/login.html'}, name='login'),
    url(r'^edit_project/(?P<id>\d+)$', 'agility.views.edit_project', name='edit_project'),
    url(r'^edit_task/(?P<id>\d+)$', 'agility.views.edit_task', name='edit_task'),
    url(r'^edit_sprint/(?P<id>\d+)$', 'agility.views.edit_sprint', name='edit_sprint'),
)
