from django.contrib import admin

# Register your models here.
from PATIENT.models import *
admin.site.register(Patient)
admin.site.register(Invoice)
admin.site.register(MultipleUploadImages)
admin.site.register(PatientImages)


@admin.register(ImagesUpload)
class ImagesUploadAdmin(admin.ModelAdmin):
    list_display = ['id','case','images','date']

@admin.register(PrescriptionOldUpload)
class PrescriptionOldUploadAdmin(admin.ModelAdmin):
    list_display = ['id','patient','images']

@admin.register(NewCasePaperUpload)
class NewCasePaperUpload(admin.ModelAdmin):
    list_display = ['id','patient','images']