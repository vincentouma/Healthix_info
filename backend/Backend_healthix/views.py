from django.shortcuts import render,redirect
from django.http  import HttpResponse,JsonResponse

import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from . models import Bills,Payment
from . forms import PaymentForm, HospitalsForm
from rest_framework.response import Response
from rest_framework.views import APIView
from . serializer import BillsSerializer

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

def lipa_na_mpesa_online(phone,amount):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone,  # replace with your phone number to get stk push
        "CallBackURL": "https://dc9428d4.ngrok.io /confirmation/",
        "AccountReference": "Obindi",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.json())
    return response.json()
    # ['CheckoutRequestID']

@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://dc9428d4.ngrok.io /api/v1/c2b/confirmation",
               "ValidationURL": "https://dc9428d4.ngrok.io /api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)
@csrf_exempt
def call_back(request):
    pass
@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    try:
        mpesa_payment_json = json.loads(mpesa_body)
    except Exception as e:
        print(e)
        context = {
            "ResultCode": 1,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context)) 
    print(mpesa_payment_json) 
    if mpesa_payment_json['Body']['stkCallback']['ResultCode']==0:
        mpesa_payment = mpesa_payment_json['Body']['stkCallback']['CallbackMetadata']['Item']
        print(mpesa_payment)
        
        b = Bills(
           phone_number=mpesa_payment[4]['Value'],
           reference=mpesa_payment[1]['Value'],
           amount=mpesa_payment[0]['Value'],
           conversation_id=mpesa_payment_json['Body']['stkCallback']['CheckoutRequestID']
        )

        b.save()
        #send_bill_receipt(b)
        context = { 
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context))    
# payment funtion that pick data from form to lipaonline

def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST,request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)

            phone_Number = form.cleaned_data['phone_Number']
            amount = form.cleaned_data['amount']
            conv = lipa_na_mpesa_online(phone_Number, amount)
            payment.conversation_id = conv
            payment.save()
            return redirect('all_customer_bills')

    else:
        form = PaymentForm()
    return render(request,'payment.html',locals())

# hospitals veiw  fuction 

def hospital(request):


    #this_user_id_number = User.objects.all()
    if request.method == 'POST':

        form = HospitalsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            phone_Number = form.cleaned_data['phone_Number']
            amount = form.cleaned_data['amount']
            # form.save(commit=False)
            # payment.save()
            lipa_na_mpesa_online(phone_Number, amount)
            return redirect('bills')
    else:
        form = HospitalsForm()
    return render(request,'toilet.html',locals())  


# retreving bill data from payment model  

def bills(request):
    url = 'https://sandbox.safaricom.co.ke/mpesa/?api_key=uw7o6kXPA0Vocl9YnAWWipp5xpwTHFMr'
    response = requests.get(url.format()).json()
    details = []
    for detail in details:
        amount = detail.get('amount')
        phone_number = detail.get('phone_number')
        reference = detail.get('reference')
        return HttpResponse(response.text)

    bills=Bills.objects.all()

    return render(request, 'all_bills.html', {'details': details})

# combining bills table and payment table     

def combinedReport(request):
    all_bills = []
    for bill in Bills.objects.all():
        payment = Payment.objects.filter(conversation_id__isnull=False, conversation_id=bill.conversation_id).first()
        _bill = {
            'id': bill.id,
            'amount': bill.amount,
            'phone_number': bill.phone_number,
            'reference': bill.reference,
            'timestamp': bill.timestamp
        }
        if payment:
            _bill['account'] = payment.account
            _bill['name'] = payment.name
        all_bills.append(_bill)
    print(all_bills)
    all_payments=Payment.objects.all()
    print(all_payments)

    return render(request,'combined.html',{'all_bills':all_bills,"all_payments":all_payments})
# creating endpoint for biils 

class BillsList(APIView):

    def get(self, request, format=None):
        all_bills = Bills.objects.all()
        serializers = BillsSerializer(all_bills, many=True)
        return Response(serializers.data) 

#consuming the bills api
def all_customer_bills(request):
    url = ('http://127.0.0.1:8000/api/bills')
    response = requests.get(url)
    customer_bills = response.json()
    for bill in customer_bills:
        id = bill.get('id')
        amount = bill.get('amount')
        phone_number = bill.get('phone_number')
        reference = bill.get('reference')
    return render(request, 'all_bills.html', {'customer_bills': customer_bills})

