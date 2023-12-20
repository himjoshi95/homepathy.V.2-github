from dataclasses import fields
from xml.parsers.expat import model
from django.forms import ModelForm
from django import forms
from .models import *
from datetime import datetime, timedelta
from ckeditor.widgets import CKEditorWidget
  

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class InvestigationForm(ModelForm):
    class Meta:
        model = InvestigationAdvised
        fields = '__all__'

class UltrasonographyForm(ModelForm):
    class Meta:
        model = Ultrasonography
        fields = '__all__'

class DopplerForm(ModelForm):
    class Meta:
        model = Doppler
        fields = '__all__'

class ObstetricsForm(ModelForm):
    class Meta:
        model = Obstetrics
        fields = '__all__'


class SonographyTypeForm(ModelForm):
    class Meta:
        model = SonographyType
        fields = '__all__'

class CTScanNewForm(ModelForm):
    class Meta:
        model = CTScanNew
        fields = '__all__'

class MRIScanNewForm(ModelForm):
    class Meta:
        model = MRIScanNew
        fields = '__all__'


class StockCreateForm(forms.ModelForm):
    
    class Meta:
        model = Stock
        fields = ['vendor','stock_name','quantity','stock_unit','branch_name','upload_stock_bill_image']
        labels = {'branch_name': ''}
        widgets = {'branch_name':forms.HiddenInput()}         

    def __init__(self,*args,**kwargs):
        self.category = kwargs.pop('cat',None)
        print("Self.cat",self.category,type(self.category))
        super(StockCreateForm,self).__init__(*args,**kwargs)
        self.fields['stock_name'].empty_label = "Please Select from the list"
        self.fields['vendor'].empty_label = "Please Select from the list"
        self.fields['upload_stock_bill_image'].error_messages = {'required': ''}
        if self.category == "Stock":
             self.fields['vendor'].queryset=AddVendorStock.objects.filter(vendor_category__category=self.category)
        self.fields['stock_name'].queryset = VendorStockProduct.objects.none()

        if 'vendor' in self.data:
            try:
                vendor_id = int(self.data.get('vendor'))
                self.fields['stock_name'].queryset = VendorStockProduct.objects.filter(vendor_id=vendor_id)
            except (ValueError, TypeError):
                 pass  # invalid input from the client; ignore and fallback to empty City queryset


class StockSearchForm(forms.ModelForm):
	
	class Meta:
	   model = Stock
	   fields = ['stock_name']

	def __init__(self,*args,**kwargs):
		super(StockSearchForm,self).__init__(*args,**kwargs)
		self.fields['stock_name'].empty_label = "Please Select from the list"

class StockIssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity','stock_unit']
                

class StockReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity','stock_unit','upload_stock_bill_image']
		

class StockReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level','stock_unit']

class AddStockNameForm(forms.ModelForm):
     
     class Meta:
          model = StockName
          fields = ['name']
          widgets = {'name':forms.TextInput(attrs={'placeholder': 'Mention here'})}

     def clean_name(self):
        name = self.cleaned_data.get('name').title()
        if not name:
            raise forms.ValidationError('This field is required')
        for instance in StockName.objects.all():
            if instance.name == name:
                 raise forms.ValidationError(str(name) + ' is already created')
        return name

class AddMedicineHRForm(forms.ModelForm):

     class Meta:
          model=AddMedicineHR
          fields = ['medicine_name']
          widgets = {'medicine_name':forms.TextInput(attrs={'placeholder': 'Mention here'})}


class AddPotencyHRForm(forms.ModelForm):

     class Meta:
          model=AddPotencyHR
          fields = ['potency_name']
          widgets = {'potency_name':forms.TextInput(attrs={'placeholder': 'Mention here'})}


class MedicineStockListCreateForm(forms.ModelForm):
     
     class Meta:
          model = MedicineStockList
          fields = ['vendor','medicine','potency','quantity','branch']
          labels = {'branch': ''}
          widgets = {'branch':forms.HiddenInput()}
    
     def __init__(self,*args,**kwargs):
        self.category = kwargs.pop('cat',None)
        # print("Self.cat",self.category,type(self.category))
        super(MedicineStockListCreateForm,self).__init__(*args,**kwargs)
        self.fields['vendor'].empty_label = "Please Select from the list"
        self.fields['medicine'].empty_label = "Please Select from the list"
        self.fields['potency'].empty_label = "Please Select from the list"
        # self.fields['upload_medicine_bill_image'].error_messages = {'required': ''}
  
        if self.category == "Medicine":
             self.fields['vendor'].queryset=AddVendorStock.objects.filter(vendor_category__category=self.category)
        self.fields['medicine'].queryset = VendorMedicine.objects.none()

        if 'vendor' in self.data:
            try:
                vendor_id = int(self.data.get('vendor'))
                self.fields['medicine'].queryset = VendorMedicine.objects.filter(vendor_id=vendor_id)
            except (ValueError, TypeError):
                 pass
              


class MedicineStockListSearchForm(forms.ModelForm):
     
     class Meta:
          model = MedicineStockList
          fields = ['medicine','potency']

     def __init__(self,*args,**kwargs):
          super(MedicineStockListSearchForm,self).__init__(*args,**kwargs)
          self.fields['medicine'].empty_label = "Please Select from the list"
          self.fields['potency'].empty_label = "Please Select from the list"

class MedicineIssueHRForm(forms.ModelForm):
	class Meta:
		model = MedicineStockList
		fields = ['issue_quantity']
          
class MedicineReceiveHRForm(forms.ModelForm):
	class Meta:
		model = MedicineStockList
		fields = ['receive_quantity']
          
class MedicineReorderLevelHRForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']
          


# ADD VENDOR FORM FOR STOCK

class AddVendorStockForm(forms.ModelForm):
     
     class Meta:
          model= AddVendorStock
          fields = '__all__'
          widgets = {'vendor_name':forms.TextInput(attrs={'placeholder': 'Enter Name here'}),
                     'mobile_number':forms.TextInput(attrs={'placeholder': 'Enter Mobile Number here'}),
                     'email':forms.TextInput(attrs={'placeholder': 'Enter Email here'}),
                     'address':forms.Textarea(attrs={'placeholder': "Enter Vendor's full Address here"})}
     def __init__(self,*args,**kwargs):
        super(AddVendorStockForm,self).__init__(*args,**kwargs)
        self.fields['vendor_category'].empty_label = "Please Select the category from the list"

class VendorStockSearchForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(VendorStockSearchForm, self).__init__(*args, **kwargs)
		self.fields['vendor_name'].required = False
		self.fields['mobile_number'].required = False
	
	class Meta:
	   model = AddVendorStock
	   fields = ['vendor_name','mobile_number']
	   widgets = {'vendor_name':forms.TextInput(attrs={'placeholder': 'Mention here'}),'mobile_number':forms.TextInput(attrs={'placeholder': 'Mention here'})}


class VendorStockProductForm(forms.ModelForm):

	class Meta:
		model = VendorStockProduct
		fields = "__all__"
		widgets = {'vendor':forms.HiddenInput()}

	def __init__(self,*args,**kwargs):
         self.category= kwargs.pop('cat',None)
        #  print("self",self.category,type(self.category),str(self.category))
         super(VendorStockProductForm,self).__init__(*args,**kwargs)
         self.fields['product_name'].empty_label = "Please Select from the list"
         if str(self.category) == 'Stock':            
            self.fields['product_name'].queryset = StockName.objects.all()

         else:
              self.fields['product_name'].queryset = StockName.objects.none()


class VendorMedicineForm(forms.ModelForm):

	class Meta:
		model = VendorMedicine
		fields = "__all__"
		widgets = {'vendor':forms.HiddenInput()}

	def __init__(self,*args,**kwargs):
         self.category= kwargs.pop('cat',None)
        #  print("self",self.category,type(self.category),str(self.category))
         super(VendorMedicineForm,self).__init__(*args,**kwargs)
         self.fields['medicine'].empty_label = "Please Select from the list"
         self.fields['potency'].empty_label = "Please Select from the list"
         if str(self.category) == 'Medicine':            
            self.fields['medicine'].queryset = AddMedicineHR.objects.all()
            self.fields['potency'].queryset = AddPotencyHR.objects.all()

         else:
              self.fields['medicine'].queryset = AddMedicineHR.objects.none()
              self.fields['potency'].queryset = AddPotencyHR.objects.none()

          

class PlaceOrderForm(forms.ModelForm):
     
    def __init__(self,*args,**kwargs):
        self.vendor_id = kwargs.pop('vendor_id',None)
        # print('forms',self.vendor_id)
        super(PlaceOrderForm,self).__init__(*args,**kwargs)
        self.fields['stock_order'].empty_label = "Please select from the list"
        self.fields['stock_order'].queryset = Stock.objects.filter(vendor__id =self.vendor_id)
     
    class Meta:
        model = PlaceOrderStock
        fields = '__all__'
        widgets = {'email_placed_flag':forms.HiddenInput(),'order_received_flag':forms.HiddenInput(),'order_delivery_date': forms.DateInput(attrs={'type': 'date'})}


class PlacedOrderStockSearchFrom(forms.ModelForm):
     
    class Meta:
        model = PlaceOrderStock
        fields = ['stock_order']

    def __init__(self,*args,**kwargs):
        self.vendor_id = kwargs.pop('vendor_id',None)
        super(PlacedOrderStockSearchFrom,self).__init__(*args,**kwargs)
        self.fields['stock_order'].empty_label = "Please Select from the list"
        if self.vendor_id:
            self.fields['stock_order'].queryset = Stock.objects.filter(vendor__id =self.vendor_id)

class PlaceMedicineOrderForm(forms.ModelForm):
     
    def __init__(self,*args,**kwargs):
        self.vendor_id = kwargs.pop('vendor_id',None)
        super(PlaceMedicineOrderForm,self).__init__(*args,**kwargs)
        self.fields['vendor_order'].empty_label = "Please select from the list"
        self.fields['medicine_order'].empty_label = "Please select from the list"
        self.fields['potency'].empty_label = "Please select from the list"
        # self.fields['medicine_order'].queryset = MedicineStockList.objects.filter(vendor__id =self.vendor_id)
        self.fields['vendor_order'].queryset = AddVendorStock.objects.filter(vendor_category__category="Medicine")


    class Meta:
        model = PlaceOrderMedicineNew
        fields = '__all__'
        widgets = {'email_placed_flag':forms.HiddenInput(),'order_received_flag':forms.HiddenInput(),'order_delivery_date': forms.DateInput(attrs={'type': 'date'})}


class CustomSelectMultiple(forms.SelectMultiple):
    def __init__(self, attrs=None):
        attrs = {'class': 'custom-select-multiple', 'style': 'width: 100%;'}  # Set your desired width here
        super().__init__(attrs=attrs)

class OrderMedicineOneForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
         super(OrderMedicineOneForm,self).__init__(*args,**kwargs)
        #  self.fields['vendor_order'].empty_label = "Select"
         self.fields['vendor_order'].queryset = AddVendorStock.objects.filter(vendor_category__category="Medicine")
         mystyle = {"style":"width:300px;"}
         self.fields['vendor_order'].widget.attrs = mystyle
         initial_date = datetime.now() + timedelta(days=7)
         self.fields['order_delivery_date'].initial = initial_date.date()
         

    class Meta:
         model = PlaceOrderMedicineOne
         fields = '__all__'
         widgets = {'order_delivery_date': forms.DateInput(attrs={'type': 'date'})}


class OrderMedicineItemForm(forms.ModelForm):
    class Meta:
         model = OrderMedicineItem
         fields = ['order_received']

class ForAppointmentHomePageForm(forms.ModelForm):
     class Meta:
          model = ForAppointmentHomePage
          fields = '__all__'
         

############# ITEMS INVENTORY FINAL CODE ############### 

class AddItemsSearchForm(forms.Form):
    item = forms.ModelChoiceField(label="",
        queryset=AddItems.objects.all(),  # Queryset to include all medicines
        empty_label="Select Items",    # Optional: Display a default empty label
        required=False 
    )     

class AddUnitSearchForm(forms.Form):
    unit = forms.ModelChoiceField(label="",
        queryset=AddUnits.objects.all(),  # Queryset to include all medicines
        empty_label="Select units",    # Optional: Display a default empty label
        required=False 
    )   

class ItemsVendorDetailsForm(forms.ModelForm):

    class Meta:
        model = ItemsVendorDetails
        fields= '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemsVendorDetailsForm, self).__init__(*args, **kwargs)
        # Set placeholders for form fields
        self.fields['vendor_name'].widget.attrs.update({'placeholder': 'Vendor Name'})
        self.fields['mobile_number'].widget.attrs.update({'placeholder': 'Mobile Number'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Address'})

class ItemUnitInventoryCreateForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(ItemUnitInventoryCreateForm,self).__init__(*args,**kwargs)        
        self.fields['item'].empty_label = "Select Here"
        self.fields['unit'].empty_label = "Select Here"

    class Meta:
        model = ItemUnitInventory
        fields = ['item','unit','branch','receive_quantity']
        # labels = {'branch': ''}       
        widgets = {
            'receive_quantity': forms.NumberInput(attrs={'placeholder': 'Enter receive quantity'}),'branch':forms.HiddenInput() }
      

class ReorderLevelItemInventoryForm(forms.ModelForm):

    class Meta:
        model = ItemUnitInventory
        fields = ['reorder_level']

class IssueItemsInventoryForm(forms.ModelForm):
    
    class Meta:
         model = ItemUnitInventory
         fields = ['issue_quantity']


class ItemUnitInventorySearchForm(forms.Form):
     
    item = forms.ModelChoiceField(label="Item",
        queryset=AddItems.objects.all(),  # Queryset to include all medicines
        empty_label="Select Item",    # Optional: Display a default empty label
        required=False 
    )

class PlacedOrderItemsForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(PlacedOrderItemsForm,self).__init__(*args,**kwargs)
        initial_date = datetime.now() + timedelta(days=7)
        self.fields['expected_delivery_date'].initial = initial_date.date()

    class Meta:
        model = PlacedOrderItems
        fields = [ 'order_items','vendors','ordered_quantity','expected_delivery_date', 'ordered_quantity']
        widgets = {'expected_delivery_date': forms.DateInput(attrs={'type': 'date'})}
     
    
################# MEDICINES INVENTORY NEW CODE #############################

class AddMedicineSearchForm(forms.Form):
    medicine = forms.ModelChoiceField(label="",
        queryset=AddMedicineList.objects.all(),  # Queryset to include all medicines
        empty_label="Select Medicine",    # Optional: Display a default empty label
        required=False 
    )     

class AddPotencySearchForm(forms.Form):
    potency = forms.ModelChoiceField(label="",
        queryset=AddPotencyList.objects.all(),  # Queryset to include all medicines
        empty_label="Select Potency",    # Optional: Display a default empty label
        required=False 
    )

class MedicinesVendorDetailsForm(forms.ModelForm):

    class Meta:
        model = MedicinesVendorDetails
        fields= '__all__'

    def __init__(self, *args, **kwargs):
        super(MedicinesVendorDetailsForm, self).__init__(*args, **kwargs)
        # Set placeholders for form fields
        self.fields['vendor_name'].widget.attrs.update({'placeholder': 'Vendor Name'})
        self.fields['mobile_number'].widget.attrs.update({'placeholder': 'Mobile Number'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Address'})

class MedicinePotencyStockCreateForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(MedicinePotencyStockCreateForm,self).__init__(*args,**kwargs)        
        self.fields['medicine'].empty_label = "Select Here"
        self.fields['potency'].empty_label = "Select Here"

    class Meta:
        model = MedicinePotencyStock
        fields = ['medicine','potency','branch','receive_quantity']
        labels = {'branch': ''}
        widgets = {
            'receive_quantity': forms.NumberInput(attrs={'placeholder': 'Enter receive quantity'}),'branch':forms.HiddenInput() }

class MedicinePotencyStockSearchForm(forms.Form):
    medicine = forms.ModelChoiceField(label="Medicine",
        queryset=AddMedicineList.objects.all(),  # Queryset to include all medicines
        empty_label="Select Medicine",    # Optional: Display a default empty label
        required=False 
    )
    potency =  forms.ModelChoiceField(label="Potency",
        queryset=AddPotencyList.objects.all(),    # Queryset to include all potencies
        empty_label="Select Potency",     # Optional: Display a default empty label
        required=False
    ) 
    
class ReorderLevelMedicineForm(forms.ModelForm):

    class Meta:
        model = MedicinePotencyStock
        fields = ['reorder_level']

class IssueMedicinePotencyStockForm(forms.ModelForm):

    class Meta:
        model = MedicinePotencyStock
        fields = ['issue_quantity']


class PlacedOrderMedicineForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(PlacedOrderMedicineForm,self).__init__(*args,**kwargs)
        initial_date = datetime.now() + timedelta(days=7)
        self.fields['expected_delivery_date'].initial = initial_date.date()
        self.fields['order_items'].empty_label = "Select Here"
        self.fields['ordered_quantity'].widget.attrs.update({'placeholder': 'Mention Order Quantity'})

    class Meta:
        model = PlacedOrderMedicine
        fields = [ 'order_items','pack','vendors','ordered_quantity','expected_delivery_date']
        widgets = {'expected_delivery_date': forms.DateInput(attrs={'type': 'date'})}


# class PlaceOrderDoctorForm(forms.ModelForm):

#     BRANCH_CHOICES = (
#          ('', 'Select Here'),
#         ('Dombivali', 'Dombivali'),
#         ('Mulund', 'Mulund'),
#         # Add more branches as needed
#     )

#     PACK_CHOICES = (
#         ('30 ML', '30 ML'),
#         ('60 ML', '60 ML'),
#         # Add more pack options as needed
#     )
#     branch = forms.ChoiceField(choices=BRANCH_CHOICES, label='Branch')
#     pack = forms.ChoiceField(choices=PACK_CHOICES, label='Pack')

#     def __init__(self,*args,**kwargs):
#         super(PlaceOrderDoctorForm,self).__init__(*args,**kwargs)
#         initial_date = datetime.now() + timedelta(days=7)
#         self.fields['expected_delivery_date'].initial = initial_date.date()
#         self.fields['vendors'].empty_label = "Select Here"
         
     
#     class Meta:
#          model= PlaceOrderDoctor
#          fields = '__all__'
#          widgets = {'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),'ordered_quantity': forms.NumberInput(attrs={'placeholder': 'Enter receive quantity'}),
#                     'order_medicine': forms.TextInput(attrs={'placeholder': 'Enter Order Medicine'}),'potency': forms.TextInput(attrs={'placeholder': 'Enter Potency'}),
#                     'email_status':forms.HiddenInput()}
    

# class HomeoBookForm(forms.ModelForm):

#     # def __init__(self,*args,**kwargs):
#     #     super(HomeoBookForm,self).__init__(*args,**kwargs)
#     #     self.fields['medicine_name'].required = False
#     #     self.fields['description'].required = False

#     class Meta:
#          model = HomeoBook
#          fields = '__all__'
#          widgets = {'medicine_name':forms.TextInput(attrs={'placeholder': 'Enter Medicine Name'}),
#                     'description': forms.Textarea(attrs={'placeholder': 'Enter Description'})}     	



class HomeoBookMedicineForm(forms.ModelForm):
    class Meta:
        model = HomeBookMedicine
        fields = ['medicine_name', 'description']
        widgets = {
            'description': CKEditorWidget(),'medicine_name':forms.TextInput(attrs={'placeholder': 'Enter Medicine Name'}),
            'description':forms.Textarea(attrs={'placeholder': 'Enter Description'})
        }

class HomeoBookDiseaseForm(forms.ModelForm):
    class Meta:
        model = HomeBookDisease
        fields = ['disease_name', 'description']
        widgets = {
            'description': CKEditorWidget(),'disease_name':forms.TextInput(attrs={'placeholder': 'Enter Disease Name'}),
            'description':forms.Textarea(attrs={'placeholder': 'Enter Description'})
        }

class HomeoBookRedlineForm(forms.ModelForm):
    class Meta:
        model = HomeBookRedline
        fields = ['redline_symptoms', 'description']
        widgets = {
            'description': CKEditorWidget(),'redline_symptoms':forms.TextInput(attrs={'placeholder': 'Enter Symptoms'}),
            'description':forms.Textarea(attrs={'placeholder': 'Enter Description'})
        }

class AssignTaskForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(AssignTaskForm,self).__init__(*args,**kwargs)
        self.fields['assign_To'].empty_label = "Select Staff Here "
     
    class Meta:
         model = AssignTask
         fields = ['task' , 'assign_To']
         widgets = {'task':forms.Textarea(attrs={'placeholder': 'Enter Task Description'})}


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['staff','start_date', 'end_date','reason']
        widgets = {'start_date':forms.DateInput(attrs={'type': 'date'}),'end_date':forms.DateInput(attrs={'type': 'date'}),
                   'staff':forms.HiddenInput()}