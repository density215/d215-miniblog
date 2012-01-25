from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login',{'login_url':'/'}, name='logout'),
    url('^$', 'entries.views.index'),
    url('^admin/', 'entries.views.admin'),
    url('^create/', 'entries.views.create'),
    url('^update/', 'entries.views.update'),
    url('^delete/', 'entries.views.delete'),
)
