from django.db import models
from datetime import date


# import in-Built User Models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
	name = models.CharField(max_length=40)
	phone = models.CharField(max_length=12,default="")
	alternative_number = models.CharField(max_length=12,null=True,blank=True)	
	email = models.CharField(max_length=50,null=True,blank=True)
	branch = models.CharField(max_length=200,default='',null=True)
	gender = models.CharField(max_length=30)
	address = models.CharField(max_length=200)
	age = models.IntegerField(default= 0 ,null=True)
	blood = models.CharField(max_length=10,null=True)
	usern = models.CharField(max_length=100)
	case = models.CharField(max_length=20)
	height = models.CharField(max_length=20,null=True,blank=True)
	weight = models.CharField(max_length=20,null=True,blank=True) 
	qualification = models.CharField(max_length=200,null=True,blank=True)
	occupation = models.CharField(max_length=200,null=True,blank=True)
	dietry_preference = models.CharField(max_length=50,null=True,blank=True)
	marital_status = models.CharField(max_length=50,null=True,blank=True)
	referred_by =  models.CharField(max_length=50,null=True,blank=True)
	diagnosis_provisional = models.CharField(max_length=200,null=True,blank=True)
	diagnosis_final =  models.CharField(max_length=200,null=True,blank=True)
	patient_images = models.ImageField(upload_to='images',null= True,blank=True)
	prescrip_images = models.ImageField(upload_to='images',null=True,blank=True)
	flag = models.BooleanField(default=True)
	display_flag = models.BooleanField(default=False)
	forget_password_token = models.CharField(max_length=100,null=True,blank=True)
	#username = models.OneToOneField(User,on_delete = models.CASCADE)
	
	def __str__(self):
		return self.case
	

class Invoice(models.Model):
	patient = models.OneToOneField(Patient,on_delete = models.CASCADE)
	outstanding = models.CharField(max_length =  10)
	paid = models.CharField(max_length = 10)



class MultipleUploadImages(models.Model):
	images = models.FileField(upload_to='images', null=True)
	#image = models.ImageField(upload_to='images', null=True)
	image= models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class ImagesUpload(models.Model):
	case = models.ForeignKey(Patient,on_delete=models.CASCADE)
	date = models.DateField(auto_now_add=True)
	images = models.ImageField(upload_to='images',null= True)

class PrescriptionOldUpload(models.Model):
	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	images = models.ImageField(upload_to='images',null=True,blank =True)

class NewCasePaperUpload(models.Model):
	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	images = models.ImageField(upload_to='images',null=True,blank=True)

class PatientImages(models.Model):
	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	images = models.ImageField(upload_to='images',null=True,blank=True)
	date = models.DateField(auto_now_add=True)

	