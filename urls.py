from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import django.contrib.auth.views
import crossfit.reports.urls
import crossfit.bren.urls
import crossfit.email_sender.urls

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/',   include(admin.site.urls)),
    (r'^reports/', include(crossfit.reports.urls)),
    (r'^email/',   include(crossfit.email_sender.urls)),
    (r'^',         include(crossfit.bren.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
