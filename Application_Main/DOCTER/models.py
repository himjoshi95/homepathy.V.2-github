from unittest.util import _MAX_LENGTH
from django.db import models
from PATIENT.models import *
from .models import *
from COMMON_APP.models import *
# Create your models here.
from jsignature.fields import JSignatureField
from django.contrib.auth.models import User
from jsignature.mixins import JSignatureFieldsMixin



# Create your models here.
class Docter(models.Model):
	name = models.CharField(max_length=40)
	phone = models.CharField(max_length=12,default="",unique=True)
	email = models.CharField(max_length=50,unique=True)
	gender = models.CharField(max_length=30)
	address = models.CharField(max_length=200)
	age = models.IntegerField(default= 0)
	blood = models.CharField(max_length=10)
	username = models.OneToOneField(User,on_delete = models.CASCADE)
	status = models.BooleanField(default = 0)
	department = models.CharField(max_length=30 , default = "")
	attendance = models.IntegerField(default = 0)
	salary = models.IntegerField(default = 10000)
	forget_password_token = models.CharField(max_length=100,null=True,blank=True)
	
	def __str__(self):
		return self.name
# Prescription Model
class Prescription2(models.Model):
	prescription = models.CharField(max_length=200)
	symptoms = models.CharField(max_length=200)
	patient = models.ForeignKey(Patient,on_delete = models.CASCADE,unique = False)
	docter = models.ForeignKey(Docter,on_delete = models.CASCADE,unique = False)
	appointment = models.ForeignKey('COMMON_APP.Appointment',on_delete = models.CASCADE,unique = False)
	prescripted_date = models.DateField(auto_now = True) 
	outstanding = models.IntegerField(default = 0)
	paid = models.IntegerField(default = 0)
	total = models.IntegerField(default = 0)


# HR Dashboard Data


class Quote(models.Model):
	test = models.CharField(max_length=200)
	cause = models.CharField(max_length=400)

	def __str__(self):
		return( self.test)
class sign(models.Model):
	text = models.CharField(max_length=200,null=True , blank=True)
	signature = JSignatureField(null=True, blank=True)
class JSignatureModel(JSignatureFieldsMixin):
    name = models.CharField(max_length=20)
    signature = JSignatureField()



class Contents(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return( self.name )
class Item(models.Model):
	content = models.ForeignKey(Contents, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	head1= models.CharField(max_length=200)
	head2 = models.CharField(max_length=200)
	def __str__(self):
		return( self.name)
class Essence(models.Model):
	name = models.CharField(max_length=200)
	item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name ='essence_itom')
	def __str__(self):
		return(self.name)
class Head1(models.Model):
	name = models.CharField(max_length=200)
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name = 'head1_item')
	def __str__(self):
		return(self.name)
class Head2(models.Model):
	name = models.CharField(max_length=200)
	item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name ='head2_item')

	def __str__(self):
		return(self.name)

class Medicine(models.Model):
	name = models.CharField(max_length=200)
	item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name ='medicine_item')
	def __str__(self):
		return(self.name)	
class Analysis(models.Model):
	name = models.CharField(max_length=200)
	item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name ='analysis_item')
	def __str__(self):
		return(self.name)	



class Gnm_Sbs(models.Model):
	Organs = models.CharField(max_length=200)
	Conflicts = models.CharField(max_length=400)

	def __str__(self):
		return( self.Organs)

class ExampleModel(JSignatureFieldsMixin):

	patient = models.ForeignKey(Patient,on_delete = models.CASCADE,unique = False,null=True,blank=True)

	
class Price(models.Model):

	new_case = models.IntegerField()
	seven_days = models.IntegerField()
	fifteen_days = models.IntegerField()
	twentyone_days = models.IntegerField()
	thirty_days = models.IntegerField()
	fortyfive_days = models.IntegerField()
	two_months = models.IntegerField()
	three_months = models.IntegerField()
	courier = models.IntegerField(null=True)

class Amount(models.Model):

	patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True,blank=True)
	paid_amount = models.IntegerField(null=True,blank=True)
	transac_id = models.TextField(null=True,blank=True)
	cash = models.BooleanField(default=True)
	online = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now=True) 
	balance_flag = models.BooleanField(default=False)
	cash_amount = models.IntegerField(null=True,blank=True)
	online_amount = models.IntegerField(null=True,blank=True)
	collected_by = models.CharField(max_length=255,null=True)

class Balance(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
	balance_amt = models.IntegerField(null=True,blank=True)
	previous_deal_date = models.DateField(auto_now=True,auto_now_add=False)
	collected_by = models.CharField(max_length=255,null=True)

class AddMedicine(models.Model):

	name = models.CharField(max_length=100)
	potency = models.CharField(max_length=10)
	quantity = models.IntegerField()
	arrival_date = models.DateField(auto_now=True)
	
class CourierDetails(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	courier_amount = models.IntegerField()
	address = models.TextField(max_length=100,null=True,blank=True)
	date = models.DateField(auto_now_add=True,auto_now=False)
	email = models.EmailField(null=True,blank=True)
	email_flag = models.BooleanField(default=False)
	receiver_flag = models.BooleanField(default=False)
	balance_amount = models.IntegerField(default=0)
	paid_amount = models.IntegerField(default=0)
	transaction_id = models.CharField(max_length=50,null=True,blank=True)
	paid_on = models.DateField(auto_now=True,auto_now_add=False)
	collected_by = models.CharField(max_length=255,null=True,blank=True)

	def __str__(self):
		return str(self.patient)

class AddStaff(models.Model):

	name = models.CharField(max_length=100,null=True,blank=True)
	staff_id = models.IntegerField(null=True,blank=True)
	email = models.EmailField(null=True,blank=True)
	phone_number = models.IntegerField(null=True,blank=True)
	join_date = models.DateField(auto_now=True)
	role = models.CharField(max_length=50,null=True,blank=True)
	branch = models.CharField(max_length=100,null=True,blank=True)
	upload_image = models.ImageField(upload_to='images',null= True,blank=True)
	upload_docs = models.ImageField(upload_to='images',null= True,blank=True)

	def __str__(self):
		return self.name


class Diagnosis(models.Model):
	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	diagnose = models.CharField(max_length=100)
	med_name = models.CharField(max_length=100,null=True,blank=True)
	date = models.DateField(auto_now=True)

class Bill(models.Model):
	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	month = models.IntegerField(null=True,blank =True)
	consulting_fees = models.IntegerField(null=True,blank=True)
	medicine_fees = models.IntegerField(null=True,blank=True)
	date = models.DateField(auto_now=True)
	date1 = models.DateField(default=None,null=True,blank=True)
	date2 = models.DateField(default=None,null=True,blank=True)

class Certificate(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	diagnose1 = models.CharField(max_length=100,null=True,blank=True)
	diagnose2 = models.CharField(max_length=100,null=True,blank=True)
	diagnose3 = models.CharField(max_length=100,null=True,blank=True)
	date1 = models.DateField(null=True,blank=True)
	date2 = models.DateField(null=True,blank=True)
	date3 = models.DateField(null=True,blank=True)
	date4 = models.DateField(null=True,blank=True)
	month = models.IntegerField(null=True,blank=True)	