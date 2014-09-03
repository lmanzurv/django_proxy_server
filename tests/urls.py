from django.conf.urls import url, patterns

urlpatterns = patterns('views',
    url(r'^test/$', 'test', name='test'),
)