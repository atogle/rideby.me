from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='index.html')),

    url(r'^stops/?$', 'project.views.stops', name='stops'),
    url(r'^routes/?$', 'project.views.routes', name='routes'),
    url(r'^transit/?$', 'project.views.transit', name='transit'),
)
