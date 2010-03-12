from django.conf.urls.defaults import *

urlpatterns = patterns('crossfit.email_sender.views',
    (r'^confirm/(\w+)/$', 'confirm'),
)
