from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^metadata/$', views.metadata, name='metadata'),
    url(r'^acs/$', views.assertion_consumer_service, name='acs'),
    url(r'^sls/', views.single_logout_service, name='sls'),
    url(r'^sso/', views.single_sign_on_service, name='sso'),
]
