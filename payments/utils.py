import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import base64
from datetime import datetime

def get_access_token():
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
   
    response = requests.get(api_url, 
                            auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Failed to get access token")


def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    encoded_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    return encoded_password, timestamp

def initiate_stk_push(phone_number, amount):
    access_token = get_access_token()
    password, timestamp = generate_password()
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",  # For Buy Goods
        "Amount": amount,
        "PartyA": phone_number,  #  format 2547XXXXXXXX
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
       # "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "Test_mpesa",
        "TransactionDesc": "Payment for reservation"
    }

    stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(stk_push_url, json=payload, headers=headers)

    return response.json() if response.status_code == 200 else response.text
    
