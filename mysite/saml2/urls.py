from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^metadata/', views.metadata, name='saml2:metadata'),
]
