from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.index', name='home'),
    url(r'^delete/(?P<id>\d+)$', 'main.views.delete'),
    url(r'^show/(?P<id>\d+)$', 'main.views.index'),
    url(r'^register/(?P<id>\d+)$', 'main.views.register'),
    # url(r'^gps_sms/', include('gps_sms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
