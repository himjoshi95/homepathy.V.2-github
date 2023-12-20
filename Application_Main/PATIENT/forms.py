from django import forms
from .models import ImagesUpload, Patient ,PrescriptionOldUpload,NewCasePaperUpload
from .models import Patient
from django.forms import TextInput

class ImagesUploadForm(forms.ModelForm):   

    class Meta:
        model = ImagesUpload
        fields ="__all__"
        labels = {'images': '', 'case': ''}
        widgets = {'case': forms.HiddenInput()}
        # widgets = {'case': forms.HiddenInput(),'images':forms.ClearableFileInput(attrs={"multiple":True})}

   
class PrescriptionOldUploadForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(PrescriptionOldUploadForm,self).__init__(*args,**kwargs)
        self.fields['patient'].empty_label = "Select Here"
        
    class Meta:
        model = PrescriptionOldUpload        
        fields = '__all__'
        labels = {'images': '','patient':'Case PaperNo.'}        
        # widgets = {'images':forms.ClearableFileInput(attrs={'multiple':True})}

class NewCasePaperUploadForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(NewCasePaperUploadForm,self).__init__(*args,**kwargs)
        self.fields['patient'].empty_label = "Select Here"
        patient_choices = [('', self.fields['patient'].empty_label)]
        patients = Patient.objects.all()
        for patient in patients:
            label = f"{patient.name} / {patient.case} / {patient.phone} (M)"
            patient_choices.append((patient.id, label))

        self.fields['patient'].choices = patient_choices

    class Meta:
        model = NewCasePaperUpload
        fields = '__all__'
        labels = {'images': '','patient':''}        
        # widgets = {'images':forms.ClearableFileInput(attrs={"multiple":True})}

class NewCasePaperUploadFormOne(forms.ModelForm):

    class Meta:
        model = NewCasePaperUpload
        fields = '__all__'
        labels = {'images': '','patient':'Case PaperNo.'}
        widgets = {'patient': forms.HiddenInput()}        
        # widgets = {'patient': forms.HiddenInput(),'images':forms.ClearableFileInput(attrs={"multiple":True})}