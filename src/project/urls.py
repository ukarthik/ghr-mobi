from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    (r'^', include('%s.urls' % settings.PROJECT_NAME)),
    
    (r'^', include('tunobase.corporate.company_info.urls')),
    
    (r'^console/', include('tunobase.console.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^secure/ckeditor/', include('ckeditor.urls')),
)

#------------------------------------------------------------------------------
# Django serves media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve', 
         {'document_root' : settings.MEDIA_ROOT, 
          'show_indexes': True}
         ),
    )
