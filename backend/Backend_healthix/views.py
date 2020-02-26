from django.shortcuts import render
from django.http  import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json

# Create your views here.
def welcome(request):
    return HttpResponse('Welcome to heathix payment')

def getAccessToken(request):
    consumer_key = 'uw7o6kXPA0Vocl9YnAWWipp5xpwTHFMr'
    consumer_secret = 'IBBflAtpUQfDKgsK'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)