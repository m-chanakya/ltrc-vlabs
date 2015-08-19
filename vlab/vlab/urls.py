from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import views as users
from experiments import views as exp

urlpatterns = patterns('',
    url(r'^$', users.home),
    url(r'^register/$', users.register),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^experiments/(?P<exp>\w+)/(?P<stage>\w+)/$', exp.experiment),
)
