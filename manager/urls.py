from django.conf.urls.defaults import *

urlpatterns = patterns('crossfit.manager.views',
    (r'^$', 'index'),
)