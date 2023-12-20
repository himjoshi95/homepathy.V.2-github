from django import forms
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget
from .models import *

class QuoteForm(forms.Form):
    test = forms.CharField(max_length=200,
		widget=forms.TextInput(
			attrs={'class' : 'form-control',  'placeholder' : 'Enter Name of Disease', 'aria-lable' : 'Dieases', 'aria-describedly' : 'add-btn'}))

    cause = forms.CharField(max_length= 400,
             widget=forms.TextInput(
			attrs={'class' : 'form-control',  'placeholder' : 'Enter Discription ', 'aria-lable' : 'Discription ', 'aria-describedly' : 'add-btn'}))

###
#class signForm(forms.Form):
  # text = forms.CharField(max_length=200,
	#	widget=forms.TextInput(
		#	attrs={'class' : 'form-control',  'placeholder' : 'question ', 'aria-lable' : 'Dieases', 'aria-describedly' : 'add-btn'}))
  # signature= JSignatureField(widget=JSignatureWidget(jsignature_attrs={'color': '#CCC'}))
###
class SignatureForm(forms.ModelForm):
  signature = JSignatureField()
  class Meta:
    model = JSignatureModel
    fields = ['name','signature']
    exclude = []
    widget = {'height':10}


class ContentsForm(forms.ModelForm):
  class Meta :
    model = Contents
    fields = ['name']
class ItemForm(forms.ModelForm):
  class Meta :
    model = Item 
    fields = ['name','head1','head2']



class Gnm_SbsForm(forms.Form):
    organs = forms.CharField(max_length=200,
		widget=forms.TextInput(
			attrs={'class' : 'form-control',  'placeholder' : 'Enter Name of Organ', 'aria-lable' : 'Organ', 'aria-describedly' : 'add-btn'}))

    conflicts = forms.CharField(max_length= 500,
             widget=forms.TextInput(
			attrs={'class' : 'form-control',  'placeholder' : 'Enter Biological Conflicts ', 'aria-lable' : 'Conflicts ', 'aria-describedly' : 'add-btn'}))
    
from jsignature.forms import JSignatureField
# class ExampleForm(forms.Form):
#     signature = JSignatureField()
#     patient = models.ChoiceField()

class ExampleForm(forms.ModelForm):
  signature = JSignatureField()

  class Meta:
    model = ExampleModel
    fields = '__all__'
    labels = {'signature': '','signature_date': ''}
    widgets = {'signature_date': forms.HiddenInput(),'patient':forms.HiddenInput()}

class PriceForm(forms.ModelForm):

  new_case = forms.IntegerField(widget=forms.TextInput())
  seven_days = forms.IntegerField(widget=forms.TextInput())
  fifteen_days = forms.IntegerField(widget=forms.TextInput())
  twentyone_days = forms.IntegerField(widget=forms.TextInput())
  thirty_days = forms.IntegerField(widget=forms.TextInput())
  fortyfive_days = forms.IntegerField(widget=forms.TextInput())
  two_months = forms.IntegerField(widget=forms.TextInput())
  three_months = forms.IntegerField(widget=forms.TextInput())
  courier = forms.IntegerField(required=False,widget=forms.TextInput())
  class Meta:
    model = Price
    fields = '__all__'



# class Meta:
#         model = ImagesUpload
#         fields ="__all__"
#         labels = {'images': '', 'case': ''}        
#         widgets = {'case': forms.HiddenInput(),'images':forms.ClearableFileInput(attrs={"multiple":True})}

class CourierDetailsForm(forms.ModelForm):

  courier_amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Rs'}))
  class Meta:
    model = CourierDetails
    fields = '__all__'
    widgets = {'patient':forms.HiddenInput()}
    labels = {'patient': ' '}


class AddStaffForm(forms.ModelForm):

  class Meta:
    model = AddStaff
    fields = '__all__'