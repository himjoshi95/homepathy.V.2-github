from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.
admin.site.register(Question)
admin.site.register(Appetite)
admin.site.register(QAnswar)
admin.site.register(Answars)

@admin.register(NewCase)
class NewCaseAdmin(admin.ModelAdmin):
    list_display = ['id','patient']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category']

@admin.register(Question1)
class Question1Admin(admin.ModelAdmin):
    list_display = ['id','category','question']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = ['id','date','patient','question','last_diagnose','duration','flag']

admin.site.register(JSModel)

admin.site.register(PersonalHabit)
admin.site.register(InFood)
admin.site.register(MentalCausative)
admin.site.register(PersonalityCharacter)
admin.site.register(MiasmOne)
admin.site.register(RubricOne)
admin.site.register(Diseases)
admin.site.register(PastHistory)
admin.site.register(PersonalHabitNew)
admin.site.register(Complain)
admin.site.register(PresentComplaintsNew)
admin.site.register(NewCaseModel)
admin.site.register(FamilyMedicalHistory)
admin.site.register(MentalCausativeNewone)
admin.site.register(MentalCausativeRecord)
admin.site.register(FamilyMedicalComplain)
admin.site.register(PatientHistoryNEW)
admin.site.register(MentalPersonalityNewOne)
admin.site.register(MentalPersonalityRecord)
admin.site.register(MiasmNewOne)
admin.site.register(MiasmRecords)
admin.site.register(ThermalReactionNewOne)
admin.site.register(ThermalReactionRecords)

class MedicineCreateAdmin(admin.ModelAdmin):
   list_display = ['medicine','potency','quantity','arrival_date','last_updated']
   form = MedicineCreateForm
   list_filter = ['medicine']
   search_fields = ['medicine','potency' , 'quantity']

admin.site.register(MedicineStock,MedicineCreateAdmin)