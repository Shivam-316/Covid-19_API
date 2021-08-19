from django.core import management
from django.http import request
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def collectData(request):
    try:
        management.call_command('run_scheduler')
        return JsonResponse({'Working':"YES!"})
    except:
        return JsonResponse({'Working':"No!"})