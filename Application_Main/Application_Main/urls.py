"""Application_Main URL Configuration

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path,include, re_path
from COMMON_APP.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from dashboard.views import *
from DOCTER.views import *
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    # Home Page
    path('', home , name = 'home' ),
    path('register', register , name = 'register' ),
    path('recep_register_patient/(?P<user>.*)', recep_register_patient , name = 'recep_register_patient' ),
    # path('login', login , name = 'login' ),
    path('about', about , name = 'about' ),
    path('login1', login1 , name = 'login1' ),
    path("forget_password/",forgetPassword,name='forgetPassword'),
    path("change_password/<token>/",changePassword,name='changePassword'),

    path('logout', logout , name = 'logout' ),
    path('profile/(?P<user>.*)', profile , name = 'profile' ),
    path('patient_appointment/(?P<user>.*)',patient_appointment,name='patient_appointment'),
    path('display_home/(?P<user>.*)',display_home,name='display_home'),
    path('dashboard/(?P<user>.*)', dashboard , name = 'dashboard'),
    path('receptionist_dashboard/(?P<user>.*)', receptionist_dashboard , name = 'receptionist_dashboard'),

    
   
    path('create_appointment/(?P<user>.*)', create_appointment , name = 'create_appointment'),
    path('delete_patient/(?P<id>\d+)', delete_patient , name = 'delete_patient'),
    path('delete_medicine/(?P<id>\d+)/<int:pk>', delete_medicine , name = 'delete_medicine'),
    path('update_patient/(?P<id>\d+)', update_patient , name = 'update_patient'),

    path('create_patient/', create_patient , name = 'create_patient'),
    path('myappointment/', myappointment , name = 'myappointment'),
    path('app_doctor',appoint_doctor,name='appoint_doctor'),
    path('doc_upload_newcase',doc_upload_newcase,name='doc_upload_newcase'),
    path('start_consultancy/<str:branch>',start_consultancy,name='start_consultancy'),
    path('stop_consultancy/<str:branch>',stop_consultancy,name='stop_consultancy'),
    path('docter_appointment/', docter_appointment , name = 'docter_appointment'),
    path('docter_appointment/Dombivali', docter_appointment_dombivali , name = 'docter_appointment_dombivali'),
    path('doc_repeat_medicine/Dombivili',doc_repeat_med_dom,name='doc_repeat_med_dom'),    
    path('doc_repeat_medicine/Mulund',doc_repeat_med_mul,name='doc_repeat_med_mul'),
    path('doc_courier_medicine/Dombivili',doc_courier_med_dom,name='doc_courier_med_dom'), 
    path('doc_courier_medicine/Mulund',doc_courier_med_mul,name='doc_courier_med_mul'),
    path('docter_appointment/Mulund', docter_appointment_mulund , name = 'docter_appointment_mulund'),
    path('docter_prescription/', docter_prescription , name = 'docter_prescription'),
    path('create_prescription/', create_prescription , name = 'create_prescription'),
    # path('medical_history/', medical_history , name = 'medical_history'),
    path('images/',images,name ='images'),
    path('delete_images/<int:id>',delete_images,name ='delete_images'),
    path('update_status/(?P<id>\d+)', update_status , name = 'update_status'),
    path('hr_dashboard/', hr_dashboard , name = 'hr_dashboard'),
    path('hr_collections/',hr_collections,name='hr_collections'),
    path('hr-courier-list/<str:branch>/',hr_courier_list,name='hr_courier_list'),
    path('all-courier/<str:branch>/',all_courier,name='all_courier'),
    path('view-courier-details/<str:branch>/',view_courier_details,name='view_courier_details'),
    path('view-payment-courier/<str:pk>/',view_payment_courier,name='view_payment_courier'),
    path('update-payment-courier/<str:pk>/',update_payment_courier,name='update_payment_courier'),
    path('mark-receive-courier/<str:pk>/',mark_receive_courier,name='mark_receive_courier'),
    path('hr_balance/', hr_balance , name = 'hr_balance'),
    path('doc_balance/', doc_balance , name = 'doc_balance'),
    path('pay_balance/<int:id>', pay_balance,name='pay_balance'),
    path('hr_accounting/', hr_accounting , name = 'hr_accounting'),
    path('hr_repeat_medicine/', hr_repeat_medicine , name = 'hr_repeat_medicine'),
    path('hr_courier_medicine/', hr_courier_medicine , name = 'hr_courier_medicine'),
    path('hr_send_mail/', hr_send_mail , name = 'hr_send_mail'),
    path('hr_medicine_prescription/<int:id>',hr_medicine_prescription,name='hr_medicine_prescription'),
    path('hr_medicine_payment/<int:id>',hr_medicine_payment,name='hr_medicine_payment'),
    path('hr_status/<int:id>',hr_status,name='hr_status'),
    path('payment-cancelation/<int:id>/',payment_cancellation,name='payment_cancellation'),
    path('update_docter/(?P<id>\d+)', update_docter , name = 'update_docter'),
    path('update_receptionist/(?P<id>\d+)', update_receptionist , name = 'update_receptionist'),
    path('delete_docter/', delete_docter , name = 'delete_docter'),
    path('patient_invoice/', patient_invoice , name = 'patient_invoice'),
    path('get_pdf/(?P<id>\d+)', get_pdf , name = 'get_pdf'),
    path('send_reminder/(?P<id>\d+)', send_reminder , name = 'send_reminder'),
    path('apointmentDetails/<int:id>/<int:token>', apointmentDetails , name = 'apointmentDetails'),
    path('health-assessment/<int:id>/<int:token>',health_assessment,name='health_assessment'),
    path('delete-health/<int:id>/<int:token>',delete_health_assessment,name="delete_health_assessment"),

    path('extra_prescription/<int:id>/<int:token>', extra_prescription , name = 'extra_prescription'),
    path('add-consultation/<int:id>/<int:token>', add_consultation , name = 'add_consultation'),
    path('delete_consultation_charges/<int:id>/<int:token>', delete_consultation_charges , name = 'delete_consultation_charges'),

    path('delete_extra_prescription/<int:id>/<int:token>',delete_extra_prescription , name = 'delete_extra_prescription'),

    path('upload_patients_image/<int:id>',upload_patients_image,name="upload_patients_image"),
    path('doc_patient_images/<int:id>',doc_patient_images,name="doc_patient_images"),

    path('investigation_patient/<int:id>', investigation_newone , name = 'investigation_newone'),
    path('ultra_sonography/<int:id>', ultra_sonography_newone , name = 'ultra_sonography_newone'),
    path('doppler_studies/<int:id>', doppler_studies_newone , name = 'doppler_studies_newone'),
    path('obstetrics/<int:id>', obstetrics_newone , name = 'obstetrics_newone'),
    path('sonography/<int:id>', sonography_newone , name = 'sonography_newone'),
    path('ct_scan/<int:id>', ct_scan_newone , name = 'ct_scan_newone'),
    path('mri_scan/<int:id>', mri_scan_newone , name = 'mri_scan_newone'),
    path('generate_investigation_pdf/<int:id>', generate_investigation_pdf , name = 'generate_investigation_pdf'),
    path('investigation_pdf/<int:pk>', Investigation_pdf.as_view() , name = 'investigation_pdf'),
    path("add_investigation/<int:pk>",add_investigation,name="add_investigation"),
    path("add_ultrasonography/<int:pk>",add_ultrasonography,name="add_ultrasonography"),
    path("add_doppler/<int:pk>",add_doppler,name="add_doppler"),
    path("add_obstetrics/<int:pk>",add_obstetrics,name="add_obstetrics"),
    path("add_sonographytype/<int:pk>",add_sonographytype,name="add_sonographytype"),
    path("add_ctscan/<int:pk>",add_ctscan,name="add_ctscan"),
    path("add_mriscan/<int:pk>",add_mriscan,name="add_mriscan"),
    path("delete_investigation/<int:id>",delete_investigation,name="delete_investigation"),
    path("delete_newcase/<int:id>",delete_newcase,name="delete_newcase"),

    path('casehistory_pdf/<int:id>',casehistory_pdf,name='casehistory_pdf'),
    path('appointmentDashboard/<int:id>',appointmentDashboard,name='appointmentDashboard'),
    path('previousDashboard/<int:id>',previousDashboard,name='previousDashboard'),
    path('imagesDashboard/<int:id>',imagesDashboard,name='imagesDashboard'),
    path('update_medicine/(?P<id>\d+/<int:pk>)',update_medicine,name="update_medicine"),
    # path('list/(?P<id>\d+)',),
    # path('detail_list/<int:pk>', ExampleDetailView.as_view(), name='detail_list'),
    path('old_images/<int:id>',old_images,name='old_images'),
    path('casepaper_new_images/<int:id>',casepaper_new_images,name='casepaper_new_images'),
    path('upload_case_image/<int:id>',upload_case_image,name='upload_case_image'),
    path('list1/<int:pk>', list1 ,name = 'list1'),
    path('list1_pdf/<int:pk>',list1_pdf,name='list1_pdf'),
    path('back_update',back_update,name='back_update'),
    path('back_delete',back_delete,name='back_delete'),
    path('apointment_detail_home',apointment_detail_home,name='apointment_detail_home'),    
    path('list', ExampleListView.as_view(), name='list'),
    path('create1/<int:pk>', create1 ,name ='create1'),
    path('create', ExampleCreateView.as_view(), name='create'),
    path('update/<int:pk>', ExampleUpdateView.as_view(), name='update'),
    # path('update_chief_complaint/<int:pk>',NewCaseUpdateView.as_view(),name='update_chief_complaint'),
    path('delete/<int:pk>',ExampleDeleteView.as_view(), name = 'delete'),
    # path('create/(?P<id>\d+)', create_view ,name = 'create_view'),
    # path('presciption_details/(?P<id>\d+)', presciption_details , name = 'presciption_details'),
    # path('payment/<int:pk>', payment , name = 'payment'),
    path('payment/(?P<id>\d+)', payment , name = 'payment'),
    path('doc_repeat_medicine/(?P<id>\d+)/<int:pk>',doc_repeat_medicine,name = "doc_repeat_medicine"),
    # path('payment/<int:id>', payment , name = 'payment'),    
    #path('create_prescription/',create_prescription , name = 'create_prescription'),
    path('patientdetail/', patientDetail , name = 'patientDetail'),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('quote/', quotation , name = 'quote'),
    path('organsconflicts/', Gnm_Sbs_Conflicts , name='Gnm_Sbs_Conflicts'),

    path('delete_organs/<int:id>/', delete_organs , name = 'delete_organs'),
    path('delete_quote/<int:id>/',delete_quote, name='delete_quote' ),

    path('mysign',my_sign , name = 'mysign'),
    path('index/',index,name='dashboard'),
    path('previous_issued_certificate',previous_issued_certificate,name="previous_issued_certificate"),
    path('regenerate_issued_certificate/<int:id>',regenerate_issued_certificate,name="regenerate_issued_certificate"),
    path('regen_medical_certificate_pdf/<int:id>',regen_medical_certificate_pdf,name="regen_medical_certificate_pdf"),
    path('regen_fitness_certificate_pdf/<int:id>',regen_fitness_certificate_pdf,name="regen_fitness_certificate_pdf"),
    path('regen_travelling_certificate_pdf/<int:id>',regen_travelling_certificate_pdf,name="regen_travelling_certificate_pdf"),
    path('regen_unfit_certificate_pdf/<int:id>',regen_unfit_certificate_pdf,name="regen_unfit_certificate_pdf"),
    path('addcertificate',addcertificate,name='addcertificate'),
    path('medical_certificate_pdf/<int:id>',medical_certificate_pdf,name="medical_certificate_pdf"),
    path('fitness_certificate_pdf/<int:id>',fitness_certificate_pdf,name="fitness_certificate_pdf"),
    path('travelling_certificate_pdf/<int:id>',travelling_certificate_pdf,name="travelling_certificate_pdf"),
    path('unfit_certificate_pdf/<int:id>',unfit_certificate_pdf,name="unfit_certificate_pdf"),
    path('previous_issued_invoice',previous_issued_invoice,name="previous_issued_invoice"),
    path('regen_bill_pdf/<int:id>',regen_bill_pdf,name='regen_bill_pdf'), 
    path('addpatient',addpatient,name='addpatient'),
    path('bills/<int:id>',bills,name='bills'),
    path('bill_pdf/<int:id>',bill_pdf,name='bill_pdf'),    
    path('pricing',pricing,name = 'pricing'),
    path('diagnosis_history',diagnosis_history,name="diagnosis_history"),
    path('chiefcomplaints/', chiefcomplaints ,name='chiefcomplaints'),
    path('fearIncidents/',fearIncidents, name='fearIncidents'),
    path('past/', pasthistory , name='past'),
    path('familymedical/',familymedical, name='familymedical'),
    path('personalhabits/',personalhabits, name='personalhabits'),
    path('personalappetite/', personalappetite , name='personalappetite'),
    path('infood/', infood , name='infood'),
    path('sexualsphere/',sexualsphere, name='sexualsphere'),
    path('investigation1/',investigation1,name='investigation'),
    path('thermalreaction/',thermalreaction,name="thermalreaction"),
    path('rubricselection/', rubricselection, name="rubricselection"),
    path('allstaff/',allstaff, name="allstaff"),
    path('dash_recep/<int:id>',dash_recep,name="dash_recep"),
    path('recep_documents/<int:id>',recep_documents,name="recep_documents"),
    path('recep_gallery/<int:id>',recep_gallery,name="recep_gallery"),
    path('dash_hr/<int:id>',dash_hr,name="dash_hr"),
    path('hr_documents/<int:id>',hr_documents,name="hr_documents"),
    path('hr_gallery/<int:id>',hr_gallery,name="hr_gallery"),
    path('addstaff/',addstaff, name="addstaff"),
    path('editstaff/',editstaff, name="editstaff"),
    path('gallery/',gallery,name="gallery"),
    path('allrooms/',allroom,name="allroom"),
    path('addrooms/',addroom,name="addroom"),
    path('editrooms/',editroom,name="editroom"),
    path('pagination/',pagination,name="pagination"),
    path('drum1bottle/',drum1bottle,name="drum1bottle"),
    path('halfdrumbottle/',halfdrumbottle,name="halfdrumbottle"),
    path('pills/',pills,name="pills"),
    path('multiple/',multiple,name="multiple"),
    path('mind2/',demo,name="mind2"),
    path('mental/',mental,name="mental"),
    path('miasm/',miasm,name='miasm'),
    path('multipleselect/',multipleselect,name="multipleselect"),
    path('personalappetite/',personalappetite,name='personalappetite'),
    path('lifestory/',lifestory,name='lifestory'),
    path('accordian/',accordian,name='accordian'),
    path('appointment/',appontment, name='appontment'),
    path('ordermedi1cine/',ordermedi1cine, name='ordermedi1cine'),
    path('addmedicine/',addmedicine, name='addmedicine'),
    path('addstaff/',addstaff, name='addstaff'),
    path('one_drum_bottles/', one_drum_bottles, name='one_drum_bottles'),
    path('half_drum_bottle/', half_drum_bottle , name='half_drum_bottle'),
    path('pills/', pills , name='pills' ),
    


    #path('create', ExampleCreateView.as_view(), name='create'),
    path('book/',book,name='book'),
    # path('list/',list,name='list'), ## commented by me
    path('listdetails/<int:pk>/',listdetails,name='listdetails'),
    
    path('upload_images/(?P<id>\d+)',upload_images, name='upload_images'),
    # path('upload_images/<int:id>',upload_images, name='upload_images'),


    
    path('myitem/<int:pk>/', myitem, name='myitem'),
    path('delitem/<int:pk>/', delitem, name='delitem'),
    path('deless/<int:id>/<int:pk>/', deless, name='deless'),
    path('delh1/<int:id>/<int:pk>/', delh1, name='delh1'),
    path('delh2/<int:id>/<int:pk>/', delh2, name='delh2'),
    path('delan/<int:id>/<int:pk>/', delan, name='delan'),
    
    path('delitem2/<int:id>/<int:pk>/', delitem2, name='delitem2'),

    path('itemDetail/<int:pk>/', itemDetail, name='itemDetail'),
    path('ess/<int:pk>/', ess, name='ess'),
    path('he1/<int:pk>/', he1, name='he1'),
    path('he2/<int:pk>/', he2, name='he2'),
    path('ana/<int:pk>/', ana, name='ana'),
    path('dash_patients_details/(?P<user>.*)',dash_patients_details, name="patients_details"),
    path('dash_appointment_details/(?P<user>.*)', dash_appointment_details, name="appointment_details"),
    path('repeat_med_details/(?P<user>.*)',repeat_med_details, name="repeat_medicicne"),
    path('doc_repeat_med_details/(?P<user>.*)',doc_repeat_med_details, name="doc_repeat_medicicne"),
    path('courier_medicine/(?P<user>.*)',courier_medicine, name="courier_medicicne"),
    path('doc_courier_mail/',doc_courier_medicine, name="doc_courier_medicicne"),
    path('send_mail/<int:id>',send_mail,name='send_mail'),

    path('send-mail-courier/<int:id>/',send_mail_courier,name='send_mail_courier'),
    path('send-mail-general-repeat/<int:id>/',send_mail_general_repeat,name='send_mail_general_repeat'),
    path('general_med_mail/<int:id>',general_med_mail,name='general_med_mail'),
    path('send_mail_hr/<int:id>',send_mail_hr,name='send_mail_hr'),
    path('online_consultation/(?P<user>.*)',online_consultation, name="online_consultation"),
    path('old_prescription/(?P<user>.*)',old_prescription,name='old_prescription'),
    path('add_question/',add_question, name='add_question'),
    path('retrive/',retrive, name='retrive'),
    path('add_appetite/',add_appetite,name='add_appetite'),
    path('appetite_retrive/',appetite_retrive,name='appetite_retrive'),
    path('answar/',answar, name='answar'),
    path('displays_fil_rec/', displays_fil_rec ,name="displays_fil_rec"),
    path('dombivali_collection',dombivali_collection,name='dombivali_collection'),
    path('dombivali_collection_general',dombivali_collection_general,name='dombivali_collection_general'),
    path('dombivali_collection_repeat',dombivali_collection_repeat,name='dombivali_collection_repeat'),
    path('dombivali_collection_courier',dombivali_collection_courier,name='dombivali_collection_courier'),
    

    path('mulund_collection',mulund_collection,name='mulund_collection'),
    path('mulund_collection_general',mulund_collection_general,name='mulund_collection_general'),
    path('mulund_collection_repeat',mulund_collection_repeat,name='mulund_collection_repeat'),
    path('mulund_collection_courier',mulund_collection_courier,name='mulund_collection_courier'),
    path('newcase/',newcase,name='newcase'),
    path('new_case',new_case_one,name='new_case_one'),
    path('addquestion',addquestion,name="addquestion"),
    path('gen_pdf/<int:case_id>',gen_pdf,name='gen_pdf'),
    path('past_history_patient_old/<int:case_id>',past_history_patient,name='past_history_patient'),
    path('present_complaints_patient/<int:case_id>',present_complaints_newone,name='past_history_newone'),

    path('present-complaints-add/<int:id>/',present_complaints_add,name='present_complaints_add'),
    path('present_complaints_patient/<int:case_id>/complain/<int:id>',complain,name='complain'),
    path('delete-present-complaints/<int:id>/',delete_present_complaints,name='delete_present_complaints'),
    path('delete_added_present_complaints/<int:id>/',delete_added_present_complaints,name='delete_added_present_complaints'),
    path('patient_history/<int:case_id>',patient_history_newone,name='patient_history_newone'),
    path('patient_history/<int:case_id>/complain/<int:id>',patient_history_complain,name='patient_history_complain'),
    path('delete-past-history/<int:id>/',delete_past_history,name='delete_past_history'),

    path('new-case-report/<int:id>/',new_case_report,name='new_case_report'),
    
    path('add_mental_causative/<int:case_id>',add_mental_causative,name='add_mental_causative'),
    path('add_mental_personality/<int:case_id>',add_mental_personality,name='add_mental_personality'),
    path('add_complain/<int:case_id>',add_complain,name='add_complain'),
    path('add_disease/<int:case_id>',add_disease_patient_history,name='add_disease_patient_history'),
    path('add_family_complain/<int:case_id>',add_family_complain,name='add_family_complain'),
    path('add_disease/<int:case_id>',add_disease,name='add_disease'),
    path('past_history_new/<int:case_id>',past_history_new,name='past_history_new'),
    path('past_history/<int:id>/patient/<int:case_id>',past_history,name='past_history'),
    path('next_history/<int:id>/patient/<int:case_id>',next_history,name='next_history'),
    path('Create', JSCreateView.as_view(), name='Create'),
    path('create_pad',NewCaseCreateView.as_view(),name ='cheif_complaint_create'),
    path('create_pad_one',NewCaseCreateViewOne.as_view(),name ='cheif_complaint_create_one'),
    path('update_pad/<int:pk>',NewCaseUpdateView.as_view(),name='chief_complaint_update'),
    path('present-complaint-appointment/<int:case_id>/<int:token>/',present_complaint_appointment,name='present_complaint_appointment'),
    path('chief_complaints/<int:case_id>',chief_complaints_newone,name='chief_complaints_newone'),
    path('view_chief_complaints/<int:case_id>',chief_complaints_view,name='chief_complaints_view'),
    path('view_present_complaints/<int:case_id>/<int:token>/',present_complaints_view,name='present_complaints_view'),
    path('update_chief_complaints/<int:id>',update_chief_complaints,name='update_chief_complaints'),
    path('ask_delete/<int:id>',ask_delete,name='ask_delete'),
    path('delete_chief_complaints/<int:id>',delete_chief_complaints,name='delete_chief_complaints'),
    path('familymedical_ho/<int:case_id>',family_medical_newone,name='family_medical_newone'),
    path('miasm/<int:case_id>',miasm_examination_newone,name='miasm_examination_newone'),
    path('mental_causative_factor/<int:case_id>',mental_causative_newone,name='mental_causative_newone'),
    path('mental_causative_factor_pad/<int:case_id>',mental_causative_jspad,name='mental_causative_jspad'),
    path('mental_causative_factor_view/<int:case_id>',mental_causative_view,name='mental_causative_view'),
    path('mental_causative_factor_update/<int:id>',mental_causative_update,name='mental_causative_update'),
    path('mental_personality_character/<int:case_id>',mental_personality_newone,name='mental_personality_newone'),
    path('mental_personality_pad/<int:case_id>',mental_personality_jspad,name='mental_personality_jspad'),
    path('mental_personality_view/<int:case_id>',mental_personality_view,name='mental_personality_view'),
    path('mental_personality_update/<int:id>',mental_personality_update,name='mental_personality_update'),
    path('personal_history/<int:case_id>',personal_history_newone,name='personal_history_newone'),
    path('personal_history_view/<int:case_id>',personal_history_view,name='personal_history_view'),
    path('update_personal_history/<int:id>',update_personal_history,name='update_personal_history'),

    path('BMS/<int:case_id>',bms_newone,name='bms_newone'),
    path('BMS_add/<int:case_id>',bms_add,name='bms_add'),
    path('BMS_view/<int:case_id>',bms_view,name='bms_view'),
    path('bms_update/<int:id>',bms_update,name='bms_update'),

    path('thermal/<int:case_id>',thermal_newone,name='thermal_newone'),
    path('thermal_view/<int:case_id>',thermal_view,name='thermal_view'),
    path('thermal_update/<int:id>',thermal_update,name='thermal_update'),

    path('report/<int:case_id>',newcase_final_report,name="newcase_final_report"),
    path('gen_pdf_new/<int:pk>',GeneratePdf.as_view(),name='gen_pdf_new'),

    path('show_case_paper/<int:pk>',ShowCasePdf.as_view(),name='show_case_paper'),

    path('personal_appetite/<int:id>/patient/<int:case_id>',personal_appetite,name='personal_appetite'),
    path('next1/<int:id>/patient/<int:case_id>',next1,name="next1"),
    path('sex_history/<int:id>/patient/<int:case_id>',sex_history,name="sex_history"),
    path('next2/<int:id>/patient/<int:case_id>',next2,name="next2"),
    path('mental_personality_old/<int:id>/patient/<int:case_id>',mental_personality,name='mental_personality'),
    path('next3/<int:id>/patient/<int:case_id>',next3,name="next3"),
    path('thermal_reaction/<int:id>/patient/<int:case_id>',thermal_reaction,name='thermal_reaction'),
    path('next4/<int:id>/patient/<int:case_id>',next4,name="next4"),
    path('investigation/<int:id>/patient/<int:case_id>',investigation,name='investigation'),
    path('next5/<int:id>/patient/<int:case_id>',next5,name="next5"),
    path('chief_complaints_old/<int:id>/patient/<int:case_id>',chief_complaints,name='chief_complaints'),
    
    path('next6/<int:id>/patient/<int:case_id>',next6,name="next6"),
    path('personal_history_old/<int:id>/patient/<int:case_id>',patient_personal_history,name='patient_personal_history'),
    path('next7/<int:id>/patient/<int:case_id>',next7,name="next7"),
    path('personal_habits/<int:case_id>',personal_habits,name='personal_habits'),
    path('personal_new_habits/<int:case_id>',personal_new_habits,name='personal_new_habits'),
    path('InFood/<int:case_id>',In_Food,name='InFood'),
    path('mental_causative_Factor/<int:case_id>',mental_causative,name='mental_causative'),
    path('personality_character/<int:case_id>',personality_character,name='personality_character'),
    path('mia_sm/<int:case_id>',mia_sm,name='mia_sm'),
    path('rubric/<int:case_id>',rubric,name='rubric'),

    path('list_medicine/', list_medicine, name='list_medicine'),
    path('reorder_list/', reorder_list, name='reorder_list'),
    path('add_medicine/', add_medicine, name='add_medicine'),
    path('update_med/<str:pk>/', update_med, name="update_med"),
    path('delete__medicine/<str:pk>/', delete_med, name="delete_med"),
    path('medicine_stock/<str:pk>/', medicine_stock, name="medicine_stock"),
    path('issue_medicine/<str:pk>/', issue_medicine, name="issue_medicine"),
    path('receive_medicine/<str:pk>/', receive_medicine, name="receive_medicine"),
    path('reorder_level/<str:pk>/', reorder_med_level, name="reorder_med_level"),

    #STOCK MANAGEMENT

    path('add-stock/', add_stock, name='add_stock'),
    path('add-stock-name/', add_stock_name, name='add_stock_name'),
    path('list-stock/', list_stock, name='list_stock'),
        # path('list-stock/', test_function, name='list_stock'),

    path('view-bill/<str:pk>',bill_view, name='bill_view'),
    path('Stock-bills/<str:pk>',all_stock_bills, name='all_stock_bills'),

    path('delete-stock/<str:pk>/', delete_stock, name="delete_stock"),
    path('stock-management/<str:pk>', stock_management, name="stock_management"),
    path('issue-stock/<str:pk>/', issue_stock, name="issue_stock"),
    path('receive-stock/<str:pk>/', receive_stock, name="receive_stock"),
    path('reorder-stock/<str:pk>/', reorder_stock, name="reorder_stock"),

    # DOCTOR DASHBOARD
    path('list-approval/<str:branch>', list_approval, name='list_approval'),
    path('approve-new-stock/<str:pk>/', approve_new_stock, name='approve_new_stock'),
    path('approve-issue-stock/<str:pk>/', approve_issue_stock, name='approve_issue_stock'),
    path('approve-receive-stock/<str:pk>/', approve_receive_stock, name='approve_receive_stock'),

    #MEDICINE MANAGEMENT

    path('add-medicine-name-hr/', add_medicine_name_hr, name='add_medicine_name_hr'),
    path('add-potency-name-hr/', add_potency_name_hr, name='add_potency_name_hr'),
    path('add-medicine-stock-hr/', add_medicine_stock_hr, name='add_medicine_stock_hr'),
    path('medicine-stock-list-hr/', medicine_stock_list_hr, name='medicine_stock_list_hr'),
    path("add-reorder-medicine/<str:pk>",add_reorder_medicine, name= 'add_reorder_medicine'),
    # path('place-reorder-medicine-hr/', place_reorder_medicine, name='place_reorder_medicine'),
    path('place-reorder-medicine-hr/', place_reorder_medicine_modelformset, name='place_reorder_medicine'),
    path('remove-reorder-medicine/<str:pk>/', remove_reorder_medicine, name='remove_reorder_medicine'),

    path('vendor-med-mail/<str:pk>',vendor_med_mail,name='vendor_med_mail'),
    path('medicine_order_history/',medicine_order_history,name='medicine_order_history'),
    path('Dom-medicine-order-history/',dom_med_order_history,name='dom_med_order_history'),
    path('doc-verify-med-order/<str:pk>/',doc_verify_med_order,name='doc_verify_med_order'), 
    path('view-medicine-order-bill/<str:pk>/',view_medicine_order_bill,name='view_medicine_order_bill'), 

    path('medicine_order_receive/<str:pk>/',medicine_order_receive,name='medicine_order_receive'),
    path('bill_medicine_order_receive/<str:pk>/',bill_medicine_order_receive,name='bill_medicine_order_receive'),


    path('del-test-med-orders/',delete_all_placed_med,name='delete_all_placed_med'), #TESTING
    path('view-bill-med/<str:pk>',med_bill_view, name='med_bill_view'),
    path('Medicine-bills/<str:pk>',all_med_bills, name='all_med_bills'),
    path('delete-medicine-stock-hr/<str:pk>/', delete_medicine_stock_hr, name='delete_medicine_stock_hr'),
    path('medicine-stock-management-hr/<str:pk>', medicine_stock_management_hr, name='medicine_stock_management_hr'),
    path('issue-medicine-hr/<str:pk>/', issue_medicine_hr, name='issue_medicine_hr'),
    path('receive-medicine-hr/<str:pk>/', receive_medicine_hr, name='receive_medicine_hr'),
    path('reorder_medicine_hr/<str:pk>/', reorder_medicine_hr, name='reorder_medicine_hr'),

    #DOCTOR DASHBOARD
    path('medicine-stock-approval/<str:branch>', medicine_stock_approval, name='medicine_stock_approval'),
    path('approve-new-med-hr/<str:pk>/', approve_new_med_hr, name='approve_new_med_hr'),
    path('approve-issue-med-hr/<str:pk>/', approve_issue_med_hr, name='approve_issue_med_hr'),
    path('approve-receive-med-hr/<str:pk>/', approve_receive_med_hr, name='approve_receive_med_hr'),

    path('add-vendor-stock/',add_vendor_stock, name='add_vendor_stock'),
    path('vendor-stock-list/',vendor_stock_list, name='vendor_stock_list'),
    path('add-product-vendor-stock/<str:pk>/',add_product_vendor_stock, name='add_product_vendor_stock'),
    path('ajax/load-products/',load_products,name='ajax_load_products'),  #AJAX 
    path('ajax/load-medicines/',load_medicines,name='ajax_load_medicines'), #AJAX
    path('place-order-stock/<str:pk>/',place_order_stock, name='place_order_stock'),
    path('order-placed-vendor-stockinfo/<str:pk>/',order_placed_vendor_stockinfo, name='order_placed_vendor_stockinfo'),
    path('delete-order-stock/<str:pk>',delete_order_stock,name="delete_order_stock"),
    path('order-summary-stock/<str:pk>/',order_summary_stock,name="order_summary_stock"),
    path('mail-order-stock-vendor/<str:pk>/',mail_order_stock, name='mail_order_stock'),
    path('place-order-medicine/<str:pk>/',place_order_medicine, name='place_order_medicine'),
    path('place-order-medicine-vendors/<str:pk>/',place_order_medicine_vendors, name='place_order_medicine_vendors'),
    path('order-medicine/<str:pk>/',order_here_medicine, name='order_here_medicine'),

    path('order-placed-vendor-medicineinfo/<str:pk>/',order_placed_vendor_medicineinfo, name='order_placed_vendor_medicineinfo'),
    path('delete-order-medicine/<str:pk>',delete_order_medicine,name="delete_order_medicine"),
    path('order-summary-medicine/<str:pk>/',order_summary_medicine,name="order_summary_medicine"),
    path('order_medicine_summary/<str:pk>',order_medicine_summary,name="order_medicine_summary"),
    path('mail-order-medicine-vendor/<str:pk>/',mail_order_medicine_new, name='mail_order_medicine_new'),


    path('mail-order-medicine-vendor/<str:pk>/',mail_order_medicine, name='mail_order_medicine'),


    path('send-mail-stock-vendor/<str:pk>/',mail_stock_vendor, name='mail_stock_vendor'),
    path('send-mail-medicine-vendor/<str:pk>/',mail_medicine_vendor, name='mail_medicine_vendor'),

    
    path('stock-orders-placed/',orders_placed_all, name='orders_placed_all'),
    path('mark-stock-delivered/<str:pk>',mark_stock_delivered, name='mark_stock_delivered'),

    # To be worked on:
    path('mark-medicine-delivered/<str:pk>',mark_medicine_delivered, name='mark_medicine_delivered'),
 

    path('medicine-orders-placed/',orders_placed_medicine, name='orders_placed_medicine'),

    # DASHBOARD 

    path('edit-home-page/',edit_home_page,name='edit_home_page'),
    path('update-branch-numbers/<str:pk>',update_branch_numbers,name='update_branch_numbers'),
    path('delete-branch-numbers/<str:pk>',delete_branch_numbers,name='delete_branch_numbers'),
    path('add-portfolio-images/',add_portfolio_images,name='add_portfolio_images'),
    path('delete-portfolio-images/<str:pk>',delete_portfolio_images,name='delete_portfolio_images'),


    # ITEMS INVENTORY -FINAL CODE

    path('items-inventory/',items_inventory_home,name='items_inventory_home'),
    path('add-items-unit',add_items_unit,name='add_items_unit'),
    path('items-vendors/',items_vendors,name='items_vendors'),
    path('items-vendor-update/<str:id>/',items_vendor_update,name='items_vendor_update'),
    path('add-items-inventory/',add_items_inventory,name='add_items_inventory'),
    path('issue-items-inventory/<str:id>/',issue_items_inventory,name='issue_items_inventory'),
    path('reorder-level-items/<str:id>/',reorder_level_items,name='reorder_level_items'),
    path('place-order-items/',place_order_items,name='place_order_items'),
    path('remove_order_items/',remove_order_items, name='remove_order_items'),
    path('upload-bill-items/<str:id>/',upload_bill_items,name='upload_bill_items'),
    path('receive-order-items/<str:id>/',receive_order_items,name='receive_order_items'),
    path('view-bill-items/<str:id>/',view_bill_items,name='view_bill_items'),
    path('approve-items-doctor/<str:branch>/',approve_items_doctor,name='approve_items_doctor'),
    path('approve-flag-new-items/<str:id>/',approve_flag_new_items,name='approve_flag_new_items'),
    path('approve-flag-issue-items/<str:id>/',approve_flag_issue_items,name='approve_flag_issue_items'),
    path('approve-flag-receive-items/<str:id>/',approve_flag_receive_items,name='approve_flag_receive_items'),
    path('order-history-items/<str:branch>/',order_history_items,name='order_history_items'),
    path('approve-bills-items/<str:id>/',approve_bills_items,name='approve_bills_items'),
    path('add-transaction-details-items/<str:id>/',add_transaction_details_items,name='add_transaction_details_items'),

    # MEDICINE INVENTORY - FINAL CODE

    path('medicines-inventory/',medicines_inventory_home,name='medicines_inventory_home'),
    path('add-medicines-potency/',add_medicines_potency,name='add_medicines_potency'),
    path('medicines-vendors/',medicines_vendors,name='medicines_vendors'),
    path('medicines-vendors-update/<str:id>',medicines_vendors_update,name='medicines_vendors_update'),
    path('add-medicines-inventory/',add_medicines_inventory,name='add_medicines_inventory'),
    path('reorder-medicines/<str:id>/',reorder_medicine,name='reorder_medicine'),
    path('issue-medicine-inventory/<str:id>/',issue_medicine_inventory,name='issue_medicine_inventory'),
    path('order-medicines-inventory/',order_medicines_inventory,name='order_medicines_inventory'),
    path('remove_order/', remove_order, name='remove_order'),
    path('upload-bills-medicine/<str:id>/',upload_bills_medicine,name='upload_bills_medicine'),
    path('receive-order-medicines/<str:id>/',receive_order_medicines,name='receive_order_medicines'),
    path('view-bill-medicines/<str:id>/',view_bill_medicines,name='view_bill_medicines'),
    path('approve-medicines-doctor/<str:branch>/',approve_medicines_doctor,name='approve_medicines_doctor'),
    path('approve-flag-new-medicine/<str:id>/',approve_flag_new_medicine,name='approve_flag_new_medicine'),
    path('approve-flag-issue-medicine/<str:id>/',approve_flag_issue_medicine,name='approve_flag_issue_medicine'),
    path('approve-flag-receive-medicine/<str:id>/',approve_flag_receive_medicine,name='approve_flag_receive_medicine'),
    path('order-history-medicines/<str:branch>/',order_history_medicines,name='order_history_medicines'),
    path('approve-bill-medicines/<str:id>/',approve_bill_medicines,name="approve_bill_medicines"),
    path('add-transaction-medicines/<str:id>/',add_transaction_medicines,name="add_transaction_medicines"),
    path('order-balances-medicines/<str:branch>/',order_balances_medicines,name='order_balances_medicines'),

    path('order-balances-items/<str:branch>/',order_balances_items,name='order_balances_items'),


    # DOCTOR DASHBOARD BALANCE LIST
    path('balance-list/<str:branch>/', balance_list,name='balance_list'),
    path('balance-list-pdf/<str:branch>/', Balance_list_pdf.as_view() , name = 'balance_list_pdf'),
    # path('place-new-order-doctor/',place_new_order_doctor,name='place_new_order_doctor'),   #NOT USED
    # path('place-order-doctor-mail/<str:id>/',place_order_doctor_mail,name='place_order_doctor_mail'),
    path('homeo-book-medicine/',homeo_book,name='homeo_book'),
    path('homeo-book-update/<str:id>/',homeo_book_update,name='homeo_book_update'),
    path('homeo-book-delete/<str:id>/',homeo_book_delete,name='homeo_book_delete'),

    path('homeo-book-disease/',homeo_book_disease,name='homeo_book_disease'),
    path('homeo-book-update-disease/<str:id>/',homeo_book_update_disease,name='homeo_book_update_disease'),
    path('home-book-delete-disease/<str:id>/',home_book_delete_disease,name='home_book_delete_disease'),

    path('homeo-book-redline-symptoms/',home_book_redline_symptoms,name='home_book_redline_symptoms'),
    path('homeo_book_update_redline/<str:id>/',homeo_book_update_redline,name='homeo_book_update_redline'),
    path('home-book-delete-redline/<str:id>/',home_book_delete_redline,name='home_book_delete_redline'),
    # RECEPTIONIST/HR NEW ORDER BALANCE
    # path('new-order-history/',new_order_history,name='name_order_history'),
    path('homeo-bhagwat-gita-pdf/',Homeo_pdf.as_view(),name='homeo_pdf'),
    path('homeo-bhagwat-gita-pdf/<int:id>/',Homeo_pdf_id.as_view(),name='homeo_pdf_id'),

    path('assign-tasks/',assign_tasks,name='assign_tasks'),
    path('delete-tasks/<str:id>/',delete_task,name='delete_task'),

    path('task-details/',task_details,name='task_details'),
    path('task-complete/<str:id>/',task_complete,name='task_complete'),

    path('apply-leave/',apply_leave,name='apply_leave'),
    path('approve-leaves/',approve_leaves,name='approve_leaves'),
    path('is-approved-leave/<str:id>/',is_approved_leave,name='is_approved_leave'),
    path('leave-details/<str:user>/',leave_details,name='leave_details'),

    path('place-new-order-medicine/',place_new_order_medicine,name='place_new_order_medicine'),


    #DOCTOR DIAGNOSE HISTORY

    path('doctor-diagnose-history/',doctor_diagnose_history,name='doctor_diagnose_history'),

    path('doctor-diagnose-pdf/',Doctor_diagnose_pdf.as_view(),name='doctor_diagnose_pdf'),
    path('doctor-pdf/<int:pk>/',Doctor_pdf.as_view(),name='doctor_pdf'),
   



] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)


