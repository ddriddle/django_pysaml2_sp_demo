from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^acs/$', views.assertion_consumer_service, name='acs'),
    url(r'^disco/', views.discovery_response, name='disco'),
    url(r'^metadata/$', views.metadata, name='metadata'),
    url(r'^sso/', views.single_sign_on_service, name='sso'),
]
