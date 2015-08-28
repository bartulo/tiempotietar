from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
import autocomplete_light
# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tiempo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', login, {'template_name': 'login.html', }, name="login"),
    url(r'^logout$', logout, {'template_name': 'logout.html', }, name="logout"),
    url(r'^web/', include('web.urls')),
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'web.views.reset_confirm', name='password_reset_confirm'),
    url(r'^reset/$', 'web.views.reset', name='reset'),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)
