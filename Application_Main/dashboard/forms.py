from django import forms
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget
from .models import *



class JSForm(forms.ModelForm):
  signature = JSignatureField(null=True,blank=True)

  class Meta:
    model = JSModel
    fields = '__all__'
    labels = {'signature': '','signature_date': ''}
    widgets = {'signature_date': forms.HiddenInput(),'question':forms.HiddenInput(),'patient':forms.HiddenInput()}

class MiasmOneForm(forms.ModelForm):

  class Meta:   

    model = MiasmOne
    fields = '__all__'

class NewCaseForm(forms.ModelForm):
  signature = JSignatureField(null=True,blank=True)

  class Meta:
    model = NewCaseModel
    fields = '__all__'
    labels = {'signature': '','signature_date': ''}
    widgets = {'signature_date': forms.HiddenInput(),'category': forms.HiddenInput(),'patient':forms.HiddenInput()}

class MedicineCreateForm(forms.ModelForm):
   
   class Meta:
     model = MedicineStock
     fields = ['medicine','potency', 'quantity']

   def clean_medicine(self):
    medicine = self.cleaned_data.get('medicine')
    if not medicine:
        raise forms.ValidationError('This field is required')
    
    return medicine

   def clean_potency(self):
     potency = self.cleaned_data.get('potency')     
     if not potency:
       raise forms.ValidationError('This field is required')
     return potency 

class MedicineSearchForm(forms.ModelForm):
   class Meta:
     model = MedicineStock
     fields = ['medicine'] 

class MedicineUpdateForm(forms.ModelForm):
	class Meta:
		model = MedicineStock
		fields = ['medicine', 'potency','quantity',]

class MedicineIssueForm(forms.ModelForm):
    class Meta:
      model = MedicineStock
      fields = ['issue_quantity']

class MedicineReceiveForm(forms.ModelForm):
	class Meta:
		model = MedicineStock
		fields = ['receive_quantity'] 
                
class MedicineReorderLevelForm(forms.ModelForm):
	class Meta:
		model = MedicineStock
		fields = ['reorder_level']
        

class PresentComplaintsForm(forms.Form):
    complaint = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Complaint'}))
    duration = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Number for Duration'}))
    duration_suffix = forms.ChoiceField(
        choices=[
            ('', 'Please Select Days / Weeks / Months / Years'),
            ('Days', 'Days'),
            ('Week', 'Week'),
            ('Months', 'Months'),
            ('Year', 'Year'),
        ]
    )
    remark = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Enter Remark if any'}))  # Assuming remark is optional


class PatientHistoryForm(forms.Form):
    
    complaint = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Complaint'}))
    last_diagnosed = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. : 2,4,5 ..'}))
    last_suffix = forms.ChoiceField(
        choices=[
            ('', 'Please Select Days / Weeks / Months / Years'),
            ('Days Back', 'Days Back'),
            ('Week Back', 'Week Back'),
            ('Months Back', 'Months Back'),
            ('Year Back', 'Year Back'),
            ('Years of Age', 'Years of Age'),
        ]
    )
    duration = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'e.g. : 2,4,5 ..'}))
    duration_suffix =  forms.ChoiceField(
        choices=[
            ('', 'Please Select Days / Weeks / Months / Years'),
            ('Days', 'Days'),
            ('Week', 'Week'),
            ('Months', 'Months'),
            ('Year', 'Year'),
        ],
        required=False
    )
    remark = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Enter Remark if any'}))
    
class FamilyMedicalHistoryForm(forms.Form):
    
    relation = forms.ChoiceField(
        choices=[
            ('', 'Please Select the Relation'),
            ('Paternal Grand Father', 'Paternal Grand Father'),
            ('Paternal Grand Mother', 'Paternal Grand Mother'),
            ('Maternal Grand Father', 'Maternal Grand Father'),
            ('Maternal Grand Mother', 'Maternal Grand Mother'),
            ('Mother', 'Mother'),
            ('Father', 'Father'),
            ('Sister', 'Sister'),
            ('Brother', 'Brother'),
        ]        
    )
    list_of_disease = forms.ModelMultipleChoiceField(queryset=FamilyMedicalComplain.objects.all())
    any_other = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Enter if any other'}))
    dead_alive = forms.ChoiceField(
        choices=[
            ('', 'Please Select '),
            ('Alive', 'Alive'),
            ('Dead', 'Dead'),
            
        ]        
    )
    age = forms.IntegerField()
    
