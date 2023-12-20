from django.contrib import admin

# Register your models here.
from DOCTER.models import *
admin.site.register(Quote)
admin.site.register(Docter)
admin.site.register(Prescription2)
admin.site.register(sign)
admin.site.register(JSignatureModel)
admin.site.register(Gnm_Sbs)
admin.site.register(Analysis)
admin.site.register(Medicine)
admin.site.register(Head1)
admin.site.register(Head2)
admin.site.register(Essence)
admin.site.register(Contents)
admin.site.register(Item)
admin.site.register(ExampleModel)

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display =  ['id','new_case','seven_days','fifteen_days','twentyone_days','thirty_days','fortyfive_days','two_months','three_months','courier']

@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ['id','date','collected_by','patient','cash','cash_amount','online','online_amount','paid_amount','transac_id','balance_flag']

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['id','patient','collected_by','balance_amt','previous_deal_date']

@admin.register(AddMedicine)
class AddMedicineAdmin(admin.ModelAdmin):
    list_display = ['id','name','potency','quantity','arrival_date']


@admin.register(CourierDetails)
class CourierDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','patient','courier_amount','address','date','email']

@admin.register(AddStaff)
class AddStaffAdmin(admin.ModelAdmin):
    list_display = ['id','name','staff_id','email','phone_number','join_date','role','branch','upload_image','upload_docs']

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['id','patient','diagnose','date']

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id','patient','month','consulting_fees','medicine_fees','date','date1','date2']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['id','patient','diagnose1','diagnose2','diagnose3','date1','date2','date3','date4','month']