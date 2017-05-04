from django.urls import reverse
from django.http import HttpResponse

def saml_client():
    reverse('saml2:metadata')

def metadata(request):
    return HttpResponse("In the future this will return metadata!")
