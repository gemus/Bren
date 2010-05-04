from django.conf.urls.defaults import *

urlpatterns = patterns('crossfit.email_sender.views',
    # /confirm/<subscribe_hash>/
    (r'^confirm/(\w+)/$', 'confirm'),
    (r'^unsubscribe/(\w+)/$', 'unsubscribe'),
)
