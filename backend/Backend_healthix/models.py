from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        
# M-pesa Payment models
class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'
class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'
class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
    def __str__(self):
        return self.first_name

#createpayment model   

class Payment(models.Model):
    name = models.CharField(max_length = 65, blank=True)
    account = models.CharField(max_length = 65, blank=True)
    phone_Number= models.CharField(max_length=15)
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    conversation_id = models.CharField(max_length=100, null=True)


    def __str__(self):
        return self.name

    def save_payment(self):
        self.save()      


# bills model where transaction are stored


class Bills(models.Model):

    amount=models.IntegerField(blank=True)
    phone_number=models.TextField(default=0)
    reference=models.TextField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    conversation_id = models.CharField(max_length=100, null=True)

    def save_bills(self):
        self.save()

    def __str__(self):

        return self.amount

# hospitals table  

class Hospitals(models.Model):

    name = models.CharField(max_length = 65, blank=True)
    reference_no =models.TextField(default=0)
    location=models.CharField(max_length = 65, blank=True)

    def save_hospitals(self):
        self.save()

    def __str__(self):

        return self.reference_no

