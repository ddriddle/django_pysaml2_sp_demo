from django.http import HttpResponse

def metadata(request):
    return HttpResponse("In the future this will return metadata!")
