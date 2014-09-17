from django.conf.urls import url, patterns

urlpatterns = patterns('views',
    url(r'^test/$', 'test'),
    url(r'^test_error/$', 'test_error'),
    url(r'^test_token_validation/$', 'test_token_validation'),
    url(r'^test_undecorated/$', 'test_undecorated'),
)
