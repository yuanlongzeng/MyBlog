from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def page_not_found(req):
    #return HttpResponse("HHHHHH")
    return render_to_response('404.html')