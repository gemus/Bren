from django.conf.urls.defaults import *

urlpatterns = patterns('crossfit.email_sender.views',
    # /confirm/<subscribe_hash>/
    (r'^confirm/(\w+)/$', 'confirm'),

    # /send_perm_request/<user_id>/
    (r'^send_perm_request/(\d+)/$', 'send_perm_request'),
)
