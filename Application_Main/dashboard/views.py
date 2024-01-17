from re import template
from django.shortcuts import render , redirect

from . models import *
from .forms import *
from django.http import HttpResponse
from  COMMON_APP.models import Appointment,prescription,Stock
from datetime import date
from PATIENT.models import Patient,ImagesUpload
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from DOCTER.forms import PriceForm
from django.contrib import messages
from DOCTER.models import Diagnosis,Bill,Certificate,AddMedicine,AddStaff,Amount,Balance,CourierDetails,ExampleModel,Price
from django.db.models import Q
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from datetime import date
from  .utils import *
from jsignature.utils import draw_signature
from django.db.models.functions import Lower
from django.views.decorators.csrf import csrf_exempt
from COMMON_APP.models import Receptionist,HR,ReceptionistDocs,HRDocs
from django.utils.decorators import method_decorator
from datetime import date





# Create your views here.
@csrf_exempt
def index(request):

    status = False
    if request.user:
        status= request.user
        # print('status----',status)

    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
    
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())
    
    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()

    return render(request,'index_new_adjust.html',{'status':status,'user':"D",'unsend_mail_count': unsent_mail_count,'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
								'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
								'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,'date':date.today()})


case_id = 0
@csrf_exempt
def addpatient(request):    
    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':        
        p_id = request.POST['patient']
        diagnose = request.POST['diagnose']
        patient = Patient.objects.get(id=p_id) 
        med_name = request.POST['med_name'] 
        obj = Diagnosis(patient=patient,diagnose=diagnose.title(),med_name=med_name.title())  
        messages.success(request,'Patient Added Successfully. Click on Next to Continue') 
        obj.save()
        global case_id
        case_id = request.POST['patient']    
        return redirect('addpatient')
       
    data = Patient.objects.all()
    
    return render(request,'dashboard/templates/addpatient_new_adjust.html',{'status':status,'user':"D",'data':data,'case_id':case_id})

@csrf_exempt
def bills(request,id):
    status = False
    if request.user:
        status=request.user
    
    if request.method == 'POST':
        p_id = id
        
        if request.POST['consulting_fees']:
            consulting_fees = request.POST['consulting_fees']
        else:
             consulting_fees = 0         
        medicine_fees = request.POST['medicine_fees']
        patient = Patient.objects.get(id=p_id)
        date1 = request.POST['date1']
        date2 = request.POST['date2']
        obj = Bill(patient=patient,consulting_fees=consulting_fees,medicine_fees=medicine_fees,date1=date1,date2=date2)              
        obj.save()                             
        messages.success(request,'Click below to Generate Bill') 
        return HttpResponseRedirect(reverse('bills',  kwargs={'id': p_id}))  
       
    
    data = Patient.objects.all()    
    
    return render(request,'dashboard/templates/addbills_new_adjust.html',{'status':status,'user':"D",'data':data,'id1':id})    

@csrf_exempt
def bill_pdf(request,id):

    if id == 0:
        return HttpResponse("Please select Case ID")
    else:
        date1 = date.today()    
        obj = Diagnosis.objects.filter(patient_id=id,date=date1)    
        obj_diagnose = [o.diagnose for o in obj]
        obj_med_name = [m.med_name for m in obj]
        print("obj_med------",obj_med_name)    
        obj2 = Bill.objects.filter(patient_id=id).last()
       
        response = HttpResponse(content_type = 'application/pdf')
        response['Content-Disposition'] = 'filename="Bill.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        letter_head = "./dashboard/document/bill.jpg"
        p.drawImage(letter_head,0,0,width=600,height=880)
        p.setFont("Helvetica", 18)
        # print("gender---?",obj2.patient.gender)
        if obj2.patient.gender == 'Male':
            p.drawString(80, 480,"Mr "+obj2.patient.name)
        else:
            p.drawString(80, 480,"Mrs/Miss "+obj2.patient.name)

        p.setFont("Helvetica", 12)
        
        p.drawString(300, 500,"From: ")
        p.setFont("Helvetica", 14)
        p.drawString(305,480,str(obj2.date1.strftime("%d-%m-%Y")))
        p.setFont("Helvetica", 12)
        p.drawString(300, 460,"To: ")
        p.setFont("Helvetica", 14)
        p.drawString(305 , 440,str(obj2.date2.strftime("%d-%m-%Y")))
        # p.drawString(320, 480,str(obj2.month)) 
        p.setFont("Helvetica", 14)     
        p.drawString(380 , 480,"Consulation")
        p.drawString(385 , 440,"Medicine")
        p.drawString(450 , 680,str(obj2.date.strftime("%d-%m-%Y")))
        
        case = obj2.patient.case.split("-")[0][0]+"-"+obj2.patient.case.split("-")[1]
               
        bill_no = case + "/"+ str(obj2.id)
        p.drawString(140 , 680,bill_no)
        p.drawString(485 , 480,"Rs "+str(obj2.consulting_fees))
        p.drawString(485 , 440,"Rs "+str(obj2.medicine_fees))

        p.setFont("Helvetica", 13)
        y = 330
        for diagnose in obj_diagnose:
            p.drawString(100, y, diagnose)
            y = y - 18
        
        y1 = 250
        p.setFont("Helvetica", 15)
        for med_name in obj_med_name:
            print("med_name",med_name)
            if med_name != '':
                p.drawString(78,250,"Rx ")
        p.setFont("Helvetica", 13)
        for med_name in obj_med_name:
            if med_name != None:
                p.drawString(110,y1, med_name)
                y1 = y1 - 18


        add_me = obj2.consulting_fees + obj2.medicine_fees
        p.setFont("Helvetica", 14)
        p.drawString(485 , 200,"Rs "+str(add_me))

        amount = convert_to_text(add_me)
        
        p.setFont("Helvetica", 16)
        p.drawString(250,166,amount)
        p.showPage
        p.save()
        p = buffer.getvalue()
        buffer.close()
        response.write(p)
        return response

@csrf_exempt    
def previous_issued_invoice(request):

    status = False
    if request.user:
        status=request.user

    query = request.GET.get('query')

    if query:
        data = Bill.objects.filter(patient__case=query.upper()).order_by('-date')
    else:
        data = ""
    obj = Bill.objects.all().order_by('-date')
    return render(request,'dashboard/templates/previous_bills_new_adjust.html',{'status':status,'user':"D",'obj':obj,'data':data})

@csrf_exempt
def regen_bill_pdf(request,id):    
    
    obj2 = Bill.objects.get(id=id)

    obj = Diagnosis.objects.filter(patient=obj2.patient.id,date=obj2.date)      
       
    obj_diagnose = [o.diagnose for o in obj] 
    obj_med_name = [o.med_name for o in obj]
    
     
       
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'filename="Bill.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    letter_head = "./dashboard/document/bill.jpg"
    p.drawImage(letter_head,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    
    if obj2.patient.gender == 'Male':
        p.drawString(80, 480,"Mr "+obj2.patient.name)
    else:
        p.drawString(80, 480,"Mrs/Miss "+obj2.patient.name)

    p.setFont("Helvetica", 12)
        
    p.drawString(300, 500,"From: ")
    p.setFont("Helvetica", 14)
    try:
        p.drawString(305,480,str(obj2.date1.strftime("%d-%m-%Y")))
    except:
        pass
    p.setFont("Helvetica", 12)
    p.drawString(300, 460,"To: ")
    p.setFont("Helvetica", 14)
    try:
        p.drawString(305 , 440,str(obj2.date2.strftime("%d-%m-%Y")))
    except:
        pass
     
    p.setFont("Helvetica", 14)     
    p.drawString(380 , 480,"Consulation")
    p.drawString(385 , 440,"Medicine")
    p.drawString(450 , 680,str(obj2.date.strftime("%d-%m-%Y")))
        
    case = obj2.patient.case.split("-")[0][0]+"-"+obj2.patient.case.split("-")[1]
               
    bill_no = case + "/"+ str(obj2.id)
    p.drawString(140 , 680,bill_no)
    p.drawString(485 , 480,"Rs "+str(obj2.consulting_fees))
    p.drawString(485 , 440,"Rs "+str(obj2.medicine_fees))

    p.setFont("Helvetica", 13)
    y = 330
    for diagnose in obj_diagnose:
        p.drawString(100, y, diagnose)
        y = y - 18
    y1 = 330

    # for m in obj_med_name:
    #     if m != None:
    #         print("False")

    for med_name in obj_med_name:
        if med_name != None:
            p.drawString(220,y1,med_name)
            y1 = y1 - 18

    add_me = obj2.consulting_fees + obj2.medicine_fees
    p.setFont("Helvetica", 14)
    p.drawString(485 , 200,"Rs "+str(add_me))

    amount = convert_to_text(add_me)
        
    p.setFont("Helvetica", 16)
    p.drawString(250,166,amount)
    p.showPage
    p.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response

  
case_id_cer = 0
@csrf_exempt  
def addcertificate(request):
    
    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':

        p_id = request.POST['patient']
        diagnose1 = request.POST['diagnose1']
        diagnose2 = request.POST['diagnose2']
        diagnose3 = request.POST['diagnose3']
        date1 = request.POST['date1']
        if request.POST['date2']:
            date2 =request.POST['date2']
        else:
            date2 = None
        if request.POST['date3']:
            date3 = request.POST['date3']
        else:
            date3=None
        if request.POST['date4']:
            date4 = request.POST['date4']
        else:
            date4 = None
        if request.POST['month']:
            month = request.POST['month']
        else:
            month = 0
        patient = Patient.objects.get(id=p_id)
        obj = Certificate(patient=patient,diagnose1=diagnose1.title(),diagnose2=diagnose2.title(),diagnose3=diagnose3.title(),date1=date1,date2=date2,date3=date3,date4=date4,month=month)
        messages.info(request,'Now Please Click on Certificates above mentioned to be Generated.')
        obj.save()
        global case_id_cer
        case_id_cer = request.POST['patient']
        return redirect('addcertificate')  

    data = Patient.objects.all()

    return render(request,'dashboard/templates/addcertificate_new_adjust.html',{'status':status,'user':"D",'data':data,'case_id':case_id_cer})

@csrf_exempt
def medical_certificate_pdf(request,id):    
    
    if id == 0:
        return HttpResponse("<h1>Please fill details to generate Medical Certificate <h1>")
    else:
        obj = Certificate.objects.filter(patient_id=id).last()

        response = HttpResponse(content_type = 'application/pdf')
        response['Content-Disposition'] = 'filename="Medical-Certificate.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)    

        letter_head = "./dashboard/document/certificate.jpg"
        p.drawImage(letter_head,0,0,width=600,height=880)

        p.setFont("Helvetica", 14)
        p.drawString(450, 680,"Date: "+str(obj.date1.strftime("%d-%m-%Y")))
        p.setFont("Helvetica", 21)
        p.drawString(250, 600,"MEDICAL CERTIFICATE")
        p.drawString(250, 598,"____________________")
        p.setFont("Helvetica", 14)

        if obj.diagnose1 and obj.diagnose2 and obj.diagnose3:
            p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
            p.drawString(185, 515,"age "+str(obj.patient.age)+" years had suffered from "+obj.diagnose1+" , "+ obj.diagnose2+" and ")
            p.drawString(185, 490,obj.diagnose3+" on "+ str(obj.date1.strftime("%d-%m-%Y"))+". So he/she was advised to take")
            p.drawString(185, 465,"bed rest from "+ str(obj.date2.strftime("%d-%m-%Y"))+ " to " +str(obj.date3.strftime("%d-%m-%Y"))+" . He/She  is fit  to" )
            p.drawString(185, 440,"resume his/her  duty/school  from "+str(obj.date4.strftime("%d-%m-%Y"))+ " onwards  "  )
            p.drawString(185,415,"accordingly.")
            p.drawString(410, 310,"Dr. Santosh K. Yadav")
            p.setFont("Helvetica", 12)
            p.drawString(437, 290,"M.D. (Homeopathy)")
            p.drawString(437, 270,"Ph.D.(Homeopathy)")
        
        elif obj.diagnose1 and obj.diagnose2:
            p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
            p.drawString(185, 515,"age "+str(obj.patient.age)+" years had suffered from "+obj.diagnose1+" and "+ obj.diagnose2)
            p.drawString(185, 490,"on "+ str(obj.date1.strftime("%d-%m-%Y"))+". So  he/she was advised to take bed rest")
            p.drawString(185, 465,"from "+ str(obj.date2.strftime("%d-%m-%Y"))+ " to " +str(obj.date3.strftime("%d-%m-%Y"))+" . He/She  is fit to resume" )
            p.drawString(185, 440,"his/her  duty/school  from "+str(obj.date4.strftime("%d-%m-%Y"))+ " onwards accordingly.  "  )
            p.drawString(410, 310,"Dr. Santosh K. Yadav")
            p.setFont("Helvetica", 12)
            p.drawString(437, 290,"M.D. (Homeopathy)")
            p.drawString(437, 270,"Ph.D.(Homeopathy)")
        
        else:
            p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
            p.drawString(185, 515,"age "+str(obj.patient.age)+" years had suffered from "+obj.diagnose1+ " on "+str(obj.date1.strftime("%d-%m-%Y"))+".")
            p.drawString(185, 490,"So he/she was advised to take bed rest from "+ str(obj.date2.strftime("%d-%m-%Y")))
            p.drawString(185, 465,"to " +str(obj.date3.strftime("%d-%m-%Y"))+" . He/She is fit to resume his/her duty/school" )
            p.drawString(185, 440,"from "+str(obj.date4.strftime("%d-%m-%Y"))+ " onwards accordingly.  "  )
            p.drawString(410, 310,"Dr. Santosh K. Yadav")
            p.setFont("Helvetica", 12)
            p.drawString(437, 290,"M.D. (Homeopathy)")
            p.drawString(437, 270,"Ph.D.(Homeopathy)")
        p.showPage
        p.save()
        p = buffer.getvalue()
        buffer.close()
        response.write(p)
        return response

@csrf_exempt
def fitness_certificate_pdf(request,id):    
    
    if id == 0:
        return HttpResponse("<h1>Please fill details to generate Fitness Certificate <h1>")
    else:
        
        obj = Certificate.objects.filter(patient_id=id).last()

        response = HttpResponse(content_type = 'application/pdf')
        response['Content-Disposition'] = 'filename="Fitness-Certificate.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        letter_head = "./dashboard/document/certificate.jpg"
        p.drawImage(letter_head,0,0,width=600,height=880)

        p.setFont("Helvetica", 14)
        p.drawString(450, 680,"Date: "+str(obj.date1.strftime("%d-%m-%Y")))
        p.setFont("Helvetica", 21)
        p.drawString(250, 600,"FITNESS CERTIFICATE")
        p.drawString(250, 598,"____________________")
        p.setFont("Helvetica", 14)
        p.drawString(180, 540,"This is to certify that Mr/Mrs/Miss/Master "+obj.patient.name)
        p.drawString(180, 515,"is physically and mentally fit to do his/her activity properly.")
        p.drawString(410, 350,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 330,"M.D. (Homeopathy)")
        p.drawString(437, 310,"Ph.D.(Homeopathy)")
        p.showPage
        p.save()
        p = buffer.getvalue()
        buffer.close()
        response.write(p)
        return response
        
    
@csrf_exempt
def travelling_certificate_pdf(request,id):    
   
    if id == 0:
        return HttpResponse("<h1>Please fill details to generate Travelling Certificate <h1>")
    else:
        obj = Certificate.objects.filter(patient_id=id).last() 

        response = HttpResponse(content_type = 'application/pdf')
        response['Content-Disposition'] = 'filename="Travelling-Certificate.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        letter_head = "./dashboard/document/certificate.jpg"
        p.drawImage(letter_head,0,0,width=600,height=880)

        p.setFont("Helvetica", 14)
        p.drawString(450, 680,"Date: "+str(obj.date1.strftime("%d-%m-%Y")))
        p.setFont("Helvetica", 21)
        p.setFont("Helvetica", 21)
        p.drawString(290, 600,"CERTIFICATE")
        p.drawString(290, 598,"____________")
        p.setFont("Helvetica", 14)        

        if obj.diagnose1 and obj.diagnose2 and obj.diagnose3:

            p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
            p.drawString(185, 515,"age  "+str(obj.patient.age)+"  years  is  under  Homeopathy  treatment  for")
            p.drawString(185, 490,obj.diagnose1+" , "+ obj.diagnose2+" and "+ obj.diagnose3+". He/She had been    ")
            p.drawString(185, 465,"given medicine for "+str(obj.month)+ " months/days according to his/her ")
            p.drawString(185,440,"disease concerned.")
            p.drawString(410, 310,"Dr. Santosh K. Yadav")
            p.setFont("Helvetica", 12)
            p.drawString(437, 290,"M.D. (Homeopathy)")
            p.drawString(437, 270,"Ph.D.(Homeopathy)")

        elif obj.diagnose1 and obj.diagnose2:
            
            p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
            p.drawString(185, 515,"age  "+str(obj.patient.age)+"  years  is  under  Homeopathy  treatment  for")
            p.drawString(185, 490,obj.diagnose1+" and "+obj.diagnose2+". He/She  had  been  given"+ " ")
            p.drawString(185, 465,"medicine for "+str(obj.month)+ " months/days according to his/her disease")
            p.drawString(185,440,"concerned.")
            p.drawString(410, 310,"Dr. Santosh K. Yadav")
            p.setFont("Helvetica", 12)
            p.drawString(437, 290,"M.D. (Homeopathy)")
            p.drawString(437, 270,"Ph.D.(Homeopathy)")
       
        else:
            p.drawString(180, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
            p.drawString(180, 515,"age  "+str(obj.patient.age)+"  years  is  under  Homeopathy  treatment  for")
            p.drawString(180, 490,obj.diagnose1+". He/She  had  been  given  medicine  for  "+ " ")
            p.drawString(180, 465,str(obj.month)+ " months/days according to his/her disease concerned.")
            p.drawString(410, 310,"Dr. Santosh K. Yadav")
            p.setFont("Helvetica", 12)
            p.drawString(437, 290,"M.D. (Homeopathy)")
            p.drawString(437, 270,"Ph.D.(Homeopathy)") 
        
        p.showPage
        p.save()
        p = buffer.getvalue()
        buffer.close()
        response.write(p)
        return response

@csrf_exempt
def unfit_certificate_pdf(request,id):
    
    if id == 0:
        return HttpResponse("<h1>Please Fill details to generate Unfit Certificate<h1>")
    else:    
        obj = Certificate.objects.filter(patient_id =id).last()

        response = HttpResponse(content_type = 'application/pdf')
        response['Content-Disposition'] = 'filename="Unfit-Certificate.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        letter_head = "./dashboard/document/certificate.jpg"
        p.drawImage(letter_head,0,0,width=600,height=880)

        p.setFont("Helvetica", 14)
        p.drawString(450, 680,"Date: "+str(obj.date1.strftime("%d-%m-%Y")))
        p.setFont("Helvetica", 21)
        p.drawString(250, 600,"UNFIT CERTIFICATE")
        p.drawString(250, 598,"__________________")
        p.setFont("Helvetica", 14)

        if obj.diagnose1 and obj.diagnose2 and obj.diagnose3:
            p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
            p.drawString(185,515,"is suffering from "+ obj.diagnose1+ ","+obj.diagnose2+" and "+obj.diagnose3)
            p.drawString(185,490,"on "+str(obj.date1.strftime("%d-%m-%Y"))+". He/She is advised to take rest accordingly.")
            p.drawString(410, 350,"Dr. Santosh K. Yadav")
            p.setFont("Helvetica", 12)
            p.drawString(437, 330,"M.D. (Homeopathy)")
            p.drawString(437, 310,"Ph.D.(Homeopathy)")

        elif obj.diagnose1 and obj.diagnose2:
            p.drawString(185, 540,"This is to certify that  Mr/Mrs/Miss/Master  "+ obj.patient.name)
            p.drawString(185,515,"is suffering from "+ obj.diagnose1+" and "+obj.diagnose2+ " on "+str(obj.date1.strftime("%d-%m-%Y"))+".")
            p.drawString(185,490,"He/She is advised to take rest accordingly.")
            p.drawString(410, 350,"Dr. Santosh K. Yadav")
            p.setFont("Helvetica", 12)
            p.drawString(437, 330,"M.D. (Homeopathy)")
            p.drawString(437, 310,"Ph.D.(Homeopathy)")

        else:
            p.drawString(185, 540,"This is to certify that  Mr/Mrs/Miss/Master  "+ obj.patient.name)
            p.drawString(185, 515,"is suffering from "+ obj.diagnose1+" on "+str(obj.date1.strftime("%d-%m-%Y"))+". He/She is")
            p.drawString(185, 490,"advised to take rest accordingly.")
            p.drawString(410, 350,"Dr. Santosh K. Yadav")
            p.setFont("Helvetica", 12)
            p.drawString(437, 330,"M.D. (Homeopathy)")
            p.drawString(437, 310,"Ph.D.(Homeopathy)")
        p.showPage
        p.save()
        p = buffer.getvalue()
        buffer.close()
        response.write(p)
        return response

@csrf_exempt
def previous_issued_certificate(request):

    status = False
    if request.user:
        status = request.user

    query = request.GET.get('query')

    if query:
        data = Certificate.objects.filter(patient__case = query.upper()).order_by('-date1')
    else:
        data = ""
    obj = Certificate.objects.all().order_by('-date1')
    return render(request,'dashboard/templates/prev_issued_certicates_new_adjust.html',{'status':status,'user':'D','obj':obj,'data':data})

@csrf_exempt
def regenerate_issued_certificate(request,id):    
    
    status = False
    if request.user:
        status= request.user

    obj = Certificate.objects.get(id=id)
    
    if request.method == 'POST':
        update = Certificate.objects.get(id=id)      
        case = request.POST['patient']
        pat = Patient.objects.get(case=case)        
        update.patient_id = pat.id
        update.diagnose1=request.POST['diagnose1']
        update.diagnose2=request.POST['diagnose2']
        update.diagnose3=request.POST['diagnose3']
        update.date1=request.POST['date1']
        if request.POST['date2']:
            update.date2=request.POST['date2']
        else:
            update.date2 = None
        if request.POST['date3']:
            update.date3=request.POST['date3']
        else:
            update.date3= None
        if request.POST['date4']:            
            update.date4=request.POST['date4']
        else:
            update.date4 = None
        update.month=request.POST['month']
        update.save() 
        messages.info(request,'Click Below to Regenerate Certificate')

        return HttpResponseRedirect(reverse('regenerate_issued_certificate',  kwargs={'id': obj.id})) 


    data = Patient.objects.all()
    return render(request,'dashboard/templates/regenerate_issued_certificate_new.html',{'status':status,'user':'D','obj':obj,'data':data})

@csrf_exempt
def regen_medical_certificate_pdf(request,id):    
    
    print('id',id)
    obj = Certificate.objects.get(id=id)
    print('obj---',obj)
        
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'filename="Medical-Certificate.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)    

    letter_head = "./dashboard/document/certificate.jpg"
    p.drawImage(letter_head,0,0,width=600,height=880)

    p.setFont("Helvetica", 14)
    p.drawString(450, 680,"Date: "+str(obj.date1.strftime("%d-%m-%Y")))
    p.setFont("Helvetica", 21)
    p.drawString(250, 600,"MEDICAL CERTIFICATE")
    p.drawString(250, 598,"____________________")
    p.setFont("Helvetica", 14)

    if obj.diagnose1 and obj.diagnose2 and obj.diagnose3:
        p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
        p.drawString(185, 515,"age "+str(obj.patient.age)+" years had suffered from "+obj.diagnose1+" , "+ obj.diagnose2+" and ")
        p.drawString(185, 490,obj.diagnose3+" on "+ str(obj.date1.strftime("%d-%m-%Y"))+". So he/she was advised to take")
        p.drawString(185, 465,"bed rest from "+ str(obj.date2.strftime("%d-%m-%Y"))+ " to " +str(obj.date3.strftime("%d-%m-%Y"))+" . He/She  is fit  to" )
        p.drawString(185, 440,"resume his/her  duty/school  from "+str(obj.date4.strftime("%d-%m-%Y"))+ " onwards  "  )
        p.drawString(185,415,"accordingly.")
        p.drawString(410, 310,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 290,"M.D. (Homeopathy)")
        p.drawString(437, 270,"Ph.D.(Homeopathy)")
        
    elif obj.diagnose1 and obj.diagnose2:
        p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
        p.drawString(185, 515,"age "+str(obj.patient.age)+" years had suffered from "+obj.diagnose1+" and "+ obj.diagnose2)
        p.drawString(185, 490,"on "+ str(obj.date1.strftime("%d-%m-%Y"))+". So  he/she was advised to take bed rest")
        p.drawString(185, 465,"from "+ str(obj.date2.strftime("%d-%m-%Y"))+ " to " +str(obj.date3.strftime("%d-%m-%Y"))+" . He/She  is fit to resume" )
        p.drawString(185, 440,"his/her  duty/school  from "+str(obj.date4.strftime("%d-%m-%Y"))+ " onwards accordingly.  "  )
        p.drawString(410, 310,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 290,"M.D. (Homeopathy)")
        p.drawString(437, 270,"Ph.D.(Homeopathy)")
        
    else:
        p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
        p.drawString(185, 515,"age "+str(obj.patient.age)+" years had suffered from "+obj.diagnose1+ " on "+str(obj.date1.strftime("%d-%m-%Y"))+".")
        p.drawString(185, 490,"So he/she was advised to take bed rest from "+ str(obj.date2.strftime("%d-%m-%Y")))
        p.drawString(185, 465,"to " +str(obj.date3.strftime("%d-%m-%Y"))+" . He/She is fit to resume his/her duty/school" )
        p.drawString(185, 440,"from "+str(obj.date4.strftime("%d-%m-%Y"))+ " onwards accordingly.  "  )
        p.drawString(410, 310,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 290,"M.D. (Homeopathy)")
        p.drawString(437, 270,"Ph.D.(Homeopathy)")
    
    p.showPage
    p.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response

@csrf_exempt
def regen_fitness_certificate_pdf(request,id): 
   
        
    obj = Certificate.objects.get(id=id)

    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'filename="Fitness-Certificate.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    letter_head = "./dashboard/document/certificate.jpg"
    p.drawImage(letter_head,0,0,width=600,height=880)

    p.setFont("Helvetica", 14)
    p.drawString(450, 680,"Date: "+str(obj.date1.strftime("%d-%m-%Y")))
    p.setFont("Helvetica", 21)
    p.drawString(250, 600,"FITNESS CERTIFICATE")
    p.drawString(250, 598,"____________________")
    p.setFont("Helvetica", 14)
    p.drawString(180, 540,"This is to certify that Mr/Mrs/Miss/Master "+obj.patient.name)
    p.drawString(180, 515,"is physically and mentally fit to do his/her activity properly.")
    p.drawString(410, 350,"Dr. Santosh K. Yadav")
    p.setFont("Helvetica", 12)
    p.drawString(437, 330,"M.D. (Homeopathy)")
    p.drawString(437, 310,"Ph.D.(Homeopathy)")
    p.showPage
    p.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response

@csrf_exempt
def regen_travelling_certificate_pdf(request,id):
    
    
    obj = Certificate.objects.get(id=id) 

    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'filename="Travelling-Certificate.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    letter_head = "./dashboard/document/certificate.jpg"
    p.drawImage(letter_head,0,0,width=600,height=880)

    p.setFont("Helvetica", 14)
    p.drawString(450, 680,"Date: "+str(obj.date1.strftime("%d-%m-%Y")))
    p.setFont("Helvetica", 21)
    p.setFont("Helvetica", 21)
    p.drawString(290, 600,"CERTIFICATE")
    p.drawString(290, 598,"____________")
    p.setFont("Helvetica", 14)        

    if obj.diagnose1 and obj.diagnose2 and obj.diagnose3:

        p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
        p.drawString(185, 515,"age  "+str(obj.patient.age)+"  years  is  under  Homeopathy  treatment  for")
        p.drawString(185, 490,obj.diagnose1+" , "+ obj.diagnose2+" and "+ obj.diagnose3+". He/She had been    ")
        p.drawString(185, 465,"given medicine for "+str(obj.month)+ " months/days according to his/her ")
        p.drawString(185,440,"disease concerned.")
        p.drawString(410, 310,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 290,"M.D. (Homeopathy)")
        p.drawString(437, 270,"Ph.D.(Homeopathy)")

    elif obj.diagnose1 and obj.diagnose2:
            
        p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
        p.drawString(185, 515,"age  "+str(obj.patient.age)+"  years  is  under  Homeopathy  treatment  for")
        p.drawString(185, 490,obj.diagnose1+" and "+obj.diagnose2+". He/She  had  been  given"+ " ")
        p.drawString(185, 465,"medicine for "+str(obj.month)+ " months/days according to his/her disease")
        p.drawString(185,440,"concerned.")
        p.drawString(410, 310,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 290,"M.D. (Homeopathy)")
        p.drawString(437, 270,"Ph.D.(Homeopathy)")
       
    else:
        p.drawString(180, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
        p.drawString(180, 515,"age  "+str(obj.patient.age)+"  years  is  under  Homeopathy  treatment  for")
        p.drawString(180, 490,obj.diagnose1+". He/She  had  been  given  medicine  for  "+ " ")
        p.drawString(180, 465,str(obj.month)+ " months/days according to his/her disease concerned.")
        p.drawString(410, 310,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 290,"M.D. (Homeopathy)")
        p.drawString(437, 270,"Ph.D.(Homeopathy)") 
        
    p.showPage
    p.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response

@csrf_exempt
def regen_unfit_certificate_pdf(request,id):
    
    obj = Certificate.objects.get(id =id)
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'filename="Unfit-Certificate.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    letter_head = "./dashboard/document/certificate.jpg"
    p.drawImage(letter_head,0,0,width=600,height=880)

    p.setFont("Helvetica", 14)
    p.drawString(450, 680,"Date: "+str(obj.date1.strftime("%d-%m-%Y")))
    p.setFont("Helvetica", 21)
    p.drawString(250, 600,"UNFIT CERTIFICATE")
    p.drawString(250, 598,"__________________")
    p.setFont("Helvetica", 14)

    if obj.diagnose1 and obj.diagnose2 and obj.diagnose3:
        p.drawString(185, 540,"This is to certify that Mr/Mrs/Miss/Master "+ obj.patient.name)
        p.drawString(185,515,"is suffering from "+ obj.diagnose1+ ","+obj.diagnose2+" and "+obj.diagnose3)
        p.drawString(185,490,"on "+str(obj.date1.strftime("%d-%m-%Y"))+". He/She is advised to take rest accordingly.")
        p.drawString(410, 350,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 330,"M.D. (Homeopathy)")
        p.drawString(437, 310,"Ph.D.(Homeopathy)")

    elif obj.diagnose1 and obj.diagnose2:
        p.drawString(185, 540,"This is to certify that  Mr/Mrs/Miss/Master  "+ obj.patient.name)
        p.drawString(185,515,"is suffering from "+ obj.diagnose1+" and "+obj.diagnose2+ " on "+str(obj.date1.strftime("%d-%m-%Y"))+".")
        p.drawString(185,490,"He/She is advised to take rest accordingly.")
        p.drawString(410, 350,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 330,"M.D. (Homeopathy)")
        p.drawString(437, 310,"Ph.D.(Homeopathy)")

    else:
        p.drawString(185, 540,"This is to certify that  Mr/Mrs/Miss/Master  "+ obj.patient.name)
        p.drawString(185, 515,"is suffering from "+ obj.diagnose1+" on "+str(obj.date1.strftime("%d-%m-%Y"))+". He/She is")
        p.drawString(185, 490,"advised to take rest accordingly.")
        p.drawString(410, 350,"Dr. Santosh K. Yadav")
        p.setFont("Helvetica", 12)
        p.drawString(437, 330,"M.D. (Homeopathy)")
        p.drawString(437, 310,"Ph.D.(Homeopathy)")
    p.showPage
    p.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response

@csrf_exempt
def pricing(request):

    status = False
    if request.user:
        status = request.user
        
    data = Price.objects.get(id=2)
    if request.method == 'POST':
        form = PriceForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'Prices Updated Successfully')
            return redirect('pricing')
    form = PriceForm(instance=data)

    
    return render(request,'dashboard/templates/pricing_new.html',{'status':status,'user':"D",'form':form})

@csrf_exempt
def diagnosis_history(request):
    
    status=False
    if request.user:
        status=request.user
        print('status',status)
    
    query = request.GET.get('query')
          
    if query:    
            data = prescription.objects.filter(Q(diagnose__icontains=query)|Q(diagnose__icontains=query.upper())|Q(patientid__case__icontains=query.upper()))            
    else:
        data = ""

                    
    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count() 
    
    return render(request,'dashboard/templates/diagnosis_history_new.html',{'status':status,'user':"D",'data':data,'count_general_dom':count_general_dom,
                                                                'count_general_mul':count_general_mul,'count_repeat_dom':count_repeat_dom,
                                                                'count_repeat_mul':count_repeat_mul,'count_courier_dom':count_courier_dom,        
                                                                    'count_courier_mul':count_courier_mul,"unsend_mail_count":unsent_mail_count,})

@csrf_exempt
def chiefcomplaints(request):   
    status = False
    if request.user:
        status = request.user
    
    return render(request,'dashboard/templates/chief_complaints.html',{'status':status,'user':"D"})
   
    # return render(request,'dashboard/templates/all-customer.html',{'status':status,'user':"D"})

@csrf_exempt
def fearIncidents(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/fear_&_incidents.html',{'status':status,'user':"D"})

@csrf_exempt
def pasthistory(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/past-history-of-illness.html',{'status':status,'user':"D"})

@csrf_exempt
def familymedical(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/familymedical.html',{'status':status,'user':"D"})

@csrf_exempt
def personalhabits(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/personal-habits.html',{'status':status,'user':"D"})


# def personalappetite(request):
#     return render(request , "dashboard/templates/appetite.html")

@csrf_exempt
def infood(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/infood.html',{'status':status,'user':"D"})

@csrf_exempt
def sexualsphere(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/sexual-sphere.html',{'status':status,'user':"D"})

@csrf_exempt
def investigation1(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/investigation.html',{'status':status,'user':"D"})

@csrf_exempt
def thermalreaction(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/thermal.html',{'status':status,'user':"D"})

@csrf_exempt
def rubricselection(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/Rubric-selection.html',{'status':status,'user':"D"})



@csrf_exempt
def allstaff(request):
    status= False
    if request.user:
        status = request.user

    data = AddStaff.objects.all()
    obj = Receptionist.objects.all()
    obj1 = HR.objects.all()
            
    

    return render(request,'dashboard/templates/all_staff_new.html',{'status':status,'user':"D",'data':data,
                                                                "header":"ALL STAFF",'obj':obj,'obj1':obj1,	})
@csrf_exempt
def dash_recep(request,id):

    status = False
    if request.user:
        status = request.user
    
    if request.method == 'POST':
        update =  Receptionist.objects.get(id=id)
        update.name =  request.POST['name']
        update.phone = request.POST['phone']
        update.email = request.POST['email']
        update.branch = request.POST['branch']        
        data = User.objects.get(username=request.POST['username'])        
        update.username = data
        if 'recep_image' in request.FILES:
            update.recep_image = request.FILES['recep_image']
        else:
            pass
        update.save()
        messages.success(request,'Updated Successfully for '+ request.POST['name'])
        return HttpResponseRedirect(reverse('dash_recep',  kwargs={'id': id}))

    obj = Receptionist.objects.get(id=id)
                
    

    return render(request,'dashboard/templates/dash_recep_new.html',{'status':status,'user':"D",'obj':obj
                                                                 ,"header":"Receptionist Details"})
@csrf_exempt
def recep_documents(request,id):

    status = False
    if request.user:
        status = request.user
    obj = Receptionist.objects.get(id=id)

    if request.method == 'POST':
        files = request.FILES.getlist('recep_doc')
        print('files',files,len(files))
        for i in files:
            data =ReceptionistDocs.objects.create(recep=obj,images=i) 
            data.save()  
           
        messages.success(request,'Documents Uploaded')
        return HttpResponseRedirect(reverse('recep_documents',  kwargs={'id': id}))

                    
    
    
    return render(request,'dashboard/templates/recep_documents_new.html',{'status':status,'user':"D",'obj':obj}) 

@csrf_exempt
def recep_gallery(request,id):
    
    status = False
    if request.user:
        status = request.user 
    
    img = ReceptionistDocs.objects.filter(recep_id = id)    

    obj = Receptionist.objects.get(id=id)
                        
    

    return render(request,'dashboard/templates/recep_gallery_new.html',{'status':status,'user':"D",'img':img,'obj':obj}) 

@csrf_exempt
def dash_hr(request,id):

    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':
        update = HR.objects.get(id=id)
        update.name =  request.POST['name']
        update.phone = request.POST['phone']
        update.email = request.POST['email']
        update.branch = request.POST['branch']        
        data = User.objects.get(username=request.POST['username'])        
        update.username = data
        if 'hr_image' in request.FILES:
            update.hr_image = request.FILES['hr_image']
        else:
            pass

        update.save()
        messages.success(request,'Updated Successfully for '+ request.POST['name'])
        return HttpResponseRedirect(reverse('dash_hr',  kwargs={'id': id}))

    obj = HR.objects.get(id=id)
                            
    

    return render(request,'dashboard/templates/dash_hr_new.html',{'status':status,'user':"D",'obj':obj})

@csrf_exempt
def hr_documents(request,id):

    status = False
    if request.user:
        status = request.user
    obj = HR.objects.get(id=id)

    if request.method == 'POST':
        files = request.FILES.getlist('hr_doc')
        print('files',files,len(files))
        for i in files:
            data = HRDocs.objects.create(hr=obj,images=i) 
            data.save()  
           
        messages.success(request,'Documents Uploaded')        
        return HttpResponseRedirect(reverse('hr_documents',  kwargs={'id': id}))
    
                                
    
    
    return render(request,'dashboard/templates/hr_documents_new.html',{'status':status,'user':"D",'obj':obj})

@csrf_exempt
def hr_gallery(request,id):
    
    status = False
    if request.user:
        status = request.user 
    
    img = HRDocs.objects.filter(hr_id = id) 

    obj = HR.objects.get(id=id)
                                    
    
    return render(request,'dashboard/templates/hr_gallery_new.html',{'status':status,'user':"D",'img':img,'obj':obj}) 

@csrf_exempt
def editstaff(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/edit-staff.html',{'status':status,'user':"D"})

@csrf_exempt
def addstaff(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/add-staff.html',{'status':status,'user':"D"})

@csrf_exempt
def gallery(request):
    return render(request,'dashboard/templates/gallery.html')


@csrf_exempt
def allroom(request):
    status= False
    if request.user:
        status = request.user

    data = AddMedicine.objects.all()
    return render(request,'dashboard/templates/all-medicine.html',{'status':status,'user':"D",'data':data})
    # return render(request,'dashboard/templates/all-rooms.html',{'status':status,'user':"D"})

@csrf_exempt
def addroom(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/add-room.html',{'status':status,'user':"D"})

@csrf_exempt
def editroom(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/edit-room.html',{'status':status,'user':"D"})

@csrf_exempt
def pagination(request):
    return render(request,'dashboard/templates/responsivepage.html')

@csrf_exempt
def drum1bottle(request):
    return render(request,'dashboard/templates/drum_1_bottle.html')

@csrf_exempt
def halfdrumbottle(request):
    return render(request,'dashboard/templates/half_drum_bottle.html')

@csrf_exempt
def pills(request):
    return render(request,'dashboard/templates/pills.html')

@csrf_exempt
def demo(request):
    return render(request,'dashboard/templates/deno.html')

@csrf_exempt
def mental(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/mind_causative_factor.html',{'status':status,'user':"D"})


@csrf_exempt
def multiple(request):
    return render(request,'dashboard/templates/multiple.html')

@csrf_exempt
def miasm(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/miasm.html',{'status':status,'user':"D"})

@csrf_exempt
def multipleselect(request):
    return render(request,'multipleselect.html')

@csrf_exempt
def personalappetite(request):    
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/appetite.html',{'status':status,'user':"D"})

@csrf_exempt
def lifestory(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/life_story.html',{'status':status,'user':"D"})

@csrf_exempt
def accordian(request):
    return render(request,'dashboard/templates/accordian.html')


@csrf_exempt
def addmedicine(request):
    status= False
    if request.user:
        status = request.user

    if request.method == 'POST':
        
        name = request.POST['medicine']
        potency = request.POST['potency']
        quantity = request.POST['quantity']
        new = AddMedicine.objects.create(name=name,potency=potency,quantity=quantity)
        new.save()
        return HttpResponseRedirect(reverse('allroom'))        
    return render(request,'dashboard/templates/add-medicine.html',{'status':status,'user':"D"})
    # return render(request,'dashboard/templates/add-room.html')


@csrf_exempt
def addstaff(request):

    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':
       
        name = request.POST['name']        
        staffid = request.POST['staffid']        
        email = request.POST['email']        
        phone = request.POST['phone']       
        date = request.POST['date']        
        role = request.POST['role']        
        branch = request.POST['branch']
        if 'images' in request.FILES:
            images = request.FILES['images']        
        files = request.FILES.getlist('documents')        
        for i in files:
            obj = AddStaff(name=name,staff_id=staffid,email=email,phone_number=phone,join_date=date,role=role,branch=branch,upload_image=images,upload_docs=i)
            obj.save()
            return redirect('addstaff')

    return render(request,'dashboard/templates/add_staff.html',{'user':"D",'status':status})

# def book(request):    
    
#     return render(request,'dashboard/templates/book.html',{'user':"D",'status':'doctor'})

@csrf_exempt
def item(request):
    return render(request,'dashboard/templates/item.html')

@csrf_exempt
def itemDetail(request):
    return render(request,'dashboard/templates/itemDetail.html')

@csrf_exempt
def one_drum_bottles(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/drum_1_bottle.html',{'status':status,'user':"D"})

@csrf_exempt
def half_drum_bottle(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/half_drum_bottle.html',{'status':status,'user':"D"})

@csrf_exempt
def pills(request):
    status= False
    if request.user:
        status = request.user
    return render(request,'dashboard/templates/pills.html',{'status':status,'user':"D"})



@csrf_exempt
def upload_images(request,id):
    print('id @@new11', id)
    status=False
    if request.user:
        status=request.user
        # print(status,'status')
    patient = Patient.objects.get(case=id)
    # patient = Patient.objects.get(id=id)
    # print('@@@@name',patient.id)  
    
    img = ImagesUpload.objects.filter(case = patient.id).order_by('-date')

    query = request.GET.get('query')
    if query:
        img = ImagesUpload.objects.filter(case = patient.id,date__contains=query).order_by('-date')
        print("img",img)
    p = Paginator(img ,3)
    page = request.GET.get('page')
    datas = p.get_page(page)
        
    return render(request,'doctor_image.html',{'status':status, 'user': "AP", 'data1':id,'data':id,'img':img,'patient':patient,'datas':datas })

@csrf_exempt
def add_question(request):
    if request.method=='POST':
        questions=request.POST['questions']
        obj=Question.objects.create(question=questions)
        obj.save()
    return render(request,'dashboard/templates/add_question.html')

@csrf_exempt
def retrive(request):
    status=False
    if request.user:
        status=request.user
    obj=QAnswar.objects.all()
    #print(obj)
    return render(request,'all-customer.html', {'obj':obj} )




@csrf_exempt
def add_appetite(request):
    if request.method=='POST':
        heading=request.POST['heading']
        questions=request.POST['questions']
        obj=Appetite.objects.create(question=questions,heading=heading)
        obj.save()
    return render(request,'dashboard/templates/addappetite.html')

@csrf_exempt
def appetite_retrive(request):
    obj=Appetite.objects.all()
    return render(request,'dashboard/templates/appetite.html',{'obj':obj})

@csrf_exempt
def answar(request):
    if request.method=='POST':
        answar=request.POST['answar']
        obj=QAnswar.objects.create(answars=answar)
        obj.save()
    return render(request,'all-customer.html')

@csrf_exempt
def dombivali_collection(request):

    status = False
    if request.user:
        status = request.user
        # print('status--1',status)
    # print('DATE',date.today())
    try:
        paid_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        # print('paid_amount',paid_amount)
        sum_paid = 0
        for pd in paid_amount:
            sum_paid += pd.paid_amount
    except:
        sum_paid = 0

    # print('sum_paid',sum_paid)

    try:
        # cash_amount = Amount.objects.filter(date__date=date.today(),cash=True,patient__branch="Dombivali")
        cash_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        sum_cash = 0
        for ca in cash_amount:
            sum_cash += ca.cash_amount
    
    except:
        sum_cash = 0


    # print('cash_paid',sum_cash)
    try:
        # online_amount = Amount.objects.filter(date__date=date.today(),online=True,patient__branch="Dombivali")
        online_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        sum_online = 0
        for ao in online_amount:
            sum_online += ao.online_amount

    except:
        sum_online = 0


    # print('online_paid',sum_online)    

    try:
        balance_amount = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Dombivali")
        sum_balance = 0
        sum_advance = 0
        for ba in balance_amount:
            # print('bal',ba.balance_amt)  
            if ba.balance_amt >= 0:      
                sum_balance += ba.balance_amt
            else:
                sum_advance += abs(ba.balance_amt)                
    except:
        sum_balance = 0
        sum_advance = 0
    
    try:
        total = sum_paid + sum_balance
    except:
        total = 0
    # print("TOTAL",total)
    balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Dombivali")    
    amount_names = Amount.objects.filter(date__date = date.today(),patient__branch="Dombivali")
    # print("Amount Names",amount_names.values())
    my_list = [] 
    for b in balance_names:                   
        app_status = Appointment.objects.filter(patientid__case=b.patient.case).last()
        my_list.append(app_status)

                
    
    hr_list = HR.objects.filter(branch="Dombivali")
    hr_payment = []
    for hr in hr_list:
        hr_payment.append(f'{hr.name} - {hr.username}')
    return render(request,'dashboard/templates/dombivali_collection_newone_mob.html',{'user':"D",'status':status,'sum_cash':sum_cash,
                                'sum_online':sum_online,'sum_paid':sum_paid,'sum_balance':sum_balance,
                                'total':total,"balance_names":balance_names,'amount_names':amount_names,
                                'appointment_status':my_list,"header":"Dombivali Collection","header1":"Collection Details",
            'sum_advance':sum_advance,'hr_payment':hr_payment})

@csrf_exempt
def dombivali_collection_general(request):

    status = False
    if request.user:
        status = request.user
        # print('status--1',status)
    # print('DATE',date.today())
    try:
        paid_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        # print('paid_amount',paid_amount)
        sum_paid = 0
        for pd in paid_amount:
            sum_paid += pd.paid_amount
    except:
        sum_paid = 0

    # print('sum_paid',sum_paid)

    try:
        # cash_amount = Amount.objects.filter(date__date=date.today(),cash=True,patient__branch="Dombivali")
        cash_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        sum_cash = 0
        for ca in cash_amount:
            sum_cash += ca.cash_amount
    
    except:
        sum_cash = 0


    # print('cash_paid',sum_cash)
    try:
        # online_amount = Amount.objects.filter(date__date=date.today(),online=True,patient__branch="Dombivali")
        online_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        sum_online = 0
        for ao in online_amount:
            sum_online += ao.online_amount

    except:
        sum_online = 0


    # print('online_paid',sum_online)    

    try:
        balance_amount = Balance.objects.filter(previous_deal_date__date=date.today(),patient__branch="Dombivali")
        sum_balance = 0
        for ba in balance_amount:        
            sum_balance += ba.balance_amt
    except:
        sum_balance = 0
    
    try:
        total = sum_paid + sum_balance
    except:
        total = 0
    # print("TOTAL",total)
    balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Dombivali")    
    amount_names = Amount.objects.filter(date__date = date.today(),patient__branch="Dombivali")
    # print("Amount Names",amount_names.values())
    my_list = [] 
    for b in balance_names:                   
        app_status = Appointment.objects.filter(patientid__case=b.patient.case).last()
        my_list.append(app_status)

                    
    
    return render(request,'dashboard/templates/dombivali_collection_general_mob.html',{'user':"D",'status':status,'sum_cash':sum_cash,
                                'sum_online':sum_online,'sum_paid':sum_paid,'sum_balance':sum_balance,
                                'total':total,"balance_names":balance_names,'amount_names':amount_names,
                                'appointment_status':my_list,"header":"Dombivali Collection","header1":"Dombivali General Collection Details"})

@csrf_exempt
def dombivali_collection_repeat(request):

    status = False
    if request.user:
        status = request.user
        # print('status--1',status)
    # print('DATE',date.today())
    try:
        paid_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        # print('paid_amount',paid_amount)
        sum_paid = 0
        for pd in paid_amount:
            sum_paid += pd.paid_amount
    except:
        sum_paid = 0

    # print('sum_paid',sum_paid)

    try:
        # cash_amount = Amount.objects.filter(date__date=date.today(),cash=True,patient__branch="Dombivali")
        cash_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        sum_cash = 0
        for ca in cash_amount:
            sum_cash += ca.cash_amount
    
    except:
        sum_cash = 0


    # print('cash_paid',sum_cash)
    try:
        # online_amount = Amount.objects.filter(date__date=date.today(),online=True,patient__branch="Dombivali")
        online_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        sum_online = 0
        for ao in online_amount:
            sum_online += ao.online_amount

    except:
        sum_online = 0


    # print('online_paid',sum_online)    

    try:
        balance_amount = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Dombivali")
        sum_balance = 0
        for ba in balance_amount:        
            sum_balance += ba.balance_amt
    except:
        sum_balance = 0
    
    try:
        total = sum_paid + sum_balance
    except:
        total = 0
    # print("TOTAL",total)
    balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Dombivali")    
    amount_names = Amount.objects.filter(date__date = date.today(),patient__branch="Dombivali")
    # print("Amount Names",amount_names.values())
    my_list = [] 
    for b in balance_names:                   
        app_status = Appointment.objects.filter(patientid__case=b.patient.case).last()
        my_list.append(app_status)

                    
    
    return render(request,'dashboard/templates/dombivali_collection_repeat_mob.html',{'user':"D",'status':status,'sum_cash':sum_cash,
                                'sum_online':sum_online,'sum_paid':sum_paid,'sum_balance':sum_balance,
                                'total':total,"balance_names":balance_names,'amount_names':amount_names,
                                'appointment_status':my_list,"header":"Dombivali Collection","header1":"Dombivali Repeat Medicine Collection Details"})

@csrf_exempt
def dombivali_collection_courier(request):

    status = False
    if request.user:
        status = request.user
        # print('status--1',status)
    # print('DATE',date.today())
    try:
        paid_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        # print('paid_amount',paid_amount)
        sum_paid = 0
        for pd in paid_amount:
            sum_paid += pd.paid_amount
    except:
        sum_paid = 0

    # print('sum_paid',sum_paid)

    try:
        # cash_amount = Amount.objects.filter(date__date=date.today(),cash=True,patient__branch="Dombivali")
        cash_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        sum_cash = 0
        for ca in cash_amount:
            sum_cash += ca.cash_amount
    
    except:
        sum_cash = 0


    # print('cash_paid',sum_cash)
    try:
        # online_amount = Amount.objects.filter(date__date=date.today(),online=True,patient__branch="Dombivali")
        online_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Dombivali")
        sum_online = 0
        for ao in online_amount:
            sum_online += ao.online_amount

    except:
        sum_online = 0


    # print('online_paid',sum_online)    

    try:
        balance_amount = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Dombivali")
        sum_balance = 0
        for ba in balance_amount:        
            sum_balance += ba.balance_amt
    except:
        sum_balance = 0
    
    try:
        total = sum_paid + sum_balance
    except:
        total = 0
    # print("TOTAL",total)
    balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Dombivali")    
    amount_names = Amount.objects.filter(date__date = date.today(),patient__branch="Dombivali")
    # print("Amount Names",amount_names.values())
    my_list = [] 
    for b in balance_names:                   
        app_status = Appointment.objects.filter(patientid__case=b.patient.case).last()
        my_list.append(app_status)

                    
    
    
    
    return render(request,'dashboard/templates/dombivali_collection_courier_mob.html',{'user':"D",'status':status,'sum_cash':sum_cash,
                                'sum_online':sum_online,'sum_paid':sum_paid,'sum_balance':sum_balance,
                                'total':total,"balance_names":balance_names,'amount_names':amount_names,
                                'appointment_status':my_list,"header":"Dombivali Collection","header1":"Dombivali Courier Medicine Collection Details"})

@csrf_exempt
def mulund_collection(request):
    
    status = False
    if request.user:
        status = request.user

    try:
        paid_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        # print('paid_amount',paid_amount)
        sum_paid = 0
        for pd in paid_amount:
            sum_paid += pd.paid_amount
    except:
        sum_paid = 0

    # print('sum_paid',sum_paid)

    try:
        # cash_amount = Amount.objects.filter(date__date=date.today(),cash=True,patient__branch="Mulund")
        cash_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        sum_cash = 0
        for ca in cash_amount:
            sum_cash += ca.cash_amount
            # sum_cash += ca.paid_amount
    
    except:
        sum_cash = 0


    # print('cash_paid',sum_cash)
    try:
        # online_amount = Amount.objects.filter(date__date=date.today(),online=True,patient__branch="Mulund")
        online_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        sum_online = 0
        for ao in online_amount:
            sum_online += ao.online_amount
            # sum_online += ao.paid_amount

    except:
        sum_online = 0


    # print('online_paid',sum_online)    

    try:
        balance_amount = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Mulund")
        sum_balance = 0
        sum_advance = 0
        for ba in balance_amount:
            if ba.balance_amt >= 0:        
                sum_balance += ba.balance_amt
            else:
                sum_advance += abs(ba.balance_amt)
    except:
        sum_balance = 0
        sum_advance = 0
    
    try:
        total = sum_paid + sum_balance
    except:
        total=0
    
    balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Mulund")
    amount_names = Amount.objects.filter(date__date = date.today(),patient__branch="Mulund")
    # print("balance_names",balance_names)
    my_list_one = [] 
    for b in balance_names:                   
        app_status = Appointment.objects.filter(patientid__case=b.patient.case).last()
        my_list_one.append(app_status)

                    
    
    hr_list = HR.objects.filter(branch="Mulund")
    hr_payment = []
    for hr in hr_list:
        hr_payment.append(f'{hr.name} - {hr.username}')       
        
    print("payment_list",hr_payment)
    return render(request,'dashboard/templates/mulund_collection_newone_mob.html',{"user":"D",'status':status,'sum_cash':sum_cash,
                    'sum_online':sum_online,'sum_paid':sum_paid,'sum_balance':sum_balance,
                    'total':total,"balance_names":balance_names,'amount_names':amount_names,
                    "header":"Mulund Collections","header1":"Collection Details",'appointment_status':my_list_one,
                                'sum_advance':sum_advance,'hr_payment':hr_payment})

@csrf_exempt
def mulund_collection_general(request):
    
    status = False
    if request.user:
        status = request.user

    try:
        paid_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        # print('paid_amount',paid_amount)
        sum_paid = 0
        for pd in paid_amount:
            sum_paid += pd.paid_amount
    except:
        sum_paid = 0

    # print('sum_paid',sum_paid)

    try:
        # cash_amount = Amount.objects.filter(date__date=date.today(),cash=True,patient__branch="Mulund")
        cash_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        sum_cash = 0
        for ca in cash_amount:
            sum_cash += ca.cash_amount
            # sum_cash += ca.paid_amount
    
    except:
        sum_cash = 0


    # print('cash_paid',sum_cash)
    try:
        # online_amount = Amount.objects.filter(date__date=date.today(),online=True,patient__branch="Mulund")
        online_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        sum_online = 0
        for ao in online_amount:
            sum_online += ao.online_amount
            # sum_online += ao.paid_amount

    except:
        sum_online = 0


    # print('online_paid',sum_online)    

    try:
        balance_amount = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Mulund")
        sum_balance = 0
        for ba in balance_amount:        
            sum_balance += ba.balance_amt
    except:
        sum_balance = 0
    
    try:
        total = sum_paid + sum_balance
    except:
        total=0
    
    balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Mulund")
    amount_names = Amount.objects.filter(date__date = date.today(),patient__branch="Mulund")
    # print("balance_names",balance_names)
    my_list_one = [] 
    for b in balance_names:                   
        app_status = Appointment.objects.filter(patientid__case=b.patient.case).last()
        my_list_one.append(app_status)

                    
        
    return render(request,'dashboard/templates/mulund_collection_general_mob.html',{"user":"D",'status':status,'sum_cash':sum_cash,
                    'sum_online':sum_online,'sum_paid':sum_paid,'sum_balance':sum_balance,
                    'total':total,"balance_names":balance_names,'amount_names':amount_names,
                    "header":"Mulund Collection","header1":"Mulund General Collection Details",'appointment_status':my_list_one})

@csrf_exempt
def mulund_collection_repeat(request):
    
    status = False
    if request.user:
        status = request.user

    try:
        paid_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        # print('paid_amount',paid_amount)
        sum_paid = 0
        for pd in paid_amount:
            sum_paid += pd.paid_amount
    except:
        sum_paid = 0

    # print('sum_paid',sum_paid)

    try:
        # cash_amount = Amount.objects.filter(date__date=date.today(),cash=True,patient__branch="Mulund")
        cash_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        sum_cash = 0
        for ca in cash_amount:
            sum_cash += ca.cash_amount
            # sum_cash += ca.paid_amount
    
    except:
        sum_cash = 0


    # print('cash_paid',sum_cash)
    try:
        # online_amount = Amount.objects.filter(date__date=date.today(),online=True,patient__branch="Mulund")
        online_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        sum_online = 0
        for ao in online_amount:
            sum_online += ao.online_amount
            # sum_online += ao.paid_amount

    except:
        sum_online = 0


    # print('online_paid',sum_online)    

    try:
        balance_amount = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Mulund")
        sum_balance = 0
        for ba in balance_amount:        
            sum_balance += ba.balance_amt
    except:
        sum_balance = 0
    
    try:
        total = sum_paid + sum_balance
    except:
        total=0
    
    balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Mulund")
    amount_names = Amount.objects.filter(date__date = date.today(),patient__branch="Mulund")
    # print("balance_names",balance_names)
    my_list_one = [] 
    for b in balance_names:                   
        app_status = Appointment.objects.filter(patientid__case=b.patient.case).last()
        my_list_one.append(app_status)

                    
        
    return render(request,'dashboard/templates/mulund_collection_repeat_mob.html',{"user":"D",'status':status,'sum_cash':sum_cash,
                    'sum_online':sum_online,'sum_paid':sum_paid,'sum_balance':sum_balance,
                    'total':total,"balance_names":balance_names,'amount_names':amount_names,
                    "header":"Mulund Collection","header1":"Mulund Repeat Medicine Collection Details",'appointment_status':my_list_one})

@csrf_exempt
def mulund_collection_courier(request):
    
    status = False
    if request.user:
        status = request.user

    try:
        paid_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        # print('paid_amount',paid_amount)
        sum_paid = 0
        for pd in paid_amount:
            sum_paid += pd.paid_amount
    except:
        sum_paid = 0

    # print('sum_paid',sum_paid)

    try:
        # cash_amount = Amount.objects.filter(date__date=date.today(),cash=True,patient__branch="Mulund")
        cash_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        sum_cash = 0
        for ca in cash_amount:
            sum_cash += ca.cash_amount
            # sum_cash += ca.paid_amount
    
    except:
        sum_cash = 0


    # print('cash_paid',sum_cash)
    try:
        # online_amount = Amount.objects.filter(date__date=date.today(),online=True,patient__branch="Mulund")
        online_amount = Amount.objects.filter(date__date=date.today(),patient__branch="Mulund")
        sum_online = 0
        for ao in online_amount:
            sum_online += ao.online_amount
            # sum_online += ao.paid_amount

    except:
        sum_online = 0


    # print('online_paid',sum_online)    

    try:
        balance_amount = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Mulund")
        sum_balance = 0
        for ba in balance_amount:        
            sum_balance += ba.balance_amt
    except:
        sum_balance = 0
    
    try:
        total = sum_paid + sum_balance
    except:
        total=0
    
    balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient__branch="Mulund")
    amount_names = Amount.objects.filter(date__date = date.today(),patient__branch="Mulund")
    # print("balance_names",balance_names)
    my_list_one = [] 
    for b in balance_names:                   
        app_status = Appointment.objects.filter(patientid__case=b.patient.case).last()
        my_list_one.append(app_status)                   
       
        
    return render(request,'dashboard/templates/mulund_collection_courier_mob.html',{"user":"D",'status':status,'sum_cash':sum_cash,
                    'sum_online':sum_online,'sum_paid':sum_paid,'sum_balance':sum_balance,
                    'total':total,"balance_names":balance_names,'amount_names':amount_names,
                    "header":"Mulund Collection","header1":"Mulund Courier Collection Details",'appointment_status':my_list_one})
# NEW CASE

case_id = 0
@csrf_exempt
def newcase(request):

    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':
        print('pat',request.POST['patient'])
        pat_id = request.POST['patient']
        patient = Patient.objects.get(id=pat_id)
        obj = NewCase(patient=patient)
        obj.save()
        messages.info(request,'Added ' +str(patient)+' for New Case') 
        global case_id
        case_id = request.POST['patient']
        return redirect('newcase')


    
    data = Patient.objects.all()
    return render(request,'dashboard/templates/newcase.html',{'user':'D','status':status,'data':data,'case_id':case_id})


case_id_new = 0
@csrf_exempt
def new_case_one(request):

    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':
        print('pat',request.POST['patient'])
        pat_id = request.POST['patient']
        patient = Patient.objects.get(id=pat_id)
        obj = NewCase(patient=patient)
        obj.save()
        messages.info(request,'Added ' +str(patient)+' for New Case') 
        global case_id_new
        case_id_new = request.POST['patient']
        return redirect('new_case_one')

    data = Patient.objects.all()
    return render(request,'dashboard/templates/new_case_one.html',{'user':'D','status':status,'data':data,'case_id':case_id_new})


@csrf_exempt
def addquestion(request):

    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':        
        print('category',request.POST['category'])
        cat_id = request.POST['category']
        category = Category.objects.get(id=cat_id)                 
        print('question',request.POST['question'])
        question = request.POST['question']
        obj = Question1.objects.create(category=category,question=question)
        obj.save()
        messages.info(request,'Question added for ' + category.category)
        return redirect('addquestion')


    data = Category.objects.all()

    return render(request,'dashboard/templates/addquestion.html',{'data':data,'status':status,'user':'D'})

# PRESENT COMPLAINTS
@csrf_exempt
def present_complaints_newone(request,case_id):

    status = False
    if request.user:
        status= request.user
    
    if case_id == 0:
        return HttpResponse('<h1>Please Select a Patient to continue</h1>')
    else:
        patient = Patient.objects.get(id=case_id)
        
        if request.method == 'POST':
            form = PresentComplaintsForm(request.POST)
            if form.is_valid():
                complaint = form.cleaned_data['complaint']
                duration =  form.cleaned_data['duration']
                duration_suffix = form.cleaned_data['duration_suffix']
                remark =  form.cleaned_data['remark']
                create_complain = Complain.objects.get_or_create(name=complaint.title())
                complain = create_complain[0]
                obj = PresentComplaintsNew(patient=patient,complain=complain,duration=duration,duration_suffix=duration_suffix,remarks=remark)
                obj.save()
                messages.success(request, 'Successfully Added the Present Complaint')
                return HttpResponseRedirect(reverse('past_history_newone', kwargs={'case_id': case_id}))
        else:
            form = PresentComplaintsForm()

        table_data = PresentComplaintsNew.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
        data = Complain.objects.all().order_by(Lower('name'))
        patient_details= Patient.objects.get(id=case_id)

        
        appoint = Appointment.objects.filter(Q(patientid=patient_details)&Q(date=date.today())).last()
        if appoint.token != 0:
            final_token = appoint.token
        else:
            final_token = appoint.token1



        context = {'user':'D',
                   'status':status,
                   'case_id':case_id,
                   'data':data,
                   'table':table_data,
                   'patient_details':patient_details,                   
                     'form': form,
                     'patient':patient_details,
                     'final_token':final_token,
                   }
    
        return render(request,'dashboard/templates/present_complaints_newone_adjust.html',context)
    
def delete_present_complaints(request,id):

    obj = PresentComplaintsNew.objects.get(id=id)
    obj.delete()
    messages.success(request,f'Present Complaint - {obj.complain} deleted')
    return HttpResponseRedirect(reverse('past_history_newone', kwargs={'case_id': obj.patient.id}))

def delete_added_present_complaints(request,id):

    obj = PresentComplaintsNew.objects.get(id=id)
    obj.delete()
    messages.success(request,f'Present Complaint - {obj.complain} deleted')
    return HttpResponseRedirect(reverse('present_complaints_add', kwargs={'id': obj.patient.id}))

@csrf_exempt
def complain(request,case_id,id):

    status = False
    if request.user:
        status = request.user
    
    complain_name = Complain.objects.get(id=id)
    patient = Patient.objects.get(id=case_id)

    if request.method == 'POST':
        form = PresentComplaintsForm(request.POST, initial={'complaint': complain_name})
        if form.is_valid():
            duration =  form.cleaned_data['duration']
            duration_suffix = form.cleaned_data['duration_suffix']
            remark =  form.cleaned_data['remark']
            obj = PresentComplaintsNew(patient=patient,complain=complain_name,duration=duration,duration_suffix=duration_suffix,remarks=remark)
            obj.save()        
            messages.success(request,'Successfully Added to the Present Complaints')
            return HttpResponseRedirect(reverse('complain',kwargs={'case_id': case_id,'id':id}))
    else:
        form = PresentComplaintsForm(initial={'complaint': complain_name})
        
    table_data = PresentComplaintsNew.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
    data = Complain.objects.all().order_by(Lower('name'))

    appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()
    if appoint.token != 0:
        final_token = appoint.token
    else:
        final_token = appoint.token1

    context = {'user':'D',
               'status':status,
               'case_id':case_id,
               'data':data,
               'complain':complain_name,
               'table':table_data,
               'patient_details':patient,
               'form':form,
               'final_token':final_token, 
               'patient':patient          
               }
    
    return render(request,'dashboard/templates/present_complaints_disease_adjust.html',context)

    # NEW PATIENT HISTORY (EARLIER PAST HISTORY)

@csrf_exempt
def patient_history_newone(request,case_id):

    status =False
    if request.user:
        status = request.user
    if case_id == 0:
        return HttpResponse('<h1>Please Select a Patient to continue</h1>')
    else:
        patient = Patient.objects.get(id=case_id)
        
        if request.method == 'POST':
            form = PatientHistoryForm(request.POST)
            if form.is_valid():
                complaint = form.cleaned_data['complaint']
                last_diagnosed = form.cleaned_data['last_diagnosed']
                last_suffix = form.cleaned_data['last_suffix']
                duration =  form.cleaned_data['duration']
                duration_suffix = form.cleaned_data['duration_suffix']
                remark =  form.cleaned_data['remark']
                create_complain = Complain.objects.get_or_create(name=complaint.title())
                complain = create_complain[0]
                obj = PatientHistoryNEW(patient=patient,complain=complain,last_diagnosed=last_diagnosed,last_suffix=last_suffix,duration=duration,duration_suffix=duration_suffix,remarks=remark)
                obj.save()
                messages.success(request,f'Successfully Added the Past History')
                return HttpResponseRedirect(reverse('patient_history_newone', kwargs={'case_id': case_id}))
        
        else:
            form = PatientHistoryForm()

        table_data = PatientHistoryNEW.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
        data = Complain.objects.all().order_by(Lower('name'))
        patient_details= Patient.objects.get(id=case_id)



        appoint = Appointment.objects.filter(Q(patientid=patient_details)&Q(date=date.today())).last()
        if appoint.token != 0:
            final_token = appoint.token
        else:
            final_token = appoint.token1

    context = {'user':'D',
               'status':status,
               'case_id':case_id,
               'table':table_data,
                'data':data,
                'patient_details':patient_details,
                'form':form,
                'patient':patient,
                'final_token':final_token
               }

    return render(request,'dashboard/templates/patient_history_newone_adjust.html',context)



def delete_past_history(request,id):

    obj = PatientHistoryNEW.objects.get(id=id)
    obj.delete()
    messages.success(request,f'Past History - {obj.complain} deleted')
    return HttpResponseRedirect(reverse('patient_history_newone', kwargs = {'case_id':obj.patient.id}))

@csrf_exempt
def patient_history_complain(request,case_id,id):

    status = False
    if request.user:
        status = request.user
    complain_name = Complain.objects.get(id=id)
    patient = Patient.objects.get(id=case_id)

    if request.method == 'POST':
        form = PatientHistoryForm(request.POST,initial={'complaint': complain_name})
        if form.is_valid():
            last_diagnosed = form.cleaned_data['last_diagnosed']
            last_suffix = form.cleaned_data['last_suffix']
            duration =  form.cleaned_data['duration']
            duration_suffix = form.cleaned_data['duration_suffix']
            remark =  form.cleaned_data['remark']
            obj = PatientHistoryNEW(patient=patient,complain=complain_name,last_diagnosed=last_diagnosed,
                                last_suffix=last_suffix,duration=duration,duration_suffix=duration_suffix,
                                remarks=remark)
            obj.save()
            messages.success(request,f'Succesfully Added to the Past History ')
            return HttpResponseRedirect(reverse('patient_history_complain',kwargs={'case_id': case_id,'id':id}))

    else:
        form = PatientHistoryForm(initial={'complaint': complain_name})       
        
    table_data = PatientHistoryNEW.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
    data = Complain.objects.all().order_by(Lower('name'))

    appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()
    if appoint.token != 0:
        final_token =  appoint.token
    else:
        final_token = appoint.token1

  

    context = {'user':'D',
               'status':status,
               'case_id':case_id,
               'data':data,
               'complain':complain_name,
               'patient':patient,
               'table':table_data,
               'form':form,
               'final_token':final_token
               }   
    return render(request,'dashboard/templates/patient_history_complain_adjust.html',context)

@csrf_exempt
def add_mental_causative(request,case_id):

    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':
        obj = MentalCausativeNewone(name=request.POST['add_mental_causative'])
        obj.save()
        messages.info(request,"Successfully! added Mental Causative Factor.")
        return HttpResponseRedirect(reverse('add_mental_causative',kwargs={'case_id':case_id}))
    
    data = MentalCausativeNewone.objects.all().order_by(Lower('name'))
    return render(request,'dashboard/templates/add_mental_causative.html',{'user':'D','status':status,
                                                                           'case_id':case_id,'data':data})

@csrf_exempt
def add_mental_personality(request,case_id):

    status = False
    if request.user:
        status=request.user

    if request.method == 'POST':
        obj = MentalPersonalityNewOne(name=request.POST['add_mental_personality'])
        obj.save()
        messages.info(request,"Successfully Added")
        return HttpResponseRedirect(reverse('add_mental_personality',kwargs={'case_id':case_id}))

    data = MentalPersonalityNewOne.objects.all().order_by(Lower('name'))

    
    context = {'user':'D',
               'status':status,
                'case_id':case_id,
                'data':data,                
                }
    return render(request,'dashboard/templates/add_mental_personality.html',context)

@csrf_exempt
def add_complain(request,case_id):

    status = False
    if request.user:
        status = request.user
    if request.method == 'POST':
        obj = Complain(name=request.POST['add_disease'])
        obj.save()
        messages.info(request,"Successfully added")
        return HttpResponseRedirect(reverse('add_complain',kwargs={'case_id':case_id}))
       
    data = Complain.objects.all().order_by(Lower('name'))

    


    context ={'user':'D',
              'status':status,
              'data':data,
              'case_id':case_id,             
              }
    return render(request,'dashboard/templates/add_complain_adjust.html',context)

@csrf_exempt
def delete_newcase(request,id):

    pre_url = request.META.get('HTTP_REFERER')
    print('pre_url---',pre_url,type(pre_url))
    obj = pre_url.split('/')
    print('obj',obj)

    if obj[3] == 'add_complain':
        new_obj = Complain.objects.get(id=id).delete()
        messages.success(request,f"Deleted Successfully!")        
        return HttpResponseRedirect(reverse('add_complain',  kwargs={'case_id':int(obj[4])}))
    elif obj[3] == 'add_disease':
        new_obj = Complain.objects.get(id=id).delete()
        messages.success(request,f"Deleted Successfully!")
        return HttpResponseRedirect(reverse('add_disease_patient_history',  kwargs={'case_id':int(obj[4])}))
    elif obj[3] == 'add_family_complain':
        messages.success(request,f"Deleted Successfully!")
        new_obj = FamilyMedicalComplain.objects.get(id=id).delete()       
        return HttpResponseRedirect(reverse('add_family_complain',  kwargs={'case_id':int(obj[4])}))
    elif obj[3] == 'add_mental_causative':
        messages.success(request,f"Deleted Successfully!")
        new_obj = MentalCausativeNewone.objects.get(id=id).delete()        
        return HttpResponseRedirect(reverse('add_mental_causative',  kwargs={'case_id':int(obj[4])}))
    elif obj[3] == 'add_mental_personality':
        messages.success(request,f"Deleted Successfully!")
        new_obj = MentalPersonalityNewOne.objects.get(id=id).delete()        
        return HttpResponseRedirect(reverse('add_mental_personality',  kwargs={'case_id':int(obj[4])}))
    elif obj[3] == 'BMS_add':
        messages.success(request,f"Deleted Successfully!")
        new_obj = Question1.objects.get(id=id).delete()              
        return HttpResponseRedirect(reverse('bms_add',  kwargs={'case_id':int(obj[4])}))

@csrf_exempt
def add_disease_patient_history(request,case_id):

    status = False
    if request.user:
        status = request.user
    if request.method == 'POST':
        obj = Complain(name=request.POST['add_disease'])
        obj.save()
        messages.info(request,"Successfully added")
        return HttpResponseRedirect(reverse('add_disease_patient_history',kwargs={'case_id':case_id}))
       
    data = Complain.objects.all().order_by(Lower('name'))

    context = {'user':'D',
               'status':status,
               'data':data,
               'case_id':case_id,
               } 
    return render(request,'dashboard/templates/add_disease_patient_history_adjust.html',context)

@csrf_exempt
def add_family_complain(request,case_id):

    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':
        obj = FamilyMedicalComplain(name=request.POST['add_disease'])
        obj.save()
        messages.info(request,"Successfully added")
        return HttpResponseRedirect(reverse('add_family_complain',kwargs={'case_id':case_id}))
    
    data = FamilyMedicalComplain.objects.all().order_by(Lower('name'))
    

    context = {'user':'D',
               'status':status,
               'case_id':case_id,
               'data':data,
               }
    return render(request,'dashboard/templates/add_family_complain_adjust.html',context)



# NOT IN USE (OLD)
@csrf_exempt
def past_history_patient(request,case_id):    
    
    status = False
    if request.user:
        status = request.user   

    if case_id == 0:
        return HttpResponse('<h1>Please Select a Patient to Continue</h1>')
    else: 
        if request.method == "POST":
            patient = Patient.objects.get(id=case_id)
            disease_id = request.POST['diseases']            
            last_diagnosed = request.POST['diagnosed']            
            duration = request.POST['duration']            
            diseases = Diseases.objects.get(id=disease_id)
            obj = PastHistory(patient=patient,disease=diseases,last_diagnose=last_diagnosed,duration=duration)
            obj.save()
            messages.info(request,'Disease added to the Past History')      
            return HttpResponseRedirect(reverse('past_history_patient',  kwargs={'case_id': case_id}))
        
        dis = Diseases.objects.all()
        list_diseases = PastHistory.objects.filter(patient__id = case_id,date = date.today())       
        return render(request,'dashboard/templates/past_history_patient.html',{'user':'D','status':status,'data':dis,'list':list_diseases,'case_id':case_id})

@csrf_exempt
def add_disease(request,case_id):

    print('case_id',case_id)
    status = False
    if request.user:
        status =request.user

    if request.method == "POST":
        disease_name = request.POST['disease']
        obj = Diseases(name=disease_name)
        obj.save()
        messages.info(request,"Added "+ str(disease_name) +" to the list.")
        return HttpResponseRedirect(reverse('past_history_patient',  kwargs={'case_id': case_id}))        

    return render(request,'dashboard/templates/add_disease.html',{'user':'D','status':status})

@csrf_exempt  
def past_history_new(request,case_id):

    print('new_case_id',case_id)
    status = False
    if request.user:
        status = request.user
    
    cat = Category.objects.get(category ='Past History')
    data = Question1.objects.filter(category=cat)

    return render(request,'dashboard/templates/past_history_new.html',{'user':'D','status':status,'data':data,'case_id':case_id})


@csrf_exempt
def past_history(request,id,case_id):

    status = False
    if request.user:
        status = request.user

    print('id--',id)

    if case_id == 0:
        return HttpResponse("<h1>Please select Patient to Continue</h1>") 
    
    else:
        data = Question1.objects.get(id=id)
        if request.method == 'POST':
            if request.POST['question'] == 'show':
                q_id = Question1.objects.get(id=id)
                p_id = Patient.objects.get(id=case_id)
                last_diagnose = request.POST['diagnose']
                duration = request.POST['duration']
                obj = Answer.objects.create(question=q_id,patient=p_id,last_diagnose=last_diagnose.title(),duration=duration.title(),flag=True)
                obj.save()
            else:
                q_id = Question1.objects.get(id=id)
                p_id = Patient.objects.get(id=case_id)
                obj = Answer.objects.create(question=q_id,patient=p_id,last_diagnose="No",duration="No",flag=True)
                obj.save()
            return HttpResponseRedirect(reverse('next_history',kwargs={'id':2,'case_id':case_id}))

    return render(request,'dashboard/templates/past_history_start.html',{'user':'D','status':status,'data':data,'case_id':case_id})


@csrf_exempt    
def next_history(request,id,case_id):

    status = False
    if request.user:
        status = request.user

    try:      
        c_id = Category.objects.get(id=1)        
        data = Question1.objects.get(id=id,category=c_id)        
        ques = Question1.objects.filter(Q(id__gt=id)&Q(category=c_id)).first()
        
        if request.method == 'POST':
            if request.POST['question'] == 'show':
                q_id = Question1.objects.get(id=id)
                p_id = Patient.objects.get(id=case_id)
                last_diagnose = request.POST['diagnose']
                duration = request.POST['duration']
                obj = Answer.objects.create(question=q_id,patient=p_id,last_diagnose=last_diagnose.title(),duration=duration.title(),flag=True)
                obj.save()
            else:
                q_id = Question1.objects.get(id=id)
                p_id = Patient.objects.get(id=case_id)
                obj = Answer.objects.create(question=q_id,patient=p_id,last_diagnose="No",duration="No",flag=True)
                obj.save()

            try:            
                return HttpResponseRedirect(reverse('next_history',kwargs={'id':ques.id,'case_id':case_id}))
            except:
                return HttpResponseRedirect(reverse('next_history',kwargs={'id':id+1,'case_id':case_id}))               
    except:                
        data = ""



    return render(request,'dashboard/templates/past_history_next.html',{'user':'D','status':status,'data':data,'case_id':case_id})



#PDF
@csrf_exempt
def casehistory_pdf(request,id):

    # data = ExampleModel.objects.filter(patient_id = id)
    data1 = ExampleModel.objects.filter(patient_id=id).last()
    if data1:
    # print('last case####',data1)    
        response = HttpResponse(content_type = 'application/pdf')
        response['Content-Disposition'] = 'filename="Case.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer,pagesize=A4)
        letter_head = "./dashboard/document/newcase.jpg"
        p.drawImage(letter_head,0,0,width=600,height=880)
        p.setFont("Helvetica", 18)
        # for d in data:
            # signature_path =draw_signature(d.signature, as_file=True)
            # p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')
        signature_path =draw_signature(data1.signature, as_file=True)
        p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        p.showPage()    

        p.save()
        p = buffer.getvalue()
        buffer.close()
        response.write(p)
        return response
    else:
        return HttpResponse('<h1> No Case History as of Now. Go Back to Create One. </h1>')

@csrf_exempt
def gen_pdf(request,case_id):

    date1 = date.today()
    data1 = Answer.objects.filter(Q(patient_id=case_id)&Q(date=date1))
    data = JSModel.objects.filter(Q(patient_id =case_id)&Q(signature_date__contains=date1)) 
    # print('data',data)

    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'filename="NewCase.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    

    letter_head = "./dashboard/document/newcase.jpg"
    blank_page =   "./dashboard/document/blankpage.jpg"

    # PAGE 1

    p.drawImage(letter_head,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(200,675,'PAST HISTORY')
    p.drawString(200,674,'_____________')

    for d in data1:
        if d.question_id == 1:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 630,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,600,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,570,"Duration: "+d.duration)
        elif d.question_id == 2:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 3:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 4:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)


    p.showPage()

    #PAGE 2

    p.drawImage(blank_page,0,0,width=600,height=880)
    for d in data1:
        if d.question_id == 5:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 6:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 7:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 8:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)
    p.showPage()

    # PAGE 3

    p.drawImage(blank_page,0,0,width=600,height=880)
    for d in data1:
        if d.question_id == 9:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 10:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 11:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 12:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)
    p.showPage()

    # PAGE 4

    p.drawImage(blank_page,0,0,width=600,height=880)

    for d in data1:
        if d.question_id == 13:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 14:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 15:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 16:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)

    p.showPage()
    
    # PAGE 5

    p.drawImage(blank_page,0,0,width=600,height=880)

    for d in data1:
        if d.question_id == 17:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 18:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 19:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 20:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)

    p.showPage()


    # PAGE 6

    p.drawImage(blank_page,0,0,width=600,height=880)

    for d in data1:
        if d.question_id == 21:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 22:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 23:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 24:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)

    p.showPage()

    # PAGE 7

    p.drawImage(blank_page,0,0,width=600,height=880)

    for d in data1:
        if d.question_id == 25:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 26:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 27:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 28:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)

    p.showPage()

    # PAGE 8

    p.drawImage(blank_page,0,0,width=600,height=880)

    for d in data1:
        if d.question_id == 29:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 30:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 31:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 32:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)

    p.showPage()

    # PAGE 9

    p.drawImage(blank_page,0,0,width=600,height=880)

    for d in data1:
        if d.question_id == 33:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 34:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 35:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 36:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)

    p.showPage()

    # PAGE 10

    p.drawImage(blank_page,0,0,width=600,height=880)

    for d in data1:
        if d.question_id == 37:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 38:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 39:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 40:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)   

    p.showPage()


    # PAGE 11

    p.drawImage(blank_page,0,0,width=600,height=880)

    for d in data1:
        if d.question_id == 41:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 42:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 43:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 44:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)   

    p.showPage()

    # PAGE 12

    p.drawImage(blank_page,0,0,width=600,height=880)

    for d in data1:
        if d.question_id == 45:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 650,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,620,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,590,"Duration: "+d.duration)
        elif d.question_id == 46:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 530,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,500,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,470,"Duration: "+d.duration)
        elif d.question_id == 47:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 410,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,380,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,350,"Duration: "+d.duration)
        elif d.question_id == 48:
            ques = str(d.question)
            p.setFont("Helvetica", 18)
            p.drawString(35, 290,"Q. " +ques)
            p.setFont("Helvetica", 14)
            p.drawString(70,260,"Last Diagnosed: "+d.last_diagnose)
            p.drawString(70,230,"Duration: "+d.duration)   

    p.showPage()

    # PAGE 13

    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(200,675,'PERSONAL APPETITE')
    p.drawString(200,674,'___________________')
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 49:
            ques =str(d.question)
            p.drawString(35, 650,"Q. " +ques[:72])
            p.drawString(45, 625,ques[72:150])
            p.drawString(45, 600,ques[150:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')
        
        elif d.question_id == 50:
            ques =str(d.question)
            p.drawString(35, 410,"Q. " +ques[:72])
            p.drawString(45, 385,ques[72:150])
            p.drawString(45, 360,ques[150:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')    

    p.showPage()

    # PAGE 14
    
    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 51:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 52:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:73])
            p.drawString(45, 385,ques[73:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    p.showPage()

    # PAGE 15

    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(200,675,'SEXUAL HISTORY')
    p.drawString(200,674,'________________')
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 53:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 54:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:73])
            p.drawString(45, 385,ques[73:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

# PAGE 16

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 55:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 56:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()


# PAGE 17

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 57:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 58:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

# PAGE 18

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 59:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 60:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

    # PAGE 19

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 61:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 62:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

    # PAGE 20

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 63:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 64:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

    # PAGE 21

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 65:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 66:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

    # PAGE 22

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 67:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 68:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()


    # PAGE 23

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 69:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 70:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()


    # PAGE 24

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 71:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 72:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

    # PAGE 25

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 73:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 74:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

    # PAGE 26

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 75:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 76:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()


    # PAGE 27

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 77:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 78:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

    # PAGE 28

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 79:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 80:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

# PAGE 29

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 81:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 82:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()


# PAGE 30

    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(200,675,'FEAR AND INCIDENTS')
    p.drawString(200,674,'___________________')
    p.setFont("Helvetica", 14)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 83:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 84:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()


# PAGE 31

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 85:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 86:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

# PAGE 32

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 87:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')   

    p.showPage()


    # PAGE 33

    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(200,675,'THERMAL REACTION')
    p.drawString(200,674,'________________')
    p.setFont("Helvetica", 14)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 88:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 89:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()


# PAGE 34

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 90:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 91:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

# PAGE 35

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 92:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 93:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

# PAGE 36

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 94:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 95:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:75])
            p.drawString(45, 385,ques[75:154])
            p.drawString(45, 360,ques[154:235]) 
            p.drawString(45, 340,ques[235:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

# PAGE 37

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 96:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 97:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:75])
            p.drawString(45, 385,ques[75:154])
            p.drawString(45, 360,ques[154:235]) 
            p.drawString(45, 340,ques[235:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()

# PAGE 38

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 98:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')    

    p.showPage()

 # PAGE 39

    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(200,675,'INVESTIGATION')
    p.drawString(200,674,'______________')
    p.setFont("Helvetica", 14)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 99:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 100:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()




    # PAGE 40

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 101:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')   

    p.showPage()


# PAGE 41

    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(200,675,'Chief Complaints')
    p.drawString(200,674,'______________')
    p.setFont("Helvetica", 14)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 102:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 103:
            ques =str(d.question)

            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    

    p.showPage()


 # PAGE 42

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 14)
    for d in data:
        if d.question_id == 104:
            ques =str(d.question)
            # ques = str(Question.objects.get(id=51))
            p.drawString(35, 650,"Q. " +ques[:76])
            p.drawString(45, 625,ques[76:156])
            p.drawString(45, 600,ques[156:])
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')

        elif d.question_id == 105: 

            ques =str(d.question)
            # ques = str(Question.objects.get(id=52))
            p.drawString(35, 410,"Q. " +ques[:74])
            p.drawString(45, 385,ques[74:153])
            p.drawString(45, 360,ques[153:]) 
            signature_path =draw_signature(d.signature, as_file=True)
            p.drawImage(signature_path,50,220,width=500,height=135,mask='auto')

    p.showPage()


    data2 = PersonalHabit.objects.filter(Q(patient_id=case_id)&Q(date=date1))
    # print('data2',data2)
# PAGE 43
    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(200,675,'Personal Habits')
    p.drawString(200,674,'_____________')
    p.setFont("Helvetica", 16)
    for d in data2:
        p.drawString(45,630,"Weather-Hot  :     "+ d.weather_hot)
        p.drawString(45,600,"Weather-Cold :     "+ d.weather_cold)
        p.drawString(45,570,"Weather-Rainy :     "+ d.weather_rainy)
        p.drawString(45,540,"Weather-Humid :     "+ d.weather_humid)
        p.drawString(45,510,"Weather-dry :     "+ d.weather_dry)
        p.drawString(45,480,"Getting-wet :     "+ d.getting_wet)
        p.drawString(45,450,"Weather -Open Air:   "+d.weather_open_air)
        p.drawString(45,420,"Weather-Wind:   "+d.weather_wind)
        p.drawString(45,390,"Weather-Seashore:   "+d.weather_seashore)
        p.drawString(45,360,"Weather-Noise:   "+d.weather_noise)
        p.drawString(45,330,"Weather-Light:   "+d.weather_light)
        p.drawString(45,300,"Weather-Strong Smell:   "+d.weather_strong_smell)
        p.drawString(45,270,"Weather-Dust:   "+d.weather_dust)
        p.drawString(45,240,"Weather-Smoke:   "+d.weather_smoke)   
    
    p.showPage()

    # PAGE 44

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 16)
    for d in data2:
        p.drawString(45,660,"Weather-Before  :     "+ d.weather_before)
        p.drawString(45,630,"Weather-During  :     "+ d.weather_during)
        p.drawString(45,600,"Weather-After Periods :     "+ d.weather_after_period)
        p.drawString(45,570,"Weather-Touch :     "+ d.weather_touch)
        p.drawString(45,540,"Weather-Masssage :     "+ d.weather_massage)
        p.drawString(45,510,"Weather-Pressure :     "+ d.weather_pressure)
        p.drawString(45,480,"Weather- Small CLosed Place :     "+ d.weather_small_closed_place)
        p.drawString(45,450,"Weather -Crowds:   "+d.weather_crowds)
        p.drawString(45,420,"Weather-Tight Clothes:   "+d.weather_tight_clothes)
        p.drawString(45,390,"Weather-Exams:   "+d.weather_exams)
        p.drawString(45,360,"Weather-Interviews:      "+d.weather_interview)
        p.drawString(45,330,"Weather-Imp Apppointment:   "+d.weather_appointment)
        p.drawString(45,300,"Weather-Exercise:   "+d.weather_exercise)
        p.drawString(45,270,"Weather-Exertion:   "+d.weather_exertion)
        p.drawString(45,240,"Weather-Walk:   "+d.weather_walk)
        p.drawString(45,210,"Weather-Running:   "+d.weather_running)                 
    
    p.showPage()


 # PAGE 45

    p.drawImage(blank_page,0,0,width=600,height=880)
    
    p.setFont("Helvetica", 16)
    for d in data2:
        p.drawString(45,660,"Weather-Full Moon:   "+ d.weather_full_moon)
        p.drawString(45,630,"Weather-New Moon:   "+d.weather_new_moon)
        p.drawString(45,600,"Weather-Sun:   "+ d.weather_sun)
        p.drawString(45,570,"Weather-Change:   "+ d.weather_change)            
    
    p.showPage()

    data3 = InFood.objects.filter(Q(patient_id=case_id)&Q(date=date1))

# PAGE 46
    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(150,675,'Likes and Dislikes In Food')
    p.drawString(150,674,'_____________________')
    p.setFont("Helvetica", 16)
    for d in data3:
        p.drawString(45,630,"Sweet  :     "+ d.sweet)
        p.drawString(45,600,"Bitter :     "+ d.bitter)
        p.drawString(45,570,"Bread :     "+ d.bread)
        p.drawString(45,540,"Eggs :     "+ d.eggs)
        p.drawString(45,510,"Cold Foods Or Drinks :     "+ d.cold_drinks)
        p.drawString(45,480,"Chocolates :     "+ d.chocolates)
        p.drawString(45,450,"Mud, Chalk ,Paper :   "+d.mud_chalk_paper)
        p.drawString(45,420,"Salty/Salt:   "+d.salt)
        p.drawString(45,390,"Fats , Fried Food:   "+d.fat)
        p.drawString(45,360,"Butter:   "+d.butter)
        p.drawString(45,330,"Meat:   "+d.meat)
        p.drawString(45,300,"Warm Food or Drinks:   "+d.warm_food_drinks)
        p.drawString(45,270,"Fruits:   "+d.fruits)
        p.drawString(45,240,"Tobbacco/Pan:   "+d.pan)


    p.showPage()

# PAGE 47
    p.drawImage(blank_page,0,0,width=600,height=880)    
    p.setFont("Helvetica", 16)
    for d in data3:
        p.drawString(45,660,"Sour  :     "+ d.sour)
        p.drawString(45,630,"Raw Salads :     "+ d.raw_salad)
        p.drawString(45,600,"Snacks :     "+ d.snack)
        p.drawString(45,570,"Fish :     "+ d.fish)
        p.drawString(45,540,"Cold Foods Or Drinks :     "+ d.cold_drinks)
        p.drawString(45,510,"Juices :     "+ d.juice)
        p.drawString(45,480,"Ice-Cream/Ice :   "+d.ice_cream)
        p.drawString(45,450,"Spicy:   "+d.spicy)
        p.drawString(45,420,"Vegetables:   "+d.vegetables)
        p.drawString(45,390,"Cheese:   "+d.cheese)
        p.drawString(45,360,"Onions:   "+d.onions)
        p.drawString(45,330,"Garlic:   "+d.garlic)
        p.drawString(45,300,"Milk:   "+d.milk)
        p.drawString(45,270,"Alcohol:   "+d.alcohol)
        p.drawString(45,240,"Smoking:   "+d.smoking)
        p.drawString(45,210,"Any Other:   "+d.any_other)
        



    p.showPage()

    data4 = MentalCausative.objects.filter(Q(patient_id=case_id)&Q(date=date1))
    print('data4--',data4)
    for d in data4:
        print(d.abandonment,d.abusive_husband)

# PAGE 48

    p.drawImage(blank_page,0,0,width=600,height=880)
    p.setFont("Helvetica", 18)
    p.drawString(150,675,'Mental Causative Factor')
    p.drawString(150,674,'____________________')
    p.setFont("Helvetica", 14)
    for d in data4:
        if d.abandonment != None: 
            p.drawString(45,630, d.abandonment)
        if d.abusive_husband != None: 
            p.drawString(45,610, d.abusive_husband)
        if d.abusive_parents != None: 
            p.drawString(45,590, d.abusive_parents)
        if d.after_anger != None: 
            p.drawString(45,570, d.after_anger)
        if d.anticipation != None: 
            p.drawString(45,550, d.anticipation)
        if d.anxiety != None: 
            p.drawString(45,610, d.anxiety)
        if d.abused_punishment != None: 
            p.drawString(45,610, d.abused_punishment)
        if d.apprehends!= None: 
            p.drawString(45,610, d.apprehends)
        

    
    


    
    
    p.showPage()


    








    p.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response


from django.views import generic
from django.urls import reverse_lazy
# JSignature


@method_decorator(csrf_exempt, name='dispatch')
class JSCreateView(generic.CreateView):
    model = JSModel
    fields = '__all__'


    def get_success_url(self): 
              

        category = Question1.objects.get(id=self.object.question_id).category

        
        if str(category) == 'Origin of Cause':
            c_id = Category.objects.get(id=8)
            data = Question1.objects.filter(Q(id__gt=self.object.question_id) & Q(category=c_id)).first()

            try:                
                return reverse_lazy('next1',kwargs= {'id':data.id,'case_id':self.object.patient_id})
            except:
                return reverse_lazy('next1',kwargs= {'id':self.object.question_id+1,'case_id':self.object.patient_id})
            
        elif str(category) == 'Sexual History':

            c_id = Category.objects.get(id=3)
            data = Question1.objects.filter(Q(id__gt=self.object.question_id) & Q(category=c_id)).first()

            try:
                return reverse_lazy('next2',kwargs= {'id':data.id,'case_id':self.object.patient_id})
            except:
                return reverse_lazy('next2',kwargs= {'id':self.object.question_id+1,'case_id':self.object.patient_id})
            
        elif str(category) == 'Temperament':

            c_id = Category.objects.get(id=4)
            data = Question1.objects.filter(Q(id__gt=self.object.question_id) & Q(category=c_id)).first()

            try:
                return reverse_lazy('next3',kwargs= {'id':data.id,'case_id':self.object.patient_id})
            except:
                return reverse_lazy('next3',kwargs= {'id':self.object.question_id+1,'case_id':self.object.patient_id})
        
        elif str(category) == 'Thermal Reaction':

            c_id = Category.objects.get(id=5)
            data = Question1.objects.filter(Q(id__gt=self.object.question_id) & Q(category=c_id)).first()

            try:
                return reverse_lazy('next4',kwargs= {'id':data.id,'case_id':self.object.patient_id})
            except:
                return reverse_lazy('next4',kwargs= {'id':self.object.question_id+1,'case_id':self.object.patient_id})
        
        elif str(category) == 'Investigation':

            c_id = Category.objects.get(id=6)
            data = Question1.objects.filter(Q(id__gt=self.object.question_id) & Q(category=c_id)).first()

            try:
                return reverse_lazy('next5',kwargs= {'id':data.id,'case_id':self.object.patient_id})
            except:
                return reverse_lazy('next5',kwargs= {'id':self.object.question_id+1,'case_id':self.object.patient_id})
            
        elif str(category) == 'Chief Complaints':

            c_id = Category.objects.get(id=7)
            data = Question1.objects.filter(Q(id__gt=self.object.question_id) & Q(category=c_id)).first()

            try:
                return reverse_lazy('next6',kwargs= {'id':data.id,'case_id':self.object.patient_id})
            except:
                return reverse_lazy('next6',kwargs= {'id':self.object.question_id+1,'case_id':self.object.patient_id})
        elif str(category) == 'Personal History':

            c_id = Category.objects.get(id=9)
            data = Question1.objects.filter(Q(id__gt=self.object.question_id) & Q(category=c_id)).first()

            try:
                return reverse_lazy('next7',kwargs= {'id':data.id,'case_id':self.object.patient_id})
            except:
                return reverse_lazy('next7',kwargs= {'id':self.object.question_id+1,'case_id':self.object.patient_id})



@csrf_exempt
def personal_appetite(request,id,case_id):

    status = False
    if request.user:
        status = request.user

    print('case',case_id)
    if case_id == 0:
        return HttpResponse(" <h1>  Please select Patient to Continue </h1>")
    else:
        c_id = Category.objects.get(id=8)
        data = Question1.objects.get(id=49,category=c_id)
        instance = Question1.objects.get(id=49,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})

        return render(request,'dashboard/personal_appetite.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})
    
@csrf_exempt
def next1(request,id,case_id):

    status = False
    if request.user:
        status = request.user
    
    print("id---",id)
    try:
        c_id = Category.objects.get(id=8)
        data = Question1.objects.get(id=id,category=c_id)
        instance = Question1.objects.get(id=id,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})
    except:
        form = JSForm()
        data = ""

    return render(request,'dashboard/next1.html',{'user':'D','status':status,'form':form,'data':data,'case_id':case_id})

prescription,Stock
def sex_history(request,id,case_id):

    status = False
    if request.user:
        status = request.user

    if case_id == 0:
        return HttpResponse("<h1>Please select Patient to Continue</h1>")
    else:

        c_id = Category.objects.get(id=3)
        data = Question1.objects.get(id=53,category=c_id)
        instance = Question1.objects.get(id=53,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})

        return render(request,'dashboard/sex_history.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})
    

def next2(request,id,case_id):

    status = False
    if request.user:
        status = request.user
    
    try:
        c_id = Category.objects.get(id=3)
        data = Question1.objects.get(id=id,category=c_id)  
        print('data',data)      
        instance = Question1.objects.get(id=id,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})
    except:
        form = JSForm()
        data = ""

    
    return render(request,'dashboard/next2.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})


def mental_personality(request,id,case_id):

    
    status = False
    if request.user:
        status = request.user    
    
    if case_id == 0:
        return HttpResponse("<h1>Please select Patient to Continue</h1>")
    
    else:

        c_id = Category.objects.get(id=4)
        data = Question1.objects.get(id=83,category=c_id)
        instance = Question1.objects.get(id=83,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})

        return render(request,'dashboard/mental_personality.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})

def next3(request,id,case_id):

    status = False
    if request.user:
        status = request.user
    
    try:
        c_id = Category.objects.get(id=4)
        data = Question1.objects.get(id=id,category=c_id)
        instance = Question1.objects.get(id=id,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})
    except:
        form = JSForm()
        data = ""

    return render(request,'dashboard/next3.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})

def thermal_reaction(request,id,case_id):

    status = False
    if request.user:
        status = request.user    
    
    if case_id == 0:
        return HttpResponse("<h1>Please select Patient to Continue</h1>")
    
    else:

        c_id = Category.objects.get(id=5)
        data = Question1.objects.get(id=88,category=c_id)
        instance = Question1.objects.get(id=88,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})

        return render(request,'dashboard/thermal_reaction.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})

def next4(request,id,case_id):

    status = False
    if request.user:
        status = request.user
    
    try:
        c_id = Category.objects.get(id=5)
        data = Question1.objects.get(id=id,category=c_id)
        instance = Question1.objects.get(id=id,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})
    except:
        form = JSForm()
        data = ""

    return render(request,'dashboard/next4.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})


def investigation(request,id,case_id):

    status = False
    if request.user:
        status = request.user    
    
    if case_id == 0:
        return HttpResponse("<h1>Please select Patient to Continue</h1>")
    
    else:

        c_id = Category.objects.get(id=6)
        data = Question1.objects.get(id=99,category=c_id)
        instance = Question1.objects.get(id=99,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})

        return render(request,'dashboard/investigation.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})


def next5(request,id,case_id):

    status = False
    if request.user:
        status = request.user
    
    try:
        c_id = Category.objects.get(id=6)
        data = Question1.objects.get(id=id,category=c_id)
        instance = Question1.objects.get(id=id,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})
    except:
        form = JSForm()
        data = ""

    return render(request,'dashboard/next5.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})

def chief_complaints(request,id,case_id):

    status = False
    if request.user:
        status = request.user    
    
    if case_id == 0:
        return HttpResponse('<h1> Please Select a Patient to Continue </h1>')
    
    else:

        c_id = Category.objects.get(id=7)
        data = Question1.objects.get(id=102,category=c_id)
        instance = Question1.objects.get(id=102,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})

        return render(request,'dashboard/chief_complaints.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})
    


def next6(request,id,case_id):

    status = False
    if request.user:
        status = request.user
    
    try:
        c_id = Category.objects.get(id=7)
        data = Question1.objects.get(id=id,category=c_id)
        instance = Question1.objects.get(id=id,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})
    except:
        form = JSForm()
        data = ""

    return render(request,'dashboard/next6.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})


def patient_personal_history(request,id,case_id):

    status = False
    if request.user:
        status = request.user
    
    if case_id == 0:
        return HttpResponse('<h1> Please Select a Patient to Continue </h1>')
    else:
        c_id = Category.objects.get(id=9)
        print('category',c_id)
        data = Question1.objects.get(id=107,category=c_id)
        instance = Question1.objects.get(id=107,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})

        return render(request,'dashboard/patient_personal_history.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})

def next7(request,id,case_id):

    status = False
    if request.user:
        status = request.user
    
    try:
        c_id = Category.objects.get(id=9)
        data = Question1.objects.get(id=id,category=c_id)
        instance = Question1.objects.get(id=id,category=c_id)
        instance1 = Patient.objects.get(id=case_id)
        form = JSForm(initial= {'question': instance,'patient':instance1})
    except:
        form = JSForm()
        data = ""

    return render(request,'dashboard/next7.html',{'user':'D','status':status,'form':form,'id':id,'data':data,'case_id':case_id})

def personal_new_habits(request,case_id):
   
    status = False
    if request.user:
        status = request.user

    if case_id == 0:
        return HttpResponse('<h1>Please Select a Patient to Continue</h1>')

    else:
        if request.method == "POST":
            p_id = Patient.objects.get(id=case_id)        
            desire = request.POST['desire']        
            aversion = request.POST['aversion']        
            appetite = request.POST['appetite']        
            thirst = request.POST['thirst']        
            stool = request.POST['stool']        
            urine = request.POST['urine']        
            sleep = request.POST['sleep']        
            dreams = request.POST['dreams']        
            obj = PersonalHabitNew(patient=p_id,desire=desire,aversion=aversion,appetite=appetite,thirst=thirst,stool=stool,urine=urine,sleep=sleep,dreams=dreams)
            obj.save()
            messages.info(request,'Personal Habit Section Done')
            return redirect('newcase')
        return render(request,'dashboard/templates/personal_new_habit.html',{'status':status,'user':'D'}) 

def personal_habits(request,case_id):

    status=False
    if request.user:
        status = request.user

    if request.method == 'POST':
        print('pr',request.POST['weather_hot'])
        p_id = Patient.objects.get(id=case_id)
        print('p_id',p_id)
        w_hot = request.POST['weather_hot']
        w_cold = request.POST['weather_cold']
        w_rainy = request.POST['weather_rainy']
        w_humid = request.POST['weather_humid']
        w_dry = request.POST['weather_dry']
        g_wet = request.POST['getting_wet']
        w_open_air = request.POST['weather_open_air']
        w_wind = request.POST['weather_wind']
        w_seashore = request.POST['weather_seashore']
        w_noise = request.POST['weather_noise']
        w_light = request.POST['weather_light']
        w_strong_smell = request.POST['weather_strong_smell']
        w_dust = request.POST['weather_dust']
        w_smoke = request.POST['weather_smoke']
        w_before = request.POST['weather_before']
        w_during = request.POST['weather_during']
        w_after_periods = request.POST['weather_after_periods']
        w_touch = request.POST['weather_touch']
        w_massage = request.POST['weather_massage']
        w_pressure = request.POST['weather_pressure']
        w_small_closed_place = request.POST['weather_small_closed_place']
        w_crowds = request.POST['weather_crowds']
        w_tight_clothes = request.POST['weather_tight_clothes']
        w_exams = request.POST['weather_exams']
        w_interviews = request.POST['weather_interviews']
        w_imp = request.POST['weather_imp']
        w_exercise = request.POST['weather_exercise']
        w_exertion = request.POST['weather_exertion']
        w_walk = request.POST['weather_walk']
        w_running = request.POST['weather_running']
        w_full_moon = request.POST['weather_full_moon']
        w_new_moon = request.POST['weather_new_moon']
        w_sun = request.POST['weather_sun']
        w_change = request.POST['weather_change']
        
        obj = PersonalHabit.objects.create(patient=p_id,weather_hot=w_hot,weather_cold=w_cold,weather_rainy=w_rainy,
                                           weather_humid=w_humid,weather_dry=w_dry,getting_wet=g_wet,weather_open_air=w_open_air,
                                           weather_wind=w_wind,weather_seashore=w_seashore,weather_noise=w_noise,weather_light=w_light,
                                           weather_strong_smell=w_strong_smell,weather_dust=w_dust,weather_smoke=w_smoke,weather_before=w_before,
                                           weather_during=w_during,weather_after_period=w_after_periods,weather_touch=w_touch,weather_massage=w_massage,
                                           weather_pressure=w_pressure,weather_small_closed_place=w_small_closed_place,
                                           weather_crowds=w_crowds,weather_tight_clothes=w_tight_clothes,weather_exams=w_exams,
                                           weather_interview=w_interviews,weather_appointment=w_imp,weather_exercise=w_exercise,
                                           weather_exertion=w_exertion,weather_walk=w_walk,weather_running=w_running,weather_full_moon=w_full_moon,
                                           weather_new_moon=w_new_moon,weather_sun=w_sun,weather_change=w_change,date=date.today())
        obj.save()  
        messages.info(request,'Personal Habit Section Done')      
        return HttpResponseRedirect(reverse('personal_habits',  kwargs={'case_id': case_id}))



    return render(request,'dashboard/templates/personal_habit.html',{'status':status,'user':'D'})


def In_Food(request,case_id):

    status = False
    if request.user:
        status = request.user

    if case_id == 0:
        return HttpResponse('<h1>Please Select a Patient to Continue</h1>')

    if request.method == 'POST':
        p_id = Patient.objects.get(id=case_id)
        print('patient---',p_id)
        sweet = request.POST['Sweet']
        bitter = request.POST['Bitter']
        bread = request.POST['Bread']
        eggs = request.POST['Eggs']
        cold_drinks = request.POST['cold']
        chocolates = request.POST['Chocolates']
        mud_chalk_paper = request.POST['mud']
        salt = request.POST['Salty']
        fat = request.POST['fat']
        butter =request.POST['Butter']
        meat = request.POST['Meat']
        warm_food_drinks =  request.POST['warm']
        fruits = request.POST['Fruits']
        pan = request.POST['pan']
        sour = request.POST['Sour']
        raw_salad = request.POST['raw_salad']
        snack= request.POST['Snacks']
        fish= request.POST['Fish']
        juice = request.POST['Juices']
        ice_cream = request.POST['ice_cream']
        spicy = request.POST['Spicy']
        vegetables = request.POST['Vegetables']
        cheese = request.POST['Cheese']
        onions= request.POST['Onions']
        garlic= request.POST['Garlic']
        milk = request.POST['Milk']
        alcohol = request.POST['Alcohol']
        smoking = request.POST['Smoking']
        any_other = request.POST['any_other']       
        
        obj = InFood.objects.create(patient=p_id,sweet=sweet,bitter=bitter,bread=bread,eggs=eggs,
                    cold_drinks=cold_drinks,chocolates=chocolates,
                    mud_chalk_paper=mud_chalk_paper,salt=salt,fat=fat,butter=butter,meat=meat,
                    warm_food_drinks=warm_food_drinks,fruits=fruits,pan=pan,sour=sour,
                    raw_salad=raw_salad,snack=snack,fish=fish,juice=juice,ice_cream =ice_cream,
                    spicy=spicy,vegetables=vegetables,cheese=cheese,onions=onions,garlic=garlic,
                    milk=milk,alcohol=alcohol,smoking =smoking,any_other=any_other)
        obj.save()
        messages.info(request,'Likes and Dislikes In Food Section Done')      
        return HttpResponseRedirect(reverse('InFood',  kwargs={'case_id': case_id}))


    
    return render(request,'dashboard/templates/In_Food.html',{'status':status,'user':'D'})


def mental_causative(request,case_id):

    status = False
    if request.user:
        status = request.user
    
    if case_id == 0:
        return HttpResponse('<h1>Please Select a Patient to Continue</h1>')
    else:

        if request.method == 'POST':

            p_id = Patient.objects.get(id=case_id)

            
            if 'abandonment' in request.POST:
                abandonment = request.POST['abandonment']
            else:
                abandonment = None
            if 'abusive_husband' in request.POST:
                abusive_husband = request.POST['abusive_husband']
            else:
                abusive_husband = None
            if 'abusive_parents' in request.POST:        
                abusive_parents = request.POST['abusive_parents']
            else:
                abusive_parents= None
            if 'after_anger' in request.POST:
                after_anger = request.POST['after_anger']
            else:
                after_anger = None
            if 'anticipation' in request.POST:
                anticipation = request.POST['anticipation']
            else:
                anticipation = None
            if 'anxiety' in request.POST:
                anxiety = request.POST['anxiety']
            else:
                anxiety = None
            if 'abused_by_punishment' in request.POST:
                abused_punishment = request.POST['abused_by_punishment']
            else:
                abused_punishment = None
            if 'apprehends' in request.POST:
                apprehends = request.POST['apprehends']
            else:
                apprehends = None
            if 'bad_tragedies' in request.POST:
                bad_tragedies = request.POST['bad_tragedies']
            else:
                bad_tragedies = None
            if 'bereavement' in request.POST:
                bereavement = request.POST['bereavement']
            else:
                bereavement= None
            if 'boredom' in request.POST:
                boredom = request.POST['boredom']
            else:
                boredom = None
            if 'business' in request.POST:
                business = request.POST['business']
            else:
                business = None
            if 'blows' in request.POST:
                blows = request.POST['blows']
            else:
                blows = None
            if 'beatings' in request.POST:
                beatings = request.POST['beatings']
            else:
                beatings = None
            if 'bad_news' in request.POST:
                bad_news = request.POST['bad_news']
            else:
                bad_news=None
            if 'bored' in request.POST:
                bored = request.POST['bored']
            else:
                bored = None
            if 'contradiction' in request.POST:
                contradiction = request.POST['contradiction']
            else:
                contradiction = None
            if 'criticism' in request.POST:
                criticism = request.POST['criticism']
            else:
                criticism = None
            if 'deceived_friendship' in request.POST:
                deceived_friendship = request.POST['deceived_friendship'] 
            else:
                deceived_friendship=None
            if 'depressing_emotion' in request.POST:
                depressing_emotion = request.POST['depressing_emotion']
            else:
                depressing_emotion = None
            if 'disagreement' in request.POST: 
                disagreement = request.POST['disagreement']
            else:
                disagreement = None
            if 'discord_chief' in request.POST:
                discord_chief = request.POST['discord_chief'] 
            else:
                discord_chief = None
            if 'discord_friends' in request.POST:
                discord_friends = request.POST['discord_friends']
            else:
                discord_friends = None
            if 'discord_parents_children' in request.POST:
                discord_parents_children = request.POST['discord_parents_children']
            else:
                discord_parents_children = None
            if 'domination_colonisation' in request.POST:
                domination_colonisation = request.POST['domination_colonisation']
            else:
                domination_colonisation = None
            if 'domination_parental' in request.POST:
                domination_parental = request.POST['domination_parental']
            else:
                domination_parental = None
            if 'domination' in request.POST:
                domination = request.POST['domination']
            else:
                domination = None
            if 'demand_fullfillment' in request.POST:
                demand_fullfillment = request.POST['demand_fullfillment']
            else:
                demand_fullfillment = None
            if 'embarrassment' in request.POST: 
                embarrassment = request.POST['embarrassment']
            else:
                embarrassment = None
            if 'excitement' in request.POST:
                excitement = request.POST['excitement']
            else:
                excitement = None
            if 'emotional' in request.POST:
                emotional = request.POST['emotional']
            else:
                emotional = None
            if 'excitement_business' in request.POST:
                excitement_business = request.POST['excitement_business']
            else:
                excitement_business = None
            if 'fail_business' in request.POST:
                fail_business = request.POST['fail_business']
            else:
                fail_business = None
            if 'failure' in request.POST:
                failure = request.POST['failure']
            else:
                failure = None
            if 'fear' in request.POST:
                fear = request.POST['fear']
            else:
                fear = None
            if 'feeling_controlled' in request.POST:
                feelings_controlled = request.POST['feeling_controlled']
            else:
                feelings_controlled = None
            if 'friendship_deceived' in request.POST:
                friendship_deceived = request.POST['friendship_deceived']
            else:
                friendship_deceived = None
            if 'fright' in request.POST:
                fright = request.POST['fright']
            else:
                fright = None
            if 'frustration' in request.POST:
                frustration = request.POST['frustration']
            else:
                frustration = None
            if 'grief_long_drawn' in request.POST:
                grief_long_drawn = request.POST['grief_long_drawn']
            else:
                grief_long_drawn = None
            if 'grudges' in request.POST:
                grudges = request.POST['grudges']
            else:
                grudges = None
            if 'guilt_trapped' in request.POST:
                guilt_trapped = request.POST['guilt_trapped']
            else:
                guilt_trapped = None
            if 'honour_wounded' in request.POST:
                honour_wounded =  request.POST['honour_wounded']
            else:
                honour_wounded = None
            if 'humiliation' in request.POST:    
                humiliation = request.POST['humiliation']
            else:
                humiliation = None
            if 'humiliation_criticised' in request.POST:
                humiliation_criticised =request.POST['humiliation_criticised']
            else:
                humiliation_criticised = None
            if 'horrible_stories' in request.POST:
                horrible_stories = request.POST['horrible_stories']
            else:
                horrible_stories = None
            if 'indulgence' in request.POST:
                indulgence = request.POST['indulgence']
            else:
                indulgence = None
            if 'insecurity_children' in request.POST:
                insecurity_children = request.POST['insecurity_children']
            else:
                insecurity_children = None
            if 'isolation' in request.POST:
                isolation = request.POST['isolation']
            else:
                isolation = None
            if 'introvert' in request.POST:
                introvert = request.POST['introvert']
            else:
                introvert = None
            if 'irritable' in request.POST:
                irritable = request.POST['irritable']
            else:
                irritable= None
            if 'jealous_professional' in request.POST:
                jealous_professional = request.POST['jealous_professional']
            else:
                jealous_professional = None
            if 'joy' in request.POST:
                joy = request.POST['joy']
            else:
                joy = None
            if 'loss_familiar' in request.POST:
                loss_familiar = request.POST['loss_familiar']
            else:
                loss_familiar = None
            if 'loss_wealth' in request.POST:
                loss_wealth = request.POST['loss_wealth']
            else:
                loss_wealth = None
            if 'love_conditional' in request.POST:
                love_conditional = request.POST['love_conditional']
            else:
                love_conditional = None
            if 'loss_possession' in request.POST:
                loss_possession = request.POST['loss_possession']
            else:
                loss_possession = None
            if 'love_unhappy' in request.POST:
                love_unhappy = request.POST['love_unhappy']
            else:
                love_unhappy = None
            if 'mental_exertion' in request.POST:
                mental_exertion = request.POST['mental_exertion']
            else:
                mental_exertion = None
            if 'maltreatment_child' in request.POST:
                maltreatment_child = request.POST['maltreatment_child']
            else:
                maltreatment_child = None
            if 'neat_clean' in request.POST:
                neat_clean = request.POST['neat_clean']
            else:
                neat_clean = None
            if 'negative_pess' in request.POST:
                negative_pess = request.POST['negative_pess']
            else:
                negative_pess = None
            if 'need_protect' in request.POST:
                need_protect = request.POST['need_protect']
            else:
                need_protect = None
            if 'overstrain_mental' in request.POST:
                overstrain_mental = request.POST['overstrain_mental']
            else:
                overstrain_mental = None
            if 'parental_arguement' in request.POST:
                parental_argument = request.POST['parental_arguement']
            else:
                parental_argument = None
            if 'parental_control' in request.POST:
                parental_control = request.POST['parental_control']
            else:
                parental_control = None
            if 'parental_violence' in request.POST:
                parental_violence = request.POST['parental_violence']
            else:
                parental_violence = None
            if 'parental_fit' in request.POST:
                parental_fit = request.POST['parental_fit']
            else:
                parental_fit = None
            if 'past_history_dominate' in request.POST:
                past_history_dominate = request.POST['past_history_dominate']
            else:
                past_history_dominate = None
            if 'perform_pressure' in request.POST:
                perform_pressure = request.POST['perform_pressure']
            else:
                perform_pressure = None
            if 'pride' in request.POST:
                pride = request.POST['pride']
            else:
                pride = None
            if 'prolonged_unhappy' in request.POST:
                prolonged_unhappy = request.POST['prolonged_unhappy']
            else:
                prolonged_unhappy = None
            if 'quarrel' in request.POST:
                quarrel = request.POST['quarrel']
            else:
                quarrel = None
            if 'rejection' in request.POST:
                rejection = request.POST['rejection']
            else:
                rejection = None
            if 'reproaches' in request.POST:
                reproaches = request.POST['reproaches']
            else:
                reproaches = None
            if 'reserved_displeasure' in request.POST:
                reserved_displeasure = request.POST['reserved_displeasure']
            else:
                reserved_displeasure = None
            if 'rudeness_children' in request.POST:
                rudeness_children = request.POST['rudeness_children']
            else:
                rudeness_children = None
            if 'restrictions' in request.POST:
                restrictions = request.POST['restrictions']
            else:
                restrictions = None
            if 'rudeness_others' in request.POST:
                rudeness_others = request.POST['rudeness_others']
            else:
                rudeness_others = None
            if 'reverse_fortune' in request.POST:
                reverse_fortune = request.POST['reverse_fortune']
            else:
                reverse_fortune = None
            if 'ridicule' in request.POST:
                ridicule = request.POST['ridicule']
            else:
                ridicule = None
            if 'scorned' in request.POST:
                scorned = request.POST['scorned']
            else:
                scorned = None
            if 'seperation' in request.POST:
                seperation = request.POST['seperation']
            else:
                seperation = None
            if 'shame' in request.POST:
                shame = request.POST['shame']
            else:
                shame = None
            if 'socio_cultural' in request.POST:
                socio_cultural = request.POST['socio_cultural']
            else:
                socio_cultural = None
            if 'stress' in request.POST:
                stress  = request.POST['stress']
            else:
                stress = None
            if 'stress_public' in request.POST:
                stress_public = request.POST['stress_public']
            else:
                stress_public = None
            if 'alcoholic_father' in request.POST:
                alcoholic_father = request.POST['alcoholic_father']
            else:
                alcoholic_father = None
            if 'witness_violence' in request.POST:
                witness_violence = request.POST['witness_violence']
            else:
                witness_violence = None
            if 'terror_wars' in request.POST:
                terror_wars = request.POST['terror_wars']
            else:
                terror_wars = None
            if 'traumetic_childhood' in request.POST:
                traumetic_childhood = request.POST['traumetic_childhood']
            else:
                traumetic_childhood = None
            if 'ugly' in request.POST:
                ugly = request.POST['ugly']
            else:
                ugly = None
            if 'unlovable' in request.POST:
                unlovable = request.POST['unlovable']
            else:
                unlovable = None
            if 'unfullfillment' in request.POST:
                unfullfillment = request.POST['unfullfillment']
            else:
                unfullfillment = None
            if 'unwanted' in request.POST:
                unwanted = request.POST['unwanted']
            else:
                unwanted = None
            if 'unpleasant_news' in request.POST:
                unpleasant_news = request.POST['unpleasant_news']
            else:
                unpleasant_news = None
            if 'unpredicted_mood_father' in request.POST:
                unpredicted_mood_father = request.POST['unpredicted_mood_father']
            else:
                unpredicted_mood_father = None
            if 'unloved' in request.POST:
                unloved = request.POST['unloved']
            else:
                unloved = None
            if 'unusal_office' in request.POST:
                unusual_office = request.POST['unusual_office']
            else:
                unusual_office = None
            if 'worry' in request.POST:
                worry = request.POST['worry']
            else:
                worry = None
            if 'wounded_sensitivity' in request.POST:
                wounded_sensitivity = request.POST['wounded_sensitivity']
            else:
                wounded_sensitivity = None
            if 'wounded_honour' in request.POST:
                wounded_honour = request.POST['wounded_honour']
            else:
                wounded_honour = None
            if 'wounded_pride' in request.POST:
                wounded_pride = request.POST['wounded_pride']
            else:
                wounded_pride = None


            obj = MentalCausative.objects.create(patient=p_id,abandonment=abandonment,abusive_husband=abusive_husband,abusive_parents=abusive_parents,
                                                after_anger=after_anger,anticipation=anticipation,anxiety=anxiety,abused_punishment=abused_punishment,
                                                apprehends=apprehends,bad_tragedies=bad_tragedies,bereavement=bereavement,boredom=boredom,
                                                business=business,blows=blows,beatings=beatings,bad_news=bad_news,bored=bored,
                                                contradiction=contradiction,criticism=criticism,deceived_friendship=deceived_friendship,
                                                depressing_emotion=depressing_emotion,disagreement=disagreement,discord_chief=discord_chief,
                                                discord_friends=discord_friends,discord_parents_children=discord_parents_children,
                                                domination_colonisation=domination_colonisation,domination_parental=domination_parental,
                                                domination=domination,demand_fullfillment=demand_fullfillment,embarrassment=embarrassment,
                                                excitement=excitement,emotional=emotional,excitement_business=excitement_business,
                                                fail_business=fail_business,failure=failure,fear=fear,feelings_controlled=feelings_controlled,
                                                friendship_deceived=friendship_deceived, fright=fright,frustration=frustration,
                                                grief_long_drawn=grief_long_drawn ,grudges=grudges,guilt_trapped=guilt_trapped,
                                                honour_wounded=honour_wounded ,humiliation=humiliation ,humiliation_criticised=humiliation_criticised,
                                                horrible_stories=horrible_stories,indulgence=indulgence,insecurity_children=insecurity_children,
                                                isolation=isolation,introvert=introvert,irritable=irritable,jealous_professional=jealous_professional,
                                                joy=joy,loss_familiar=loss_familiar,loss_wealth=loss_wealth,love_conditional=love_conditional,
                                                loss_possession=loss_possession,love_unhappy=love_unhappy,mental_exertion=mental_exertion,
                                                maltreatment_child=maltreatment_child,neat_clean=neat_clean,negative_pess=negative_pess,
                                                need_protect=need_protect,overstrain_mental=overstrain_mental,parental_argument=parental_argument,
                                                parental_control=parental_control,parental_violence =parental_violence ,parental_fit=parental_fit,
                                                past_history_dominate=past_history_dominate,perform_pressure=perform_pressure,
                                                pride=pride,prolonged_unhappy=prolonged_unhappy,quarrel=quarrel,rejection=rejection,
                                                reproaches=reproaches,reserved_displeasure=reserved_displeasure,rudeness_children=rudeness_children,
                                                restrictions=restrictions,rudeness_others=rudeness_others,
                                                reverse_fortune=reverse_fortune,ridicule=ridicule,scorned=scorned,seperation=seperation,
                                                shame=shame,socio_cultural=socio_cultural,stress=stress,stress_public=stress_public,
                                                alcoholic_father=alcoholic_father,witness_violence=witness_violence,terror_wars=terror_wars,
                                                traumetic_childhood=traumetic_childhood,ugly=ugly,unlovable=unlovable,
                                                unfullfillment=unfullfillment,unwanted=unwanted,unpleasant_news=unpleasant_news,
                                                unpredicted_mood_father=unpredicted_mood_father,unloved=unloved,unusual_office=unusual_office,
                                                worry=worry,wounded_sensitivity=wounded_sensitivity,wounded_honour=wounded_honour,
                                                wounded_pride=wounded_pride)
            obj.save()
            messages.info(request,'Mental Causative Factor Section Done')      
            return HttpResponseRedirect(reverse('mental_causative',  kwargs={'case_id': case_id}))

        
            
            
            

        return render(request,'dashboard/templates/mental_causative.html',{'status':status,'user':'D'})


def personality_character(request,case_id):

    status = False
    if request.user:
        status = request.user

    if case_id == 0:
        return HttpResponse('<h1> Please Select a Patient to Continue </h1>')
    
    else:

        if request.method == 'POST':

            p_id = Patient.objects.get(id=case_id)

            if 'Absentminded' in request.POST:
                absentminded = request.POST['Absentminded']
            else:
                absentminded = None
            if 'Active' in request.POST:
                active = request.POST['Active']
            else:
                absentminded = None
            if 'Amiable' in request.POST:
                amiable = request.POST['Amiable']
            else:
                amiable = None
            if 'Angry' in request.POST:
                angry = request.POST['Angry']
            else:
                angry = None
            if 'Benevolence' in request.POST:
                benevolence = request.POST['Benevolence']
            else:
                benevolence = None
            if 'Company(Like/Dislike)' in request.POST:
                company_like_dislike = request.POST['Company(Like/Dislike)']
            else:
                company_like_dislike = None
            if 'Energetic' in request.POST:
                energetic = request.POST['Energetic']
            else:
                energetic = None
            if 'Extrovert' in request.POST:
                extrovert = request.POST['Extrovert']
            else:
                extrovert = None
            if 'Forsaken' in request.POST:
                forsaken = request.POST['Forsaken']
            else:
                forsaken = None

            if 'Greedy' in request.POST:
                greedy = request.POST['Greedy']
            else:
                greedy = None
            if 'Hurried' in request.POST:
                hurried = request.POST['Hurried']
            else:
                hurried = None
            if 'Indifferent' in request.POST:
                indifferent = request.POST['Indifferent']
            else:
                indifferent = None
            if 'Impatient' in request.POST:
                impatient = request.POST['Impatient']
            else:
                impatient = None
            if 'Impetious' in request.POST:
                impetious = request.POST['Impetious']
            else:
                impetious = None
            if 'Introvert' in request.POST:
                introvert = request.POST['Introvert']
            else:
                introvert = None
            if 'Irritable' in request.POST:
                irritable = request.POST['Irritable']
            else:
                irritable = None
            if 'Jealous' in request.POST:
                jealous = request.POST['Jealous']
            else:
                jealous = None
            if 'Methodical' in request.POST:
                methodical = request.POST['Methodical']
            else:
                methodical = None
            if 'Mild' in request.POST:
                mild = request.POST['Mild']
            else:
                mild = None
            if 'Morose' in request.POST:
                morose = request.POST['Morose']
            else:
                morose = None
            if 'Neat(Clean)' in request.POST:
                neat_clean = request.POST['Neat(Clean)']
            else:
                neat_clean = None
            if 'Negative(Pessimistic)' in request.POST:
                neg_pess = request.POST['Negative(Pessimistic)']
            else:
                neg_pess = None
            if 'Organised' in request.POST:
                organised = request.POST['Organised']
            else:
                organised = None
            if 'Positive(Optimistic)' in request.POST:
                positive_opt = request.POST['Positive(Optimistic)']
            else:
                positive_opt = None
            if 'Punctual' in request.POST:
                punctual = request.POST['Punctual']
            else:
                punctual = None
            if 'Quarrelsome' in request.POST:
                quarrelsome = request.POST['Quarrelsome']
            else:
                quarrelsome = None
            if 'Restless' in request.POST:
                restless = request.POST['Restless']
            else:
                restless = None
            if 'Sentimental(Weepy)' in request.POST:
                sentimental_weepy = request.POST['Sentimental(Weepy)']
            else:
                sentimental_weepy = None
            if 'Slow' in request.POST:
                slow = request.POST['Slow']
            else:
                slow = None
            if 'Sluggish' in request.POST:
                sluggish = request.POST['Sluggish']
            else:
                sluggish = None
            if 'Sociable' in request.POST:
                sociable = request.POST['Sociable']
            else:
                sociable = None
            if 'Stubborn' in request.POST:
                stubborn = request.POST['Stubborn']
            else:
                stubborn = None
            if 'Suspicious' in request.POST:
                suspicious = request.POST['Suspicious']
            else:
                suspicious = None
            if 'Sympathetic' in request.POST:
                sympathetic = request.POST['Sympathetic']
            else:
                sympathetic = None
            if 'Talkative' in request.POST:
                talkative = request.POST['Talkative']
            else:
                talkative = None
            if 'Untidy(Unclean)' in request.POST:
                untidy_unclean = request.POST['Untidy(Unclean)']
            else:
                untidy_unclean = None
            if 'Absentminded_one' in request.POST:
                absentminded_one = request.POST['Absentminded_one']
            else:
                absentminded_one = None
            if 'Affectionate' in request.POST:
                affectionate = request.POST['Affectionate']
            else:
                affectionate = None
            if 'Aggressive' in request.POST:
                aggressive = request.POST['Agressive']
            else:
                aggressive = None
            if 'Ambitious' in request.POST:
                ambitious = request.POST['Ambitious']
            else:
                ambitious = None
            if 'Amiable_one' in request.POST:
                amiable_one = request.POST['Amiable_one']
            else:
                amiable_one = None
            if 'Anxious' in request.POST:
                anxious = request.POST['Anxious']
            else:
                anxious = None
            if 'Artistic' in request.POST:
                artistic = request.POST['Artistic']
            else:
                artistic = None
            if 'Assertive' in request.POST:
                assertive = request.POST['Assertive']
            else:
                assertive = None
            if 'Bossy' in request.POST:
                bossy = request.POST['Bossy']
            else:
                bossy = None
            if 'Broods' in request.POST:
                broods = request.POST['Broods']
            else:
                broods = None
            if 'Bubbly' in request.POST:
                bubbly = request.POST['Bubbly']
            else:
                bubbly = None
            if 'Careful' in request.POST:
                careful = request.POST['Careful']
            else:
                careful = None
            if 'Caring' in request.POST:
                caring = request.POST['Caring']
            else:
                caring = None
            if 'Cautious' in request.POST:
                cautious = request.POST['Cautious']
            else:
                cautious = None
            if 'Changeable' in request.POST:
                changeable = request.POST['Changeable']
            else:
                changeable = None
            if 'Comptitive' in request.POST:
                compititive = request.POST['Comptitive']
            else:
                compititive = None
            if 'Lack_of_Confidence' in request.POST:
                lack_confidence = request.POST['Lack_of_Confidence']
            else:
                lack_confidence = None
            if 'Confident' in request.POST:
                confident = request.POST['Confident']
            else:
                confident = None
            if 'Conscientious' in request.POST:
                conscientious = request.POST['Conscientious']
            else:
                conscientious = None
            if 'Conservative' in request.POST:
                conservative = request.POST['Conservative']
            else:
                conservative = None
            if 'Considerate' in request.POST:
                considerate = request.POST['Considerate']
            else:
                considerate = None
            if 'Conventional' in request.POST:
                conventional = request.POST['Conventional']
            else:
                conventional = None
            if 'Creative' in request.POST:
                creative = request.POST['Creative']
            else:
                creative = None
            if 'Discontented' in request.POST:
                discontented = request.POST['Discontented']
            else:
                discontented = None
            if 'Dutiful' in request.POST:
                dutiful = request.POST['Dutiful']
            else:
                dutiful = None
            if 'Easy_Going' in request.POST:
                easy_going = request.POST['Easy_Going']
            else:
                easy_going = None
            if 'Emotional' in request.POST:
                emotional = request.POST['Emotional']
            else:
                emotional = None
            if 'Excitable' in request.POST:
                excitable = request.POST['Excitable']
            else:
                excitable = None
            if 'Extrovert_one' in request.POST:
                extrovert_one = request.POST['Extrovert_one']
            else:
                extrovert_one = None
            if 'Family_Oriented' in request.POST:
                family_oriented = request.POST['Family_Oriented']
            else:
                family_oriented = None
            if 'Fault_Finding' in request.POST:
                fault_finding = request.POST['Fault_Finding']
            else:
                fault_finding = None
            if 'Fault_Finding' in request.POST:
                fault_finding = request.POST['Fault_Finding']
            else:
                fault_finding = None
            if 'Fearful' in request.POST:
                fearful = request.POST['Fearful']
            else:
                fearful = None
            if 'Friendly' in request.POST:
                friendly = request.POST['Friendly']
            else:
                friendly = None
            if 'Fun_loving' in request.POST:
                fun_loving = request.POST['Fun_loving']
            else:
                fun_loving = None
            if 'Generous' in request.POST:
                generous = request.POST['Generous']
            else:
                generous = None
            if 'Hesitant' in request.POST:
                hesistant = request.POST['Hesitant']
            else:
                hesistant = None
            if 'Homely' in request.POST:
                homely = request.POST['Homely']
            else:
                homely = None
            if 'Honest' in request.POST:
                honest = request.POST['Honest']
            else:
                honest = None
            if 'Humorous' in request.POST:
                humourous = request.POST['Humorous']
            else:
                humourous = None
            if 'Impatience' in request.POST:
                impatience = request.POST['Impatience']
            else:
                impatience = None
            if 'Independant' in request.POST:
                independent = request.POST['Independant']
            else:
                independent = None
            if 'Fears_Insects_and_spiders' in request.POST:
                fear_insects = request.POST['Fears_Insects_and_spiders']
            else:
                fear_insects = None
            if 'Intolerent' in request.POST:
                intolerant = request.POST['Intolerent']
            else:
                intolerant = None
            if 'Introvert_one' in request.POST:
                introvert_one = request.POST['Introvert_one']
            else:
                introvert_one = None
            if 'Irritable_one' in request.POST:
                irritable_one = request.POST['Irritable_one']
            else:
                irritable_one = None
            if 'Jealous_one' in request.POST:
                jealous_one = request.POST['Jealous_one']
            else:
                jealous_one = None
            if 'Kind' in request.POST:
                kind = request.POST['Kind']
            else:
                kind = None
            if 'Loving' in request.POST:
                loving = request.POST['Loving']
            else:
                loving = None
            if 'Loyal' in request.POST:
                loyal = request.POST['Loyal']
            else:
                loyal = None
            if 'Materialistic' in request.POST:
                materialistic = request.POST['Materialistic']
            else:
                materialistic = None
            if 'Messy' in request.POST:
                messy = request.POST['Messy']
            else:
                messy = None
            if 'Mild_one' in request.POST:
                mild_one = request.POST['Mild_one']
            else:
                mild_one = None
            if 'Moaning' in request.POST:
                moaning = request.POST['Moaning']
            else:
                moaning = None
            if 'Moody' in request.POST:
                moody = request.POST['Moody']
            else:
                moody = None
            if 'Lack_of_Motivation' in request.POST:
                lack_of_motivation = request.POST['Lack_of_Motivation']
            else:
                lack_of_motivation = None
            if 'Negative_Attitude' in request.POST:
                neg_attitude = request.POST['Negative_Attitude']
            else:
                neg_attitude = None
            if 'Optimistic' in request.POST:
                optimistic = request.POST['Optimistic']
            else:
                optimistic = None
            if 'OutGoing' in request.POST:
                outgoing = request.POST['OutGoing']
            else:
                outgoing = None
            if 'Passionate' in request.POST:
                passionate = request.POST['Passionate']
            else:
                passionate = None
            if 'Passionate' in request.POST:
                passionate = request.POST['Passionate']
            else:
                Passionate = None
            if 'Perceptive' in request.POST:
                perceptive = request.POST['Perceptive']
            else:
                perceptive = None
            if 'Perfectionist' in request.POST:
                perfectionist = request.POST['Perfectionist']
            else:
                perfectionist = None
            if 'Pessimistic' in request.POST:
                pessimistic = request.POST['Pessimistic']
            else:
                pessimistic = None
            if 'Planner' in request.POST:
                planner = request.POST['Planner']
            else:
                planner = None
            if 'Wants_to_please' in request.POST:
                wants_to_please = request.POST['Wants_to_please']
            else:
                wants_to_please = None
            if 'Precocious' in request.POST:
                precocious = request.POST['Precocious']
            else:
                precocious = None
            if 'Private' in request.POST:
                private = request.POST['Private']
            else:
                private = None
            if 'Avoids_Quarrel' in request.POST:
                avoids_quarrel = request.POST['Avoids_Quarrel']
            else:
                avoids_quarrel = None
            if 'Reliable' in request.POST:
                reliable = request.POST['Reliable']
            else:
                reliable = None
            if 'Resentful' in request.POST:
                resentful = request.POST['Resentful']
            else:
                resentful = None
            if 'Reserved' in request.POST:
                reserved = request.POST['Reserved']
            else:
                reserved = None
            if 'Restless_one' in request.POST:
                restless_one = request.POST['Restless_one']
            else:
                restless_one = None
            if 'Risks_Avoids' in request.POST:
                risk_avoid = request.POST['Risks_Avoids']
            else:
                risk_avoid = None
            if 'Romantic' in request.POST:
                romantic = request.POST['Romantic']
            else:
                romantic = None
            if 'Follows Routine' in request.POST:
                follows_routine = request.POST['Follows Routine']
            else:
                follows_routine = None
            if 'Strong_Principled' in request.POST:
                strong_principled = request.POST['Strong_Principled']
            else:
                strong_principled = None
            if 'Safe_Person' in request.POST:
                safe_person = request.POST['Safe_Person']
            else:
                safe_person = None
            if 'Selfish' in request.POST:
                selfish = request.POST['Selfish']
            else:
                selfish = None
            if 'Sensitive' in request.POST:
                sensitive = request.POST['Sensitive']
            else:
                sensitive = None
            if 'Sentimental' in request.POST:
                sentimental = request.POST['Sentimental']
            else:
                sentimental = None
            if 'Serious' in request.POST:
                serious = request.POST['Serious']
            else:
                serious = None
            if 'Sincere' in request.POST:
                sincere = request.POST['Sincere']
            else:
                sincere = None
            if 'Shy' in request.POST:
                shy = request.POST['Shy']
            else:
                shy = None
            if 'Sociable_one' in request.POST:
                sociable_one = request.POST['Sociable_one']
            else:
                sociable_one = None
            if 'Sociable_friendly' in request.POST:
                sociable_friendly = request.POST['Sociable_friendly']
            else:
                sociable_friendly = None
            if 'Soft' in request.POST:
                soft = request.POST['Soft']
            else:
                soft = None
            if 'Desires Solitude' in request.POST:
                desires_solitude = request.POST['Desires Solitude']
            else:
                desires_solitude = None
            if 'Stubborn_one' in request.POST:
                stubborn_one = request.POST['Stubborn_one']
            else:
                stubborn_one = None
            if 'Superstitious' in request.POST:
                superstitious = request.POST['Superstitious']
            else:
                superstitious = None
            if 'Sympathetic_one' in request.POST:
                sympathetic_one = request.POST['Sympathetic_one']
            else:
                sympathetic_one = None
            obj = PersonalityCharacter.objects.create(patient=p_id,absentminded=absentminded,active=active,amiable=amiable,angry=angry,
                                                    benevolence=benevolence,company_like_dislike=company_like_dislike,energetic=energetic,
                                                    extrovert=extrovert, forsaken=forsaken,greedy=greedy,hurried=hurried,indifferent=indifferent,
                                                    impatient=impatient, impetious=impetious,introvert=introvert,irritable=irritable,jealous=jealous,
                                                    methodical=methodical,mild=mild,morose=morose,neat_clean=neat_clean,neg_pess=neg_pess,organised=organised,
                                                    positive_opt=positive_opt,punctual=punctual,quarrelsome=quarrelsome,restless=restless,sentimental_weepy=sentimental_weepy,
                                                    slow=slow,sluggish=sluggish,sociable=sociable,stubborn=stubborn,suspicious=suspicious,sympathetic=sympathetic,talkative=talkative,
                                                    untidy_unclean=untidy_unclean,absentminded_one=absentminded_one,affectionate=affectionate,aggressive=aggressive,ambitious=ambitious,
                                                    amiable_one=amiable_one,anxious=anxious,artistic=artistic,assertive=assertive,bossy=bossy,broods=broods,bubbly=bubbly,careful=careful,caring=caring,changeable=changeable,
                                                    compititive=compititive,lack_confidence=lack_confidence,confident=confident,conscientious=conscientious,conservative=conservative,considerate=considerate,conventional=conventional,
                                                    creative=creative,discontented=discontented,dutiful=dutiful,easy_going=easy_going, emotional=emotional, excitable=excitable, extrovert_one=extrovert_one,family_oriented=family_oriented,
                                                    fault_finding=fault_finding,fearful=fearful,friendly=friendly,fun_loving=fun_loving,generous=generous,hesistant=hesistant,homely=homely,honest=honest,humourous=humourous,impatience=impatience,
                                                    independent=independent,fear_insects=fear_insects,intolerant=intolerant,introvert_one=introvert_one,irritable_one=irritable_one,jealous_one=jealous_one,kind=kind,loving=loving,loyal=loyal,materialistic=materialistic,messy=messy,mild_one=mild_one,moaning=moaning,
                                                    moody=moody,lack_of_motivation=lack_of_motivation,neg_attitude=neg_attitude,optimistic=optimistic,outgoing=outgoing,passionate=passionate,perceptive=perceptive,perfectionist=perfectionist,pessimistic=pessimistic,planner=planner,wants_to_please=wants_to_please,precocious=precocious,
                                                    private=private,strong_principled=strong_principled,safe_person=safe_person,selfish=selfish,sensitive=sensitive,sentimental=sentimental,serious=serious,sincere=sincere,shy=shy,sociable_one=sociable_one,
                                                    sociable_friendly=sociable_friendly,soft=soft,desires_solitude=desires_solitude,stubborn_one=stubborn_one,superstitious=superstitious,sympathetic_one=sympathetic_one,avoids_quarrel=avoids_quarrel,
                                                    reliable=reliable,resentful=resentful,reserved=reserved,restless_one=restless_one,risk_avoid=risk_avoid,romantic=romantic,follows_routine=follows_routine)
            
            obj.save()
            messages.info(request,'Personality Character Section Done')      
            return HttpResponseRedirect(reverse('personality_character',  kwargs={'case_id': case_id}))
        
        return render(request,'dashboard/templates/personality_character.html',{'status':status,'user': 'D'})

from dashboard.forms import MiasmOneForm

def mia_sm(request,case_id):

    status = False
    if request.user:
        status = request.user

    if case_id == 0:
        return HttpResponse('<h1> Please Select a Patient to Continue </h1>')
    
    else:

        if request.method == 'POST':
            p_id = Patient.objects.get(id=case_id)
            
            if 'Psora' in request.POST:
                psora = request.POST['Psora']
            else:
                psora = None
            if 'Sycosis' in request.POST:
                sycosis = request.POST['Sycosis']
            else:
                sycosis = None
            if 'Syphilis' in request.POST:    
                syphilis = request.POST['Syphilis']
            else:
                syphilis = None
            if 'Tubercular' in request.POST:
                tubercular = request.POST['Tubercular']
            else:
                tubercular = None
            if 'Psora Sycosis' in request.POST:
                psora_sycosis = request.POST['Psora Sycosis']
            else:
                psora_sycosis = None
            if 'Psora Syphilis' in request.POST:
                psora_syphilis = request.POST['Psora Syphilis']
            else:
                psora_syphilis=None
            obj = MiasmOne.objects.create(patient=p_id,psora=psora,sycosis=sycosis,syphilis=syphilis,tubercular=tubercular,
                                        psora_sycosis=psora_sycosis,psora_syphilis=psora_syphilis)
            obj.save()
            messages.info(request,'Miasm Examination Section Done')      
            return HttpResponseRedirect(reverse('mia_sm',  kwargs={'case_id': case_id}))

        return render(request,'dashboard/templates/mia_sm.html',{'status':status,'user':'D'})

def rubric(request,case_id):

    status = False
    if request.user:
        status = request.user

    if request.method == 'POST':

        p_id = Patient.objects.get(id=case_id)
        rubric = request.POST['rubric']
        obj = RubricOne.objects.create(patient=p_id,rubric=rubric)
        obj.save()        
        messages.info(request,'Rubric Selection Section added ' +str(rubric)+ ' for '+ p_id.name)
        return HttpResponseRedirect(reverse('rubric',  kwargs={'case_id': case_id}))
    

    
    return render(request,'dashboard/templates/rubric.html',{'status':status,'user':'D'})

from dashboard.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View

class GeneratePdf(View):


    
    def get(self, request, *args, **kwargs):
        
        case_id = self.kwargs['pk']

        if case_id == 0:
            return HttpResponse("<h1>Please Select a Patient to Generate PDF</h1>")

        else:
            patient = Patient.objects.get(id=case_id)
            present_complaints = PresentComplaintsNew.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
            obj_chief_complaints = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=7) )
            past_history = PatientHistoryNEW.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))        
            question = Question1.objects.filter(category__id=9)
            obj_personal_history = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=9))
            for o in obj_personal_history:
                print('-----',o.patient,o.category,obj_personal_history.count())
            table_data = FamilyMedicalHistory.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
            my_list = []
            for t in table_data:
                x = t.list_of_disease         
                x = x.replace("[","").replace("'","").replace("]","")        
                my_list.append(x)    
            zipped_list = zip(table_data,my_list)

            table_data1 = MentalCausativeRecord.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
            my_list1 = []
            for t in table_data1:
                x = t.factors
                x = x.replace("[","").replace("'","").replace("]","")
                my_list1.append(x)
            mental_causative = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=10))

            table_data2 = MentalPersonalityRecord.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
            my_list2 = []
            for t in table_data2:
                x = t.characters
                x = x.replace("[","").replace("'","").replace("]","")
                my_list2.append(x)
            mental_personality = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=11))
            
            bms_question = Question1.objects.filter(category__id=12)
            bms_view = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=12))

            thermal_question = Question1.objects.filter(category__id=13)
            thermal_view = obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=13))

            table_data3 =MiasmRecords.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
            my_list3 = []
            for t in table_data3:
                x = t.records
                x = x.replace("[","").replace("'","").replace("]","")
                my_list3.append(x)

            table_data4 =ThermalReactionRecords.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
            my_list4 = []
            for t in table_data4:
                x = t.records
                x = x.replace("[","").replace("'","").replace("]","")
                my_list4.append(x)


            date1 = date.today()

            data = {
                'patient_details': patient,
                'table1':present_complaints,
                'table2':obj_chief_complaints,
                'table3': past_history,
                'question':question,
                'personal_history':obj_personal_history,
                'list':zipped_list,
                'my_list1':my_list1,
                'mental':mental_causative,
                'my_list2':my_list2,
                'personality':mental_personality,
                'bms':bms_question,
                'bms_view':bms_view,
                'thermal':thermal_question,
                'thermal_view':thermal_view,
                'my_list3':my_list3,
                'date1':date1,
                'my_list4':my_list4,
                
            }
            pdf = render_to_pdf('dashboard/templates/newcase_final_report_pdf.html', data)
            return HttpResponse(pdf, content_type='application/pdf')


class ShowCasePdf(View):
    
    def get(self, request, *args, **kwargs):
        
        case_id = self.kwargs['pk']

        if case_id == 0:
            return HttpResponse("<h1>Please Select a Patient to Generate PDF</h1>")

        else:
            patient = Patient.objects.get(id=case_id)
            present_complaints = PresentComplaintsNew.objects.filter(patient__id=case_id)
            obj_chief_complaints = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=7) )
            past_history = PatientHistoryNEW.objects.filter(Q(patient__id=case_id) )        
            question = Question1.objects.filter(category__id=9)
            obj_personal_history = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=9))
            for o in obj_personal_history:
                print('-----',o.patient,o.category,obj_personal_history.count())
            table_data = FamilyMedicalHistory.objects.filter(Q(patient__id=case_id) )
            my_list = []
            for t in table_data:
                x = t.list_of_disease         
                x = x.replace("[","").replace("'","").replace("]","")        
                my_list.append(x)    
            zipped_list = zip(table_data,my_list)

            table_data1 = MentalCausativeRecord.objects.filter(Q(patient__id=case_id) )
            my_list1 = []
            for t in table_data1:
                x = t.factors
                x = x.replace("[","").replace("'","").replace("]","")
                my_list1.append(x)
            mental_causative = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=10))

            table_data2 = MentalPersonalityRecord.objects.filter(Q(patient__id=case_id) )
            my_list2 = []
            for t in table_data2:
                x = t.characters
                x = x.replace("[","").replace("'","").replace("]","")
                my_list2.append(x)
            mental_personality = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=11))
            
            bms_question = Question1.objects.filter(category__id=12)
            bms_view = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=12))

            thermal_question = Question1.objects.filter(category__id=13)
            thermal_view = obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=13))

            table_data3 =MiasmRecords.objects.filter(Q(patient__id=case_id) )
            my_list3 = []
            for t in table_data3:
                x = t.records
                x = x.replace("[","").replace("'","").replace("]","")
                my_list3.append(x)

            table_data4 =ThermalReactionRecords.objects.filter(Q(patient__id=case_id) )
            my_list4 = []
            for t in table_data4:
                x = t.records
                x = x.replace("[","").replace("'","").replace("]","")
                my_list4.append(x)


            date1 = date.today()

            data = {
                'patient_details': patient,
                'table1':present_complaints,
                   'len_present_complaint': len(present_complaints),

                    'table2':obj_chief_complaints,
                    'len_obj_chief_complaints':len(obj_chief_complaints),

                    'table3': past_history,
                    'len_past_history':len( past_history),

                    # 'question':question,
                    'personal_history':obj_personal_history,
                    'len_personal_history':len(obj_personal_history),

                    'list':list(zipped_list),
                    'len_family_medical':len(list(zipped_list)),


                    'my_list1':my_list1,
                    'len_my_list1':len(my_list1),
                    'mental':mental_causative,
                    


                    'my_list2':my_list2,
                    'len_my_list2':len(my_list2),
                    'personality':mental_personality,

                    #  'bms':bms_question,

                     'bms_view':bms_view,
                     'len_bms':len(bms_view),

                    'my_list4':my_list4,
                    'len_thermal_reaction': len(my_list4),
                    #  'thermal':thermal_question,
                    #  'thermal_view':thermal_view,
                      
                      'my_list3':my_list3,
                      'len_miasm': len(my_list3),
                      
                      'today':date.today(),
            }
            pdf = render_to_pdf('dashboard/templates/show_case_pdf.html', data)
            return HttpResponse(pdf, content_type='application/pdf')


def newcase_final_report(request,case_id):

    status = False
    if request.user:
        status = request.user

    if case_id == 0:
        return HttpResponse("<h1> Please Select a Patient to Generate Final Report ")
    else:
        patient_details = Patient.objects.get(id=case_id)
        present_complaints = PresentComplaintsNew.objects.filter(Q(patient__id=case_id))
        obj_chief_complaints = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=7))
        past_history = PatientHistoryNEW.objects.filter(Q(patient__id=case_id) )        
        question = Question1.objects.filter(category__id=9)
        obj_personal_history = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=9))
       
        for o in obj_personal_history:
            print('-----',o.patient,o.category,obj_personal_history.count())
       
        table_data = FamilyMedicalHistory.objects.filter(Q(patient__id=case_id) )
        my_list = []
        for t in table_data:
            x = t.list_of_disease         
            x = x.replace("[","").replace("'","").replace("]","")        
            my_list.append(x)    
        zipped_list = zip(table_data,my_list)

        table_data1 = MentalCausativeRecord.objects.filter(Q(patient__id=case_id) )
        my_list1 = []
        for t in table_data1:
            x = t.factors
            x = x.replace("[","").replace("'","").replace("]","")
            my_list1.append(x)
        mental_causative = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=10))

        table_data2 = MentalPersonalityRecord.objects.filter(Q(patient__id=case_id) )
        my_list2 = []
        for t in table_data2:
            x = t.characters
            x = x.replace("[","").replace("'","").replace("]","")
            my_list2.append(x)
        mental_personality = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=11) )
        
        bms_question = Question1.objects.filter(category__id=12)
        bms_view = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=12))

        thermal_question = Question1.objects.filter(category__id=13)
        thermal_view = obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=13))

        table_data3 =MiasmRecords.objects.filter(Q(patient__id=case_id) )
        my_list3 = []
        for t in table_data3:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list3.append(x)
        
        table_data4 =ThermalReactionRecords.objects.filter(Q(patient__id=case_id))
        my_list4 = []
        for t in table_data4:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list4.append(x)

        appoint = Appointment.objects.filter(Q(patientid=patient_details)&Q(date=date.today())).last()
        if appoint.token != 0:
            final_token = appoint.token
        else:
            final_token = appoint.token1

        context = {'status':status,
                   'user':'D',
                   'case_id':case_id,
                   'patient_details':patient_details,
                   'table1':present_complaints,
                   'len_present_complaint': len(present_complaints),

                    'table2':obj_chief_complaints,
                    'len_obj_chief_complaints':len(obj_chief_complaints),

                    'table3': past_history,
                    'len_past_history':len( past_history),

                    # 'question':question,
                    'personal_history':obj_personal_history,
                    'len_personal_history':len(obj_personal_history),

                    'list':list(zipped_list),
                    'len_family_medical':len(list(zipped_list)),


                    'my_list1':my_list1,
                    'len_my_list1':len(my_list1),
                    'mental':mental_causative,
                    


                    'my_list2':my_list2,
                    'len_my_list2':len(my_list2),
                    'personality':mental_personality,

                    #  'bms':bms_question,

                     'bms_view':bms_view,
                     'len_bms':len(bms_view),

                    'my_list4':my_list4,
                    'len_thermal_reaction': len(my_list4),
                    #  'thermal':thermal_question,
                    #  'thermal_view':thermal_view,
                      
                      'my_list3':my_list3,
                      'len_miasm': len(my_list3),
                      
                      'today':date.today(),
                      'final_token':final_token
                      
                       }

        return render(request,'dashboard/templates/newcase_final_report_adjust1.html',context)

@method_decorator(csrf_exempt, name='dispatch')
class NewCaseCreateView(generic.CreateView):
    
    model = NewCaseModel
    fields = '__all__'    
    
    def get_success_url(self):
        print('self----',self.object.category,type(self.object.category),self.object.patient_id,type(self.object.patient_id))
        if str(self.object.category) == 'Chief Complaints':
            messages.add_message(self.request, messages.INFO, 'Chief Complaints Submission Success')
            return reverse_lazy('chief_complaints_newone',kwargs= {'case_id':self.object.patient_id})
        elif str(self.object.category) == 'Personal History':
            messages.add_message(self.request, messages.INFO, 'Personal History Submission Success')
            return reverse_lazy('personal_history_newone',kwargs= {'case_id':self.object.patient_id})
        elif str(self.object.category) == 'Mental Causative Factor':
            messages.add_message(self.request, messages.INFO, 'Mental Causative Factor Submission Success')
            return reverse_lazy('mental_causative_jspad',kwargs= {'case_id':self.object.patient_id})
        elif str(self.object.category) == 'Mental Personality Character':
            messages.add_message(self.request, messages.INFO, 'Mental Personality Character Submission Success')
            return reverse_lazy('mental_personality_jspad',kwargs= {'case_id':self.object.patient_id})
        elif str(self.object.category) == 'Brief Mind Symptoms':
            messages.add_message(self.request, messages.INFO, 'Brief Mind Symptoms Submission Success')
            return reverse_lazy('bms_newone',kwargs= {'case_id':self.object.patient_id})
        elif str(self.object.category) == 'Thermal':
            messages.add_message(self.request, messages.INFO, 'Thermal Reaction Submission Success')
            return reverse_lazy('thermal_newone',kwargs= {'case_id':self.object.patient_id})

@method_decorator(csrf_exempt, name='dispatch')
class NewCaseCreateViewOne(generic.CreateView):
    
    model = NewCaseModel
    fields = '__all__'

    def get_success_url(self):
        # print('self----',self.object.category,type(self.object.category),self.object.patient_id,type(self.object.patient_id))
        previous_url = self.request.META.get('HTTP_REFERER')
        obj =previous_url.split('/')
        # print("previous url", obj[5])
        if str(self.object.category) == 'Chief Complaints':
            messages.add_message(self.request, messages.INFO, 'Present Complaints Submission Success')
            return reverse_lazy('present_complaint_appointment',kwargs= {'case_id':self.object.patient_id,'token':obj[5]}) 

@method_decorator(csrf_exempt, name='dispatch')        
class NewCaseUpdateView(generic.UpdateView):
    
    model=NewCaseModel
    fields = ['signature']

    def get_success_url(self):
        previous_url = self.request.META.get('HTTP_REFERER')
        obj =previous_url.split('/')
        print("Obj",obj)
        if str(self.object.category) == 'Chief Complaints' and str(obj[3]) == 'update-present-complaints-pad':
            messages.add_message(self.request, messages.INFO, 'Present Complaints Update Success')
            return reverse_lazy('update_present_complaints_pad',kwargs={'pk':self.object.id})
        elif str(self.object.category) == 'Chief Complaints' and obj[3] != 'update-present-complaints-pad':
            messages.add_message(self.request, messages.INFO, 'Chief Complaints Update Success')
            return reverse_lazy('chief_complaints_view',kwargs={'case_id':self.object.patient_id})
        elif str(self.object.category) == 'Personal History':
            messages.add_message(self.request, messages.INFO, 'Personal History Update Success')
            return reverse_lazy('personal_history_view',kwargs= {'case_id':self.object.patient_id})
        elif str(self.object.category) == 'Mental Causative Factor':
            messages.add_message(self.request, messages.INFO, 'Mental Causative Update Success')
            return reverse_lazy('mental_causative_view',kwargs= {'case_id':self.object.patient_id})
        elif str(self.object.category) == 'Mental Personality Character':
            messages.add_message(self.request, messages.INFO, 'Mental Personality Update Success')
            return reverse_lazy('mental_personality_view',kwargs= {'case_id':self.object.patient_id})
        elif str(self.object.category) == 'Brief Mind Symptoms':
            messages.add_message(self.request, messages.INFO, 'Brief Mind Symptoms Update Success')
            return reverse_lazy('bms_view',kwargs= {'case_id':self.object.patient_id}) 
        elif str(self.object.category) == 'Thermal':
            messages.add_message(self.request, messages.INFO, 'Thermal Reaction Update Success')
            return reverse_lazy('thermal_view',kwargs= {'case_id':self.object.patient_id})      

@csrf_exempt
def update_present_complaints_pad(request,pk):    

    present_complaint = NewCaseModel.objects.get(id=pk)    
    form=NewCaseForm(instance=present_complaint)

    app_token = Appointment.objects.filter(Q(patientid=present_complaint.patient) & Q(date=date.today())).last()
    print("APpp_token",app_token.patientid.id,app_token.token,app_token.token1)


    if app_token.token != 0:
        final_token=app_token.token
    else:
        final_token=app_token.token1



    context = {
        'form':form,
        'pk':pk,
        'final_token':final_token,
        'patient_id':app_token.patientid.id,
    }

    return render(request,'update_present_complaints_pad_adjust.html',context)

@csrf_exempt
def chief_complaints_newone(request,case_id):

    print('id',case_id)
    status = False
    if request.user:
        status = request.user

    # c_id = Category.objects.get(id=9)
    # p_id = Patient.objects.get(id=case_id)
    if case_id == 0:
        return HttpResponse("<h1>Please Add a Patient for Chief Complaints</h1>")
    else:
        instance =Category.objects.get(id=7)
        instance1 = Patient.objects.get(id=case_id)
        form = NewCaseForm(initial= {'category': instance,'patient':instance1})
        
        table_data = PresentComplaintsNew.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
        
        appoint = Appointment.objects.filter(Q(patientid=instance1)&Q(date=date.today())).last()
        if appoint.token != 0:
            final_token = appoint.token
        else:
            final_token = appoint.token1

    context = {'status':status,
               'user':'D',
               'case_id':case_id,
               'table':table_data,
               'form':form,
               'patient_details':instance1,               
                'patient':instance1,
                'final_token':final_token
               }
    

    return render(request,'dashboard/templates/chief_complaints_newone_adjust.html',context)



@csrf_exempt
def chief_complaints_view(request,case_id):

    status = False
    if request.user:
        status = request.user
    obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=7))
    # print('obj',obj)
    patient_details = Patient.objects.get(id=case_id)
    
    context = {'status':status,
               'user':'D',
               'case_id':case_id,
               'patient':patient_details,
               'obj':obj,
               
               }


    return render(request,'dashboard/templates/chief_complaints_view_adjust.html',context)

@csrf_exempt
def present_complaints_view(request,case_id,token):
    
    status = False
    if request.user:
        status = request.user

    obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=7))

    patient_details = Patient.objects.get(id=case_id)
    

    context = {'status':status,
               'user':'D',
               'case_id':case_id,
               'patient_details':patient_details,
               'obj':obj,               
                'token':token,
                'patient':patient_details,
               }



    
    return render(request,'present_complaints_view_adjust.html',context)

def delete_present_complaints_pad(request,pk):

    present_complaint = NewCaseModel.objects.get(id=pk)
    app_token = Appointment.objects.filter(Q(patientid=present_complaint.patient) & Q(date=date.today())).last()
    if app_token.token != 0:
        final_token=app_token.token
    else:
        final_token=app_token.token1

    present_complaint.delete()
    messages.success(request,f"Successfully Deleted the Present Complaint")
    return HttpResponseRedirect(reverse('present_complaints_view',kwargs={'case_id':app_token.patientid.id,'token':final_token}))

@csrf_exempt
def update_chief_complaints(request,id):

    status = False
    if request.user:
        status = request.user
    pre_url = request.META.get('HTTP_REFERER')
    obj = pre_url.split("view_chief_complaints/")  

    chief_complaint = NewCaseModel.objects.get(id=id)    
    form=NewCaseForm(instance=chief_complaint)
    

    context = {'status':status,
               'user':'D',
               'case_id':int(obj[1]),
                'form':form,
                'id':id,
                'patient_details':chief_complaint,
               
                }
    return render(request,'dashboard/templates/update_chief_complaints.html',context)

def ask_delete(request,id):

    status=False
    if request.user:
        status=request.user
    
    category = NewCaseModel.objects.get(id=id)
    # print(type(category.category),category.category)
    if str(category.category) == 'Chief Complaints':
        pre_url = request.META.get('HTTP_REFERER')
        pat_id = pre_url.split("view_chief_complaints/")
        obj = int(pat_id[1])
    elif str(category.category) == 'Personal History':
        pre_url = request.META.get('HTTP_REFERER')
        pat_id = pre_url.split("personal_history_view/")
        obj = int(pat_id[1])
    elif str(category.category) == 'Mental Causative Factor':
        pre_url = request.META.get('HTTP_REFERER')
        pat_id = pre_url.split("mental_causative_factor_view/")
        obj = int(pat_id[1])
    elif str(category.category) == 'Mental Personality Character':
        pre_url = request.META.get('HTTP_REFERER')
        pat_id = pre_url.split("mental_personality_view/")
        obj = int(pat_id[1])
    elif str(category.category) == 'Brief Mind Symptoms':
        pre_url = request.META.get('HTTP_REFERER')
        pat_id = pre_url.split("BMS_view/")
        obj = int(pat_id[1])
    elif str(category.category) == 'Thermal':
        pre_url = request.META.get('HTTP_REFERER')
        pat_id = pre_url.split("thermal_view/")
        obj = int(pat_id[1])

    
    context = {'status':status,
               'user':'D',
               'id':id,
               'case_id':obj ,
               'category':str(category.category),                
               }
    return render(request,'dashboard/templates/ask_delete_adjust.html',context)

def delete_chief_complaints(request,id):
    
    category = NewCaseModel.objects.get(id=id)
    obj = NewCaseModel.objects.get(id=id).patient_id        
    obj1 = NewCaseModel.objects.get(id=id).delete()

    if str(category.category) == 'Chief Complaints':
        messages.success(request,f'Deleted Chief Complaints Successfully!')
        return HttpResponseRedirect(reverse('chief_complaints_view',kwargs={'case_id':obj}))
    elif str(category.category) == 'Personal History':
        messages.success(request,f'Deleted Personal History Successfully!')
        return HttpResponseRedirect(reverse('personal_history_view',kwargs={'case_id':obj}))
    elif str(category.category) == 'Mental Causative Factor':
        messages.success(request,f'Deleted Mental Causative Factor Successfully!')
        return HttpResponseRedirect(reverse('mental_causative_view',kwargs={'case_id':obj}))
    elif str(category.category) == 'Mental Personality Character':
        messages.success(request,f'Deleted Mental Personality Successfully!')
        return HttpResponseRedirect(reverse('mental_personality_view',kwargs={'case_id':obj}))
    elif str(category.category) == 'Brief Mind Symptoms':
        messages.success(request,f'Deleted Brief Mind Symptoms Successfully!')
        return HttpResponseRedirect(reverse('bms_view',kwargs={'case_id':obj})) 
    elif str(category.category) == 'Thermal':
        messages.success(request,f'Deleted Thermal Reaction Successfully!')
        return HttpResponseRedirect(reverse('thermal_view',kwargs={'case_id':obj}))  

@csrf_exempt
def family_medical_newone(request,case_id):

    status = False
    if request.user:
        status = request.user   

    if case_id == 0:
        return HttpResponse('<h1>Please Select a Patient to Continue </h1>')
    else:
        if request.method == 'POST':
            form = FamilyMedicalHistoryForm(request.POST)
            if form.is_valid():
                patient = Patient.objects.get(id=case_id)
                relation = form.cleaned_data['relation']
                list_of_disease = form.cleaned_data['list_of_disease']
                # list_of_disease_values = list_of_disease.values_list('name', flat=True)                
                any_other = form.cleaned_data['any_other']
                dead_alive = form.cleaned_data['dead_alive']
                age = form.cleaned_data['age']
                list_of_disease_str = ', '.join(map(str, list_of_disease))

                obj = FamilyMedicalHistory(patient=patient, relation=relation,
                list_of_disease=list_of_disease_str,
                any_other=any_other,
                dead_alive=dead_alive,
                age=age,)
                obj.save()           
                messages.success(request,"Family Medical History Added Successfully")
                return HttpResponseRedirect(reverse('family_medical_newone',kwargs={'case_id':case_id}))
        else:
            form = FamilyMedicalHistoryForm()

        table_data = FamilyMedicalHistory.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
        my_list = []
        
        for t in table_data:
            # print("LIST",t.list_of_disease)
            x = t.list_of_disease         
            x = x.replace("[","").replace("'","").replace("]","")        
            my_list.append(x)    
        zipped_list = zip(table_data,my_list)
        
        data = FamilyMedicalComplain.objects.all().order_by(Lower('name'))
        complain = FamilyMedicalComplain.objects.all()
        
        patient_details = Patient.objects.get(id=case_id)

        appoint = Appointment.objects.filter(Q(patientid=patient_details)&Q(date=date.today())).last()
        if appoint.token != 0:
            final_token = appoint.token
        else:
            final_token = appoint.token1

        context = {
            'status':status,
            'user':'D',
            'case_id':case_id,
            'data':data,
            'complain':complain,
            'list':zipped_list,
            'patient':patient_details,
            'form':form,
            'final_token':final_token,
           
        }

        return render(request,'dashboard/templates/family_medical_newone_adjust.html',context)


def new_case_report(request,id):

    status = False
    if request.user:
        status = request.user

    case_id = id

    if case_id == 0:
        return HttpResponse("<h1> Please Select a Patient to Generate Final Report ")
    else:
        patient_details = Patient.objects.get(id=case_id)
        present_complaints = PresentComplaintsNew.objects.filter(Q(patient__id=case_id))
        obj_chief_complaints = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=7))
        past_history = PatientHistoryNEW.objects.filter(Q(patient__id=case_id))        
        question = Question1.objects.filter(category__id=9)
        obj_personal_history = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=9))
        for o in obj_personal_history:
            print('-----',o.patient,o.category,obj_personal_history.count())
        table_data = FamilyMedicalHistory.objects.filter(Q(patient__id=case_id) )
        my_list = []
        for t in table_data:
            x = t.list_of_disease         
            x = x.replace("[","").replace("'","").replace("]","")        
            my_list.append(x)    
        zipped_list = zip(table_data,my_list)

        table_data1 = MentalCausativeRecord.objects.filter(Q(patient__id=case_id))
        my_list1 = []
        for t in table_data1:
            x = t.factors
            x = x.replace("[","").replace("'","").replace("]","")
            my_list1.append(x)
        mental_causative = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=10))

        table_data2 = MentalPersonalityRecord.objects.filter(Q(patient__id=case_id) )
        my_list2 = []
        for t in table_data2:
            x = t.characters
            x = x.replace("[","").replace("'","").replace("]","")
            my_list2.append(x)
        mental_personality = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=11) )
        
        bms_question = Question1.objects.filter(category__id=12)
        bms_view = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=12))

        thermal_question = Question1.objects.filter(category__id=13)
        thermal_view = obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=13))

        table_data3 =MiasmRecords.objects.filter(Q(patient__id=case_id) )
        my_list3 = []
        for t in table_data3:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list3.append(x)
        
        table_data4 =ThermalReactionRecords.objects.filter(Q(patient__id=case_id) )
        my_list4 = []
        for t in table_data4:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list4.append(x)

        
        appoint = Appointment.objects.filter(Q(patientid=patient_details)&Q(date=date.today())).last()
        if appoint.token != 0:
            final_token = appoint.token
        else:
            final_token = appoint.token1



    return render(request,'dashboard/templates/newcase_final_report_adjust.html',{'status':status,'user':'D','case_id':case_id,
                                                                               'patient_details':patient_details,'table1':present_complaints,
                                                                               'table2':obj_chief_complaints,'table3': past_history,
                                                                               'question':question,'personal_history':obj_personal_history,'list':zipped_list,'my_list1':my_list1,
                                                                               'mental':mental_causative,'my_list2':my_list2,'personality':mental_personality,
                                                                               'bms':bms_question,'bms_view':bms_view,'thermal':thermal_question,'thermal_view':thermal_view,
                                                                               'my_list3':my_list3,'my_list4':my_list4,'id':id,'final_token':final_token})





@csrf_exempt
def miasm_examination_newone(request,case_id):

    status = False
    if request.user:
        status = request.user
    
    if case_id == 0:
        return HttpResponse('<h1>Please Select the Patient to Continue the Miasm Examination</h1>')
    else:
        patient_details = Patient.objects.get(id=case_id)
        if request.method == 'POST':
            records = request.POST.getlist('Select-Mind')
            obj = MiasmRecords(patient=patient_details,records=records)
            obj.save()
            messages.info(request,"Miasm Examination Submission Success!")
            return HttpResponseRedirect(reverse('miasm_examination_newone',kwargs={'case_id':case_id}))
        
        data = MiasmNewOne.objects.all().order_by(Lower('name'))
        mental =  MiasmNewOne.objects.all()
        table_date =MiasmRecords.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
        my_list = []
        for t in table_date:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)
        
        token_check = Appointment.objects.filter(patientid_id=case_id,date=date.today()).last()

        if token_check.patientid.branch == 'Dombivali':
            token = token_check.token
        else:
            token = token_check.token1
            
        context = {'status':status,
                   'user':'D',
                   'case_id':case_id,
                   'mental':mental,
                   'data':data,
                   'patient':patient_details,
                   'my_list':my_list,                  
                    'final_token':token,
                    
                     }
        return render(request,'dashboard/templates/miasm_newone_adjust.html',context)

@csrf_exempt    
def mental_causative_newone(request,case_id):

    status= False
    if request.user:
        status = request.user

    if case_id == 0 :
        return HttpResponse("<h1>Please Select a Patient Case Paper Number to continue</h1>")
    else:
        patient_details = Patient.objects.get(id=case_id)
        if request.method == 'POST':            
            print(request.POST.getlist('Select-Mind'))
            factors = request.POST.getlist('Select-Mind')
            obj = MentalCausativeRecord(patient=patient_details,factors=factors)
            obj.save()
            messages.success(request,f'Mental Causative Factors added Successfully!')
            return HttpResponseRedirect(reverse('mental_causative_newone',kwargs={'case_id':case_id}))
        
        data = MentalCausativeNewone.objects.all().order_by(Lower('name'))
        mental = MentalCausativeNewone.objects.all()
        table_date = MentalCausativeRecord.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
        my_list = []
        for t in table_date:
            x = t.factors
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)

        appoint = Appointment.objects.filter(Q(patientid=patient_details)&Q(date=date.today())).last()   
        if appoint.token != 0:
            final_token = appoint.token
        else:
            final_token = appoint.token1

        context ={'status':status,
                  'user':'D',
                  'case_id':case_id,
                  'mental':mental,
                  'data':data,
                  'patient':patient_details,
                  'my_list':my_list,
                  'final_token':final_token,
                  }
        
        return render(request,'dashboard/templates/mental_causative_newone_adjust.html',context)
@csrf_exempt    
def mental_personality_newone(request,case_id):

    status = False
    if request.user:
        status = request.user
    
    if case_id == 0 :
        return HttpResponse("<h1>Please Select a Patient Case Paper Number to continue</h1>")
    else:
        patient_details = Patient.objects.get(id=case_id)
        if request.method == 'POST':            
            print(request.POST.getlist('Select-Mind'))
            characters = request.POST.getlist('Select-Mind')
            obj = MentalPersonalityRecord(patient=patient_details,characters=characters)
            obj.save()
            messages.success(request,f'Successfully! Added Mental Personality Character.')
            return HttpResponseRedirect(reverse('mental_personality_newone',kwargs={'case_id':case_id}))
        data = MentalPersonalityNewOne.objects.all().order_by(Lower('name'))
        mental = MentalPersonalityNewOne.objects.all()
        table_date = MentalPersonalityRecord.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
        my_list = []
        for t in table_date:
            x = t.characters
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)
    
        appoint = Appointment.objects.filter(Q(patientid=patient_details)&Q(date=date.today())).last()
        if appoint.token != 0 :
            final_token = appoint.token
        else:
            final_token = appoint.token1
    context = {'status':status,
               'user':'D',
               'case_id':case_id,
               'patient':patient_details,
                'mental':mental, 
                'data':data,
                'my_list':my_list,
                'final_token':final_token,
                }

    return render(request,'dashboard/templates/mental_personality_newone_adjust.html',context)

@csrf_exempt
def mental_causative_jspad(request,case_id):

    status = False
    if request.user:
        status = request.user
    instance =Category.objects.get(id=10)
    print(instance.category)
    instance1 = Patient.objects.get(id=case_id)
    form = NewCaseForm(initial= {'category': instance,'patient':instance1})

    table_date = MentalCausativeRecord.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
    my_list = []
    for t in table_date:
        x = t.factors
        x = x.replace("[","").replace("'","").replace("]","")
        my_list.append(x)

    appoint = Appointment.objects.filter(Q(patientid=instance1)&Q(date=date.today())).last()
    if appoint.token != 0:
        final_token = appoint.token        
    else:
        final_token = appoint.token1

    context = {'status':status,
               'user':'D',
               'case_id':case_id,
               'patient':instance1,
               'form':form,
               'my_list':my_list,
               'final_token':final_token
              }
    
    return render(request,'dashboard/templates/mental_causative_jspad_adjust.html',context)
@csrf_exempt
def mental_personality_jspad(request,case_id):

    status = False
    if request.user:
        status = request.user
    instance1 = Patient.objects.get(id=case_id)
    instance = Category.objects.get(id=11)
    # print('----------',instance.category)   
    form = NewCaseForm(initial= {'category': instance,'patient':instance1}) 
    table_date = MentalPersonalityRecord.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
    my_list = []
    for t in table_date:
        x = t.characters
        x = x.replace("[","").replace("'","").replace("]","")
        my_list.append(x)
    appoint = Appointment.objects.filter(Q(patientid=instance1)&Q(date=date.today())).last()
    if appoint.token != 0:
        final_token = appoint.token 
    else:
        final_token = appoint.token1

    context = {'status':status,
               'user':'D',
               'case_id':case_id,
                'patient':instance1,
                'form':form,
                'my_list':my_list,  
                'final_token':final_token,              
                }

    
    return render(request,'dashboard/templates/mental_personality_jspad_adjust.html',context)
@csrf_exempt
def mental_causative_view(request,case_id):

    status = False
    if request.user:
        status = request.user
    obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=10)).order_by('-signature_date')
    # print('obj',obj)
    patient_details = Patient.objects.get(id=case_id)    
    return render(request,'dashboard/templates/mental_causative_view_adjust.html',{'status':status,'user':'D','case_id':case_id,
                                                                            'patient':patient_details,'obj':obj})

@csrf_exempt
def mental_personality_view(request,case_id):

    status = False
    if request.user:
        status= request.user
    obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=11)).order_by('-signature_date')
    patient_details = Patient.objects.get(id=case_id)

    
    context = {'status':status,
               'user':'D',
               'case_id':case_id,
               'patient':patient_details,
               'obj':obj,              
               }

    return render(request,'dashboard/templates/mental_personality_view_adjust.html',context)

@csrf_exempt
def mental_causative_update(request,id):

    status = False
    if request.user:
        status = request.user
    pre_url = request.META.get('HTTP_REFERER')
    obj = pre_url.split("mental_causative_factor_view/")  

    complaint = NewCaseModel.objects.get(id=id)    
    form=NewCaseForm(instance=complaint)
    return render(request,'dashboard/templates/mental_causative_update.html',{'status':status,'user':'D','case_id':int(obj[1]),
                                                                              'form':form,'id':id,'patient_details':complaint})

@csrf_exempt
def mental_personality_update(request,id):

    status = False
    if request.user:
        status = request.user
    pre_url = request.META.get('HTTP_REFERER')
    obj = pre_url.split("mental_personality_view/")  

    complaint = NewCaseModel.objects.get(id=id)    
    form=NewCaseForm(instance=complaint)
    return render(request,'dashboard/templates/mental_personality_update.html',{'status':status,'user':'D','case_id':int(obj[1]),
                                                                              'form':form,'id':id,'patient_details':complaint})

@csrf_exempt    
def personal_history_newone(request,case_id):

    status = False
    if request.user:
        status = request.user

    if case_id == 0:
        return HttpResponse('<h1>Please Select a Patient to Continue taking Personal History</h1>')
    else:
        instance =Category.objects.get(id=9)
        instance1 = Patient.objects.get(id=case_id)
        form = NewCaseForm(initial= {'category': instance,'patient':instance1})

        c_id = Category.objects.get(id=9)    
        # c_id2 = Category.objects.get(id=8)    
        question = Question1.objects.filter(category=c_id)  
        patient_details = Patient.objects.get(id=case_id)

        appoint = Appointment.objects.filter(Q(patientid=instance1)&Q(date=date.today())).last()
        if appoint.token != 0:
            final_token = appoint.token
        else:
            final_token = appoint.token1


        context = {'status':status,
                   'user':'D',
                   'case_id':case_id,
                   'question':question,
                   'patient':patient_details,
                    'form':form,
                    'final_token':final_token,
                    
                    }
        return render(request,'dashboard/templates/personal_history_newone_adjust.html',context)
@csrf_exempt
def thermal_newone(request,case_id):

    status = False
    if request.user:
        status = request.user
    
    if case_id == 0:
        return HttpResponse('<h1>Please Select the Patient to Continue the Miasm Examination</h1>')
    else:
        patient_details = Patient.objects.get(id=case_id)
        if request.method == 'POST':
            records = request.POST.getlist('Select-Mind')
            obj = ThermalReactionRecords(patient=patient_details,records=records)
            obj.save()
            messages.info(request,"Thermal Reaction Submission Success!")
            return HttpResponseRedirect(reverse('thermal_newone',kwargs={'case_id':case_id}))
        
        data = ThermalReactionNewOne.objects.all().order_by(Lower('name'))
        mental =  ThermalReactionNewOne.objects.all()
        table_date =ThermalReactionRecords.objects.filter(Q(patient__id=case_id) & Q(date=date.today()))
        my_list = []
        for t in table_date:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)

        
        token_check = Appointment.objects.filter(patientid_id=case_id,date=date.today()).last()

        if token_check.patientid.branch == 'Dombivali':
            token = token_check.token
        else:
            token = token_check.token1
            
        
        

        context = {'status':status,
                   'user':'D',
                   'case_id':case_id,
                   'mental':mental,
                   'data':data,
                   'patient':patient_details,
                   'my_list':my_list,                   
                    'token':token,
                    'final_token':token,                
                     }
        

        return render(request,'dashboard/templates/thermal_newone_adjust.html',context)
        
        # return render(request,'dashboard/templates/thermal_newone.html',{'status':status,'user':'D','case_id':case_id,
        #                                                         'question':question,'patient_details':instance1 ,'form':form})

@csrf_exempt
def bms_add(request,case_id):

    status = False
    if request.user:
        status = request.user

    c_id = Category.objects.get(id=12)
    if request.method == 'POST':
        obj = Question1(category=c_id,question=request.POST['add_BMS'])
        obj.save()
        messages.info(request,"Successfully Added")
        return HttpResponseRedirect(reverse('bms_add',kwargs={'case_id':case_id}))

    data = Question1.objects.filter(category=c_id)    
    return render(request,'dashboard/templates/bms_add.html',{'user':'D','status':status,'case_id':case_id,'data':data})

@csrf_exempt
def bms_newone(request,case_id):

    status = False
    if request.user:
        status = request.user  

    if case_id == 0:
        return HttpResponse('<h1> Please Select Patient to Continue</h1>')
    else:
        instance =Category.objects.get(id=12)
        instance1 = Patient.objects.get(id=case_id)
        form = NewCaseForm(initial= {'category': instance,'patient':instance1})        
        question = Question1.objects.filter(category=instance)
        appoint = Appointment.objects.filter(Q(patientid=instance1)&Q(date=date.today())).last()
        if appoint.token != 0:
            final_token = appoint.token
        else:
            final_token = appoint.token1        
        context =   {'status':status,
                     'user':'D',
                     'case_id':case_id,
                     'question':question,
                     'patient':instance1 ,
                     'form':form,
                     'final_token':final_token, 
                     }  
        return render(request,'dashboard/templates/bms_newone_adjust.html',context)

@csrf_exempt
def bms_view(request,case_id):

    status = False
    if request.user:
        status = request.user
    obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=12))
    # print('obj',obj)
    patient_details = Patient.objects.get(id=case_id)

    
    context =   {'status':status,
                 'user':'D',
                 'case_id':case_id,
                 'patient':patient_details,
                 'obj':obj,                 
                 }
      
    return render(request,'dashboard/templates/bms_view_adjust.html',context)

@csrf_exempt
def thermal_view(request,case_id):

    status = False
    if request.user:
        status = request.user
    obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=13)).order_by('-signature_date')
    patient_details = Patient.objects.get(id=case_id)
    return render(request,'dashboard/templates/thermal_view.html',{'status':status,'user':'D','case_id':case_id,
                                                                            'patient_details':patient_details,'obj':obj})

@csrf_exempt
def personal_history_view(request,case_id):

    status = False
    if request.user:
        status = request.user
    obj = NewCaseModel.objects.filter(Q(patient_id=case_id) & Q(category=9))
    # print('obj',obj)
    patient_details = Patient.objects.get(id=case_id)

    context = {'status':status,
               'user':'D',
               'case_id':case_id,
               'patient':patient_details,
               'obj':obj,
              
                }    
    return render(request,'dashboard/templates/personal_history_view_adjust.html',context)
@csrf_exempt
def thermal_update(request,id):

    status = False
    if request.user:
        status = request.user
    pre_url = request.META.get('HTTP_REFERER')
    obj = pre_url.split("thermal_view/")  

    complaint = NewCaseModel.objects.get(id=id)    
    form=NewCaseForm(instance=complaint)
    return render(request,'dashboard/templates/thermal_update.html',{'status':status,'user':'D','case_id':int(obj[1]),
                                                                              'form':form,'id':id,'patient_details':complaint})

@csrf_exempt
def bms_update(request,id):
    status = False
    if request.user:
        status = request.user
    pre_url = request.META.get('HTTP_REFERER')
    obj = pre_url.split("BMS_view/")  

    complaint = NewCaseModel.objects.get(id=id)    
    form=NewCaseForm(instance=complaint)

    return render(request,'dashboard/templates/bms_update.html',{'status':status,'user':'D','case_id':int(obj[1]),
                                                                              'form':form,'id':id,'patient_details':complaint})

@csrf_exempt
def update_personal_history(request,id):

    status = False
    if request.user:
        status = request.user
    pre_url = request.META.get('HTTP_REFERER')
    obj = pre_url.split("personal_history_view/")  

    chief_complaint = NewCaseModel.objects.get(id=id)    
    form=NewCaseForm(instance=chief_complaint)


    
    context = {'status':status,
               'user':'D',
               'case_id':int(obj[1]),
               'form':form,
               'id':id,
               'patient_details':chief_complaint,
              
               }
    return render(request,'dashboard/templates/update_personal_history_adjust.html',context)
@csrf_exempt
def list_medicine(request):

    status=False
    if request.user:
        status = request.user
        
    header = 'List of Medicines'
    form = MedicineSearchForm(request.POST or None)
    queryset = MedicineStock.objects.all()

    reorder_count = 0
    for q in queryset:
        print('---',q.quantity,q.reorder_level)
        if q.quantity < q.reorder_level:
            reorder_count +=1

    print('reorder_count',reorder_count)

    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()




    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
        "status":status,
        "user":'D',
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
        "unsend_mail_count":unsent_mail_count,
        "reorder_count":reorder_count,
	}
    if request.method == 'POST':
        queryset = MedicineStock.objects.filter(medicine__icontains=form['medicine'].value())
        context = {
		"form": form,
		"header": header,
		"queryset": queryset,
        "status":status,
        "user":'D',
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
        "unsend_mail_count":unsent_mail_count,
        "reorder_count":reorder_count,
	}
    return render(request, "list_medicine.html", context)

def reorder_list(request):

    status = False
    if request.user:
        status = request.user

    form = MedicineSearchForm(request.POST or None)
    queryset = MedicineStock.objects.all()
    my_list = []
    count_reorder=0
    for q in queryset:
        if q.quantity < q.reorder_level:
            count_reorder += 1
            my_list.append(q)
    
    my_list.sort(key=lambda x: x.medicine.upper())   
    
    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()


    context={
        'status':status,
        'user':'D',
        'form':form,
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
        "unsend_mail_count":unsent_mail_count,
        "my_list":my_list,
        "count_reorder":count_reorder,
    }
    if request.method == 'POST':
        queryset = MedicineStock.objects.filter(medicine__icontains=form['medicine'].value())
        context = {
		"form": form,		
		"queryset": queryset,
        "status":status,
        "user":'D',
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
        "unsend_mail_count":unsent_mail_count,
        "my_list":my_list,
        "count_reorder":count_reorder,
	}
    return render(request,'reorder_list.html',context)


def add_medicine(request):

    status = False
    if request.user:
        status = request.user
    
    form = MedicineCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Added Successfully')
        return redirect('list_medicine')
    

    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()

    
    context = {
        "status":status,
        "user":'D',
		"form": form,
		"title": "Add Medicine",
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
        "unsend_mail_count":unsent_mail_count,
	}
    return render(request, "add_medicine.html", context)

def update_med(request, pk):
    status = False
    if request.user:
        status = request.user
    queryset = MedicineStock.objects.get(id=pk)
    form = MedicineUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = MedicineUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('list_medicine')
        

    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()


    context = {
        "status":status,
        "user":'D',
		'form':form,
		"title": "Update Medicine - " + str(queryset.medicine) ,
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
        "unsend_mail_count":unsent_mail_count,
	}
    return render(request, 'add_medicine.html', context)

def delete_med(request, pk):
    status = False
    if request.user:
        status = request.user
    queryset = MedicineStock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('list_medicine')
            
    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()

    context = {
        "status":status,
        "user":'D',
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
        "unsend_mail_count":unsent_mail_count,		
	}
    return render(request, 'delete_items.html',context)

def medicine_stock(request, pk):
    status= False
    if request.user:
        status = request.user

    queryset = MedicineStock.objects.get(id=pk)

    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()

    context = {		
		"queryset": queryset,
        "status":status,
        "user":'D',
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
        "unsend_mail_count":unsent_mail_count,
	}
    return render(request, "medicine_stock.html", context)

def issue_medicine(request, pk):
    status=False
    if request.user:
        status=request.user
    queryset = MedicineStock.objects.get(id=pk)
    print('quantity--',queryset.quantity)
    form = MedicineIssueForm(request.POST or None, instance=queryset)
    if form.is_valid():        
        instance = form.save(commit=False)        
        instance.receive_quantity = 0        
        instance.quantity -= instance.issue_quantity
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.medicine) + " now left in Store")
        instance.save()
        return redirect('/medicine_stock/'+str(instance.id)+'/')
    
    
    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()

    context = {
		"title": 'Issue Medicine -  ' + str(queryset.medicine),
		"queryset": queryset,
		"form": form,
        "status":status,
        "user":'D',
        "store":queryset.quantity,
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
        "unsend_mail_count":unsent_mail_count,
		
	}
    return render(request, "add_medicine.html", context)

def receive_medicine(request, pk):

    status = False
    if request.user:
        status = request.user
    queryset = MedicineStock.objects.get(id=pk)
    form = MedicineReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.medicine) +" now in Store")
        return redirect('/medicine_stock/'+str(instance.id)+'/')
    
        
    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()

    
    context = {
			"title": 'Receive ' + str(queryset.medicine),
			"instance": queryset,
			"form": form,	
            "status":status,
            "user":'D',	
            "store":queryset.quantity,
            'count_general_dom':count_general_dom,
            'count_general_mul':count_general_mul,
		    'count_repeat_dom':count_repeat_dom,
            'count_repeat_mul':count_repeat_mul,
		    'count_courier_dom':count_courier_dom,        
            'count_courier_mul':count_courier_mul,
            "unsend_mail_count":unsent_mail_count,	
		}
    return render(request, "add_medicine.html", context)

def reorder_med_level(request, pk):

    status = False
    if request.user:
        status = request.user
    queryset = MedicineStock.objects.get(id=pk)
    form = MedicineReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.medicine) + " is updated to " + str(instance.reorder_level))
        return redirect('list_medicine')
    
            
    general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_dom = str(general_dom.count())
    general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
    count_general_mul = str(general_mul.count())
	
    repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_dom = str(repeat_medicine_dom.count())
    repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
    count_repeat_mul = str(repeat_medicine_mul.count())

    courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_dom = str(courier_medicine_dom.count())
    courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
    count_courier_mul = str(courier_medicine_mul.count())

    mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
    unsent_mail_count = mail_count.count()

    context = {
			"instance": queryset,
			"form": form,
			"title": "Set Reorder Level for  " + str(queryset.medicine),
            "status":status,
            'user':'D',
            "store":queryset.quantity,
            'count_general_dom':count_general_dom,
            'count_general_mul':count_general_mul,
		    'count_repeat_dom':count_repeat_dom,
            'count_repeat_mul':count_repeat_mul,
		    'count_courier_dom':count_courier_dom,        
            'count_courier_mul':count_courier_mul,
            "unsend_mail_count":unsent_mail_count,	
		}
    return render(request, "add_medicine.html", context)


