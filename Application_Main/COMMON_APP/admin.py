from django.contrib import admin
from .models import Article ,prescription
# Register your models here.
from .models import *
admin.site.register(Receptionist)
# admin.site.register(Appointment)
admin.site.register(HR)
admin.site.register(Article)
# admin.site.register(prescription)
admin.site.register(OtherPrescription)
admin.site.register(AddConsultationCharges)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id','docterid','patientid','time','status','date','stat','token','token1','email_flag','notification_flag','doctor_notification','medicine_flag']


@admin.register(prescription)
class prescription(admin.ModelAdmin):
    list_display = ['id','patientid','medicine','potency','date','durations','flag','diagnose','start_date','dose','note']

@admin.register(TokenUpdate)
class TokenUpdateAdmin(admin.ModelAdmin):
    list_display = ['id','token','consultancy']

@admin.register(ReceptionistDocs)
class ReceptionistDocsAdmin(admin.ModelAdmin):
    list_display = ['id','recep','date','images']

@admin.register(HRDocs)
class HRDocsAdmin(admin.ModelAdmin):
    list_display = ['id','hr','date','images']


admin.site.register(InvestigationAdvised)
admin.site.register(InvestigationRecords)
admin.site.register(Ultrasonography)
admin.site.register(UltrasonographyRecords)
admin.site.register(Doppler)
admin.site.register(DopplerRecords)
admin.site.register(Obstetrics)
admin.site.register(ObstetricRecords)
admin.site.register(SonographyType)
admin.site.register(SonographyTypeRecords)
admin.site.register(CTScanNew)
admin.site.register(CTScanNewRecords)
admin.site.register(MRIScanNew)
admin.site.register(MRIScanNewRecords)

admin.site.register(StockName)
admin.site.register(VendorCategory)
admin.site.register(AddVendorStock)
admin.site.register(VendorStockProduct)
admin.site.register(Stock)
admin.site.register(BillImageStock)
admin.site.register(AddMedicineHR)
admin.site.register(AddPotencyHR)
admin.site.register(VendorMedicine)
admin.site.register(MedicineStockList)
# admin.site.register(BillImageMedicine)
admin.site.register(PlaceOrderStock)
admin.site.register(PlaceOrderMedicine)

admin.site.register(PlaceOrderMedicineOne)
# @admin.register(PlaceOrderMedicineOne)
# class PlaceOrderMedicineOneAdmin(admin.ModelAdmin):
#     # list_display = ('id' , 'vendor_order', 'medicine_order', 'potency' , 'pack')
#     list_display = ('id')
admin.site.register(OrderMedicineItem)
admin.site.register(BillOrderMedicineImage)
admin.site.register(OurPortfolioImages)
admin.site.register(ForAppointmentHomePage)


### ITEMS INVENTORY #####

@admin.register(AddItems)
class AddItemsAdmin(admin.ModelAdmin):
    list_display = ('item_name',)

@admin.register(AddUnits)
class AddUnitsAdmin(admin.ModelAdmin):
    list_display = ('unit_name',)

admin.site.register(ItemsVendorDetails)

@admin.register(ItemUnitInventory)
class ItemUnitInventoryAdmin(admin.ModelAdmin):
    list_display = ('item','is_order_able','unit','quantity', 'branch', 'receive_quantity', 'issue_quantity', 'reorder_level', 'last_updated', 'timestamp', 'approval_flag_new','approval_flag_issue','approval_flag_receive')

admin.site.register(PlacedOrderItems)
admin.site.register(ReceiveOrderItems)
admin.site.register(OrderItemsBillImage)


###### MEDICINES INVENTORY NEW CODE ############

admin.site.register(AddMedicineList)
admin.site.register(AddPotencyList)
admin.site.register(MedicinesVendorDetails)

@admin.register(MedicinePotencyStock)
class MedicinePotencyStockAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'is_order_able','potency', 'quantity', 'branch', 'receive_quantity', 'issue_quantity', 'reorder_level', 'last_updated', 'timestamp', 'approval_flag_new','approval_flag_issue','approval_flag_receive')

admin.site.register(PlacedOrderMedicine)
admin.site.register(ReceiveOrderMedicine)
admin.site.register(OrderMedicinesBillImage)
# admin.site.register(PlaceOrderDoctor)

# admin.site.register(HomeoBook)
admin.site.register(HomeBookMedicine)
admin.site.register(HomeBookDisease)
admin.site.register(HomeBookRedline)

admin.site.register(AssignTask)
admin.site.register(LeaveRequest)

admin.site.register(HealthAssessment)