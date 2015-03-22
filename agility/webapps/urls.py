from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agility.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index$', 'agility.views.index', name='index'),
    url(r'^register$', 'agility.views.register', name='register'),
    url(r'^create_task$', 'agility.views.create_task', name='create_task'),
)
