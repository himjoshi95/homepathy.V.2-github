from datetime import date
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from DOCTER.models import *
from PATIENT.models import *
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

# Model For Receptionist
class Receptionist(models.Model):
	name = models.CharField(max_length=40)
	phone = models.CharField(max_length=12,default="",unique=True)
	email = models.CharField(max_length=50,unique=True)
	address = models.CharField(max_length=200)
	branch = models.CharField(max_length=200,default='',null=True)
	username = models.OneToOneField(User,on_delete = models.CASCADE)
	recep_image = models.ImageField(upload_to='images',null= True,blank=True)
	forget_password_token = models.CharField(max_length=100,null=True,blank=True)

class ReceptionistDocs(models.Model):

	recep = models.ForeignKey(Receptionist,on_delete=models.CASCADE)
	date = models.DateField(auto_now=True)
	images = models.ImageField(upload_to='images',null= True,blank=True)

# Model For Appointment
class Appointment(models.Model):
	docterid = models.ForeignKey('DOCTER.Docter',on_delete = models.CASCADE)
	patientid = models.ForeignKey('PATIENT.Patient',on_delete = models.CASCADE)
	time = models.CharField(max_length =40,null=True,blank=True)
	date = models.CharField(max_length=40,default="")
	status = models.BooleanField(max_length = 15, default=False)
	stat = models.CharField(max_length=50,null=True,blank=True)
	token = models.IntegerField(null=True,blank=True,default=0)     # For Dombivali branch
	token1 = models.IntegerField(null=True,blank=True,default=0)		# For Mulund branch
	notification_flag = models.BooleanField(default=False)	
	doctor_notification = models.BooleanField(default=False)
	medicine_flag = models.BooleanField(default=False)
	patient_new_old = models.CharField(max_length=10,null=True,blank=True)	
	email_flag = models.BooleanField(default=False)
	#case = models.ForeignKey('PATIENT.Patient',on_delete = models.CASCADE)
	#phone = models.ForeignKey('PATIENT.Patient',on_delete = models.CASCADE)

	def save(self,*args, **kwargs):
		print('args',args)

		if args:

			if args[2]:
				super(Appointment,self).save()
			elif args[3]:
				super(Appointment,self).save()
			elif args[4]:
				super(Appointment,self).save()
			elif args[5]:
				super(Appointment,self).save()
			
			else:
				if args[0] == 'Dombivali' and args[1] == 'General':
					self.object_list = Appointment.objects.filter(Q(date=date.today()) & Q(patientid__branch=str(args[0])) & Q(stat = str(args[1]))).order_by('token')						
					if len(self.object_list) == 0:
						self.token = 1					
					else:				
						self.token = self.object_list.last().token + 1
					super(Appointment,self).save()
				else:
					self.object_list1 = Appointment.objects.filter(Q(date=date.today()) & Q(patientid__branch=str(args[0])) & Q(stat = str(args[1])))			
					if len(self.object_list1) == 0:
						self.token1 = 1
					else:				
						self.token1 = self.object_list1.last().token1 + 1							
					super(Appointment,self).save()
		else:
			super(Appointment,self).save()

class HealthAssessment(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
	bp = models.CharField(max_length=50)
	weight =  models.CharField(max_length=10)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return str(self.patient)


class TokenUpdate(models.Model):
	token = models.IntegerField(default=0,null=True,blank=True)	
	consultancy = models.BooleanField(default=False)	 

class Payment(models.Model):
	docterid = models.ForeignKey('DOCTER.Docter',on_delete = models.CASCADE)
	patientid = models.ForeignKey('PATIENT.Patient',on_delete = models.CASCADE)
	time = models.CharField(max_length =40)
	date = models.CharField(max_length=40,default="")
	cunsulting=models.BooleanField(default=False)
	extraMedicine=models.IntegerField(default=0) 
	balance=models.IntegerField(default=0)

	def __str__(self):
		return self.patientid.name
		

	
P_CHOICES =(
    ("Q", "Q"),
    ("3X", "3X"),
    ("6X", "6X"),
    ("6", "6"),
    ("30", "30"),("200", "200"),("1M", "1M"),('10M','10M'),('0/1','0/1'),('0/2','0/2'),('0/3','0/3'),('0/4','0/4'),
	('0/5','0/5'),('0/6','0/6'),('0/7','0/7'),('0/8','0/8'),('0/9','0/9'),('0/10','0/10'),('0/11','0/11'),('0/12','0/12'),
	('0/13','0/13'),('0/14','0/14'),('0/15','0/15')
)

D_CHOICES=( ("7 days", "7 days"), ("15 days", "15 days"), ("1 month", "1 month"), ("2 month", "2 month"), ("3 month", "3 month"), ("4 month", "4 month"), ("6month", "6 month"),)

class prescription(models.Model):
	patientid = models.ForeignKey('PATIENT.Patient',on_delete = models.CASCADE)
	medicine = models.CharField(max_length=200)
	potency = models.CharField(max_length=50)
	date=models.DateField()
	durations=models.CharField(max_length=50)
	flag = models.BooleanField(default=True)
	diagnose = models.CharField(max_length=300,null=True,blank=True)
	start_date = models.CharField(max_length=50,null=True,blank=True)
	dose = models.CharField(max_length=200,null=True)
	note =models.TextField(null=True,blank=True)

class OtherPrescription(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	other_price = models.TextField(null=True)
	description = models.TextField(null=True,blank=True)
	date = models.DateField(auto_now_add=True)

class AddConsultationCharges(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	other_price = models.CharField(max_length=10,null=True,blank=True)
	name =  models.CharField(max_length=50,null=True,blank=True)
	date = models.DateField(auto_now_add=True)
	

# Model For HR
class HR(models.Model):
	name = models.CharField(max_length=40)
	phone = models.CharField(max_length=12,default="",unique=True)
	email = models.CharField(max_length=50,unique=True)
	address = models.CharField(max_length=200)
	branch = models.CharField(max_length=200,default='',null=True)
	username = models.OneToOneField(User,on_delete = models.CASCADE)
	hr_image = models.ImageField(upload_to='images',null= True,blank=True)
	forget_password_token = models.CharField(max_length=100,null=True,blank=True)



CHOICES = (
    ("Hedoc", "Hedoc"),
    ("Stomach", "Stomach"),
    ("Brain", "Brain"),
    ("Heart", "Heart"),
    ("Liver", "Liver"),
    ("Kideney", "Kideney"),
    ("Oncho", "Oncho"),
    ("Yash", "Yash"),
)

class HRDocs(models.Model):

	hr = models.ForeignKey(HR,on_delete=models.CASCADE)
	date = models.DateField(auto_now=True)
	images = models.ImageField(upload_to='images',null= True,blank=True)

class Article(models.Model):
    title = models.CharField(max_length=255,choices=CHOICES)
    content = RichTextField(blank=True, null=True)
    content_upload = RichTextUploadingField(blank=True, null=True)


class InvestigationAdvised(models.Model):

	name = models.CharField(max_length=250,null=True,blank=True)

	def __str__(self):
		return self.name
	
class InvestigationRecords(models.Model):

	patient = models.ForeignKey(Patient,on_delete = models.CASCADE,null=True,blank=True)
	records = models.CharField(max_length=500, null=True,blank=True)
	any_other = models.CharField(max_length=100,null=True,blank=True)
	date = models.DateField(auto_now_add=True)

class Ultrasonography(models.Model):

	name = models.CharField(max_length=250,null=True,blank=True)

	
	
class UltrasonographyRecords(models.Model):

	patient = models.ForeignKey(Patient,on_delete = models.CASCADE,null=True,blank=True)
	records = models.CharField(max_length=500, null=True,blank=True)	
	date = models.DateField(auto_now_add=True)

class Doppler(models.Model):

	name = models.CharField(max_length=250,null=True,blank=True)

	def __str__(self):
		return self.name
	
class DopplerRecords(models.Model):

	patient = models.ForeignKey(Patient,on_delete = models.CASCADE,null=True,blank=True)
	records = models.CharField(max_length=500, null=True,blank=True)	
	date = models.DateField(auto_now_add=True)

class Obstetrics(models.Model):

	name = models.CharField(max_length=250, null=True,blank=True)

	def __str__(self):
		return self.name


class ObstetricRecords(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
	records = models.CharField(max_length=500, null=True,blank=True)
	date = models.DateField(auto_now_add=True)


class SonographyType(models.Model):

	name = models.CharField(max_length=250,null=True,blank=True)

	def __str__(self):
		return self.name


class SonographyTypeRecords(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
	records = models.CharField(max_length=100, null=True,blank=True)
	date = models.DateField(auto_now_add=True)


class CTScanNew(models.Model):

	name = models.CharField(max_length=250,null=True,blank=True)

	def __str__(self):
		return self.name
	
	
class CTScanNewRecords(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
	records = models.CharField(max_length=250, null=True,blank=True)
	date = models.DateField(auto_now_add=True)


class MRIScanNew(models.Model):

	name = models.CharField(max_length=250,null=True,blank=True)

	def __str__(self):
		return self.name
	
	
class MRIScanNewRecords(models.Model):

	patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
	records = models.CharField(max_length=250, null=True,blank=True)
	any_other = models.CharField(max_length=100,null=True,blank=True)
	date = models.DateField(auto_now_add=True)


class StockName(models.Model):

	name = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.name
	
class VendorCategory(models.Model):

	category = models.CharField(max_length=225)

	def __str__(self):
		return self.category
	
class AddVendorStock(models.Model):

	vendor_name = models.CharField(max_length=255)
	vendor_category = models.ForeignKey(VendorCategory,on_delete=models.CASCADE,null=True) 
	mobile_number = models.IntegerField()
	email = models.EmailField()
	address = models.TextField()

	def __str__(self):
		return self.vendor_name
	
class VendorStockProduct(models.Model):

	vendor = models.ForeignKey(AddVendorStock,on_delete=models.CASCADE)
	product_name = models.ForeignKey(StockName,on_delete=models.CASCADE)

	def __str__(self):
		return self.product_name.name

	
unit_choices = [
	('','Please Select Unit from list'),
	('Kg','Kg'),
	('Piece','Piece'),
	('Packet','Packet'),
	('Bottle','Bottle'),
	('Box','Box'),
]


class Stock(models.Model):

	branch_name = models.CharField(max_length=50,null=True,blank=True)
	stock_name = models.ForeignKey(VendorStockProduct,on_delete=models.CASCADE,null=True,blank=True)
	vendor = models.ForeignKey(AddVendorStock,on_delete=models.CASCADE,null=True,blank=True)
	quantity = models.IntegerField(default='0',null=True,blank=True)
	stock_unit = models.CharField(max_length=50,choices=unit_choices, null=True,blank=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)	
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)	
	approval_flag_new = models.BooleanField(default=True)
	approval_flag_updtate = models.BooleanField(default=False)
	approval_flag_receive = models.BooleanField(default=False)
	upload_stock_bill_image = models.ImageField(upload_to='stock/',null=True)

	def __str__(self):
		return str(self.stock_name.product_name)
	
@receiver(post_save, sender=Stock)
def add_bill_image(sender,instance,created,**kwargs):

	# print("instance",instance,instance.id)
	stock_bill = Stock.objects.get(id=instance.id)
	# print("bill",stock_bill,stock_bill.bill_image)
	if created:
		new_obj = BillImageStock.objects.create(stock = stock_bill, stock_image=stock_bill.upload_stock_bill_image)
	

class BillImageStock(models.Model):

	stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
	stock_image = models.ImageField(upload_to='stock_bill/')
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)	

	

class AddMedicineHR(models.Model):

	medicine_name = models.CharField(max_length=225)

	def __str__(self):
		return self.medicine_name
	
	
class AddPotencyHR(models.Model):
	potency_name = models.CharField(max_length=30)

	def __str__(self):
		return self.potency_name
	
class VendorMedicine(models.Model):

	vendor = models.ForeignKey(AddVendorStock,on_delete=models.CASCADE)
	medicine = models.ForeignKey(AddMedicineHR,on_delete=models.CASCADE)
	potency = models.ForeignKey(AddPotencyHR,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.medicine.medicine_name)
	
	
class MedicineStockList(models.Model):

	medicine = models.ForeignKey(VendorMedicine,on_delete=models.CASCADE,null=True)
	vendor = models.ForeignKey(AddVendorStock,on_delete=models.CASCADE,null=True,blank=True)
	potency =models.ForeignKey(AddPotencyHR,on_delete=models.CASCADE)	
	quantity = models.IntegerField(default='0', blank=True, null=True)
	branch = models.CharField(max_length=50,null=True,blank=True)	
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)	
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	approval_flag_new = models.BooleanField(default=True)
	approval_flag_updtate = models.BooleanField(default=False)
	approval_flag_receive = models.BooleanField(default=False)	
	order_status = models.BooleanField(default=True)	

	def __str__(self):
		return str(self.medicine.medicine)
	

class PlaceOrderStock(models.Model):

	stock_order = models.ForeignKey(Stock,on_delete=models.CASCADE)
	order_quantity = models.IntegerField()
	unit = models.CharField(max_length=50,choices=unit_choices, null=True)
	order_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	order_delivery_date = models.DateField()
	email = models.EmailField()
	email_placed_flag = models.BooleanField(default=False)
	order_received_flag =models.BooleanField(default=False)

	def __str__(self):
		return str(self.stock_order)
	

class PlaceOrderMedicine(models.Model):

	vendor_order = models.ForeignKey(VendorMedicine,on_delete = models.CASCADE,null=True)
	medicine_order = models.CharField(max_length=100,null=True)
	potency = models.CharField(max_length=100,null=True)
	order_quantity = models.IntegerField()	
	order_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	order_delivery_date = models.DateField()
	email = models.EmailField()
	email_placed_flag = models.BooleanField(default=False)
	order_received_flag =models.BooleanField(default=False)


	def __str__(self):
		return str(self.medicine_order)
	
class PlaceOrderMedicineNew(models.Model):

	vendor_order = models.ForeignKey(AddVendorStock,on_delete = models.CASCADE,null=True)
	medicine_order = models.ForeignKey(MedicineStockList, on_delete=models.CASCADE,null=True)
	potency = models.ForeignKey(AddPotencyHR, on_delete= models.CASCADE,null=True)
	order_quantity = models.IntegerField()
	order_timestamp = models.DateField(auto_now_add=True, auto_now=False)
	order_delivery_date = models.DateField()
	email = models.EmailField()
	email_placed_flag = models.BooleanField(default=False)
	order_received_flag = models.BooleanField(default=False)

	def __str__(self):
		return str(self.medicine_order)
	
pack_choices = [
	('',' Select '),
	('10 ML','10 ML'),
	('30 ML','30 ML'),
	('100 ML','100 ML'),
	('450 ML','450 ML'),
]
	

class PlaceOrderMedicineOne(models.Model):

	vendor_order = models.ManyToManyField(AddVendorStock)
	medicine_order = models.ForeignKey(MedicineStockList, on_delete=models.CASCADE)
	potency = models.ForeignKey(AddPotencyHR, on_delete=models.CASCADE)
	pack = models.CharField(max_length=100,choices=pack_choices,null=True,default='30 ML')
	order_quantity = models.IntegerField()
	order_timestamp = models.DateField(auto_now_add=True, auto_now=False)
	order_delivery_date = models.DateField(null=True)
	order_received_flag = models.BooleanField(default=False)

	def __str__(self):
		return str(self.medicine_order)


	
class OrderMedicineItem(models.Model):

	vendor = models.ForeignKey(AddVendorStock, on_delete=models.CASCADE)
	ordered_med = models.ForeignKey(PlaceOrderMedicineOne, on_delete=models.CASCADE)
	order_received = models.PositiveIntegerField(default= 0)
	order_balance = models.PositiveIntegerField(default= 0)
	email_status = models.BooleanField(default=False)
	order_receive_flag = models.BooleanField(default=False)	
	is_verified = models.BooleanField(default=False)

	def __str__(self):
		return str(self.vendor)+" :" + str(self.ordered_med) + " :" + str(self.ordered_med.order_timestamp)
	
class BillOrderMedicineImage(models.Model):

	ordered_med = models.ForeignKey(OrderMedicineItem,on_delete=models.CASCADE)
	bill_images = models.ImageField(upload_to='images')
	bill_image_timestamp = models.DateField(auto_now_add=True,auto_now=False)

	def __str__(self):
		return str(self.ordered_med)
	
class OurPortfolioImages(models.Model):

	images = models.ImageField(upload_to='images')


class ForAppointmentHomePage(models.Model):

	branch_name = models.CharField(max_length=100)
	contact_number_one = models.CharField(max_length=50)
	contact_number_two = models.CharField(max_length=50,null=True,blank=True)

	def __str__(self):
		return self.branch_name
	

######### ITEMS INVENTORY FINAL CODE   ####################

class AddItems(models.Model):

	item_name = models.CharField(max_length=100)

	def __str__(self):
		return self.item_name
	
class AddUnits(models.Model):

	unit_name = models.CharField(max_length=50)

	def __str__(self):
		return self.unit_name
	

class ItemsVendorDetails(models.Model):

	vendor_name = models.CharField(max_length=100)
	mobile_number = models.CharField(max_length=10)
	email = models.EmailField()
	address = models.TextField()

	def __str__(self):
		return self.vendor_name
	
class ItemUnitInventory(models.Model):

    item = models.ForeignKey(AddItems, on_delete=models.CASCADE)
    unit = models.ForeignKey(AddUnits,on_delete=models.CASCADE)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    branch = models.CharField(max_length=50,null=True,blank=True)	
    receive_quantity = models.IntegerField(default='0',blank=True, null=True)	
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    approval_flag_new = models.BooleanField(default=True)
    approval_flag_issue = models.BooleanField(default=False)
    approval_flag_receive = models.BooleanField(default=False)
    is_order_able = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.item}'
	

class PlacedOrderItems(models.Model):
    order_date = models.DateField(auto_now_add=True, auto_now=False)
    expected_delivery_date = models.DateField(null=True, blank=True)    
    ordered_quantity = models.PositiveIntegerField()    
    order_items = models.ForeignKey(ItemUnitInventory,on_delete=models.CASCADE,null=True) 
    vendors = models.ManyToManyField(ItemsVendorDetails)    

    def __str__(self):
        return f'{self.order_items }Order placed on {self.order_date}' 
	
class ReceiveOrderItems(models.Model):

    vendor = models.ForeignKey(ItemsVendorDetails,on_delete=models.CASCADE)
    order = models.ForeignKey(PlacedOrderItems,on_delete=models.CASCADE)
    actual_delivery_date = models.DateField(null=True,blank=True)
    received_quantity = models.PositiveIntegerField(default=0)
    order_balance = models.PositiveIntegerField(default=0)
    order_receive_flag = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.vendor} - {self.order.order_items}, order_date: {self.order.order_date}'
	
class OrderItemsBillImage(models.Model):

    item = models.ForeignKey(ReceiveOrderItems,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images')
    receive_timestamp = models.DateField(auto_now_add=True,auto_now=False)
    payment_method = models.CharField(max_length=100,null=True,blank=True)
    payment_date = models.DateField(auto_now_add=False, auto_now=True)
    transaction_detail = models.CharField(max_length=50,null=True,blank=True)
    remark = models.TextField(null=True,blank=True)
    image_two = models.ImageField(upload_to='images')
	
    def __str__(self):
        return f'{self.item} : {self.receive_timestamp}'
	

########### MEDICINE INVENTORY FINAL CODE #################

class AddMedicineList(models.Model):

	medicine_name = models.CharField(max_length=100)

	def __str__(self):
		return self.medicine_name
	
class AddPotencyList(models.Model):

	potency_name = models.CharField(max_length=50)

	def __str__(self):
		return self.potency_name
	
class MedicinesVendorDetails(models.Model):

	vendor_name = models.CharField(max_length=100)
	mobile_number = models.CharField(max_length=10)
	email = models.EmailField()
	address = models.TextField()

	def __str__(self):
		return self.vendor_name
	
class MedicinePotencyStock(models.Model):

    medicine = models.ForeignKey(AddMedicineList, on_delete=models.CASCADE)
    potency = models.ForeignKey(AddPotencyList,on_delete=models.CASCADE)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    branch = models.CharField(max_length=50,null=True,blank=True)	
    receive_quantity = models.IntegerField(default='0',blank=True, null=True)	
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    approval_flag_new = models.BooleanField(default=True)
    approval_flag_issue = models.BooleanField(default=False)
    approval_flag_receive = models.BooleanField(default=False)
    is_order_able = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.medicine} {self.potency}'

class PlacedOrderMedicine(models.Model):
    order_date = models.DateField(auto_now_add=True, auto_now=False)
    expected_delivery_date = models.DateField(null=True, blank=True)    
    ordered_quantity = models.PositiveIntegerField()    
    order_items = models.ForeignKey(MedicinePotencyStock,on_delete=models.CASCADE,null=True) 
    pack = models.CharField(max_length=100,null=True,default='30 ML')   
    vendors = models.ManyToManyField(MedicinesVendorDetails)
    added_by = models.CharField(max_length=50,null=True,blank=True)    

    def __str__(self):
        return f'{self.order_items }Order placed on {self.order_date}'

class ReceiveOrderMedicine(models.Model):

    vendor = models.ForeignKey(MedicinesVendorDetails,on_delete=models.CASCADE)
    order = models.ForeignKey(PlacedOrderMedicine,on_delete=models.CASCADE)
    actual_delivery_date = models.DateField(null=True,blank=True)
    received_quantity = models.PositiveIntegerField(default=0)
    order_balance = models.PositiveIntegerField(default=0)
    order_receive_flag = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    added_by = models.CharField(max_length=50,null=True,blank=True) 

    def __str__(self):
        return f'{self.vendor} - {self.order.order_items}, order_date: {self.order.order_date}'

class OrderMedicinesBillImage(models.Model):

    medicine = models.ForeignKey(ReceiveOrderMedicine,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images')
    receive_timestamp = models.DateField(auto_now_add=True,auto_now=False)
    payment_method = models.CharField(max_length=100,null=True,blank=True)
    payment_date = models.DateField(auto_now_add=False, auto_now=True)
    transaction_detail = models.CharField(max_length=50,null=True,blank=True)
    remark = models.TextField(null=True,blank=True)
    image_two = models.ImageField(upload_to='images')
	
    def __str__(self):
        return f'{self.medicine} : {self.receive_timestamp}' 

# class PlaceOrderDoctor(models.Model):

# 	order_date = models.DateField(auto_now_add=True, auto_now=False)
# 	expected_delivery_date = models.DateField(null=True, blank=True)
# 	branch = models.CharField(max_length=50,null=True)
# 	order_medicine =  models.CharField(max_length=255)
# 	potency = models.CharField(max_length=50)
# 	ordered_quantity = models.PositiveIntegerField()
# 	pack = models.CharField(max_length=100,null=True,default='30 ML')
# 	vendors = models.ForeignKey(MedicinesVendorDetails,on_delete=models.CASCADE)
# 	email_status = models.BooleanField(default=False)

# 	def save(self, *args, **kwargs):
# 		self.order_medicine = self.order_medicine.upper()
# 		self.potency = self.potency.upper()
# 		super(PlaceOrderDoctor, self).save(*args, **kwargs)

# 	def __str__(self):
# 		return f'{self.order_medicine} {self.potency} '
	

# class HomeoBook(models.Model):

# 	medicine_name = models.CharField(max_length=255)
# 	description = models.TextField()
# 	timestamp = models.DateField(auto_now_add=False, auto_now=True)

# 	def save(self, *args,**kwargs):
# 		self.medicine_name = self.medicine_name.upper()
# 		super(HomeoBook, self).save(*args,**kwargs)

# 	def __str__(self):
# 		return f'{self.medicine_name} {self.timestamp}'


class HomeBookMedicine(models.Model):
    medicine_name = models.CharField(max_length=255)
    description = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args,**kwargs):
        self.medicine_name = self.medicine_name.upper()
        super(HomeBookMedicine, self).save(*args,**kwargs)

    def __str__(self):
        return self.medicine_name
	
class HomeBookDisease(models.Model):
    disease_name = models.CharField(max_length=255)
    description = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args,**kwargs):
        self.disease_name = self.disease_name.upper()
        super(HomeBookDisease, self).save(*args,**kwargs)

    def __str__(self):
        return self.disease_name
	
class HomeBookRedline(models.Model):
    redline_symptoms = models.CharField(max_length=255)
    description = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args,**kwargs):
        self.redline_symptoms = self.redline_symptoms.upper()
        super(HomeBookRedline, self).save(*args,**kwargs)

    def __str__(self):
        return self.redline_symptoms
	
class AssignTask(models.Model):

	task = models.TextField()
	assign_To = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to=Q(receptionist__isnull=False) | Q(hr__isnull=False),null=True)
	created_at = models.DateField(auto_now_add=True)
	completed = models.BooleanField(default=False)

	def __str__(self):
		return self.task
	

class LeaveRequest(models.Model):

	staff = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to=Q(receptionist__isnull=False) | Q(hr__isnull=False),null=True)
	start_date = models.DateField()
	end_date = models.DateField()
	reason = models.TextField()
	is_approved = models.BooleanField(default=False)
	duration = models.PositiveIntegerField(null=True, blank=True)

	def __str__(self):
		return f'{self.staff} :{self.reason}'
	
	def save(self, *args, **kwargs):
		if self.start_date and self.end_date:
			delta = self.end_date - self.start_date
			self.duration = delta.days + 1
		super(LeaveRequest, self).save(*args, **kwargs)

