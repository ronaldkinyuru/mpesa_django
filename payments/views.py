from django.shortcuts import render
from django.http import JsonResponse
from .utils import initiate_stk_push
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
 

def home(request):
    return HttpResponse("mpesa daraja 2.0")

@csrf_exempt
def stk_push_view(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone")
        amount = request.POST.get("amount")
    
        if not phone_number or not amount:
            return JsonResponse({"error": "phone number and amount required "}, status=400)
    
        response = initiate_stk_push(phone_number, int(amount))
        return JsonResponse(response)
    return JsonResponse({"error": "Invalid request method"}, status="405")
    
    
#@csrf_exempt
# def callback_view(request):
 #   data = request.body
  #  print("Callback received:", data)  # save to database 
   # return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
