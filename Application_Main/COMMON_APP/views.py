from email.utils import quote
from xml.dom.minidom import NamedNodeMap
from django.shortcuts import render , redirect , HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View
from django import template
from django.template.loader import get_template
from io import BytesIO
import xhtml2pdf.pisa as pisa
from .utils import render_to_pdf #created in step 4
from django.db import IntegrityError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from DOCTER.models import *
from PATIENT.models import *
from COMMON_APP.models import *
from Application_Main.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.db.models import Q,F ,Max

from django.contrib.auth import get_user_model
from DOCTER.forms import *
from jsignature.utils import draw_signature

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PATIENT.forms import ImagesUploadForm ,PrescriptionOldUploadForm
from PATIENT.models import ImagesUpload ,PrescriptionOldUpload

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import DeleteView 
from DOCTER.models import ExampleModel

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import  render_to_string

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


from .helpers import send_forget_password_mail

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dashboard.models import *
from dashboard.forms import *
from django.contrib.auth.decorators import login_required
from Application_Main import settings



#checking signature fields




# Create your views here.

def home(request):

	data = OurPortfolioImages.objects.all()

	print(f"request.user main home {request.user}")
	branch = ForAppointmentHomePage.objects.all()
	return render(request , 'home_new_adjust.html',{"user":None,"data":data,"branch":branch})

@csrf_exempt
def register(request) :

	print(f"request.user register {request.user}")
	if request.method == 'POST':
		# print(request.POST['name'])
		# print(request.POST['post'])
		try:
			user = User.objects.get(username=request.POST['username'])
			if user:
				messages.info(request,'Username already Exists')
				return render(request,'register_new_adjust.html',{'user':None})
			
		except User.DoesNotExist:
			user = User.objects.create_user(username=request.POST['username'],password=request.POST['pass1'])
			branch1 =request.POST['post'][0:3].upper()+"-"+"NEW"
			
			new = Patient(phone=request.POST['phone'],name=request.POST['name'],email=request.POST['email'],alternative_number=request.POST['alt_number'],branch=request.POST['post'],usern=user, case =branch1)
			#branch=request.POST['post']
			#print(branch)	
			new.save()
			messages.info(request,'Your Registration is complete only when you login and update your Profile.')	
            
			# c_patient = Invoice(patient = new , outstanding = 0 , paid = 0)
			# c_patient.save()
			

			return redirect('login1')
	else:
		return render(request , 'register_new_adjust.html',{'user':None})

@csrf_exempt
def recep_register_patient(request,user):

	status = False
	if request.user:
		status = request.user

	recep = Receptionist.objects.get(username = status)

	context = {
		'status' : status,
		'user':user,
		'branch': recep.branch,

	}

	if request.method == 'POST':

		try:
			first_name = request.POST['name'].lower().split(' ')[0]
			auto_gen_username = first_name+request.POST['phone'][-4:]
			print("auto-gen-username-old-user---------------",auto_gen_username)
			user = User.objects.get(username=auto_gen_username)
			if user:
				messages.success(request,'Username already Exists')
				return render(request,"recep_register_patient_adjust.html",context)
				# return render(request,"recep_register_patient.html",context)
			
		except User.DoesNotExist:
			first_name = request.POST['name'].lower().split(' ')[0]
			auto_gen_username = first_name+request.POST['phone'][-4:]
			auto_generate_password = request.POST['post'][0:3].upper()+"-"+auto_gen_username
			print("auto-gen-username---------------",auto_gen_username)
			print("auto-gen-pass---------------",auto_generate_password)
			user_new = User.objects.create_user(username=auto_gen_username,password=auto_generate_password)
			default_case_number =request.POST['post'][0:3].upper()+"-"+"NEW"

			# phone_unique = Patient.objects.filter(phone = request.POST['phone'])

			# if phone_unique:
			# 	messages.success(request,'Phone Number already Exists')
			# 	return render(request,"recep_register_patient.html",context)
			# else:
			# print("Title---",request.POST['name'].title())
			new = Patient(phone=request.POST['phone'],name=request.POST['name'].title(),email=request.POST['email'],
		 					alternative_number=request.POST['alt_number'],branch=request.POST['post'],usern=user_new,	
							 case =default_case_number)
			new.save()
			messages.success(request,"Patient Registered Successfully" + " Username : " + str(user_new) + " Password : " + str(auto_generate_password))
			return redirect('recep_register_patient',user=user)
	
	return render(request,"recep_register_patient_adjust.html",context)

# Login
# def login(request):
# 	if request.method == 'POST':
# 		try:
#  			# Check User in DB
# 			uname = request.POST['username']
# 			pwd = request.POST['pass1']
# 			user_authenticate = auth.authenticate(username=uname,password=pwd)
# 			if user_authenticate != None:
# 	 			user = User.objects.get(username=uname)
# 	 			try:
# 	 				data = Patient.objects.get(username = user)
# 	 				auth.login(request,user_authenticate)				
# 	 				return redirect('dashboard',user= "P")
# 	 			except:
# 	 				try:
# 	 					data = Docter.objects.get(username = user )
# 	 					auth.login(request,user_authenticate)				
# 	 					print('Docter has been Logged')
# 	 					return redirect('dashboard',user = "D")	 					
# 	 				except:
# 	 					try:
# 		 					data = Receptionist.objects.get(username = user )
# 		 					auth.login(request,user_authenticate)				
# 		 					print('Receptionist has been Logged')
# 		 					return redirect('receptionist_dashboard',user = "R")
# 		 				except:
# 		 					try:
# 		 						data = HR.objects.get(username = user )
# 		 						auth.login(request,user_authenticate)				
# 		 						print('HR has been Logged')
# 		 						return redirect('dashboard',user = "H")
# 		 					except:
# 		 						return redirect('/')
# 			else:
# 	 			print('Login Failed')
# 	 			return render(request,'login.html')
# 		except:
# 	 		return render(request,'login.html')
# 		messages.success(self.request, 'Form submission successful')
# 	return render(request , 'login.html')

#login Portion

@csrf_exempt	
def login(request):
	if request.method=="POST":
		try: 
			uname=request.POST['username']
			print("Username",uname)
			
			pwd=request.POST["pass1"]
			print("password",pwd)
			try:
				user = User.objects.get(username=uname)
				user_authenticate=auth.authenticate(username=uname , password=pwd)
				print('user_auth',user_authenticate)
			except User.DoesNotExist:
				
				print('User does not exist.')
			if user_authenticate != None:
				user = User.objects.get(username = uname)
				print('user is ', user)
				try:
					# data=Patient.objects.get(username = user)
					data=Patient.objects.get(usern = user)
					print('data.flag',data.display_flag)
					if data.display_flag:
						auth.login(request , user_authenticate)
						print("Dispaly has been logged ")
						return redirect("display_home", user="DIS")
					else:
						auth.login(request , user_authenticate)
						print("Patient has been logged ")
						return redirect("dashboard" , user="P")
				except:
					try:
						data=Docter.objects.get(username = user)
						auth.login(request , user_authenticate)
						print("Docter has been logged ")
						return redirect("dashboard",user="D")
					except:
						try:
							data = Receptionist.objects.get(username = user )
							auth.login(request,user_authenticate)
							print('Receptionist has been Logged')
							return redirect('receptionist_dashboard',user = "R")
						

						except:
							try:
								data = HR.objects.get(username = user)
								auth.login(request , user_authenticate)
								print("HR has been logged ")
								return redirect("hr_dashboard")
								# return redirect("dashboard" , user="H") hr_dashboard
							except:
								return redirect('/')
			else:
				print("True","Invalid")
				messages.success(request,'Username or Password is incorrect')
				return render(request,'login_new_adjust.html',{'user':None})

		except:
			messages.success(request,'Username or Password is incorrect')
			# messages.success(request, 'Form submission successful')
			return render(request,'login_new_adjust.html',{'user':None})
			
	return render(request , 'login_new_adjust.html',{'user':None})

import uuid
@csrf_exempt
def forgetPassword(request):
	try:
		if request.method == 'POST':
			
			username = request.POST['username']			
			email_add = request.POST['email_add']
			
			data1 = Patient.objects.filter(Q(email=email_add) & Q(usern=username)).first()
			print("DATA 1",data1)
			data2 = Docter.objects.filter(Q(email=email_add) & Q(username__username=username)).first()
			print("DATA 2",data2)			
			data3 = Receptionist.objects.filter(Q(email=email_add) & Q(username__username=username)).first()
			print("DATA 3",data3)
			data4 = HR.objects.filter(Q(email=email_add) & Q(username__username=username)).first()
			print("DATA 4",data4)

			if data1 or data2 or data3 or data4:	
				
				if data1:
					user_obj = Patient.objects.filter(Q(email=email_add) & Q(usern=username)).first()
					print("pate_user_obj",user_obj.email)
					token = str(uuid.uuid4())
					patient_profile = Patient.objects.get(usern=username)
					patient_profile.forget_password_token = token
					patient_profile.save()
					send_forget_password_mail(user_obj.email,token)
					messages.success(request,"An Email has been sent on you Registered Email ID")
					return redirect('/forget_password/')
				elif data2:
					user_obj =Docter.objects.filter(Q(email=email_add) & Q(username__username=username)).first()
					print("docter_user_obj",user_obj.email)
					token = str(uuid.uuid4())
					docter_profile = Docter.objects.get(username__username=username)
					docter_profile.forget_password_token = token
					docter_profile.save()
					send_forget_password_mail(user_obj.email,token)
					messages.success(request,"An Email has been sent on you Registered Email ID")
					return redirect('/forget_password/')
				elif data3:
					user_obj = Receptionist.objects.filter(Q(email=email_add) & Q(username__username=username)).first()
					print("recep_user_obj",user_obj.email)
					token = str(uuid.uuid4())
					recep_profile = Receptionist.objects.get(username__username=username)
					recep_profile.forget_password_token = token
					recep_profile.save()
					send_forget_password_mail(user_obj.email,token)
					messages.success(request,"An Email has been sent on you Registered Email ID")
					return redirect('/forget_password/')
				elif data4:
					user_obj = HR.objects.filter(Q(email=email_add) & Q(username__username=username)).first()
					print("HR_user_obj",user_obj.email)
					token = str(uuid.uuid4())
					hr_recep = HR.objects.get(username__username=username)
					hr_recep.forget_password_token = token
					hr_recep.save()
					send_forget_password_mail(user_obj.email,token)
					messages.success(request,"An Email has been sent on you Registered Email ID")
					return redirect('/forget_password/')
			else:
				messages.success(request," Username/Email is not Registered with Us.")
				return redirect('/forget_password/')


	
	except Exception as e:
		print(e)
	return render(request,'forgot-password-adjust.html',{'user':None})

@csrf_exempt
def changePassword(request,token):

	context = {}

	try:
		if Patient.objects.filter(forget_password_token=token).first():
			profile_obj = Patient.objects.get(forget_password_token=token)
			print("Patient profile",profile_obj,profile_obj.usern)
			user_obj = User.objects.get(username=profile_obj.usern)
		
		elif Docter.objects.filter(forget_password_token=token).first():
			profile_obj = Docter.objects.get(forget_password_token=token)
			print("Docter profle_obj",profile_obj.username_id)
			user_obj = User.objects.get(id=profile_obj.username_id)
		
		elif Receptionist.objects.filter(forget_password_token=token).first():
			profile_obj = Receptionist.objects.get(forget_password_token=token)
			print("Recep profle_obj",profile_obj.username_id)
			user_obj = User.objects.get(id=profile_obj.username_id)

		elif HR.objects.filter(forget_password_token=token).first():			
			profile_obj = HR.objects.get(forget_password_token=token)
			print("HR-profle_obj",profile_obj.username_id)
			user_obj = User.objects.get(id=profile_obj.username_id)
		

		# user_obj = User.objects.get(username=profile_obj.usern)
		context = { 'user_id': user_obj.id}

		if request.method == 'POST':
			new_password = request.POST['pass1']
			confirm_password = request.POST['pass2']
			user_id = request.POST['user_id']

			if user_id is None:
				messages.success(request,"No User found")
				return redirect(f'/change_password/{token}/')
			
			if new_password != confirm_password:
				messages.success(request,"Both Passwords Should be Same")
				return redirect(f'/change_password/{token}/')
			
			user_set_pass = User.objects.get(id=user_obj.id)
			print("user_old",user_set_pass.password)
			user_set_pass.set_password(new_password)
			print("new_pass----",user_set_pass.password)
			user_set_pass.save()
			messages.success(request,"Password has been Updated. Please Login to Continue.")
			return redirect('login1')
			
		

	except Exception as e:
		print(e)

	return render(request,'change-password.html',context)



	
def display_home(request,user):

	status = False
	if request.user:
		status = request.user
		print('status',status)

	data = Patient.objects.get(usern = status)
	print("Branch",data.branch)
	date1 = datetime.now()
	
	token = Appointment.objects.all().filter(date=date.today(),patientid__branch="Dombivali")
	print('token',token)
	return render(request,'dashboard/templates/new_page.html',{'status':status,'user':user,'date':date1,'token':token})
	# return render(request,'display_home.html',{'status':status,'user':user,'date':date1,'token':token})
	

# Logout
@csrf_exempt
def logout(request):
	auth.logout(request)
	print('Logout')
	return redirect('/login1')

@csrf_exempt
def patient_appointment(request,user):
	
	status = False
	if request.user:
		status=request.user			
		app = Appointment.objects.filter(patientid__usern = status,date__lt=date.today()).order_by('-date')[:2:-1]	
			
		# app1 = Appointment.objects.filter(patientid__usern = status,date__gte=date.today())[0:2]		

	pat = Patient.objects.get(usern = str(status))
	
	
	duration_new =prescription.objects.filter(patientid=pat.id).last()
	print('duration_new',duration_new)
	
	if duration_new:			
		obj_new = duration_new.durations.split(' ')
		if obj_new[1] == "Days":
			rem_days = int(obj_new[0]) % 7
			num_days = int(obj_new[0]) - rem_days			
			next_visit = duration_new.date + relativedelta(days=num_days)
			
		else:			
			next_visit = duration_new.date + relativedelta(months=int(obj_new[0]))

	else:
		next_visit = " "		
	return render(request,'patient_appointment_new_adjust.html',{'status':status,'user':user,'app':app,'pat':pat,'next_visit':next_visit,"pat_branch": pat.branch})

# Profile
@csrf_exempt
def profile(request, user):
	
	# userid = User.objects.get(username=request.user)
	status = False
	if request.user:
		status = request.user
		userid = User.objects.get(username=status)
		
	if request.method == "POST":
		
		if user == "P":
			update = Patient.objects.get(usern=userid)
			update.name = request.POST['name']
			update.phone = request.POST['phone']
			update.alternative_number = request.POST['alt_number']
			update.email = request.POST['email']
			update.gender = request.POST['gender']
			print('gender',request.POST['gender'])
			update.age = request.POST['age']
			update.blood = request.POST['blood']
			print('blood',request.POST['blood'])
			update.address = request.POST['address']
			update.case = request.POST['case']				
			if 'patient_images' in request.FILES:
				update.patient_images = request.FILES['patient_images']							
			else:
				pass
			
			# try:
			# 	myfile = request.FILES['report']
			# 	fs = FileSystemStorage(location='media/report/')
			# 	filename = fs.save(myfile.name,myfile)
			# print(name,file)
			# 	url = fs.url(filename)				
			# 	update.medical = url
			# except:
			# 	pass
			update.save()
			messages.info(request,"Profile Updated")
			return redirect('profile',user = user)
			# return redirect('dashboard',user = user)
		else:
			update = Docter.objects.get(username=userid)
			update.name = request.POST['name']
			update.phone = request.POST['phone']
			update.email = request.POST['email']
			update.gender = request.POST['gender']
			update.age = request.POST['age']
			update.blood = request.POST['blood']
			update.address = request.POST['address']
			update.save()
			return redirect('dashboard',user = user)


	if user == "P":
		# userdata = Patient.objects.get(username=userid)
		userdata = Patient.objects.get(usern=userid)
		return render(request  , 'patient_profile_new_adjust.html',{'userdata' : userdata , 'user':user, "status": status})

	else:
		userdata  = Docter.objects.get(username=userid)
		return render(request  , 'docter_profile.html',{'userdata' : userdata , 'user':user, "status": status})


	# return redirect('/')

@csrf_exempt
def editProfile(request,user):

	print("user",request.user)
	if request.user:
		status = request.user


	userid = User.objects.get(username=status)
	data = Patient.objects.get(usern=userid)

	if request.method == "POST":
		update = Patient.objects.get(usern=userid)
		update.name = request.POST['name']
		update.usern = request.POST['username']
		update.phone = request.POST['phone']
		update.alternative_number = request.POST['alt_number']
		update.email = request.POST['email']
		update.gender = request.POST['gender']
		update.age = request.POST['age']
		update.address = request.POST['address']
		update.case = request.POST['case']
		update.qualification = request.POST['qualification']
		update.occupation =  request.POST['occupation']
		update.dietry_preference = request.POST['dietry']
		update.marital_status = request.POST['marital']
		if 'patient_images' in request.FILES:
			update.patient_images = request.FILES['patient_images']
			update.save()
		else:
			pass
		update.save()
		messages.info(request,f'You have Successfully Updated your Profile !')
		return HttpResponseRedirect(reverse('editProfile', kwargs={'user':user})) 


	context = {
		'status':status,
		'user':user,
		'data':data,
	}
	return render(request,'editProfile_new_adjust.html',context)

@csrf_exempt
def add_case_paper(request,id):
	
	data = Patient.objects.get(id=id)

	if data.branch == "Dombivali":
		key_branch = "DOM-"
	elif data.branch == "Mulund":
		key_branch = "MUL-"

	if request.method == 'POST':
		old_case = f'{key_branch}{request.POST['case']}'
		# print("Old case", old_case, type(old_case))
		update = Patient.objects.get(id=id)
		update.case= old_case
		update.save()
		messages.success(request,"Successfully Added Case Paper Number")
		return HttpResponseRedirect(reverse('add_case_paper',kwargs={'id':id}))	

	obj_case = data.case.split('-')	
	context = {
		'data':obj_case[1]
	}
	return render(request, 'add_case_paper_new_adjust.html',context)


@csrf_exempt
# @login_required
def dashboard(request , user):

	status = False
	if request.user:
		status = request.user
	print('-------Dashboard--------------------')
	print('user',user,type(user),status)	
	print('---------------------------')
	if user == "AnonymousUser":
		return redirect('home')
	elif user == "AP":
		return redirect('docter_appointment')
	try:
		data1 = HR.objects.get(username = status)
		data_branch= data1.branch
		general = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="General") & Q(notification_flag = False) & Q(doctor_notification = True))	
		count_general = str(general.count())
		repeat_medicine = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(notification_flag = False) & Q(doctor_notification = True))
		count_repeat = str(repeat_medicine.count())
		courier = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(notification_flag = False) & Q(doctor_notification = True))
		count_courier = str(courier.count())
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=data_branch))
		unsent_mail_count = str(mail_count.count())
		data = OurPortfolioImages.objects.all()
		branch = ForAppointmentHomePage.objects.all()

		return render(request , 'home_new_adjust.html', {'user':user, "status": status,'general':count_general,'repeat':count_repeat,'courier':count_courier,'unsend_mail_count': unsent_mail_count,"data":data,"branch":branch})

	except:
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
		data = OurPortfolioImages.objects.all()
		branch = ForAppointmentHomePage.objects.all()


	
	
		return render(request , 'home_new_adjust.html', {'user':user, "status": status,'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
								'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
								'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,'unsend_mail_count': unsent_mail_count,"data":data,"branch":branch})	
		


@csrf_exempt
def receptionist_dashboard(request , user):
	status = False
	if request.user:
		status = request.user
		recep = Receptionist.objects.get(username =status) #added
		recep_name = recep.name     #added
		recep_branch = recep.branch  #added
	row = Appointment.objects.filter(patientid__branch =recep_branch,date=date.today(),stat="General")
	print('row',len(row),row)
	for r in row:
		print(r.status)
	status_done = len(Appointment.objects.filter(patientid__branch =recep_branch,date=date.today() ,medicine_flag = True,stat="General"))
	print('status_done',status_done)
	status_pending = len(row) - status_done
	last_patients = Patient.objects.all().order_by('-pk')[0:5]

	task_details = AssignTask.objects.filter(Q(assign_To = status) & Q(completed = False))

	
	# receptionist_dashboard_new.html - earlier
	return render(request , 'receptionist_dashboard_new_adjust.html' , {'user':user, "status": status , "Total" : len(row) ,'date':date.today(),
															"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients,
															"recep_name" : recep_name ,"recep_branch":recep_branch,'task_count':task_details.count()})

@csrf_exempt
def dash_patients_details(request,user):
	status = False
	if request.user:
		status = request.user		
		# recep = Receptionist.objects.get(username = status)
	try:
		recep = Receptionist.objects.get(username = status)
		branch1=Patient.objects.filter(branch = recep.branch)
	except:
		doc = Docter.objects.get(username = status)
		branch1 = Patient.objects.all()

	# User = get_user_model()
	# users = User.objects.all()
	# #all_users = User.objects.values()
	# branch1=Patient.objects.all().filter(branch="branch")
	# if users=="R" and branch1=="Dombivli":
	# 	print(users)
	
	#name1=request.POST['name']
	#branch=request.POST['branch']
	# name=User.objects.get(name)
	# branch=User.objects.get(branch)
	# if name=="Ragini" and branch=="Dombivli":
	# 	print("Hi Ragini")
	# else:
	# 	print("Hellow Dr.")


	row = Appointment.objects.all()
	status_done = len(Appointment.objects.filter(status = 1))
	status_pending = len(row) - status_done
	last_patients = Patient.objects.all().order_by('-pk')[0:15]
	query=request.GET.get('query')
	
	# branch1=Patient.objects.all()
	# branch1=Patient.objects.filter(branch = recep.branch)

	#query1=Patient.objects.get(case=query) 
	#print(query1.id)
	print("Branch Recep",recep.branch)
	if query:		
		branch1 = Patient.objects.filter(Q(case__icontains=query.upper())|Q(phone__icontains=query)|Q(email__icontains=query)|Q(name__icontains=query) ,branch=recep.branch)
		
		# appointment_list=Appointment.objects.filter(Q(patientid=query))
		#print(appointment_list)
		# return render(request , 'patients_details.html' , {'user':user, "status": status , "Total" : len(row) ,
		# 													"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients, 'branch1':branch1 })

		# return render(request , 'patients_details.html' , {'user':user, "status": status , "Total" : len(row) ,
															# "Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients, 'appointment_list':appointment_list , 'branch1':branch1})

	p = Paginator(branch1 ,15)
	page = request.GET.get('page')
	# print("Page-",page)
	datas = p.get_page(page)
	
	return render(request , 'patients_details_new_adjust.html' , {'user':user, "status": status , "Total" : len(row) ,
															"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients , 'branch1':branch1,'datas':datas})


#	return render(request,'patients_details.html')

@csrf_exempt
def displays_fil_rec(request):
	return render(request,"displays_fil_rec")
	# status = False
	# if request.user:
	# 	status = request.user
	# row = Appointment.objects.all()
	# status_done = len(Appointment.objects.filter(status = 1))
	# status_pending = len(row) - status_done
	# last_patients = Patient.objects.all().order_by('-pk')[0:15]
	# query=request.GET.get('query')
	# branch1=Patient.objects.all().filter(branch="Dombivli")
	# query1=Patient.objects.get(case = query) 
	# print(query1)

	# if query:
	# 	appointment_list=Appointment.objects.filter(Q(patientid=query1.id))
	# 	#print(appointment_list)
	# 	return render(request , 'filter_records.html' , {'user':user, "status": status , "Total" : len(row) ,
	# 														"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients, 'appointment_list':appointment_list , 'branch1':branch1,'query2':query1})

	# return render(request , 'filter_records.html' , {'user':user, "status": status , "Total" : len(row) ,
	# 														"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients , 'branch1':branch1})






@csrf_exempt
def dash_appointment_details(request,user):
	status = False
	if request.user:
		status = request.user
		# recep = Receptionist.objects.get(username = status)
	try:
		recep = Receptionist.objects.get(username = status)
		row = Appointment.objects.filter(patientid__branch = recep.branch,date=date.today())
	except:
		doc = Docter.objects.get(username = status)
		row = Appointment.objects.filter(date=date.today())

	# print('ROW--',row)	
	# for r in row:
	# 	print(r.patientid,r.stat)	
	# row = Appointment.objects.filter(patientid__branch = recep.branch,date=date.today())
	# print("Row",row)
	# for r in row:
	# 	print("@@@@",r.status)
	status_done = len(Appointment.objects.filter(status = 1))
	status_pending = len(row) - status_done
	last_patients = Patient.objects.all().order_by('-pk')[0:15]	
	
	query=request.GET.get('query')
	
	# query=request.GET.get('query')
	# print(query)
	# if query is not None:
	# 	appointment1_list=Appointment.objects.filter(patientid=query)
	# 	print(appointment1_list.query)
	# 	return render(request , 'appointment_details.html' , {'user':user, "status": status , "Total" : len(row) ,
	# 														"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients,'appointment1_list':appointment1_list})

	if query:
		# row = Appointment.objects.filter(Q(patientid__case=query.upper()),date=date.today())
		row = Appointment.objects.filter(Q(patientid__case__icontains=query.upper())|Q(patientid__phone__icontains=query)|Q(patientid__name__icontains=query)|Q(patientid__email__icontains=query) ,date=date.today())

		# return render(request , 'appointment_details.html' , {'user':user, "status": status , "Total" : len(row) ,
															# "Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients})
	p = Paginator(row ,15)
	page = request.GET.get('page')
	datas = p.get_page(page)
	d1 = date.today()
		
	return render(request , 'appointment_details_new_adjust.html' , {'user':user, "status": status , "Total" : len(row) ,
															"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients,'datas':datas,'date':d1})

	#return render(request,'dash_appointment_details.html')
@csrf_exempt
def create_appointment(request , user):
	status = False
	if request.user:
		status = request.user
		recep = Receptionist.objects.get(username = status)

	if request.method == "POST":	
		
		p_id = request.POST.get('patient')
		stat = request.POST.get('status')		
		appoint_stat = request.POST.get('status')
		if p_id is None:
			messages.info(request,"Please Select Patient's CasePaper No. to create an Appointment Type.")
			return redirect('create_appointment',user = "R")
		elif stat is None:
			messages.info(request,"Please Select an Appointment Type.")
			return redirect('create_appointment',user = "R")
		else:
			d_id = int(request.POST['docter'])			
			docter = Docter.objects.get(pk=d_id)	
			patient = Patient.objects.get(pk=p_id)
			pat_branch = patient.branch
			pat_flag_new = patient.flag
			str_pat_flag = str(pat_flag_new)				
			notification = False
			doctor_notification = False
			status = False
			email_flag = False
			if Appointment.objects.filter(Q(patientid = patient) & Q(date=date.today())):
				messages.success(request, 'You have already created appointment for today.')
				return redirect('create_appointment',user = "R")
			else:	
				new_appointment = Appointment(docterid = docter , patientid = patient ,time = request.POST['time'] ,  date = request.POST['date'] , stat  = stat,patient_new_old=str_pat_flag )
				new_appointment.save(pat_branch,stat,notification,doctor_notification,status,email_flag)
				# return redirect('receptionist_dashboard', user = "R")
				messages.success(request,f'Created {appoint_stat} Appointment  for Patient - {patient.name}/{patient.case}/{patient.phone}(M)') 
				return redirect('create_appointment', user = "R")

	patient_names = Patient.objects.filter(branch = recep.branch)
	docter_names = Docter.objects.all()

	today = date.today().strftime("%Y-%m-%d")
	print("today----",today)

	return render(request , 'create_appointment_new_adjust.html' , {'user':user, "status": status , "patient_names" : patient_names , 
		"docter_names" : docter_names, 'today': today })




# Delete Patient
@csrf_exempt
def delete_patient(request , id ):
	data = Patient.objects.get(id=id)
	data.delete()
	return redirect('receptionist_dashboard' , user="R")
@csrf_exempt
def delete_medicine(request,id,pk):


	print("Testing123--------")
	print('pk',pk)
	app = Appointment.objects.get(date=date.today(),patientid_id=id)
	print("branch",app.patientid.branch)
	if app.patientid.branch == 'Dombivali':
		tok = app.token
	else:
		tok = app.token1	
	print('tok',tok)
	patient = Patient.objects.get(id=id)
	# pres = prescription.objects.filter(patientid=id).last()
	# pres = prescription.objects.filter(patientid=id)
	pres = prescription.objects.get(id=pk)
	print('pres',pres)
	pres.delete()
	return HttpResponseRedirect(reverse('apointmentDetails',  kwargs={'id': patient.id,'token':tok}))
	


# Create Patient => Receptionist
@csrf_exempt
def create_patient(request):
	status = False
	mylist=[]
	displaysuser=User.objects.values_list('username')
	for data in displaysuser:
		mylist.append(data[0])

	if request.user:
		status = request.user
		# print(status)
	if request.method =="POST":
		# try: 
		# 	print("hwhfwdhfwhdffwhdfhwdf")
		# 	print(request.POST['selectuser'])
		# 	#user = User.objects.get(username=request.POST['username'])
		# 	#print(user,'This is ')
		# 	return redirect('receptionist_dashboard', user = "R")
		# except User.DoesNotExist:

		# 	user = User.objects.create_user(username=request.POST['username'],password='default')	
		# 	try:
		# 		myfile = request.FILES['report']
		# 		fs = FileSystemStorage(location='media/report/')
		# 		filename = fs.save(myfile.name,myfile)
		# 	# print(name,file)
		# 		url = fs.url(filename)

		# 	except:
		# 		url = ""		
			name1=request.POST['name']
			suser=request.POST['selectuser']
			email1=request.POST['email']
			phone1=request.POST['phone']
			age1=request.POST['age']
			gender1=request.POST['gender']
			blood1=request.POST['blood']
			address=request.POST['address']
			branch1=request.POST['branch']
			caseno=request.POST['case']
			case1=branch1[0:3].upper()+"-"+caseno
			new = Patient.objects.create(phone=phone1,branch=branch1 ,name=name1,usern=suser,email=email1, age=age1 ,address =address , gender =  gender1 , blood = blood1 , case =case1)	
			
			# new = Patient.objects.update_or_create(phone=phone1,branch=branch1 ,name=name1,usern=suser,email=email1, age=age1 ,address =address , gender =  gender1 , blood = blood1 , case =case1)
			new.save()	

			# c_patient = Invoice(patient = new , outstanding = request.POST['outstanding'] , paid = request.POST['paid'])
			# c_patient.save()
			return redirect('create_patient')

	return render(request , 'create_patient.html' , {'user' : "R" , 'status' :status , 'users':mylist})



# Update Patient=> Receptionist
@csrf_exempt
def update_patient(request , id ):
	status = False
	if request.user:
		status = request.user

	print('id',id)
		
	if request.method == "POST":
			update = Patient.objects.get(id=id)
			update.name = request.POST['name']
			update.usern = request.POST['username']
			update.phone = request.POST['phone']
			update.alternative_number = request.POST['alt_number']
			update.email = request.POST['email']
			update.gender = request.POST['gender']
			
			update.age = request.POST['age']
			# update.blood = request.POST['blood']
			update.address = request.POST['address']
			update.case = request.POST['case']
			# update.height = request.POST['height']
			# update.weight = request.POST['weight']
			update.qualification = request.POST['qualification']
			update.occupation =  request.POST['occupation']
			update.dietry_preference = request.POST['dietry']
			update.marital_status = request.POST['marital']
			update.referred_by =  request.POST['referred']
			if 'patient_images' in request.FILES:
				update.patient_images = request.FILES['patient_images']	
				update.save()
			else:
				pass
			update.save()
			# if 'prescrip_images' in request.FILES:
			# 	update.prescrip_images = request.FILES['prescrip_images']
			# 	update.save()
			# else:
			# 	pass	
			# try:
			# 	myfile = request.FILES['report']
			# 	fs = FileSystemStorage(location='media/report/')
			# 	filename = fs.save(myfile.name,myfile)
			# # print(name,file)
			# 	url = fs.url(filename)
			# 	print(url)
			# 	update.medical = url
			# except:
			# 	pass
			
			# extra_update = Invoice.objects.get(patient = update)

			# extra_update.outstanding = request.POST['outstanding']
			# extra_update.paid = request.POST['paid']
			# extra_update.save()
			messages.info(request,"Profile Updated for  " + request.POST['name'])
			# return redirect('patients_details' , user = "R")
			return HttpResponseRedirect(reverse('update_patient',  kwargs={'id': id}))
	data = Patient.objects.get(id=id)
	# extra = Invoice.objects.get(patient = data)
	# return render(request , 'update_patient.html' , {'data':data , 'extra':extra , 'user' :"R" , 'status':status})
	return render(request , 'update_patient_new_adjust.html' , {'data':data , 'user' :"R" , 'status':status})

@csrf_exempt
def myappointment(request):
	status = False
	if request.user:
		status = request.user
		
	user_id = User.objects.get(username=request.user)	
	# patient= Patient.objects.get(username=user_id)
	patient= Patient.objects.get(usern=user_id)	
	data = Appointment.objects.filter(patientid=patient)
	
	return render(request , 'my_appointment.html' , {'data':data, 'user' :"P" , 'status':status})


# Docter Appointsments
@csrf_exempt
def appoint_doctor(request):

	status =False
	if request.user:
		status = request.user			
	
	if request.method == 'POST':		
		
		
		p_id = request.POST.get('patient')		
		stat = request.POST.get('status')

		if p_id is None:
			messages.info(request,"Please Select Patient's CasePaper No. to create an Appointment Type.")
			return redirect('appoint_doctor')
		elif stat is None:
			messages.info(request,"Please Select an Appointment Type.")
			return redirect('appoint_doctor')
		else:		
			d_id =	request.POST['docter']	
			doctor = Docter.objects.get(id=d_id)	
			date1 = request.POST['date']
			time = request.POST['time']			
			notification = False	
			doctor_notification = False	
			status = False	
			email_flag = False
			patient = Patient.objects.get(id=p_id)
			pat_branch = patient.branch
			pat_flag_new = patient.flag
			# print("pat_flag_new",pat_flag_new,type(pat_flag_new))
			str_pat_flag = str(pat_flag_new)
			# print("string",str_pat_flag)
			if Appointment.objects.filter(Q(patientid=patient) & Q(date=date.today())):
				messages.success(request,"You have already created appointment for today.")
				return redirect('appoint_doctor')
			else:
				new_appointment = Appointment(docterid=doctor,patientid=patient,time=time,date=date1,stat=stat,patient_new_old=str_pat_flag)
				new_appointment.save(pat_branch,stat,notification,doctor_notification,status,email_flag)
				date_object = datetime.strptime(date1, "%Y-%m-%d")
				formatted_date = date_object.strftime("%d %B %Y")
				# print("formatted date",formatted_date)	
				messages.success(request,f'{stat} Appointment Created for {patient.name} {patient.case} for {formatted_date}')
				return redirect('appoint_doctor')

	patient_names = Patient.objects.all()
	doctor_names = Docter.objects.all()
	
	
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
	unsent_mail_count = str(mail_count.count())
	
	today = date.today().strftime("%Y-%m-%d")
	
	return render(request,'appoint_doctor_new_adjust.html',{'user':"D",'status':status,'patient_names':patient_names,'doctor_names':doctor_names,
					      'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,"unsend_mail_count":unsent_mail_count,
						  'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,"today":today,
						  'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul})

from PATIENT.forms import NewCasePaperUploadForm,NewCasePaperUploadFormOne
@csrf_exempt
def doc_upload_newcase(request):

	status = False
	if request.user:
		status = request.user

	if request.method == 'POST':
		form = NewCasePaperUploadForm(request.POST,request.FILES)
		files = request.FILES.getlist('images')

		if form.is_valid():
			print("patient",form.cleaned_data['patient'])
			obj = Patient.objects.get(case= form.cleaned_data['patient'])
			form.save(commit = False)
			for i in files:
				NewCasePaperUpload.objects.create(patient=obj,images=i)
			messages.info(request,"New Case Paper Images Uploaded for "+ obj.name +" "+obj.case)
			return redirect('doc_upload_newcase')	
		
	form = NewCasePaperUploadForm()

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
	unsent_mail_count = str(mail_count.count())



	return render(request,'doc_upload_newcase_adjust.html',{'user':"D",'status':status,'form':form,
						  'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,"unsend_mail_count":unsent_mail_count,
						  'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
						  'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul})

# from django.http import HttpResponse
from django.http import JsonResponse

def start_consultancy(request,branch):
	
	print('start branch',branch)
	
	obj = TokenUpdate.objects.last()
	obj.consultancy = True
	obj.save()
	print('value1',obj.consultancy)	
	if branch == 'Dombivali':

		# data = {'d': "stop_consultancy_now"}	
		# return JsonResponse(data)	
		return redirect('docter_appointment_dombivali')		
	elif branch == 'Mulund':				
		return redirect('docter_appointment_mulund')

def stop_consultancy(request,branch):

	print(' stop branch',branch)
	obj = TokenUpdate.objects.last()
	obj.consultancy = False
	obj.save()
	print('value2',obj.consultancy)
	if branch == 'Dombivali':	
		# return HttpResponse()	
		return redirect('docter_appointment_dombivali')
	elif branch == 'Mulund':
		return redirect('docter_appointment_mulund')
	

	

@csrf_exempt
def docter_appointment(request):
	status = False
	if request.user:
		status = request.user
	
	user_id = User.objects.get(username=request.user)
	docter= Docter.objects.get(username=user_id)
	data = Appointment.objects.filter(date=date.today())	
	# p = Paginator(data ,2)
	# page = request.GET.get('page')
	# datas = p.get_page(page)
	query = request.GET.get('query')	
	if query:
		data = Appointment.objects.filter(date=date.today(),patientid__case= query)

	else:
		data = Appointment.objects.filter(date=date.today())	
	p = Paginator(data ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)

	d1 = date.today()
	consult_flag = False
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

	time = datetime.now().strftime("%H:%M")
	# print('time---------------',time.strftime("%H:%M"))
	new_patient = Appointment.objects.filter(date=date.today(),patientid__flag=True).count()
	appointment_due = Appointment.objects.filter(date=date.today(),doctor_notification=False).count()
	medicine_not_issued = Appointment.objects.filter(Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False)).count()
	medicine_issued = Appointment.objects.filter( Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True)).count()
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
	unsent_mail_count = mail_count.count()
	print("unsent_mail---",unsent_mail_count,type(unsent_mail_count))
	
	return render(request , 'my_appointment_newone.html',  {'user' :"D" , 'status':status,'datas':datas,'date':d1,'consult_flag':consult_flag,'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
						  'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
						   'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul
						   ,'time':time,"header": "General Appointments Today","new_patient":new_patient,"appointment_due":appointment_due,
		"medicine_not_issued":medicine_not_issued,'medicine_issued':medicine_issued,"unsend_mail_count":unsent_mail_count })
@csrf_exempt
def doc_courier_med_dom(request):

	status = False
	if request.user:
		status = request.user

	user_id = User.objects.get(username=request.user)

	data1 = Appointment.objects.filter(patientid__branch = 'Dombivali',date =date.today()).order_by('time')
	query = request.GET.get('query')
	if query:
		data1 = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & ( Q(patientid__case__icontains = query) | Q(patientid__phone__icontains = query) | Q(patientid__name__icontains = query)))
		# data1 = Appointment.objects.filter(patientid__branch = 'Dombivali',date =date.today(),patientid__case = query).order_by('time')
	
	p = Paginator(data1 ,7)
	page = request.GET.get('page')
	datas = p.get_page(page)
	d1 = date.today()
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

	new_patient = Appointment.objects.filter(patientid__branch="Dombivali",date=date.today(),patientid__flag=True,stat="Courier Medicine",doctor_notification=False).count()
	appointment_due = Appointment.objects.filter(patientid__branch="Dombivali",date=date.today(),doctor_notification=False,stat="Courier Medicine",patientid__flag=False).count()
	medicine_not_issued = Appointment.objects.filter(Q(patientid__branch="Dombivali") &Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False) & Q(stat="Courier Medicine")).count()
	medicine_issued = Appointment.objects.filter(Q(patientid__branch="Dombivali") & Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True) & Q(stat="Courier Medicine")).count()
	
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
	unsent_mail_count = mail_count.count()
	
	
	return render(request , 'doc_courier_med_dom_newone_adjust.html', {'user' :"D" , 'status':status, "datas":datas ,'date':d1,
						      'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
							  'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
							  'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,
							  "header":"Courier Medicine Dombivali","new_patient":new_patient,"appointment_due":appointment_due,
		"medicine_not_issued":medicine_not_issued,'medicine_issued':medicine_issued,"unsend_mail_count":unsent_mail_count })
@csrf_exempt
def doc_repeat_med_dom(request):

	status = False
	if request.user:
		status = request.user

	user_id = User.objects.get(username=request.user)

	data1 = Appointment.objects.filter(patientid__branch = 'Dombivali',date =date.today()).order_by('time')
	query = request.GET.get('query')
	if query:
		data1 = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & ( Q(patientid__case__icontains = query) | Q(patientid__phone__icontains = query) | Q(patientid__name__icontains = query)))
	
	p = Paginator(data1 ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)
	d1 = date.today()
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

	new_patient = Appointment.objects.filter(patientid__branch="Dombivali",date=date.today(),patientid__flag=True,stat="Repeat Medicine").count()
	appointment_due = Appointment.objects.filter(patientid__branch="Dombivali",date=date.today(),doctor_notification=False,stat="Repeat Medicine",patientid__flag=False).count()
	medicine_not_issued = Appointment.objects.filter(Q(patientid__branch="Dombivali") &Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False) & Q(stat="Repeat Medicine")).count()
	medicine_issued = Appointment.objects.filter(Q(patientid__branch="Dombivali") & Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True) & Q(stat="Repeat Medicine")).count()
	
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
	unsent_mail_count = mail_count.count()

	return render(request , 'doc_repeat_med_dom_newone_adjust.html', {'user' :"D" , 'status':status, "datas":datas ,'date':d1,
						     'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
							 'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
							 'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,
							 "header": "Repeat Medicine Dombivali","new_patient":new_patient,"appointment_due":appointment_due,
							"medicine_not_issued":medicine_not_issued,'medicine_issued':medicine_issued,
							"unsend_mail_count":unsent_mail_count})
@csrf_exempt
def docter_appointment_dombivali(request):
	status = False
	if request.user:
		status = request.user
	
	user_id = User.objects.get(username=request.user)
	docter= Docter.objects.get(username=user_id)	
	data1 = Appointment.objects.filter(patientid__branch = 'Dombivali',date =date.today())
	
	query = request.GET.get('query')
	print("Query",query)
	if query:
		data1 = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & ( Q(patientid__case__icontains = query) | Q(patientid__phone__icontains = query) | Q(patientid__name__icontains = query)))
		# data1 = Appointment.objects.filter(patientid__branch = 'Dombivali',date =date.today(),patientid__case = query)
	
	p = Paginator(data1 ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)
	d1 = date.today()

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
	
	new_patient = Appointment.objects.filter(patientid__branch="Dombivali",date=date.today(),patientid__flag=True,stat="General",doctor_notification=False).count()
	appointment_due = Appointment.objects.filter(patientid__branch="Dombivali",date=date.today(),doctor_notification=False,stat="General",patientid__flag=False).count()
	medicine_not_issued = Appointment.objects.filter(Q(patientid__branch="Dombivali") &Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False) & Q(stat="General")).count()
	medicine_issued = Appointment.objects.filter(Q(patientid__branch="Dombivali") & Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True) & Q(stat="General")).count()
	
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
	unsent_mail_count = mail_count.count()

	context ={
		'user' :"D" , 'status':status, 
		"datas":datas ,'date':d1,		
		'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,
		"header":"General Appointments Dombivili",
		"new_patient":new_patient,"appointment_due":appointment_due,
		"medicine_not_issued":medicine_not_issued,'medicine_issued':medicine_issued,
		"unsend_mail_count":unsent_mail_count}	
	
	return render(request , 'my_appointment_dombivali_newone_adjust.html', context)
@csrf_exempt
def doc_repeat_med_mul(request):

	status = False
	if request.user:
		status = request.user
	
	user_id = User.objects.get(username=request.user)
	docter= Docter.objects.get(username=user_id)	
	data2 = Appointment.objects.filter(patientid__branch = 'Mulund',date =date.today()).order_by('time')

	print("data2---",data2)
	print("Length",len(data2))
	query = request.GET.get('query')	
	if query:
		data2 = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & ( Q(patientid__case__icontains = query) | Q(patientid__phone__icontains = query) | Q(patientid__name__icontains = query)))
		# data2 = Appointment.objects.filter(patientid__branch = 'Mulund',date =date.today(),patientid__case = query).order_by('time')
	p = Paginator(data2 ,7)
	page = request.GET.get('page')
	datas = p.get_page(page)
	d1 = date.today()
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

	new_patient = Appointment.objects.filter(patientid__branch="Mulund",date=date.today(),patientid__flag=True,stat="Repeat Medicine").count()
	appointment_due = Appointment.objects.filter(patientid__branch="Mulund",date=date.today(),doctor_notification=False,stat="Repeat Medicine",patientid__flag=False).count()
	medicine_not_issued = Appointment.objects.filter(Q(patientid__branch="Mulund") &Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False) & Q(stat="Repeat Medicine")).count()
	medicine_issued = Appointment.objects.filter(Q(patientid__branch="Mulund") & Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True) & Q(stat="Repeat Medicine")).count()
	
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
	unsent_mail_count = mail_count.count()
	

	return render(request , 'doc_repeat_med_mul_newone_adjust.html', {'user' :"D" , 'status':status, "datas":datas ,'date':d1,
						     'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
							 'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
							  'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,
							  "header":"Repeat Medicine Mulund","new_patient":new_patient,"appointment_due":appointment_due,
							"medicine_not_issued":medicine_not_issued,'medicine_issued':medicine_issued,
							"unsend_mail_count":unsent_mail_count})
@csrf_exempt
def doc_courier_med_mul(request):

	status = False
	if request.user:
		status = request.user
	
	user_id = User.objects.get(username=request.user)
	docter= Docter.objects.get(username=user_id)	
	data2 = Appointment.objects.filter(patientid__branch = 'Mulund',date =date.today()).order_by('time')
	query = request.GET.get('query')	
	if query:
		data2 = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & ( Q(patientid__case__icontains = query) | Q(patientid__phone__icontains = query) | Q(patientid__name__icontains = query)))
		# data2 = Appointment.objects.filter(patientid__branch = 'Mulund',date =date.today(),patientid__case = query).order_by('time')
	p = Paginator(data2 ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)
	d1 = date.today()
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

	new_patient = Appointment.objects.filter(patientid__branch="Mulund",date=date.today(),patientid__flag=True,stat="Courier Medicine",doctor_notification=False).count()
	appointment_due = Appointment.objects.filter(patientid__branch="Mulund",date=date.today(),doctor_notification=False,stat="Courier Medicine",patientid__flag=False).count()
	medicine_not_issued = Appointment.objects.filter(Q(patientid__branch="Mulund") &Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False) & Q(stat="Courier Medicine")).count()
	medicine_issued = Appointment.objects.filter(Q(patientid__branch="Mulund") & Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True) & Q(stat="Courier Medicine")).count()
	
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
	unsent_mail_count = mail_count.count()

	return render(request , 'doc_courier_med_mul_newone_adjust.html', {'user' :"D" , 'status':status, "datas":datas ,'date':d1,
						      'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
							  'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
							  'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,
							  "header":"Courier Medicine Mulund","new_patient":new_patient,"appointment_due":appointment_due,
		"medicine_not_issued":medicine_not_issued,'medicine_issued':medicine_issued,"unsend_mail_count":unsent_mail_count})

@csrf_exempt
def docter_appointment_mulund(request):
	status = False
	if request.user:
		status = request.user
	
	user_id = User.objects.get(username=request.user)
	docter= Docter.objects.get(username=user_id)	
	data2 = Appointment.objects.filter(patientid__branch = 'Mulund',date =date.today())
	query = request.GET.get('query')	
	if query:
		data2 = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & ( Q(patientid__case__icontains = query) | Q(patientid__phone__icontains = query) | Q(patientid__name__icontains = query)))
		# data2 = Appointment.objects.filter(patientid__branch = 'Mulund',date =date.today(),patientid__case = query)
	p = Paginator(data2 ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)
	d1 = date.today()

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

	new_patient = Appointment.objects.filter(patientid__branch="Mulund",date=date.today(),patientid__flag=True,stat="General").count()
	appointment_due = Appointment.objects.filter(patientid__branch="Mulund",date=date.today(),doctor_notification=False,stat="General",patientid__flag=False).count()
	medicine_not_issued = Appointment.objects.filter(Q(patientid__branch="Mulund") &Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False) & Q(stat="General")).count()
	medicine_issued = Appointment.objects.filter(Q(patientid__branch="Mulund") & Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True) & Q(stat="General")).count()
	
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
	unsent_mail_count = mail_count.count()
	
	return render(request , 'my_appointment_mulund_newone_adjust.html', {'user' :"D" , 'status':status, "datas":datas ,'date':d1,
							'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
							'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
							'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,
							"header":"General Appointments Mulund","new_patient":new_patient,"appointment_due":appointment_due,
							"medicine_not_issued":medicine_not_issued,'medicine_issued':medicine_issued,"unsend_mail_count":unsent_mail_count})

# Apointment Details
@csrf_exempt
def apointmentDetails(request,id,token):

	status = False
	if request.user:
		status = request.user		
	data = Patient.objects.get(id=id)			
	data2 =prescription.objects.all().filter(patientid=data.id,date=date.today()).order_by('-date')	

	obj = TokenUpdate.objects.last()
	if obj.consultancy:
		obj.token=token
		obj.save()
	
	app = Appointment.objects.get(date=date.today(),patientid_id=id)
	if app.patientid.branch == 'Dombivali':
		tok = app.token
	else:
		tok = app.token1

	notify = Appointment.objects.filter(patientid=id,date=date.today())
	for n in notify:
		patient_flag = n.patientid.flag
	if request.method == "POST":
		for n in notify:
			not_flag = get_object_or_404(Appointment,id=n.id)
			not_flag.doctor_notification = True
			not_flag.status=True
			not_flag.save(not_flag.patientid.branch,not_flag.stat,not_flag.notification_flag,not_flag.doctor_notification,not_flag.status)
		pa = Patient.objects.get(id=id)		
		me = request.POST['medicine']		
		po = request.POST['potency']
		da = date.today()	
		du = request.POST['duration']
		diagnose = request.POST.getlist('select-diagnose')
		list_of_disease_str = ', '.join(map(str, diagnose))
		list_of_disease_str_uppercase = list_of_disease_str.upper()
		start_date = request.POST['start_date']
		dose = request.POST['dose']
		note = request.POST['note']
		p= prescription.objects.create(patientid=pa ,medicine=me.upper(),potency=po,date=da,durations=du,diagnose=list_of_disease_str_uppercase,start_date=start_date,dose=dose,note=note)
		p.save()
		messages.success(request,f"Successfully Added {me}-{po} for {du}.")
		return HttpResponseRedirect(reverse('apointmentDetails',  kwargs={'id': pa.id,'token':tok}))				
		
	patient_details = Patient.objects.get(id=id)	

	today = date.today()
	duration_new =prescription.objects.filter(patientid=data.id,date=date.today()).last()
	if duration_new:
		obj_new = duration_new.durations.split(' ')
		if obj_new[1] == "Days":	
			rem_days = int(obj_new[0]) % 7
			num_days = int(obj_new[0]) - rem_days
			next_visit = today + relativedelta(days=num_days)
		else:
			next_visit = today + relativedelta(months=int(obj_new[0]))

	else:
		next_visit = " "

	patient_balance = Balance.objects.filter(patient_id=id).last()
	# status_medicine = Appointment.objects.filter(patientid_id =id ).last()
	
	data1 = OtherPrescription.objects.filter(patient__id = id, date=date.today())
	data_issued =prescription.objects.filter(patientid__id=id,date=date.today()).first()
	# print("status_medicine",status_medicine.patientid.name,status_medicine.date,status_medicine.stat)
	# print("------------")
	# print("balance",patient_balance.patient.case,patient_balance.patient.name,patient_balance.balance_amt)

	diagnose_dropdown = PresentComplaintsNew.objects.filter(patient__id=id)

	previous_prescriptions = prescription.objects.all().filter(patientid=id).order_by('-date')

	
	medicine = request.GET.get('medicine')

	if medicine:
		previous_prescriptions = prescription.objects.filter(Q(patientid=id) & Q(medicine__icontains=medicine)).order_by('-date')	

	# print("APPOINTMENT TYPE-------",app.stat)

	health = HealthAssessment.objects.filter(patient = id).order_by('-date')
	# print("Health",health)
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
			# 'user':"AP",
		
			'user':"D",
			'status':status,
			'data':data,
			'data2':data2,
			'id':id,
			'token':tok,
			'patient_flag':patient_flag,
			'data1':data1,
			'data_issued':data_issued,
			"header": "Today's Prescription",
			"header_one":"Prescribe Medicine",
			"patient_details":patient_details,
			"next_visit":next_visit,
			'balance':patient_balance,
			'diagnose_dropdown':diagnose_dropdown,
			'previous_prescriptions':previous_prescriptions,
			'today':date.today(),
			'appointment_type':app.stat,
			'health':health,
			'count_general_dom':count_general_dom,
			'count_general_mul':count_general_mul,
			'count_repeat_dom':count_repeat_dom,
			'count_repeat_mul':count_repeat_mul,
			'count_courier_dom':count_courier_dom,
			'count_courier_mul':count_courier_mul,
			"unsend_mail_count":unsent_mail_count}
	return render(request,'apointmentDetails_newone_adjust.html',context ) 


def search_prescriptions(request):
	if request.method == 'GET' and  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
		query = request.GET.get('query', '')
		# print("Queryyyy--",query)
		patient_id = request.GET.get('patient_id', None)
		# print("Patient__id",patient_id)
		if patient_id is not None:
			prescriptions = prescription.objects.filter(patientid_id=patient_id, medicine__icontains=query).order_by('-date')
			data = [{'patient': prescription.patientid.name, 'medicine': prescription.medicine, 'potency': prescription.potency ,'date':prescription.date} for prescription in prescriptions]
			return JsonResponse(data, safe=False)
	return JsonResponse({}, status=400)




@csrf_exempt
def health_assessment(request,id,token):

	pat  = Patient.objects.get(id=id)

	if request.method == 'POST':
		# print("BP",request.POST['bloodPressure'])
		# print("weight",request.POST['weight'])
		blood_press = request.POST['bloodPressure']
		wt = request.POST['weight']
		HealthAssessment.objects.create(patient = pat, bp = blood_press,weight=wt)
		messages.success(request,f'Successfully Added BP: {blood_press} mm/Hg , Weight : {wt} kgs.')
		return HttpResponseRedirect(reverse('apointmentDetails',kwargs={'id':id,'token':token})) 
	
def delete_health_assessment(request,id,token):

	data = HealthAssessment.objects.get(id=id)
	data.delete()
	messages.success(request,'Successfully Deleted the Health Assessment')
	return HttpResponseRedirect(reverse('apointmentDetails',kwargs={'id':data.patient.id,'token':token}))

	


@csrf_exempt

def present_complaint_appointment(request,case_id,token):

	status = False
	if request.user:
		status =  request.user

	patient_details = Patient.objects.get(id=case_id)

	instance =Category.objects.get(id=7)
	instance1 = Patient.objects.get(id=case_id)
	form = NewCaseForm(initial= {'category': instance,'patient':instance1})

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
		'status':status,
		'user' : 'D',
		 "unsend_mail_count":unsent_mail_count,
        'count_general_dom':count_general_dom,
        'count_general_mul':count_general_mul,
        'count_repeat_dom':count_repeat_dom,
        'count_repeat_mul':count_repeat_mul,
        'count_courier_dom':count_courier_dom,        
        'count_courier_mul':count_courier_mul,
		'patient_details':patient_details,
		'form':form,
		'token':token,
		'case_id':case_id,
		'patient':patient_details,
		
	}
	return render(request,'present_complaint_appointment_adjust.html',context)
@csrf_exempt
def present_complaints_add(request,id):

	status = False
	if request.user:
		status = request.user

	patient = Patient.objects.get(id=id)
	print("Patient",patient)
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
			messages.success(request, 'Successfully Added to the Present Complaint')
			return HttpResponseRedirect(reverse('present_complaints_add', kwargs={'id':id}))
	
	else:
		form = PresentComplaintsForm()

	
	table_data = PresentComplaintsNew.objects.filter(patient__id=id).order_by('-date')
	context = {
		'status': status,
		'user': 'D',
		'form': form,
		'table_data':table_data,
	}
	return render(request,'COMMON_APP/present_complaints_add_adjust.html',context)


@csrf_exempt
def add_consultation(request,id,token):

	status = False
	if request.user:
		status = request.user

	data = Patient.objects.get(id=id)	
	if request.method == 'POST':

		patient = Patient.objects.get(id=id)
		consultation_name = request.POST['consultation_text']
		price = request.POST['price']
		obj = AddConsultationCharges(patient=patient,name=consultation_name,other_price=price)
		obj.save()
		messages.success(request,"Added Consultation Charges of Rs " + request.POST['price'] )
		return HttpResponseRedirect(reverse('add_consultation',  kwargs={'id': id,'token':token}))
	
	consult_data = AddConsultationCharges.objects.filter(patient__id = id, date=date.today())
	data2 =prescription.objects.filter(patientid__id=id,date=date.today()).first()

	context = {
		'status' : status,
		'user' : 'AP',
		'id':id,
		'token':token,
		'data':data,
		'consult_data':consult_data,
		'data2':data2,
		'patient':data
	}
	return render(request,'add_consultation_adjust.html',context)

@csrf_exempt
def delete_consultation_charges(request,id,token):


	data = AddConsultationCharges.objects.get(id=id)
	pat_id = data.patient.id

	data.delete()
	messages.success(request,"Deleted Consultation Charges of Rs " + data.other_price )
	return HttpResponseRedirect(reverse('add_consultation',  kwargs={'id': pat_id,'token':token}))

@csrf_exempt	
def extra_prescription(request,id,token):

	status = False
	if request.user:
		status = request.user

	if request.method == 'POST':

		patient = Patient.objects.get(id=id)
		any_other_med = request.POST['any_other_med']
		price = request.POST['price']
		obj = OtherPrescription(patient=patient,description=any_other_med,other_price=price)
		obj.save()
		messages.success(request,"Added Extra Prescription")
		return HttpResponseRedirect(reverse('extra_prescription',  kwargs={'id': id,'token':token}))

	data1 = OtherPrescription.objects.filter(patient__id = id, date=date.today())
	patient_details = Patient.objects.get(id=id)
	data = Patient.objects.get(id=id)

	data2 =prescription.objects.filter(patientid__id=id,date=date.today()).first()

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
		'status':status,
		'user':'D',
		'data': data,
		'data1':data1,
		'patient_details':patient_details,
		'id':id,
		'token':token,
		'data2':data2,
		'count_general_dom':count_general_dom,
			'count_general_mul':count_general_mul,
			'count_repeat_dom':count_repeat_dom,
			'count_repeat_mul':count_repeat_mul,
			'count_courier_dom':count_courier_dom,
			'count_courier_mul':count_courier_mul,
			"unsend_mail_count":unsent_mail_count
	}
	return render(request,'extra_prescription_adjust.html',context)

@csrf_exempt
def delete_extra_prescription(request,id,token):


	data = OtherPrescription.objects.get(id=id)
	pat_id = data.patient.id

	data.delete()
	return HttpResponseRedirect(reverse('extra_prescription',  kwargs={'id': pat_id,'token':token}))
@csrf_exempt
def upload_patients_image(request,id):

	status = False
	if request.user:
		status = request.user

	patient_details = Patient.objects.get(id=id)

	if request.method == 'POST':

		patient = Patient.objects.get(id=id)
		images = request.FILES.getlist('images')

		for image in images:
			photo = PatientImages.objects.create(patient=patient,images=image)
		
		messages.success(request,"Patient's Images Uploaded Successfully")
		return HttpResponseRedirect(reverse('upload_patients_image',  kwargs={'id': id}))

	appoint = Appointment.objects.filter(Q(patientid=patient_details)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1



	context = {
		"patient_details":patient_details,
		"status":status,
		"user":"D",
		"patient":patient_details,
		'id':id,
		'final_token': final_token,
	}
	return render(request,'upload_patients_image.html',context)

@csrf_exempt
def doc_patient_images(request,id):

	status = False
	if request.user:
		status = request.user

	patient_details = Patient.objects.get(id=id)
	img = PatientImages.objects.filter(patient = id)
	p = Paginator(img,9)
	page = request.GET.get('page')
	datas = p.get_page(page)

	appoint = Appointment.objects.filter(Q(patientid=patient_details)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1


	context= {
		"status":status,
		"user": 'D',
		"patient":patient_details,
		"datas":datas,
		'id':id,
		'final_token':final_token,
	}


	return render(request,'doc_patinet_images.html',context)

@csrf_exempt	
def investigation_newone(request,id):

	status = False
	if request.user:
		status = request.user

	data = InvestigationAdvised.objects.all()
	patient= Patient.objects.get(id=id)

	if request.method == 'POST':
		records = request.POST.getlist('investigation-advised')
		any_other = request.POST['any_other']
		obj = InvestigationRecords(patient=patient,records=records,any_other=any_other)
		obj.save()
		messages.success(request,f"Successfully! Added Investigations to be done.")
		return HttpResponseRedirect(reverse('investigation_newone',kwargs={'id':id}))
	
	table_data = InvestigationRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list = []
	for t in table_data:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)


	appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1
	
	    
	context = {
		"status" : status,
		"user" : 'D',
		"patient_details":patient,
		"data": data,
		"my_list": my_list,
		"id":id,
		'final_token': final_token,
		'patient':patient,
	}
	return render(request,'investigation_newone_adjust.html',context)

@csrf_exempt
def ultra_sonography_newone(request,id):

	status = False
	if request.user:
		status = request.user

	data = Ultrasonography.objects.all()
	patient= Patient.objects.get(id=id)

	if request.method == 'POST':
		records = request.POST.getlist('investigation-advised')		
		obj = UltrasonographyRecords(patient=patient,records=records)
		obj.save()
		messages.success(request,f'Successfully Added Ultra-Sonography to done.')
		return HttpResponseRedirect(reverse('ultra_sonography_newone',kwargs={'id':id}))
	
	table_data = UltrasonographyRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list = []
	for t in table_data:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)

	appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1
	    
	context = {
		"status" : status,
		"user" : 'D',
		"patient_details":patient,
		"data": data,
		"my_list": my_list,
		"id":id,
		'final_token': final_token,
		'patient':patient,
	}
	return render(request,'ultra_sonography.html',context)

@csrf_exempt
def doppler_studies_newone(request,id):

	status = False
	if request.user:
		status = request.user

	data = Doppler.objects.all()
	patient= Patient.objects.get(id=id)

	if request.method == 'POST':
		records = request.POST.getlist('investigation-advised')		
		obj = DopplerRecords(patient=patient,records=records)
		obj.save()
		messages.success(request,f"Successfully Added Doppler Studies to done.")
		return HttpResponseRedirect(reverse('doppler_studies_newone',kwargs={'id':id}))
	
	table_data = DopplerRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list = []
	for t in table_data:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)

	appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1
	    
	context = {
		"status" : status,
		"user" : 'D',
		"patient_details":patient,
		"data": data,
		"my_list": my_list,
		"id":id,
		'patient':patient,
		'final_token':final_token,
	}
	return render(request,'doppler_studies_adjust.html',context)
@csrf_exempt
def  obstetrics_newone(request,id):
	status = False
	if request.user:
		status = request.user

	data = Obstetrics.objects.all()
	patient= Patient.objects.get(id=id)

	if request.method == 'POST':
		records = request.POST.getlist('investigation-advised')		
		obj = ObstetricRecords(patient=patient,records=records)
		obj.save()
		messages.success(request,f"Successfully! Added Obstetrics(Pregnancy) to be done.")
		return HttpResponseRedirect(reverse('obstetrics_newone',kwargs={'id':id}))
	
	table_data = ObstetricRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list = []
	for t in table_data:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)
	
	appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1

	context = {
		"status" : status,
		"user" : 'D',
		"patient_details":patient,
		"data": data,
		"my_list": my_list,
		"id":id,
		'final_token': final_token,
		'patient':patient,
	}
	return render(request,'obstetrics_newone_adjust.html',context)

@csrf_exempt
def  sonography_newone(request,id):
	status = False
	if request.user:
		status = request.user

	data = SonographyType.objects.all()
	patient= Patient.objects.get(id=id)
	
	if request.method == 'POST':
		records = request.POST.getlist('investigation-advised')		
		obj = SonographyTypeRecords(patient=patient,records=records)
		obj.save()
		messages.success(request,f"Successfully! Added Sonography to be done.")
		return HttpResponseRedirect(reverse('sonography_newone',kwargs={'id':id}))
	
	table_data = SonographyTypeRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list = []
	for t in table_data:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)

	appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1

	    
	context = {
		"status" : status,
		"user" : 'D',
		"patient_details":patient,
		"data": data,
		"my_list": my_list,
		"id":id,
		'final_token': final_token,
		'patient':patient,
	}
	return render(request,'sonography_newone_adjust.html',context)

@csrf_exempt
def ct_scan_newone(request,id):
	status = False
	if request.user:
		status = request.user

	data = CTScanNew.objects.all()
	patient= Patient.objects.get(id=id)
	
	if request.method == 'POST':
		records = request.POST.getlist('investigation-advised')		
		obj = CTScanNewRecords(patient=patient,records=records)
		obj.save()
		messages.success(request,f'Successfully! Added CT Scan to be done ')
		return HttpResponseRedirect(reverse('ct_scan_newone',kwargs={'id':id}))
	
	table_data = CTScanNewRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list = []
	for t in table_data:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)
	appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1
	
	    
	context = {
		"status" : status,
		"user" : 'D',
		"patient_details":patient,
		"data": data,
		"my_list": my_list,
		"id":id,
		'final_token': final_token,
		'patient':patient,
	}
	return render(request,'ct_scan_newone_adjust.html',context)

@csrf_exempt
def mri_scan_newone(request,id):
	status = False
	if request.user:
		status = request.user

	data = MRIScanNew.objects.all()
	patient= Patient.objects.get(id=id)
	
	if request.method == 'POST':
		records = request.POST.getlist('investigation-advised')	
		any_other = request.POST['any_other']	
		obj = MRIScanNewRecords(patient=patient,any_other=any_other,records=records)
		obj.save()
		messages.success(request,f'Successfully! Added 1.5 Tesla MRI Scan to be done.')
		return HttpResponseRedirect(reverse('mri_scan_newone',kwargs={'id':id}))
	
	table_data = MRIScanNewRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list = []
	for t in table_data:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list.append(x)

	appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1
	  
	context = {
		"status" : status,
		"user" : 'D',
		"patient_details":patient,
		"data": data,
		"my_list": my_list,
		"id":id,
		'final_token':final_token,
		'patient':patient,
	}

	return render(request,'mri_scan_newone_adjust.html',context)

@csrf_exempt
def generate_investigation_pdf(request,id):

	status =False
	if request.user:
		status = request.user

	table_data_one = InvestigationRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list_one = []
	for t in table_data_one:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list_one.append(x)
	    
	table_data_two = UltrasonographyRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list_two = []
	for t in table_data_two:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list_two.append(x)

	table_data_three = DopplerRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list_three = []
	for t in table_data_three:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list_three.append(x)
	    
	table_data_four = ObstetricRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list_four = []
	for t in table_data_four:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list_four.append(x)
	    
	table_data_five = SonographyTypeRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list_five = []
	for t in table_data_five:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list_five.append(x)
	
	table_data_six = CTScanNewRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list_six = []
	for t in table_data_six:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list_six.append(x)
	    
	table_data_seven = MRIScanNewRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
	my_list_seven = []
	for t in table_data_seven:
            x = t.records
            x = x.replace("[","").replace("'","").replace("]","")
            my_list_seven.append(x)
	    
	patient=Patient.objects.get(id=id)    
	

	context={
		"id": id,
		"status" : status,
		"user" : 'D',
		"header": "List of Investigations",
		"len_one" : len(my_list_one),
		"my_list_one": my_list_one,
		"len_two" : len(my_list_two),
		"my_list_two": my_list_two,
		"len_three" : len(my_list_three),
		"my_list_three": my_list_three,
		"len_four" : len(my_list_four),
		"my_list_four": my_list_four,
		"len_five" : len(my_list_five),
		"my_list_five":my_list_five,
		"len_six" : len(my_list_six),
		"my_list_six":my_list_six,
		"len_seven" : len(my_list_seven),
		"my_list_seven":my_list_seven,
		'patient':patient,
		'today':date.today(),
	}
	return render(request,'generate_investigation_pdf_adjust.html',context)

from COMMON_APP.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View

@method_decorator(csrf_exempt, name='dispatch')
class Investigation_pdf(View):

	def get(self,request,*args,**kwargs):
		id = self.kwargs['pk']
		patient_details = Patient.objects.get(id=id)

		table_data_one = InvestigationRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
		my_list_one = []
		for t in table_data_one:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list_one.append(x)

		table_data_two = UltrasonographyRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
		my_list_two = []
		for t in table_data_two:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list_two.append(x)

		table_data_three = DopplerRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
		my_list_three = []
		for t in table_data_three:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list_three.append(x)

		table_data_four = ObstetricRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
		my_list_four = []
		for t in table_data_four:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list_four.append(x)

		table_data_five = SonographyTypeRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
		my_list_five = []
		for t in table_data_five:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list_five.append(x)

		table_data_six = CTScanNewRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
		my_list_six = []
		for t in table_data_six:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list_six.append(x)

		table_data_seven = MRIScanNewRecords.objects.filter(Q(patient__id=id) & Q(date=date.today()))
		my_list_seven = []
		for t in table_data_seven:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list_seven.append(x)

		data = {
			"header": "List of Investigations",
			"patient_details": patient_details,
		"len_one" : len(my_list_one),
		"my_list_one": my_list_one,
		"len_two" : len(my_list_two),
		"my_list_two": my_list_two,
		"len_three" : len(my_list_three),
		"my_list_three": my_list_three,
		"len_four" : len(my_list_four),
		"my_list_four": my_list_four,
		"len_five" : len(my_list_five),
		"my_list_five":my_list_five,
		"len_six" : len(my_list_six),
		"my_list_six":my_list_six,
		"len_seven" : len(my_list_seven),
		"my_list_seven":my_list_seven,
		"today":date.today(),

		}
		pdf = render_to_pdf('investigation_pdf.html',data)
		return HttpResponse(pdf, content_type='application/pdf')

from .forms import *
@csrf_exempt
def add_investigation(request,pk):

	status = False
	if request.user:
		status = request.user

	form = InvestigationForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request,"Added a New Investigation Successfully!")
		return HttpResponseRedirect(reverse('add_investigation',  kwargs={'pk':pk})) 

	data = InvestigationAdvised.objects.all()
	patient = Patient.objects.get(id=pk)


	context = {
		"status":status,
		"user": "D",
		"form":form,
		"pk":pk,
		"data":data,
		"header" : "Add a New Investigation :",
		"table_header" : "Add  (New Investigation)",		
		'patient':patient,

	}

	return render(request,"add_investigation_adjust.html",context)

@csrf_exempt		
def add_ultrasonography(request,pk):

	status = False
	if request.user:
		status = request.user

	form = UltrasonographyForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request,f"Added New Utra-Sonography Successfully.")
		return HttpResponseRedirect(reverse('add_ultrasonography',  kwargs={'pk':pk})) 

	data = Ultrasonography.objects.all()
	patient = Patient.objects.get(id=pk)
	context = {
		"status":status,
		"user": "D",
		"form":form,
		"pk":pk,
		"data":data,
		"header" : "Add a New Ultra-Sonography :",
		"table_header" : "Add  (New Ultrasonography)",
		'patient':patient,
	}
	return render(request,"add_investigation_adjust.html",context)

@csrf_exempt
def add_doppler(request,pk):

	status = False
	if request.user:
		status = request.user

	form = DopplerForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request,f'Added New Doppler Study Successfully !')
		return HttpResponseRedirect(reverse('add_doppler',  kwargs={'pk':pk})) 

	data = Doppler.objects.all()
	context = {
		"status":status,
		"user": "D",
		"form":form,
		"pk":pk,
		"data":data,
		"header" : "Add a New Doppler Studies :",
		"table_header" : "Add  (New Doppler Studies)",
	}
	return render(request,"add_investigation_adjust.html",context)

@csrf_exempt
def add_obstetrics(request,pk):

	status = False
	if request.user:
		status = request.user

	form = ObstetricsForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request,f'Added a new Obstetrics(Pregnancy) Successfully!')
		return HttpResponseRedirect(reverse('add_obstetrics',  kwargs={'pk':pk})) 

	data = Obstetrics.objects.all()
	patient = Patient.objects.get(id=pk)
	context = {
		"status":status,
		"user": "D",
		"form":form,
		"pk":pk,
		"data":data,
		"header" : "Add a New Obstetrics :",
		"table_header" : "Add  (New Obstetrics)",
		'patient':patient,
	}
	return render(request,"add_investigation_adjust.html",context)

@csrf_exempt
def add_sonographytype(request,pk):

	status = False
	if request.user:
		status = request.user

	form = SonographyTypeForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request,f'Added a New Sonography Successfully!')		
		return HttpResponseRedirect(reverse('add_sonographytype',  kwargs={'pk':pk})) 

	data = SonographyType.objects.all()
	patient = Patient.objects.get(id=pk)
	context = {
		"status":status,
		"user": "D",
		"form":form,
		"pk":pk,
		"data":data,
		"header" : "Add a New Sonography Type :",
		"table_header" : "Add  (New Sonography Type)",
		'patient':patient,
	}
	return render(request,"add_investigation_adjust.html",context)

@csrf_exempt
def add_ctscan(request,pk):

	status = False
	if request.user:
		status = request.user

	form = CTScanNewForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request,f'Added a new 16 Slice C.T Scan Successfully!')
		return HttpResponseRedirect(reverse('add_ctscan',  kwargs={'pk':pk})) 

	data = CTScanNew.objects.all()
	
	context = {
		"status":status,
		"user": "D",
		"form":form,
		"pk":pk,
		"data":data,
		"header" : "Add a New  16 Slice C.T Scan :",
		"table_header" : "Add  (New 16 Slice C.T Scan)",
	}
	return render(request,"add_investigation_adjust.html",context)

@csrf_exempt
def add_mriscan(request,pk):

	status = False
	if request.user:
		status = request.user

	form = MRIScanNewForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request,f'Successfully! Added a new 1.5 Tesla MRI Scan.')
		return HttpResponseRedirect(reverse('add_mriscan',  kwargs={'pk':pk})) 

	data = MRIScanNew.objects.all()
	context = {
		"status":status,
		"user": "D",
		"form":form,
		"pk":pk,
		"data":data,
		"header" : "Add a New  1.5 Tesla MRI Scan :",
		"table_header" : "Add  (New 1.5 Tesla MRI Scan)",
	}
	return render(request,"add_investigation_adjust.html",context)

@csrf_exempt
def delete_investigation(request,id):

	pre_url = request.META.get('HTTP_REFERER')
	print('pre_url-----',pre_url,type(pre_url))
	
	obj =pre_url.split('/')
	print('obj',obj,obj[3],obj[4])

	if obj[3] == "add_investigation":
		print("True----------")
		new_obj = InvestigationAdvised.objects.get(id=id).delete()
		messages.info(request,"Deleted Successfully")
		return HttpResponseRedirect(reverse('add_investigation',  kwargs={'pk':int(obj[4])}))
	elif obj[3] =="add_ultrasonography":
		new_obj = Ultrasonography.objects.get(id=id).delete()
		messages.info(request,"Deleted Successfully")
		return HttpResponseRedirect(reverse('add_ultrasonography',  kwargs={'pk':int(obj[4])}))
	elif obj[3] =="add_doppler":
		new_obj = Doppler.objects.get(id=id).delete()
		messages.info(request,"Deleted Successfully")
		return HttpResponseRedirect(reverse('add_doppler',  kwargs={'pk':int(obj[4])}))
	elif obj[3] =="add_obstetrics":
		new_obj =Obstetrics.objects.get(id=id).delete()
		messages.info(request,"Deleted Successfully")
		return HttpResponseRedirect(reverse('add_obstetrics',  kwargs={'pk':int(obj[4])}))
	elif obj[3] =="add_sonographytype":
		new_obj =SonographyType.objects.get(id=id).delete()
		messages.info(request,"Deleted Successfully")
		return HttpResponseRedirect(reverse('add_sonographytype',  kwargs={'pk':int(obj[4])}))
	elif obj[3] =="add_ctscan":
		new_obj =CTScanNew.objects.get(id=id).delete()
		messages.info(request,"Deleted Successfully")
		return HttpResponseRedirect(reverse('add_ctscan',  kwargs={'pk':int(obj[4])}))
	elif obj[3] =="add_mriscan":
		new_obj =MRIScanNew.objects.get(id=id).delete()
		messages.info(request,"Deleted Successfully")
		return HttpResponseRedirect(reverse('add_mriscan',  kwargs={'pk':int(obj[4])}))
	


	
	
	
	
	

	
	
@csrf_exempt
def appointmentDashboard(request,id):
	
	print('id----',id)
	status = False
	if request.user:
		status = request.user		
		data = Patient.objects.get(id=id)			
		data2 =prescription.objects.all().filter(patientid=data.id,date=date.today()).order_by('-date')	

	if request.method == "POST":
		pa = Patient.objects.get(id=id)		
		me = request.POST['medicine']		
		po = request.POST['potency']
		da = date.today()	
		du = request.POST['duration']
		diagnose = request.POST['diagnose']
		print('diagnose',diagnose,diagnose.upper())
		start_date = request.POST['start_date']
		print('start_date',start_date)	
		# print('du@@@@',du)
		p= prescription.objects.create(patientid=pa ,medicine=me.upper(),potency=po,date=da,durations=du,diagnose=diagnose.upper(),start_date=start_date)
		return HttpResponseRedirect(reverse('appointmentDashboard',  kwargs={'id': pa.id}))

	return render(request,'appointmentDashboard.html',{'user':"DASH",'status':status,'data':data,'data2':data2} )

@csrf_exempt
def update_medicine(request,id,pk):

	# print("---testing123-----")
	# print('pk',pk)
	status = False
	if request.user:
		status= request.user

	patient = Patient.objects.get(id=id)
	# print('id',id)
	app = Appointment.objects.get(date=date.today(),patientid_id=id)
	# print("branch",app.patientid.branch)
	if app.patientid.branch == 'Dombivali':
		tok = app.token
	else:
		tok = app.token1
		
	if request.method == 'POST':
		# update = prescription.objects.filter(patientid=id).last()
		update = prescription.objects.get(id=pk)
		update.medicine = request.POST['medicine']
		update.potency = request.POST['potency']
		# print("print",request.POST['duration'])
		update.durations = request.POST['duration']
		diagnose_one = request.POST.getlist('select-diagnose')
		list_of_disease_str = ', '.join(map(str, diagnose_one))
		list_of_disease_str_uppercase = list_of_disease_str.upper()

		update.diagnose = list_of_disease_str_uppercase
		update.start_date = request.POST['start_date']
		update.dose = request.POST['dose']
		update.note = request.POST['note']
		update.save()
		messages.success(request,f'Successfully Updated')
		return HttpResponseRedirect(reverse('apointmentDetails',  kwargs={'id': patient.id,'token':tok}))
	# pres = prescription.objects.filter(patientid=id).last()
	pres = prescription.objects.get(id=pk)	
	pre_url = request.META.get('HTTP_REFERER')	
	obj =pre_url.split('/')
	diagnose_dropdown = PresentComplaintsNew.objects.filter(patient__id=id)

	update_complain = prescription.objects.get(id=pk)

	
	context = {'user':"D",
			'status': status,
			'data':patient.case,
			'pat':patient,
			'pres':pres,
			'id':id,
			'token':obj[5],
			'diagnose_dropdown':diagnose_dropdown,
			'update_complain':update_complain.diagnose,
			}
	return render(request,'update_medicine_adjust.html',context)



##signature Pad for doctor's prescription

@method_decorator(csrf_exempt, name='dispatch')
class ExampleCreateView(generic.CreateView):	
	model = ExampleModel	
	fields = '__all__'
	success_url = reverse_lazy('apointmentDetails')

	def get_success_url(self):		
		data = ExampleModel.objects.get(id=self.object.id)				
		return reverse_lazy('apointmentDetails', kwargs={'id': data.patient_id,'token':10000})

	def form_valid(self,form):
		response = super().form_valid(form)
		messages.success(self.request,f"Successfully Added Follow Up Details.")
		return response		

@method_decorator(csrf_exempt, name='dispatch')	
class ExampleUpdateView(generic.UpdateView):	
	model = ExampleModel
	fields = ['signature']
	success_url = reverse_lazy('apointmentDetails')		

	def get_success_url(self):		
		data = ExampleModel.objects.get(id=self.object.pk)		
		return reverse_lazy('apointmentDetails', kwargs={'id': data.patient_id,'token':10000})

	def form_valid(self,form):
		response = super().form_valid(form)
		messages.success(self.request,f"Successfully Updated Follow Up Details.")
		return response			

@method_decorator(csrf_exempt, name='dispatch')
class ExampleListView(generic.ListView):
	pass

from django.views.generic.detail import DetailView
@method_decorator(csrf_exempt, name='dispatch')
class ExampleDetailView(DetailView):	
	model = ExampleModel	

@method_decorator(csrf_exempt, name='dispatch')
class ExampleDeleteView(DeleteView):
	model = ExampleModel
	fields = '__all__'
	# success_url = reverse_lazy('list1')
	success_url = reverse_lazy('list1')

	def get_success_url(self):
		data = self.object
		print("data",self.object)
		return reverse_lazy('list1',kwargs={'pk':data.patient.id})

####customizing list view
@csrf_exempt
def list1(request,pk):

	global var
	def getSubstringBetweenTwoChars(ch1,ch2,str):
				return s[s.find(ch1)+0:s.find(ch2)] 
	status = False
	if request.user:
		status =  request.user

	s = request.META.get('HTTP_REFERER')
	s2= getSubstringBetweenTwoChars('a','d',s)
	var = s2
	print('list1-----',s2)			
	obj = ExampleModel.objects.filter(patient_id=pk).order_by('-signature_date')
	p = Paginator(obj ,2)
	page = request.GET.get('page')
	datas = p.get_page(page)

	patient = Patient.objects.get(id=pk)
	
	return render(request,'DOCTER/list1_adjust.html',{'patient':patient,'status':status,'user':'D','obj':obj,'datas':datas,'s2':s2})

from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
@csrf_exempt
def list1_pdf(request,pk):
	# print("------PK----",pk)
	response = HttpResponse(content_type = 'application/pdf')
	response['Content-Disposition'] = 'filename="Case.pdf"'
	buffer = BytesIO()
	p = canvas.Canvas(buffer,pagesize=A4)
	letter_head = "./dashboard/document/newcase.jpg"
	p.drawImage(letter_head,0,0,width=600,height=880)
	p.setFont("Helvetica", 18)
	data1 = ExampleModel.objects.get(id=pk)
	# print('----data1----',data1,data1.id)
	signature_path =draw_signature(data1.signature, as_file=True)
	p.drawImage(signature_path,50,460,width=500,height=135,mask='auto')
	p.showPage()
	p.save()
	p = buffer.getvalue()
	buffer.close()
	response.write(p)
	return response
@csrf_exempt
def create1(request,pk):

	status = False
	if request.user:
		status = request.user
	
	instance = Patient.objects.get(id=pk)
	form = ExampleForm(initial = {'patient': instance})
	id = pk	
	return render(request,'DOCTER/create1_adjust.html',{'form':form,'id':id,'status':status,'user':'D','patient':instance})
@csrf_exempt
def old_images(request,id):

	patient = Patient.objects.get(id=id)
	img =  PrescriptionOldUpload.objects.filter(patient = id)
	p = Paginator(img ,9)
	page = request.GET.get('page')
	datas = p.get_page(page)

	appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()

	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1
	




	return render(request,'old_images.html',{'datas':datas,'patient':patient,'id':id,'final_token':final_token})





@csrf_exempt
def casepaper_new_images(request,id):

	patient = Patient.objects.get(id=id)
	img =  NewCasePaperUpload.objects.filter(patient = id)
	p = Paginator(img ,9)
	page = request.GET.get('page')
	datas = p.get_page(page)

	appoint = Appointment.objects.filter(Q(patientid=patient)&Q(date=date.today())).last()

	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1
	

    

	return render(request,'new_images_casepaper.html',{'datas':datas,'patient':patient,'id':id,'final_token':final_token})
@csrf_exempt
def upload_case_image(request,id):

	instance = Patient.objects.get(id=id)
	
	if request.method == 'POST':
		form = NewCasePaperUploadFormOne(request.POST,request.FILES)
		files =request.FILES.getlist('images')
		if form.is_valid():	
			for i in files:
				NewCasePaperUpload.objects.create(patient = instance ,images =i)
			messages.info(request,"Casepaper Images Uploaded for "+ instance.name +" " +instance.case)
			return HttpResponseRedirect(reverse('upload_case_image', kwargs={'id':id}))
	form = NewCasePaperUploadFormOne(initial={'patient': instance})
	appoint = Appointment.objects.filter(Q(patientid=instance)&Q(date=date.today())).last()
	if appoint.token != 0:
		final_token = appoint.token
	else:
		final_token = appoint.token1
	return render(request,'upload_case_image.html',{'form':form,'patient':instance,'id':id,'final_token':final_token})


@csrf_exempt
def back_update(request):
	pre_url = request.META.get('HTTP_REFERER')
	# print('pre_url-----',pre_url,type(pre_url))
	obj = pre_url.split("update/")			
	data = ExampleModel.objects.get(id=int(obj[1]))	
	return HttpResponseRedirect(reverse('list1',  kwargs={'pk': data.patient_id}))
@csrf_exempt
def back_delete(request):
	pre_url = request.META.get('HTTP_REFERER')
	obj = pre_url.split("delete/")
	data = ExampleModel.objects.get(id=int(obj[1]))
	return HttpResponseRedirect(reverse('list1',  kwargs={'pk': data.patient_id}))
@csrf_exempt
def apointment_detail_home(request):	
	
	try:
		try:
			pre_url = request.META.get('HTTP_REFERER')
			obj = pre_url.split("create1/")
			return HttpResponseRedirect(reverse('apointmentDetails',  kwargs={'id': int(obj[1]),'token':10000}))
		except:
			pre_url = request.META.get('HTTP_REFERER')
			obj = pre_url.split("update/")
			data = ExampleModel.objects.get(id=int(obj[1]))
			return HttpResponseRedirect(reverse('apointmentDetails', kwargs= {'id':data.patient_id,'token':10000}))
	except:
		try:
			if var == 'appointmentDashboar':
				pre_url = request.META.get('HTTP_REFERER')
				obj = pre_url.split("list1/")
				return HttpResponseRedirect(reverse('appointmentDashboard',  kwargs={'id': int(obj[1])}))
			else:
				pre_url = request.META.get('HTTP_REFERER')
				obj = pre_url.split("list1/")
				return HttpResponseRedirect(reverse('apointmentDetails',  kwargs={'id': int(obj[1]),'token':10000}))
			# print('s2 Home',s2)
			# if s2 == 'apointmentDetail'	:		
			# 	pre_url = request.META.get('HTTP_REFERER')
			# 	obj = pre_url.split("list1/")
			# 	return HttpResponseRedirect(reverse('apointmentDetails',  kwargs={'id': int(obj[1]),'token':10000}))
			# else:
			# 	pre_url = request.META.get('HTTP_REFERER')
			# 	obj = pre_url.split("list1/")
			# 	return HttpResponseRedirect(reverse('appointmentDashboard',  kwargs={'id': int(obj[1])}))

			
		except:
			def getSubstringBetweenTwoChars(ch1,ch2,str):
				return s[s.find(ch1)+5:s.find(ch2)] 

			s = request.META.get('HTTP_REFERER')
			s2= getSubstringBetweenTwoChars('i','?',s)
			# print('s2',s2)
			return HttpResponseRedirect(reverse('apointmentDetails',  kwargs={'id': int(s2),'token':10000}))
			
			
@csrf_exempt
def create_view(request,id):

	instance = Patient.objects.get(id=id)
	

	# if request.method == 'POST':
		
	form = ExampleForm(request.POST or None,request.FILES,initial={'patient': instance})
	if form.is_valid():
		# print('cleaned_data--------',form.cleaned_data.get['signature'])
		# print('cleaned_data@2',form.cleaned_data['patient'])
		signature = form.cleaned_data.get('signature')
		if signature:
			signature_picture = draw_signature(signature)
			signature_file_path = draw_signature(signature, as_file=True)
		form.save()
		return redirect('create_view')
	form = ExampleForm(initial={'patient': instance})	

	return render(request,'create_view.html',{'form':form,'data':id})
@csrf_exempt
def previousDashboard(request,id):
	
	data = prescription.objects.filter(patientid__id=id).order_by('-date')
	patient = Patient.objects.get(id=id)
	
	# return HttpResponseRedirect(reverse('appointmentDashboard',  kwargs={'id':id}))
	return render(request,'previousdashboard.html',{'patient':patient,'data':data})
@csrf_exempt	
def imagesDashboard(request,id):
	
	patient = Patient.objects.get(id=id)
	
	img = ImagesUpload.objects.filter(case__id=id)
	
	return render(request,'imagesdashboard.html',{'patient':patient,'img':img})

#payment
@csrf_exempt
def payment(request, id):
	status = False
	
	if request.user:
		status = request.user		
		data = Patient.objects.get(case=id)	
		data2 =prescription.objects.all().filter(patientid=data.id).order_by('-date')
	try:
		pres = prescription.objects.filter(patientid__case = id).last()
		print("pres date",pres.date)
		rep_pres = prescription.objects.filter(patientid__case = id,date=pres.date)
		print('rep PRES',rep_pres)
		for r in rep_pres:
			print(r.id)
		pres1= pres.id
	except:
		pres1 = " "
		rep_pres = " "
	return render(request,'payment.html',{'user':"AP",'status':status,'data':data,'data2':data2,'pres':pres1,'rep_pres':rep_pres})

@csrf_exempt
def doc_repeat_medicine(request,id,pk):
	
	print('pk',pk)
	status =False
	if request.user:
		status = request.user	
	
	app = Appointment.objects.get(date=date.today(),patientid__case=id)
	
	if app.patientid.branch == 'Dombivali':
		tok = app.token
	else:
		tok = app.token1

	notify = Appointment.objects.filter(patientid__case=id,date=date.today())
	print('notification',notify)	
	
	if request.method == "POST":

		print('notify_POST',notify)
		for n in notify:
			print('app_id',n.id)
			print('before payment',n.doctor_notification)
			not_flag = get_object_or_404(Appointment,id=n.id)
			print('not_flag',not_flag)
			not_flag.doctor_notification = True
			not_flag.status = True
			print('after_payment',n.doctor_notification)
			print('branch',not_flag.patientid.branch)
			not_flag.save(not_flag.patientid.branch,not_flag.stat,not_flag.notification_flag,not_flag.doctor_notification,not_flag.status)


		pa = Patient.objects.get(case=id)				
		me = request.POST['medicine']		
		po = request.POST['potency']		
		da = date.today()			
		du = request.POST['duration']
		diagnose = request.POST['diagnose']
		start_date = request.POST['start_date']	
		p= prescription.objects.create(patientid=pa ,medicine=me,potency=po,date=da,durations=du,diagnose=diagnose,start_date=start_date)
		p.save()
		return HttpResponseRedirect(reverse('apointmentDetails',  kwargs={'id': pa.id,'token':tok}))

	pat = Patient.objects.get(case=id)
	# med = prescription.objects.filter(patientid__case = id).last()
	med = prescription.objects.get(id= pk)

	return render(request,'doc_repeat_medicine.html',{'user':"AP",'status':status,'data':id,'pat':pat,'med':med})

# Docter Prescription
@csrf_exempt
def docter_prescription(request):
	status = False
	if request.user:
		status = request.user
	user_id = User.objects.get(username=request.user)
	docter = Docter.objects.get(username=user_id)
	
	pers   = Prescription2.objects.filter(docter = docter)
	# print(len(pers))
	# for i in pers:
	# 	print(i.patient)
	return render(request , 'docter_prescription.html' , {'pers':pers, 'user' :"D" , 'status':status})


# Create Prescription 
@csrf_exempt
def create_prescription(request):
	status = False
	if request.user:
		status = request.user
	if request.method == 'POST':

		appointment = Appointment.objects.get(id=request.POST['appointment'])
		
		user_id = User.objects.get(username=request.user)
		docter = Docter.objects.get(username=user_id)
		new_prescrition = Prescription2(symptoms = request.POST['symptoms'] , prescription = request.POST['prescription'] , patient = appointment.patientid , docter = docter , appointment = appointment)
		new_prescrition.save()
		return redirect('docter_prescription')
	user_id = User.objects.get(username=request.user)
	docter = Docter.objects.get(username=user_id)
	data = Appointment.objects.filter(docterid=docter, status=0)
	

	return render(request , 'create_prescription.html',{"data":data , 'user' : "D" , 'status' : status})

# Mediacal History
@csrf_exempt
def images(request):

	status = False
	if request.user:
		status= request.user		
		patient = Patient.objects.get(usern = status)
	
	
	if request.method == 'POST':
		patient = Patient.objects.get(usern = status)
		images = request.FILES.getlist('images')

		for image in images:
			photo = ImagesUpload.objects.create(case=patient,images=image)		
						
		messages.success(request,"Successfully Uploaded the Image!")			
		return redirect('images')
	
	
	img = ImagesUpload.objects.filter(case = patient).order_by("-date")
	p = Paginator(img ,6)
	page = request.GET.get('page')
	datas = p.get_page(page)
	return render(request,"images_newone_adjust.html",{'img':img,'user' : "P" , 'status' : status,'datas':datas,"patient_details":patient})

@csrf_exempt	
def delete_images(request,id):

	obj_delete = ImagesUpload.objects.get(id=id).delete()
	return redirect('images')
	
@csrf_exempt	
def medical_history(request):
	
	status = False
	if request.user:
		status = request.user
		
		patient = Patient.objects.get(usern = status)
		# print('patient',patient.case)
		# print('ID',patient.id)

	# if request.method == "POST":
	# 	form = ImagesUploadForm(data=request.POST,files=request.FILES)
	# 	if form.is_valid():
	# 		form.save()
	# 		obj = form.instance
	# 		return render(request,"upload.html",{"obj":obj})
	# 	else:
	# 		form = ImagesUploadForm()
	# 	img =ImagesUpload.objects.all()
	# 	return render(request,"upload.html",{"img":img,"form":form})
	# if request.method == 'POST':
	# 	patient = Patient.objects.get(usern = status)
	# 	new_image = ImagesUpload(case__id = request.POST['case'],date = date.today())
	# 	new_image.save()
	# 	return redirect('medical_history')
		
	user_id = User.objects.get(username=request.user)	
	# patient = Patient.objects.get(username = user_id)
	patient = Patient.objects.get(usern = user_id)
	data = Prescription2.objects.filter(patient = patient)
	
	return render(request , 'upload.html',{"data":data , 'user' : "P" , 'status' : status,'patient':patient})


# def upload(request):
#     if request.method == "POST":
#         images = request.FILES.getlist('images')
#         for image in images:
#             MultipleImage.objects.create(images=image)
#     images = MultipleImage.objects.all()
#     return render(request, 'index.html', {'images': images})




# Upadate Status
@csrf_exempt
def update_status(request  , id):

	status = False
	if request.user:
		status = request.user
	
	if request.method == "POST":
		data  = Appointment.objects.get(id = id)
		pers = Prescription2.objects.create(appointment = data)
		pers.outstanding =  request.POST['outstanding']
		pers.paid = request.POST['paid']
		pers.total = int(request.POST['outstanding'])+int(request.POST['paid'])
		pers.save()
		data.status = 1
		data.save()
		return redirect('receptionist_dashboard' , user = "R")

	return render(request , 'update_status.html' , {'user' : "R" , "id" : id , 'status' : status})


# HR Dashboard
@csrf_exempt
def hr_dashboard(request):
	status = False
	if request.user:
		status = request.user		
		hr = HR.objects.get(username=status)
		hr_branch = hr.branch
		hr_name = hr.name
	# all_p = Patient.objects.all()
	all_p =Patient.objects.filter(branch =hr_branch)
	all_d = Docter.objects.all()
	all_r = Receptionist.objects.filter(branch = hr_branch)
	active_d = Docter.objects.filter(status = 1) 

	general = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=hr_branch))
	unsent_mail_count = str(mail_count.count())

	task_details = AssignTask.objects.filter(Q(assign_To = status) & Q(completed = False))


	return render(request , 'hr_dashboard_new_adjust.html' ,{"all_p":len(all_p) ,"all_d":len(all_d) ,"all_data" : all_d , "active_d":len(active_d) ,'user' : "H" , 'status' : status,
													"hr_branch":hr_branch,"hr_name":hr_name,'all_r':all_r,'general':count_general,'repeat': count_repeat,'courier':count_courier,
													'unsend_mail_count': unsent_mail_count,'date':date.today(),'task_count':task_details.count()})

def hr_collections(request):

	status = False
	if request.user:
		status = request.user

	hr = HR.objects.get(username=status)
	hr_branch = hr.branch

	print('hr_name',f'{hr.name} - {hr.username}')

	general = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=hr_branch))
	unsent_mail_count = str(mail_count.count())
	hr_name = f'{hr.name} - {hr.username}'
	try:
		paid_amount = Amount.objects.filter(date__date=date.today(),patient__branch=hr_branch,collected_by=hr_name)
		sum_paid = 0
		for pd in paid_amount:
			sum_paid += pd.paid_amount
	except:
		sum_paid = 0

	try:
		cash_amount = Amount.objects.filter(date__date=date.today(),patient__branch = hr_branch,collected_by=hr_name)
		sum_cash = 0
		for ca in cash_amount:
			sum_cash += ca.cash_amount

	except:
		sum_cash = 0
		
	try:
		online_amount = Amount.objects.filter(date__date=date.today(),patient__branch=hr_branch,collected_by=hr_name)
		sum_online = 0
		for ao in online_amount:
			sum_online += ao.online_amount

	except:
		sum_online = 0

	try:
		balance_amount = Balance.objects.filter(previous_deal_date=date.today(),patient__branch=hr_branch,collected_by=hr_name)
		sum_balance = 0
		sum_advance= 0 
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
		total = 0 
	balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient__branch=hr_branch,collected_by=hr_name)
	amount_names =  Amount.objects.filter(date__date = date.today(),patient__branch=hr_branch,collected_by=hr_name)

	my_list = []
	for b in balance_names:
		app_status = Appointment.objects.filter(patientid__case=b.patient.case).last()
		my_list.append(app_status)

	


	context = {
		'status':status,
		'user':'H',
		'general':count_general,
		'repeat': count_repeat,
		'courier':count_courier,
		'unsend_mail_count': unsent_mail_count,
		'date':date.today(),
		'header': f'{hr_branch} - Collections ',
		'sum_cash':sum_cash,
		'sum_online':sum_online,
		'sum_paid':sum_paid,
		'sum_balance':sum_balance,
		'total':total,
		"balance_names":balance_names,
		'amount_names':amount_names,
		'sum_advance':sum_advance,
		'appointment_status':my_list,
		'hr_name':hr_name,
		'hr_branch':hr_branch,
	}

	return render(request,'hr_collections_adjust.html',context)


	# return HttpResponse(f'Hr Collections {hr.branch} - {hr.name} - {hr.username}')

def hr_courier_list(request,branch):

	status = False
	if request.user:
		status = request.user

	hr = HR.objects.get(username=status)
	hr_branch = hr.branch

	general = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=hr_branch))
	unsent_mail_count = str(mail_count.count())

	patient_details = Patient.objects.filter(branch=branch)

	balance_due_list = []
	appointment_type = []
	for p in patient_details:
		appoint = Appointment.objects.filter(Q(patientid=p)).last()
		if appoint is not None and appoint.stat == 'Courier Medicine':
			balance_amount = Balance.objects.filter(patient=appoint.patientid).last()
			if balance_amount is not None and balance_amount.balance_amt > 0:
				balance_due_list.append(balance_amount)
				appointment_type.append(appoint)
					
	zipped_list = list(zip(balance_due_list,appointment_type))
	
	context = {
		'status':status,
		'user':'H',
		'hr_branch':branch,
		'date':date.today(),
		'general':count_general,
		'repeat': count_repeat,
		'courier':count_courier,
		'unsend_mail_count': unsent_mail_count,
		'zipped_list':zipped_list,
		
	}


	return render(request, 'hr_courier_list.html',context)

def view_courier_details(request,branch):

	status = False
	if request.user:
		status = request.user

	details = CourierDetails.objects.filter(patient__branch=branch).order_by('-date')

	context = {
		'status':status,
		'user':'D',
		'branch':branch,
		'details':details,		
		'date':date.today(),
	}

	return render(request,'view_courier_details_adjust.html',context)

def all_courier(request,branch):

	status = False
	if request.user:
		status = request.user

	try:
		hr = HR.objects.get(username=status)
		hr_branch = hr.branch
		details = CourierDetails.objects.filter(patient__branch=branch).order_by('-date')

		general = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
		count_general = str(general.count())
		repeat_medicine = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
		count_repeat = str(repeat_medicine.count())
		courier = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
		count_courier = str(courier.count())
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=hr_branch))
		unsent_mail_count = str(mail_count.count())	

	# print("details",details)
		context = {
			'status':status,
			'user':'H',
			'hr_branch':hr_branch,
			'details':details,
			'date':date.today(),
			'general':count_general,
			'repeat': count_repeat,
			'courier':count_courier,
			'unsend_mail_count': unsent_mail_count,
			
		}
	except:
		recep = Receptionist.objects.get(username=status)
		hr_branch = recep.branch
		details = CourierDetails.objects.filter(patient__branch=branch).order_by('-date')

		general = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
		count_general = str(general.count())
		repeat_medicine = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
		count_repeat = str(repeat_medicine.count())
		courier = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
		count_courier = str(courier.count())
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=hr_branch))
		unsent_mail_count = str(mail_count.count())
			

	# print("details",details)
		context = {
			'status':status,
			'user':'R',
			'hr_branch':hr_branch,
			'details':details,
			'date':date.today(),
			'general':count_general,
			'repeat': count_repeat,
			'courier':count_courier,
			'unsend_mail_count': unsent_mail_count,
			
		}

	
	return render(request,'all_courier_adjust.html',context)

def view_payment_courier(request,pk):

	data = CourierDetails.objects.get(id=pk)

	context = {
		'data':data,
		'branch':data.patient.branch
	}

	return render(request,'view_payment_courier.html',context)

@csrf_exempt
def update_payment_courier(request,pk):

	status = False
	if request.user:
		status = request.user

	try:
		hr = HR.objects.get(username=status)
		hr_name = f'{hr.name} - {hr.username}'

		data = CourierDetails.objects.get(id=pk)

		if request.method == 'POST':
			data.paid_amount = request.POST['paid_amount']
			data.transaction_id = request.POST['transaction']
			data.balance_amount -= int(request.POST['paid_amount'])
			data.collected_by = hr_name
			last_balance = Balance.objects.filter(patient=data.patient).last()
			last_amount = Amount.objects.filter(patient=data.patient).last()
			if last_amount is not None:
				last_amount.paid_amount = int(request.POST['paid_amount'])
				last_amount.transac_id = request.POST['transaction']
				last_amount.cash = False
				last_amount.online=True
				last_amount.balance_flag = True
				last_amount.online_amount = int(request.POST['paid_amount'])
				last_amount.collected_by = hr_name
				last_amount.save()


			if last_balance is not None:
				last_balance.balance_amt -= int(request.POST['paid_amount'])
				last_balance.collected_by = hr_name
				last_balance.save()
			data.save()
			messages.success(request,"Payment Updated Successfully")
			return HttpResponseRedirect(reverse('update_payment_courier', kwargs = {'pk':pk}))

		context = {
			'status':status,
			'user':'H',
			'pk':pk,
			'branch':data.patient.branch,
			'data':data,
		}
	except:
		hr = Receptionist.objects.get(username=status)
		hr_name = f'{hr.name} - {hr.username}'

		data = CourierDetails.objects.get(id=pk)

		if request.method == 'POST':
			data.paid_amount = request.POST['paid_amount']
			data.transaction_id = request.POST['transaction']
			data.balance_amount -= int(request.POST['paid_amount'])
			data.collected_by = hr_name
			last_balance = Balance.objects.filter(patient=data.patient).last()
			last_amount = Amount.objects.filter(patient=data.patient).last()
			if last_amount is not None:
				last_amount.paid_amount = int(request.POST['paid_amount'])
				last_amount.transac_id = request.POST['transaction']
				last_amount.cash = False
				last_amount.online=True
				last_amount.balance_flag = True
				last_amount.online_amount = int(request.POST['paid_amount'])
				last_amount.collected_by = hr_name
				last_amount.save()


			if last_balance is not None:
				last_balance.balance_amt -= int(request.POST['paid_amount'])
				last_balance.collected_by = hr_name
				last_balance.save()
			data.save()
			messages.success(request,"Payment Updated Successfully")
			return HttpResponseRedirect(reverse('update_payment_courier', kwargs = {'pk':pk}))

		context = {
			'status':status,
			'user':'R',
			'pk':pk,
			'branch':data.patient.branch,
			'data':data,
		}


	return render(request, 'update_courier_payment_adjust.html',context)

@csrf_exempt
def mark_receive_courier(request,pk):

	data = get_object_or_404(CourierDetails,pk=pk)
	data.receiver_flag = True
	data.save()
	return HttpResponseRedirect(reverse('all_courier',kwargs={'branch':data.patient.branch}))

@csrf_exempt
def update_receptionist(request,id):
	status = False
	if request.user:
		status = request.user

	hr = HR.objects.get(username=status)
	hr_branch = hr.branch
	if request.method == 'POST':
		update = Receptionist.objects.get(id=id)
		update.name = request.POST['name']
		update.phone = request.POST['phone']
		update.email = request.POST['email']
		update.address = request.POST['address']
		update.branch = request.POST['branch']		
		update.save()
		return redirect('hr_dashboard')
	
	general = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=hr_branch))
	unsent_mail_count = str(mail_count.count())
	
	data = Receptionist.objects.get(id=id)	
	return render(request,'update_receptionist_adjust.html',{'userdata':data,'user' : "H",'status' : status,'general':count_general,'repeat': count_repeat,'courier':count_courier,
													'unsend_mail_count': unsent_mail_count})

	# => Docter Update
@csrf_exempt	
def update_docter(request , id):
	status = False
	if request.user:
		status = request.user

	hr = HR.objects.get(username=status)
	hr_branch = hr.branch
	if request.method == "POST":
		update = Docter.objects.get(id=id)
		update.name = request.POST['name']
		update.phone = request.POST['phone']
		update.email = request.POST['email']
		update.gender = request.POST['gender']
		update.age = request.POST['age']
		update.blood = request.POST['blood']
		update.address = request.POST['address']
		update.department = request.POST['department']
		update.salary = request.POST['salary']
		update.status = request.POST['status']
		update.attendance = request.POST['attendance']
		update.save()
		messages.success(request,"Doctor's Details Updated")
		return redirect('hr_dashboard')
	data = Docter.objects.get(id= id)
	general = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = hr_branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=hr_branch))
	unsent_mail_count = str(mail_count.count())
	return render(request , 'update_docter_new_adjust.html' , {"userdata" : data , 'user' : "H" , 'status' : status,'general':count_general,'repeat': count_repeat,'courier':count_courier,
													'unsend_mail_count': unsent_mail_count})



# Docter Delete
@csrf_exempt
def delete_docter(request):
	return HttpResponse('<h2 style="color:red">You are Not authorized</h2>')

@csrf_exempt
def doc_balance(request):

	status = False
	if request.user:
		status = request.user

	query = request.GET.get('query')

	if query:
		data = Balance.objects.filter(patient__case = query.upper()).last()
	else:
		data = ""
	if data:
		status_medicine = Appointment.objects.filter(patientid = data.patient).last()
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
		unsent_mail_count = str(mail_count.count())
		

		return render(request,'doc_balance_newone.html',{'user':"D",'status':status,'data':data,'status_medicine':status_medicine,
					    'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
						'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,"unsend_mail_count":unsent_mail_count,
						'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,"header":"Balance History"})
	else:
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
		unsent_mail_count = str(mail_count.count())

		return render(request,'doc_balance_newone.html',{'user':"D",'status':status,'data':data,
					    'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
						'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,"unsend_mail_count":unsent_mail_count,
						'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,"header":"Balance History"})

	
@csrf_exempt
def hr_balance(request):

	global bal_amt
	global bal_id
	status = False
	if request.user:
		status=request.user
		# print('status',status)
		# recep = HR.objects.get(name=status)
		recep = HR.objects.get(username = status)
		# recep_branch = recep.branch
	
	query = request.GET.get('query')

	if query:
		# data = Balance.objects.filter(patient__branch=recep.branch,patient__case__icontains = query,patient__name__icontains= query).last()
		data_one =  Balance.objects.filter(patient__branch=recep.branch)
		data = data_one.filter(Q(patient__case__icontains = query) | Q(patient__name__icontains=query) |Q(patient__phone__icontains= query)).last()			
		try:
			bal_amt = data.balance_amt
			bal_id = data.id						
		except:			
			pass	
	else:
		data = ""
	if data:
		# print("True")
		status_medicine = Appointment.objects.filter(patientid = data.patient).last()
		# print('date',status_medicine.date)
		date_object = datetime.strptime(status_medicine.date, "%Y-%m-%d")
		formatted_date = date_object.strftime("%d %B %Y")
		print("formatted date",formatted_date)

		general = Appointment.objects.filter(Q(patientid__branch = recep.branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
		count_general = str(general.count())
		repeat_medicine = Appointment.objects.filter(Q(patientid__branch = recep.branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
		count_repeat = str(repeat_medicine.count())
		courier = Appointment.objects.filter(Q(patientid__branch = recep.branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
		count_courier = str(courier.count())
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) &Q(patient__branch = recep.branch))
		unsent_mail_count = str(mail_count.count())
		return render(request,'hr_balance_newone_adjust.html',{'user':"H",'status':status,'data':data,'status_medicine':status_medicine,
					   'general':count_general,'repeat': count_repeat,'courier':count_courier,'unsend_mail_count': unsent_mail_count,'formatted_date':formatted_date})
	else:
		# print("False")
		general = Appointment.objects.filter(Q(patientid__branch = recep.branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
		count_general = str(general.count())
		repeat_medicine = Appointment.objects.filter(Q(patientid__branch = recep.branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
		count_repeat = str(repeat_medicine.count())
		courier = Appointment.objects.filter(Q(patientid__branch = recep.branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
		count_courier = str(courier.count())
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch = recep.branch))
		unsent_mail_count = str(mail_count.count())
		return render(request,'hr_balance_newone_adjust.html',{'user':"H",'status':status,'data':data,'general':count_general,
					   'repeat': count_repeat,'courier':count_courier,'unsend_mail_count': unsent_mail_count})
		
@csrf_exempt	
def pay_balance(request,id):

	status = False
	if request.user:
		status = request.user
	# print('bal_id',bal_id)
	hr = HR.objects.get(username=status)
	patient = Patient.objects.get(id=id)
	# print('patient',patient.case,patient.name,patient.id)
	# obj = Balance.objects.get(id=bal_id)
	# print('obj',obj)
	save_data = Amount.objects.filter(patient_id=id).last()
	print("--- save_data_mode ---",save_data.paid_amount,save_data.cash,save_data.online,save_data.cash_amount,save_data.online_amount)
	if save_data.cash:
		print("True")
	else:
		print("False")
	# print('Amount PAID',save_data.paid_amount,type(save_data.paid_amount),type(save_data.date.strftime("%Y-%m-%d")))
	previous_paid_amt = save_data.paid_amount
	previous_paid_cash = save_data.cash_amount
	previous_paid_online = save_data.online_amount
	# print('date',date.today(),type(date.today()))
	# if save_data.date.strftime("%Y-%m-%d") == str(date.today()):
	# 	print("last amount paid today",previous_paid_amt)
	# 	print("Right")
	# else:
	# 	print("last amount paid----",previous_paid_amt)
	# 	print("wrong")
	if request.method == 'POST':
		
		if request.POST['example'] == "hide":
			
			id=id			
			amt = request.POST['email']
			amount = int(amt)			

			if save_data.date.strftime("%Y-%m-%d") == str(date.today()):
				tt_amt = amount+ previous_paid_amt
				tt_cash = amount + previous_paid_cash
			else:
				tt_amt = amount	
				tt_cash = amount		

			data = Amount.objects.filter(patient_id=id).last()
			data.patient_id = id
			data.cash =True
			data.cash_amount = tt_cash
			data.online = False
			data.paid_amount = tt_amt
			data.balance_flag = True
			data.collected_by = f'{hr.name} - {hr.username}'
			data.save()

			balance = bal_amt - amount			

			update = Balance.objects.get(id=bal_id)			
			update.patient_id = id
			update.balance_amt =balance
			update.collected_by = f'{hr.name} - {hr.username}'
			update.save()
			messages.success(request,"Rs "+ amt +"  " + "Balance Paid Successfully")			
			return HttpResponseRedirect(reverse('hr_balance'))
		else:
			id=id
			amt = request.POST['email']
			transac_id = request.POST['email1']			
			amount = int(amt)

			if save_data.date.strftime("%Y-%m-%d") == str(date.today()):
				tt_amt = amount+ previous_paid_amt
				try:
					tt_online = amount + previous_paid_online
				except:
					tt_online = amount
			else:
				tt_amt =amount	
				tt_online = amount
		
			data = Amount.objects.filter(patient_id=id).last()
			data.patient_id = id
			data.cash = False
			data.online = True
			data.online_amount = tt_online
			data.paid_amount = tt_amt
			data.transac_id =transac_id
			data.balance_flag = True
			data.collected_by = f'{hr.name} - {hr.username}'
			data.save()			

			balance = bal_amt - amount			

			update = Balance.objects.get(id=bal_id)			
			update.patient_id = id
			update.balance_amt =balance
			update.collected_by = f'{hr.name} - {hr.username}'
			update.save()
			messages.success(request,"Rs "+amt +"  "+"Balance Paid Successfully")			
			return HttpResponseRedirect(reverse('hr_balance'))
	
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) &Q(patient__branch = patient.branch))
	unsent_mail_count = str(mail_count.count())
	
	return render(request,'pay_balance_newone_adjust.html',{'status':status,'user':'H','bal_amt':bal_amt,'patient':patient,
						  'save_data.cash':save_data.cash,"unsend_mail_count":unsent_mail_count})

# HR Accounting
@csrf_exempt
def hr_accounting(request):
	status = False
	if request.user:
		status = request.user		
		# data1 = HR.objects.get(name=status)
		data1 = HR.objects.get(username = status)
		data_branch = data1.branch
	data = Appointment.objects.filter(patientid__branch = data_branch,date =date.today(),doctor_notification=True).order_by('time')
	
	query = request.GET.get('query')
	print("Query",query)
	if query:
		data = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & ( Q(patientid__case__icontains = query) | Q(patientid__phone__icontains = query) | Q(patientid__name__icontains = query))).order_by('time')
	else:
		data = Appointment.objects.filter(patientid__branch = data_branch,date=date.today(),doctor_notification=True).order_by('time')	
	p = Paginator(data ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)
	# individual = Invoice.objects.all()
	# consulation =  Prescription2.objects.all()	
	# return render(request , 'hr_accounting.html' , {'individual' : individual , 'consulation' : consulation , 'user' : 'H' , 'status' : status})

	general = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine")  & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="Courier Medicine")  & Q(doctor_notification = True)  & Q(notification_flag = False))
	count_courier = str(courier.count())

	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=data_branch))
	unsent_mail_count = str(mail_count.count())

	new_patient = Appointment.objects.filter(patientid__branch=data_branch,date=date.today(),patientid__flag=True,stat="General",doctor_notification=True).count()
	# appointment_due = Appointment.objects.filter(patientid__branch=data_branch,date=date.today(),doctor_notification=False,stat="General",patientid__flag=False).count()
	medicine_not_issued = Appointment.objects.filter(Q(patientid__branch=data_branch) &Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False) & Q(stat="General") &Q(patientid__flag=False)).count()
	medicine_issued = Appointment.objects.filter(Q(patientid__branch=data_branch) & Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True) & Q(stat="General")).count()
	



	d1 = date.today()
	print('---d1----',d1)
	return render(request , 'hr_accounting_newone_adjust.html' , {'user' : 'H' , 'status' : status,'datas':datas
						 ,'unsend_mail_count': unsent_mail_count,'general':count_general,'repeat': count_repeat,
						 'courier':count_courier,'date':d1,"new_patient":new_patient,
							"medicine_not_issued":medicine_not_issued,'medicine_issued':medicine_issued})
@csrf_exempt
def hr_repeat_medicine(request):

	status = False
	if request.user:
		status = request.user		
		# data1 = HR.objects.get(name=status)
		data1 = HR.objects.get(username = status)
		data_branch = data1.branch
	data = Appointment.objects.filter(patientid__branch = data_branch,date =date.today(),doctor_notification=True).order_by('time')
	
	query = request.GET.get('query')
	if query:
		data = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & ( Q(patientid__case__icontains = query) | Q(patientid__phone__icontains = query) | Q(patientid__name__icontains = query))).order_by('time')
	else:
		data = Appointment.objects.filter(patientid__branch = data_branch,date=date.today(),doctor_notification=True).order_by('time')	
	p = Paginator(data ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)
	# individual = Invoice.objects.all()
	# consulation =  Prescription2.objects.all()
	
	# return render(request , 'hr_accounting.html' , {'individual' : individual , 'consulation' : consulation , 'user' : 'H' , 'status' : status})
	general = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="Courier Medicine")  & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())
	d1 = date.today()
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=data_branch))
	unsent_mail_count = str(mail_count.count())

	medicine_not_issued = Appointment.objects.filter(Q(patientid__branch=data_branch) &Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False) & Q(stat="Repeat Medicine")).count()
	medicine_issued = Appointment.objects.filter(Q(patientid__branch=data_branch) & Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True) & Q(stat="Repeat Medicine")).count()
	
	
	return render(request , 'hr_repeat_medicine_newone_adjust.html' , {'user' : 'H' , 'status' : status,'datas':datas,'general':count_general,'repeat': count_repeat,
						      'courier':count_courier,'date':d1,'unsend_mail_count': unsent_mail_count,"medicine_not_issued":medicine_not_issued,"medicine_issued":medicine_issued})
@csrf_exempt
def hr_courier_medicine(request):

	status = False
	if request.user:
		status = request.user		
		# data1 = HR.objects.get(name=status)
		data1 = HR.objects.get(username = status)
		data_branch = data1.branch
	data = Appointment.objects.filter(patientid__branch = data_branch,date =date.today(),doctor_notification=True).order_by('time')
	
	query = request.GET.get('query')
	if query:
		data = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & ( Q(patientid__case__icontains = query) | Q(patientid__phone__icontains = query) | Q(patientid__name__icontains = query))).order_by('time')
	else:
		data = Appointment.objects.filter(patientid__branch = data_branch,date=date.today(),doctor_notification=True).order_by('time')	
	p = Paginator(data ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)
	# individual = Invoice.objects.all()
	# consulation =  Prescription2.objects.all()
	
	# return render(request , 'hr_accounting.html' , {'individual' : individual , 'consulation' : consulation , 'user' : 'H' , 'status' : status})
	general = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="General") & Q(notification_flag = False) & Q(doctor_notification=True))
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(notification_flag = False) & Q(doctor_notification=True))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = data_branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(notification_flag = False) & Q(doctor_notification=True))
	count_courier = str(courier.count())
	d1 = date.today()
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)& Q(patient__branch=data_branch))
	unsent_mail_count = str(mail_count.count())

	new_patient = Appointment.objects.filter(patientid__branch=data_branch,date=date.today(),patientid__flag=True,stat="Courier Medicine",doctor_notification=False).count()
	old_patient = Appointment.objects.filter(patientid__branch=data_branch,date=date.today(),patientid__flag=False,stat="Courier Medicine",doctor_notification=True).count()
	# appointment_due = Appointment.objects.filter(patientid__branch=data_branch,date=date.today(),doctor_notification=False,stat="Courier Medicine",patientid__flag=False).count()
	# medicine_not_issued = Appointment.objects.filter(Q(patientid__branch=data_branch) &Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=False) & Q(stat="Courier Medicine")).count()
	medicine_issued = Appointment.objects.filter(Q(patientid__branch=data_branch) & Q(date=date.today()) & Q(doctor_notification=True) & Q(medicine_flag=True) & Q(stat="Courier Medicine")).count()
	
	return render(request , 'hr_courier_medicine_newone_adjust.html' , {'user' : 'H' , 'status' : status,'datas':datas,'general':count_general,'repeat': count_repeat,
						       'courier':count_courier,'date':d1,'unsend_mail_count': unsent_mail_count,"new_patient":new_patient,
							"old_patient":old_patient,'medicine_issued':medicine_issued})

@csrf_exempt
def hr_send_mail(request):

	status = False
	if request.user:
		status = request.user
		hr_branch = HR.objects.get(username=status)
		print('hr_branch',type(hr_branch))
		
	data = CourierDetails.objects.filter(Q(patient__branch = str(hr_branch.branch))&Q(date=date.today()))

	query=request.GET.get('query')

	if query:
		data = CourierDetails.objects.filter(patient__case=query,date=date.today())
	p = Paginator(data ,5)
	page = request.GET.get('page')
	datas = p.get_page(page)

	general = Appointment.objects.filter(Q(patientid__branch = hr_branch.branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = hr_branch.branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = hr_branch.branch) & Q(date=date.today()) & Q(stat="Courier Medicine")  & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())

	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch.branch))
	unsent_mail_count = str(mail_count.count())
	print('notification------',unsent_mail_count)	

	return render(request , 'hr_send_mail_newone_adjust.html' , {'user' : 'H' , 'status' : status,'datas':datas,'general':count_general,'repeat': count_repeat,'courier':count_courier,
						'unsend_mail_count': unsent_mail_count})
@csrf_exempt
def hr_medicine_prescription(request,id):

	try:
		amount_paid_today = Amount.objects.filter(Q(patient=id) & Q(date__date=date.today())).first()
		print("Amount Paid",amount_paid_today.patient.name, amount_paid_today.paid_amount)
		prescription_duration = prescription.objects.filter(Q(patientid=id) & Q(date=date.today())).first()
		print("Prescription Durations",prescription_duration.durations)
	except:
		amount_paid_today = None
		prescription_duration = None
	
	global bal	
	status = False
	if request.user:
		status = request.user
	data = prescription.objects.filter(date=date.today(),patientid_id=id)
	# print('data',data)
	# print('data.first',data.first())
	data1 = data.first()
	patient = Patient.objects.get(id=id)
	patient_name = patient.name
	patient_case = patient.case
	patient_id = patient.id
	try:	
		balance = Balance.objects.filter(patient_id=id).last()
		bal = balance.balance_amt
		# print('bal----',type(bal),bal)
	except:
		bal = 0

	general = Appointment.objects.filter(Q(patientid__branch = patient.branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = patient.branch) & Q(date=date.today()) & Q(stat="Repeat Medicine")  & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = patient.branch) & Q(date=date.today()) & Q(stat="Courier Medicine")  & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())

	today = date.today()
	# print("Today",today)
	duration_new =prescription.objects.filter(patientid_id=id,date=date.today()).last()
	if duration_new:
		# print("duration_days",duration_new.durations,duration_new.durations.split(' '))		
		obj_new = duration_new.durations.split(' ')
		if obj_new[1] == "Days":
			rem_days = int(obj_new[0]) % 7
			num_days = int(obj_new[0]) - rem_days	
			# print('obj_new',obj_new[0],type(obj_new[0]))
			next_visit = today + relativedelta(days=num_days)
			# print("Update_date",next_visit,type(next_visit))
		else:
			# print('obj_new',obj_new[0],type(obj_new[0]))
			next_visit = today + relativedelta(months=int(obj_new[0]))
			# print("Update_date",next_visit,type(next_visit))

	else:
		next_visit = " "

	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=patient.branch))
	unsent_mail_count = mail_count.count()
	# print("unsend--",unsent_mail_count,type(unsent_mail_count))

	data_extra = OtherPrescription.objects.filter(patient__id=id,date=date.today())
	# print("data",data_extra)

	data2 =prescription.objects.filter(patientid__id=id,date=date.today()).first()
	# print("data2---",data2.medicine,data2.flag)
	return render(request,'hr_medicine_prescription_newone_adjust.html',{'user':'H','status':status,'data':data,'data1':data1,'name':patient_name,"data2":data2,
							'case':patient_case,'id':patient_id,'balance':str(bal),'general':count_general,"pat":patient,'data_extra':data_extra,
							'repeat': count_repeat,'courier':count_courier,"next_visit":next_visit,'unsend_mail_count': unsent_mail_count,"date":today,'amount_paid_today':amount_paid_today,'prescription_duration':prescription_duration})
@csrf_exempt
def hr_medicine_payment(request,id):

	# global total_amt
	
	global total_clearance
	status = False
	if request.user:
		status = request.user
	patient = Patient.objects.get(id=id)
	data = prescription.objects.filter(date=date.today(),patientid_id=id)
	# print('data',data.first())	
	price = Price.objects.get(id=2)
	# print('balance2',bal)
	try:	
		balance = Balance.objects.filter(patient_id=id).last()
		bal = balance.balance_amt
		# print('bal----',type(bal),bal)
	except:
		bal = 0
	

	if patient.flag:
		for d in data:
			if d.durations == "7 Days":
				total_amt = price.new_case + price.seven_days
			elif d.durations == "15 Days":
				total_amt = price.new_case + price.fifteen_days
			elif d.durations == "21 Days":
				total_amt = price.new_case + price.twentyone_days
			elif d.durations == "30 Days":
				total_amt = price.new_case + price.thirty_days
			elif d.durations == "45 Days":
				total_amt = price.new_case + price.fortyfive_days
			elif d.durations == "2 Months":
				total_amt = price.new_case + price.two_months
			elif d.durations == "3 Months":
				total_amt = price.new_case + price.three_months
	else:
		for d in data:
			if d.durations == "7 Days":
				total_amt = price.seven_days
			elif d.durations == "15 Days":
				total_amt = price.fifteen_days
			elif d.durations == "21 Days":
				total_amt = price.twentyone_days
			elif d.durations == "30 Days":
				total_amt = price.thirty_days
			elif d.durations == "45 Days":
				total_amt = price.fortyfive_days
			elif d.durations == "2 Months":
				total_amt = price.two_months
			elif d.durations == "3 Months":
				total_amt = price.three_months
	# print("Total amt",total_amt,type(total_amt))

	data_extra = OtherPrescription.objects.filter(patient__id=id,date=date.today())
	if data_extra:
		total_extra_med = 0
		for d in data_extra:
			total_extra_med += int(d.other_price)
		total_clearance = total_amt + bal + total_extra_med
		print('total',total_amt)
		x = total_amt + total_extra_med
		print('new_total--',x)
	else:
		total_extra_med = 0
		x = total_amt
		total_clearance = total_amt + bal 

	old_pat_consultation_charges = AddConsultationCharges.objects.filter(patient__id=id,date=date.today()).last()

	if old_pat_consultation_charges:
		old_consult = old_pat_consultation_charges.other_price
		total_clearance += int(old_consult)
	else:
		old_consult = 0
		total_clearance += int(old_consult)

	# print("consultaion_charges",old_pat_consultation_charges.other_price)
	print('clearance',total_clearance,type(total_clearance))
	app = Appointment.objects.filter(patientid_id=id,date=date.today()).last()
	# print("app",app.stat)
	form = CourierDetailsForm(initial = {'patient': patient,'address':patient.address,'email':patient.email})
	general = Appointment.objects.filter(Q(patientid__branch = patient.branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = patient.branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = patient.branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())

	duration_new =prescription.objects.filter(patientid_id=patient.id,date=date.today()).last()
	# print("-------",duration_new)
	today = date.today()
	# print("Today",today)
	duration_new =prescription.objects.filter(patientid_id=id,date=date.today()).last()
	if duration_new:
		obj_new = duration_new.durations.split(' ')
		if obj_new[1] == "Days":
			rem_days = int(obj_new[0]) % 7
			num_days = int(obj_new[0]) - rem_days	
			next_visit = today + relativedelta(days=num_days)
		else:
			next_visit = today + relativedelta(months=int(obj_new[0]))
	else:
		next_visit = " "

	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=patient.branch))
	unsent_mail_count = str(mail_count.count())

	if patient.flag:
		med_charges = total_amt - price.new_case
	else:
		med_charges = total_amt
	return render(request,'hr_medicine_payment_newone_adjust.html',{'user':'H','status':status ,'patient':patient,'x':x,'data_extra':data_extra,'old_consult':old_consult,
						   'id':id,'bal':bal ,'total_clearance':total_clearance,'app_stat':app.stat,'form':form,"unsend_mail_count":unsent_mail_count,"extra_med":total_extra_med,
						   'general':count_general,'repeat': count_repeat,'courier':count_courier,"next_visit":next_visit,"date":today,"med_charges":med_charges,"consult_charges":price.new_case})
@csrf_exempt
def hr_status(request,id):

	status = False
	if request.user:
		status = request.user

	hr = HR.objects.get(username=status)

	print("HR-name",hr.name,hr.username)	
	
	data = prescription.objects.filter(patientid=id,date=date.today())
	notify = Appointment.objects.filter(patientid=id,date=date.today())	
	flag1 = get_object_or_404(Patient,id=id)

	if request.method == 'POST':
		for n in notify:
			# print('before payment---------',n.notification_flag,n.medicine_flag)
			not_flag = get_object_or_404(Appointment,id=n.id)
			not_flag.notification_flag = True
			not_flag.medicine_flag = True
			# print('after_payment---------',not_flag.notification_flag,not_flag.medicine_flag)
			not_flag.save(not_flag.patientid.branch,not_flag.stat,not_flag.notification_flag,not_flag.medicine_flag)	

		for d in data:
			new_flag = get_object_or_404(prescription,id=d.id)
			new_flag.flag = False
			new_flag.save(update_fields=['flag'])
		flag1.flag = False			
		flag1.save(update_fields=['flag'])		
		if request.POST['example'] == "hide":
			id = id
			cash = request.POST['example']			
			amt = request.POST['Email']			
			try:
				courier = request.POST['courier_amount']	
				total = total_clearance + int(courier)				
			except:
				courier = 0
				total = total_clearance + int(courier)
		
			balance = total - int(amt)
			# balance = total_clearance - int(amt)
			amount = int(amt)
			new = Amount.objects.create(patient_id=id,cash=True,paid_amount=amount,cash_amount=amount,online_amount=0,transac_id= "_",collected_by= f'{hr.name} - {hr.username}')
			new.save()
			new_balance = Balance.objects.create(patient_id=id,balance_amt=balance,collected_by= f'{hr.name} - {hr.username}')
			new_balance.save()
			try:
				courier_amount = request.POST['courier_amount']			
				address = request.POST['address']			
				email = request.POST['email']			
				courier = CourierDetails.objects.create(patient_id=id,courier_amount=courier_amount,address=address,email=email,balance_amount=balance)
				courier.save()
			except:
				pass
		else:
			id =id 			
			amt = request.POST['Email']
			transac_id = request.POST['Email1']
			try:
				courier = request.POST['courier_amount']
				# print('courier',courier,type(courier))
				# print('total_clearqance',total_clearance)
				total = total_clearance + int(courier)
				# print("total",total)
			except:
				courier = 0
				total = total_clearance + int(courier)
			
			balance = total - int(amt)
			amount = int(amt)
			new = Amount.objects.create(patient_id=id,cash=False,online=True,paid_amount=amount,transac_id=transac_id,online_amount=amount,cash_amount=0,collected_by= f'{hr.name} - {hr.username}')
			new.save()
			new_balance = Balance.objects.create(patient_id=id,balance_amt = balance,collected_by= f'{hr.name} - {hr.username}')
			new_balance.save()
			try:
				courier_amount = request.POST['courier_amount']			
				address = request.POST['address']			
				email = request.POST['email']			
				courier = CourierDetails.objects.create(patient_id=id,courier_amount=courier_amount,address=address,email=email,balance_amount=balance)
				courier.save()
			except:
				pass	
	messages.success(request,"Payment Success")
	return HttpResponseRedirect(reverse('hr_medicine_prescription',  kwargs={'id': id}))

def payment_cancellation(request,id):

	print("id",id)

	pres = prescription.objects.filter(patientid=id,date=date.today())
	appoint = Appointment.objects.filter(patientid=id,date=date.today()).last()
	appoint.notification_flag = False
	appoint.medicine_flag = False
	appoint.save()
	for p in pres:
		chng_flag = get_object_or_404(prescription,id=p.id)
		chng_flag.flag= True
		chng_flag.save()
		

	balance = Balance.objects.filter(patient_id=id,previous_deal_date=date.today()).last()

	print("BALANCE--",balance.balance_amt)
	balance.delete()

	amount = Amount.objects.filter(patient_id=id,date__date=date.today()).last()
	print("AMOUNT PAID-----",amount.paid_amount)
	amount.delete()
	try:
		courier_details = CourierDetails.objects.filter(patient_id=id,date=date.today()).last()
		courier_details.delete()
	except:
		pass

	pre_url = request.META.get('HTTP_REFERER')
	obj =pre_url.split('/')
	# print('obj--',obj,obj[3])
	if obj[3] == 'mulund_collection':
		return redirect('mulund_collection')
	else:
		return redirect('dombivali_collection')



	

	

# Patient invoice

@csrf_exempt 
def patient_invoice(request):
	status = False
	if request.user:
		status = request.user
	user_id =  User.objects.get(username = request.user)
	p = Patient.objects.get(username = user_id)
	data = Prescription2.objects.filter(patient = p)
	return render(request , 'patient_invoice.html' , {'data':data , 'user' : 'P' , 'status' : status})




# About
# @csrf_exempt 
def about(request):
	status = False
	if request.user:
		status = request.user
	return render(request , 'about.html' )




#  Invoice Generator
@csrf_exempt
def get_pdf(request , id):
	data = Prescription2.objects.get(id=id)
	pdf_data = {'data':data}
	template = get_template('invoice.html')
	data_p = template.render(pdf_data)
	response = BytesIO()
	pdf_page = pisa.pisaDocument(BytesIO(data_p.encode('UTF_8')),response)
	if not pdf_page.err:
		return HttpResponse(response.getvalue(),content_type = 'application/pdf')
	else:
		return HttpResponse('Error')




# Send Reminder
@csrf_exempt
def send_reminder(request,id):
	p = Prescription2.objects.get(id=id)
	email = p.patient.email
	subject = 'Payment Reminder '
	message = 'Your Due Amount is {} outstanding and {} rs. you have already paid'.format(p.outstanding,p.paid)
	recepient = [email]
	send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = False)
	return redirect('hr_accounting')


#def patientDetail(request):
#	return render(request,'patientdetails.html' )

#   ckeditor section

from .forms import ArticleForm
from .models import Article

@csrf_exempt
def patientDetail(request):
    article = Article.objects.all()

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patientdetails.html')
    else:
        form = ArticleForm()

    return render(request, 'patientdetails.html', {'article': article, 'form': form})

# quotation
@csrf_exempt 
def quotation(request):
	status = False
	if request.user:
		status = request.user
		
	if request.method =='POST' :
		form = QuoteForm(request.POST)
		if form.is_valid():
			new_todo = Quote(test=request.POST['test'],cause=request.POST['cause'])
			new_todo.save()

		return redirect('quote')
	
	query = request.GET.get("q")
	if query :
		quote = Quote.objects.filter(Q(test=query) | Q(cause=query))
		# print(quote)
	else :
		quote = Quote.objects.all().order_by('test')
	form = QuoteForm()
	context = {'form':form,'quote':quote,'status':status,'user':"D"} 
	return render(request, 'quote_new.html', context)

@csrf_exempt
def my_sign(request):
	if request.method == 'POST' :
		form = SignatureForm(request.POST or None)
		if form.is_valid():
			signature = form.cleaned_data.get('signature')
			if signature:
				# as an image
				signature_picture = draw_signature(signature)
				s=JSignatureModel(name=request.POST['name'],signature=signature_picture)
				s.save()
		return redirect('mysign')
	query = sign.objects.all()
	form = SignatureForm()
	context = { 'query':query ,'form':form}
	return render (request , 'sign.html',context)
		
def appontment(request):
	return render(request,'appointment.html')

def ordermedi1cine(request):
	return render(request,'order.html')

#Organs
def Gnm_Sbs_Conflicts(request):

	status = False
	if request.user:
		status = request.user

	if request.method =='POST' :
		form = Gnm_SbsForm(request.POST)
		if form.is_valid():
			new_todo = Gnm_Sbs(Organs=request.POST['organs'],Conflicts=request.POST['conflicts'])
			new_todo.save()

		return redirect('Gnm_Sbs_Conflicts')
	
	querydata = request.GET.get("q")
	if querydata :
		quotedata = Gnm_Sbs.objects.filter(Q(Organs__icontains=querydata) & Q(Conflicts__icontains=querydata))
	else :
		quotedata = Gnm_Sbs.objects.all().order_by('Organs')
	form = Gnm_SbsForm()
	context = {'form':form,'quote':quotedata,'status':status,'user':"D"} 
	return render(request, 'orgns_conflicts_new.html', context)



def delete_organs(request , id):
	data = Gnm_Sbs.objects.get(pk=id)
	data.delete()
	return redirect('Gnm_Sbs_Conflicts')


def delete_quote(request , id):
	data=Quote.objects.get(pk=id)
	data.delete()
	return redirect('quote')

@csrf_exempt
def doc_repeat_med_details(request,user):
	
	status = False
	if request.user:
		status = request.user
	
	data = Appointment.objects.filter(date=date.today()).order_by('time')
	
	query = request.GET.get('query')	
	if query:
		data = Appointment.objects.filter(date=date.today(),patientid__case= query).order_by('time')
		
	p = Paginator(data ,5)
	page = request.GET.get('page')
	datas = p.get_page(page)


	return render(request,'doc_repeat_med.html',{'user':user,'status':status,'datas':datas})

@csrf_exempt
def repeat_med_details(request,user):
	status = False
	if request.user:
		status = request.user
		try:
			recep = Receptionist.objects.get(username = status)
			row_one = Appointment.objects.filter(patientid__branch = recep.branch,date=date.today(),stat="Repeat Medicine")
			last_patients = Patient.objects.filter(branch =recep.branch).order_by('-pk')[0:15]
		except:
			row_one = Appointment.objects.filter(date=date.today())
			last_patients = Patient.objects.all().order_by('-pk')[0:15]
	
	
	row = Appointment.objects.all()
	status_done = len(Appointment.objects.filter(status = 1))
	status_pending = len(row) - status_done
	# last_patients = Patient.objects.all().order_by('-pk')[0:15]
	# last_patients = Patient.objects.filter(branch =recep.branch).order_by('-pk')[0:15]
	
	query=request.GET.get('query')
	
	if query:
		# row_one = Appointment.objects.filter(Q(patientid__case=query.upper()))
		row_one = Appointment.objects.filter(Q(patientid__case__icontains=query.upper())|Q(patientid__phone__icontains=query)|Q(patientid__name__icontains=query)|Q(patientid__email__icontains=query) ,date=date.today())
		last_patients = Patient.objects.filter(Q(phone=query)|Q(email=query)|Q(name=query))
		# appointment_list=Appointment.objects.filter(patientid__icontains=query)
		# print(appointment_list)
		# return render(request , 'repeat_med_details.html' , {'user':user, "status": status , "Total" : len(row) ,
		# 													"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients})
	p = Paginator(row_one ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)
	# datas = p.get_page(page)
	d1 = date.today()
	return render(request , 'repeat_med_details_new_adjust.html' , {'user':user, "status": status , "Total" : len(row) ,
															"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients,'datas':datas,'date':d1})

@csrf_exempt
def send_mail(request,id):


	pre_url = request.META.get('HTTP_REFERER')
	print('pre_url-----',pre_url,type(pre_url))
	
	obj =pre_url.split('/')
	
	# print('obj--',obj[3])	
	# print('id',id)
	courier = CourierDetails.objects.get(id=id)
	# print('courier-----',courier.patient)

	duration_new = prescription.objects.filter(patientid=courier.patient).last()
	# print("duration",duration_new,duration_new.durations)
	
	if duration_new:			
		obj_new = duration_new.durations.split(' ')
		if obj_new[1] == "Days":
			rem_days = int(obj_new[0]) % 7
			num_days = int(obj_new[0]) - rem_days			
			next_visit = duration_new.date + relativedelta(days=num_days)
			
		else:			
			next_visit = duration_new.date + relativedelta(months=int(obj_new[0]))

	else:
		next_visit = " "

	bal = Balance.objects.filter(patient = courier.patient).last()
	# print('bal',bal,bal.patient,bal.balance_amt)

	patient = Patient.objects.get(id=courier.patient.id)
	print("patient_flag",patient.flag)

	data = prescription.objects.filter(date=date.today(),patientid_id=courier.patient.id)
	price = Price.objects.get(id=2)
	print("data",data)
	for d in data:
		print('----',d.durations)

	appoint_pat = Appointment.objects.filter(Q(date=date.today()) & Q(patientid_id=courier.patient.id)).last()
	print("app_patient",appoint_pat.patient_new_old)


	if appoint_pat.patient_new_old == "True":
		for d in data:
			if d.durations == "7 Days":
				total_amt = price.new_case + price.seven_days
			elif d.durations == "15 Days":
				total_amt = price.new_case + price.fifteen_days
			elif d.durations == "21 Days":
				total_amt = price.new_case + price.twentyone_days
			elif d.durations == "30 Days":
				total_amt = price.new_case + price.thirty_days
			elif d.durations == "45 Days":
				total_amt = price.new_case + price.fortyfive_days
			elif d.durations == "2 Months":
				total_amt = price.new_case + price.two_months
			elif d.durations == "3 Months":
				total_amt = price.new_case + price.three_months
	else:
		for d in data:
			if d.durations == "7 Days":
				total_amt = price.seven_days
			elif d.durations == "15 Days":
				total_amt = price.fifteen_days
			elif d.durations == "21 Days":
				total_amt = price.twentyone_days
			elif d.durations == "30 Days":
				total_amt = price.thirty_days
			elif d.durations == "45 Days":
				total_amt = price.fortyfive_days
			elif d.durations == "2 Months":
				total_amt = price.two_months
			elif d.durations == "3 Months":
				total_amt = price.three_months

	print("new",total_amt,price.new_case)    

	# In case of new patient
	# total_amt - med charges + consulatation charges

	#In case of old patient
	#total_amt - med charges


	data_extra = OtherPrescription.objects.filter(patient__id=courier.patient.id,date=date.today())
	if data_extra:
		total_extra_med = 0
		for d in data_extra:
			total_extra_med += int(d.other_price)		
		# x = total_amt + other prescription
		x = total_amt + total_extra_med
		print('new_total--',x)
	else:
		total_extra_med = 0
				#x = total_amt
		x = total_amt
	# Now x has total_amt for both case old and new patient

	if appoint_pat.patient_new_old == "True":
		extra_medicine = total_extra_med
		bill_today = x + courier.courier_amount 
		med_charges = total_amt - price.new_case
		print("bal.balance_amt",bal.balance_amt)
		prev_balance = bal.balance_amt - bill_today		
		template = render_to_string('email_template.html',{'courier':courier,"bill_today":bill_today,'total_amount':bal.balance_amt,"next_visit":next_visit,"med_charges":med_charges,
						     "consult_price":price.new_case,"new_flag":appoint_pat.patient_new_old,'balance':prev_balance,'extra_medicine':extra_medicine})
	
	else:
		extra_medicine = total_extra_med
		bill_today = x + courier.courier_amount		
		print("balance", bal.balance_amt)
		prev_balance = bal.balance_amt - bill_today
		# balance = bal.balance_amt - (total_amt + courier.courier_amount)		
		template = render_to_string('email_template.html',{'courier':courier,"bill_today":bill_today,'total_amount':bal.balance_amt,"next_visit":next_visit,
						     "med_charges":total_amt,"new_flag":appoint_pat.patient_new_old,'balance':prev_balance,'extra_medicine':extra_medicine})
	
	
	email_id = courier.email
	mylist = []
	mylist.append(email_id)	

	email = EmailMessage(
		'Courier Details',
		template,
		settings.EMAIL_HOST_USER,
		mylist
	)
	email.fail_silently = True
	email.send()

	flag = get_object_or_404(CourierDetails,id=id)
	flag.email_flag = True
	flag.save(update_fields=['email_flag'])
	if obj[3] == 'doc_courier_mail':
		return HttpResponseRedirect(reverse('doc_courier_medicicne'))
	else:
		return HttpResponseRedirect(reverse('hr_send_mail'))


def send_mail_courier(request,id):

	courier = CourierDetails.objects.get(id=id)

	pat_id = courier.patient

	duration_new = prescription.objects.filter(patientid=courier.patient).last()

	if duration_new:			
		obj_new = duration_new.durations.split(' ')
		if obj_new[1] == "Days":
			rem_days = int(obj_new[0]) % 7
			num_days = int(obj_new[0]) - rem_days			
			next_visit = duration_new.date + relativedelta(days=num_days)
			
		else:			
			next_visit = duration_new.date + relativedelta(months=int(obj_new[0]))

	else:
		next_visit = " "

	balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient=pat_id).last()
	amount_names = Amount.objects.filter(date__date = date.today(),patient=pat_id).last()
	

	if balance_names.balance_amt < 0:
		advance = abs(balance_names.balance_amt)
	else:
		advance = 0
	
	

	context = {
		'courier':courier,
		'next_visit':next_visit,
		'paid':amount_names.paid_amount,
		'balance':balance_names.balance_amt,
		'advance':advance,
	}

	template = render_to_string('send_mail_courier.html',context)
	email_id = courier.email
	mylist = []
	mylist.append(email_id)
	email = EmailMessage(
		'Wings Classical Homeopathy - Courier Details',
		template,
		settings.EMAIL_HOST_USER,
		mylist
	)
	email.fail_silently = True
	email.send()
	flag = get_object_or_404(CourierDetails,id=id)
	flag.email_flag = True
	flag.save(update_fields=['email_flag'])

	pre_url = request.META.get('HTTP_REFERER')
	obj =pre_url.split('/')
	if obj[3] == 'doc_courier_mail':
		return HttpResponseRedirect(reverse('doc_courier_medicicne'))
	else:
		return HttpResponseRedirect(reverse('hr_send_mail'))




def send_mail_general_repeat(request,id):

	gen = Appointment.objects.get(id=id)

	pat_id = gen.patientid

	duration_new = prescription.objects.filter(patientid=gen.patientid).last()

	if duration_new:			
		obj_new = duration_new.durations.split(' ')
		if obj_new[1] == "Days":
			rem_days = int(obj_new[0]) % 7
			num_days = int(obj_new[0]) - rem_days			
			next_visit = duration_new.date + relativedelta(days=num_days)
			
		else:			
			next_visit = duration_new.date + relativedelta(months=int(obj_new[0]))

	else:
		next_visit = " "

	
	balance_names = Balance.objects.filter(previous_deal_date=date.today(),patient=pat_id).last()
	amount_names = Amount.objects.filter(date__date = date.today(),patient=pat_id).last()
	

	if balance_names.balance_amt < 0:
		print("adv",balance_names.balance_amt)		
		advance = abs(balance_names.balance_amt)
	else:
		advance = 0

	context = {
		'appoint':gen,
		'today':date.today(),
		'next_visit':next_visit,
		'paid':amount_names.paid_amount,
		'balance':balance_names.balance_amt,
		'advance':advance,
	}

	template = render_to_string('send_mail_general_repeat.html',context)
	email_id =gen.patientid.email
	mylist = []
	mylist.append(email_id)
	email = EmailMessage(
		'Wings Classical Homeopathy- Bill Details',
		template,
		settings.EMAIL_HOST_USER,
		mylist
	)
	email.fail_silently = True
	email.send()

	flag = get_object_or_404(Appointment,id=id)
	flag.email_flag = True
	flag.save(update_fields=['email_flag'])

	pre_url = request.META.get('HTTP_REFERER')
	print('pre_url-----new',pre_url,type(pre_url))
	
	obj =pre_url.split('/')
	print(obj)
	if obj[3] == 'docter_appointment' and obj[4] == 'Dombivali':
		return HttpResponseRedirect(reverse('docter_appointment_dombivali'))
	elif obj[3] == 'docter_appointment' and obj[4] == 'Mulund':
		return HttpResponseRedirect(reverse('docter_appointment_mulund'))
	elif obj[3] == 'doc_repeat_medicine' and obj[4] == 'Dombivili':
		return HttpResponseRedirect(reverse('doc_repeat_med_dom'))
	elif obj[3] == 'doc_repeat_medicine' and obj[4] == 'Mulund':	
		return HttpResponseRedirect(reverse('doc_repeat_med_mul'))
	elif obj[3] == 'hr_accounting':
		return HttpResponseRedirect(reverse('hr_accounting'))
	elif obj[3] == 'hr_repeat_medicine':
		return HttpResponseRedirect(reverse('hr_repeat_medicine'))



	# return render(request, 'send_mail_general_repeat.html',context)

	
@csrf_exempt
def general_med_mail(request,id):

	gen = Appointment.objects.get(id=id)

	# print("Email",gen.patientid.email)

	#NEXT VISIT QUERY
	duration_new = prescription.objects.filter(patientid=gen.patientid).last()

	# print("duration",duration_new.durations)
	
	if duration_new:			
		obj_new = duration_new.durations.split(' ')
		if obj_new[1] == "Days":
			rem_days = int(obj_new[0]) % 7
			num_days = int(obj_new[0]) - rem_days			
			next_visit = duration_new.date + relativedelta(days=num_days)
			
		else:			
			next_visit = duration_new.date + relativedelta(months=int(obj_new[0]))

	else:
		next_visit = " "

	# END NEXT VISIT

	#MEDICINE CHARGES QUERY
	data = prescription.objects.filter(date=date.today(),patientid_id=gen.patientid)
	price = Price.objects.get(id=2)
	for d in data:
		duration = d.durations

	# print("patient_flag",gen.patient_new_old)



	if gen.patient_new_old == "True":
		for d in data:
			if d.durations == "7 Days":
				total_amt = price.new_case + price.seven_days
			elif d.durations == "15 Days":
				total_amt = price.new_case + price.fifteen_days
			elif d.durations == "21 Days":
				total_amt = price.new_case + price.twentyone_days
			elif d.durations == "30 Days":
				total_amt = price.new_case + price.thirty_days
			elif d.durations == "45 Days":
				total_amt = price.new_case + price.fortyfive_days
			elif d.durations == "2 Months":
				total_amt = price.new_case + price.two_months
			elif d.durations == "3 Months":
				total_amt = price.new_case + price.three_months
	else:
		for d in data:
			if d.durations == "7 Days":
				total_amt = price.seven_days
			elif d.durations == "15 Days":
				total_amt = price.fifteen_days
			elif d.durations == "21 Days":
				total_amt = price.twentyone_days
			elif d.durations == "30 Days":
				total_amt = price.thirty_days
			elif d.durations == "45 Days":
				total_amt = price.fortyfive_days
			elif d.durations == "2 Months":
				total_amt = price.two_months
			elif d.durations == "3 Months":
				total_amt = price.three_months

	# could include both med + consultaion
	# print("new",total_amt,price.new_case)

	data_extra = OtherPrescription.objects.filter(patient__id=gen.patientid.id,date=date.today())
	if data_extra:
		total_extra_med = 0
		for d in data_extra:
			total_extra_med += int(d.other_price)		
		# x = total_amt + other prescription
		bill_today = total_amt + total_extra_med
		# print('new_total--',x)
	else:
		total_extra_med = 0
				#x = total_amt
		bill_today = total_amt


	if gen.patient_new_old == "True":
		med_charges = total_amt - price.new_case
		previous_bal = 0
		balance = Balance.objects.filter(patient =gen.patientid).last()

	else:
		med_charges = total_amt
		balance = Balance.objects.filter(patient =gen.patientid).last()
		# print("balance",balance.balance_amt)
		prev_balance_query = Balance.objects.filter(patient =gen.patientid).order_by('-id')[:2]
		previous_bal = prev_balance_query[1].balance_amt		

	paid_amount = Amount.objects.filter(patient__id = gen.patientid.id).last()
	# print("Paid amount",paid_amount.paid_amount)

	print('other',total_extra_med,type(total_extra_med))
	context = {"gen":gen,
	    		"next_visit":next_visit,
				"today":date.today(),
				"duration":duration,
				"other_medicine":total_extra_med,
				"bill_today": bill_today,
				"med_charges":med_charges,
				"amount_paid_today":paid_amount.paid_amount,
				"previous_balance":previous_bal,
				"new_balance" : balance.balance_amt,
				"consultation_charges":price.new_case,
				
				}
	template = render_to_string('general_med_mail.html',context)
	email_id = gen.patientid.email
	mylist = []
	mylist.append(email_id)
	email = EmailMessage(
		'Wings Classical Homeopathy- Bill Details',
		template,
		settings.EMAIL_HOST_USER,
		mylist
	)
	email.fail_silently = True
	email.send()

	flag = get_object_or_404(Appointment,id=id)
	flag.email_flag = True
	flag.save(update_fields=['email_flag'])

	pre_url = request.META.get('HTTP_REFERER')
	print('pre_url-----new',pre_url,type(pre_url))
	
	obj =pre_url.split('/')
	print(obj)
	if obj[3] == 'docter_appointment' and obj[4] == 'Dombivali':
		return HttpResponseRedirect(reverse('docter_appointment_dombivali'))
	elif obj[3] == 'docter_appointment' and obj[4] == 'Mulund':
		return HttpResponseRedirect(reverse('docter_appointment_mulund'))
	elif obj[3] == 'doc_repeat_medicine' and obj[4] == 'Dombivili':
		return HttpResponseRedirect(reverse('doc_repeat_med_dom'))
	elif obj[3] == 'doc_repeat_medicine' and obj[4] == 'Mulund':	
		return HttpResponseRedirect(reverse('doc_repeat_med_mul'))
	elif obj[3] == 'hr_accounting':
		return HttpResponseRedirect(reverse('hr_accounting'))
	elif obj[3] == 'hr_repeat_medicine':
		return HttpResponseRedirect(reverse('hr_repeat_medicine'))
	

	

@csrf_exempt	
def send_mail_hr(request,id):

	print('id',id)
	courier = CourierDetails.objects.get(id=id)
	print('courier',courier.patient)

	bal = Balance.objects.filter(patient = courier.patient).last()
	print('bal',bal,bal.patient,bal.balance_amt)
	
	template = render_to_string('email_template.html',{'courier':courier,'total_amount':bal.balance_amt})
	email_id = courier.email
	mylist = []
	mylist.append(email_id)	

	email = EmailMessage(
		'Courier Details',
		template,
		settings.EMAIL_HOST_USER,
		mylist
	)
	email.fail_silently = True
	email.send()

	flag = get_object_or_404(CourierDetails,id=id)
	flag.email_flag = True
	flag.save(update_fields=['email_flag'])
	return HttpResponseRedirect(reverse('hr_send_mail'))

@csrf_exempt
def doc_courier_medicine(request):	

	status = False
	if request.user:
		status = request.user
		
	
	data = CourierDetails.objects.filter(date=date.today())	
	query=request.GET.get('query')
	
	if query:
		data = CourierDetails.objects.filter(patient__case=query,date=date.today())
	p = Paginator(data ,10)
	page = request.GET.get('page')
	datas = p.get_page(page)
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
	print('notification------',unsent_mail_count)
	
	return render(request,'doc_courier_medicine_newone_adjust.html',{'user':'D','status':status,'datas':datas,
						    'count_general_dom':count_general_dom,'count_general_mul':count_general_mul,
							'count_repeat_dom':count_repeat_dom,'count_repeat_mul':count_repeat_mul,
							'count_courier_dom':count_courier_dom,'count_courier_mul':count_courier_mul,
							'unsend_mail_count': unsent_mail_count,"header":"E-mail Courier Medicine Details"})

@csrf_exempt
def courier_medicine(request,user):
	status = False
	if request.user:
		status = request.user
		try:
			recep = Receptionist.objects.get(username = status)
			row_one = Appointment.objects.filter(patientid__branch = recep.branch,date=date.today(),stat="Courier Medicine")
			last_patients = Patient.objects.filter(branch = recep.branch).order_by('-pk')[0:15]
		except:
			row_one = Appointment.objects.filter(date=date.today())
			last_patients = Patient.objects.all().order_by('-pk')[0:15]
		
	row = Appointment.objects.all()
	status_done = len(Appointment.objects.filter(status = 1))
	status_pending = len(row) - status_done
	# last_patients = Patient.objects.all().order_by('-pk')[0:15]
	# last_patients = Patient.objects.filter(branch = recep.branch).order_by('-pk')[0:15]
	
	query=request.GET.get('query')
	
	if query:
		row_one = Appointment.objects.filter(Q(patientid__case__icontains=query.upper())|Q(patientid__phone__icontains=query)|Q(patientid__name__icontains=query)|Q(patientid__email__icontains=query) ,date=date.today())

		last_patients =  Patient.objects.filter(Q(phone=query)|Q(email=query)|Q(name=query))
		# appointment_list=Appointment.objects.filter(patientid__icontains=query)
	
		# return render(request , 'courier_medicine.html' , {'user':user, "status": status , "Total" : len(row) ,
		# 													"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients })
	p = Paginator(row_one ,3)
	# p = Paginator(last_patients ,3)
	page = request.GET.get('page')
	row_ones = p.get_page(page)
	d1= date.today()
	return render(request , 'courier_medicine_new_adjust.html' , {'user':user, "status": status , "Total" : len(row) ,
															"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients,'row_one':row_ones,
															'date': d1})

@csrf_exempt
def online_consultation(request,user):
	status = False
	if request.user:
		status = request.user
		try:
			recep = Receptionist.objects.get(username = status)
			last_patients = Patient.objects.filter(branch = recep.branch).order_by('-pk')[0:15]
		except:
			last_patients = Patient.objects.all().order_by('-pk')[0:15]
		
	row = Appointment.objects.all()
	status_done = len(Appointment.objects.filter(status = 1))
	status_pending = len(row) - status_done
	# last_patients = Patient.objects.all().order_by('-pk')[0:15]
	# last_patients = Patient.objects.filter(branch = recep.branch).order_by('-pk')[0:15]
	
	query=request.GET.get('query')
	if query:
		last_patients =  Patient.objects.filter(Q(phone=query)|Q(email=query)|Q(name=query))
		# appointment_list=Appointment.objects.filter(patientid__icontains=query)
		# print(appointment_list)
		# return render(request , 'online_consultation.html' , {'user':user, "status": status , "Total" : len(row) ,
		# 													"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients})
	p = Paginator(last_patients ,3)
	page = request.GET.get('page')
	datas = p.get_page(page)
	return render(request , 'online_consultation.html' , {'user':user, "status": status , "Total" : len(row) ,
															"Done" : status_done , "Pending" : status_pending , 'all_data' : row ,  'last_patients' : last_patients,'datas':datas})


@csrf_exempt
def old_prescription(request,user):
	status = False
	if request.user:
		status = request.user
	recep =  Receptionist.objects.get(username = status)
	# recep_branch = recep.branch
	# rcp=recep_branch
	if request.method == 'POST':
		form = PrescriptionOldUploadForm(request.POST,request.FILES)
		files = request.FILES.getlist('images')		
		if form.is_valid():
			patient_info = str(form.cleaned_data['patient'])
			# print("Patient_info",patient_info.split('/')[0].strip())
			# first_part = patient_info.split('/')[0].strip()
			# print("first",first_part)

			# print("form",form.cleaned_data['patient'].split('/')[0])			
			obj = Patient.objects.get(case = patient_info.split('/')[0].strip())	
			print("obj",obj)		
			form.save(commit = False)			
			for i in files:				
				PrescriptionOldUpload.objects.create(patient = obj,images =i)
			messages.success(request,'Old Prescriptions Uploaded')							
			return HttpResponseRedirect(reverse('old_prescription',  kwargs={'user': user}))
		
	form = PrescriptionOldUploadForm()
	patient_names = Patient.objects.filter(branch = recep.branch)
	return render(request,'old_prescription_new_adjust.html',{'status':status,'user':user,'form':form,"patient_names":patient_names})


""""STOCK MANAGEMENT CODE """
@csrf_exempt
def add_stock_name(request):

	status = False
	if request.user:
		status = request.user

	

	form = AddStockNameForm(request.POST or None)
	if form.is_valid():
		stock_name = form.cleaned_data['name']
		obj = form.save(commit=False)
		if stock_name.title():
			obj.save()
		else:
			obj.name = stock_name.title()
			obj.save()

		messages.success(request,"Successfully added " + str(stock_name) + " to the Stock Name list")
		return redirect('add_stock_name')
	try:
		hr_branch = HR.objects.get(username = status).branch
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
	
		context = {
			'form':form,
			'status':status,
			'user':'H',
			"title":"Add New Stock Name",
			"unsend_mail_count":unsent_mail_count,
		}
	except:
		context = {
		'form':form,
		'status':status,
		'user':'R',
		"title":"Add New Stock Name",
		
	}

	return render(request,"add_stock_name.html",context)

@csrf_exempt
def add_stock(request):

	status = False
	if request.user:
		status=request.user
	
	try:
		hr_branch = HR.objects.get(username = status)
		print("Branch-----",hr_branch.branch,status)
		form = StockCreateForm(request.POST or None,request.FILES or None,initial = {'branch_name':hr_branch.branch},cat="Stock")
		if form.is_valid():
			stock = form.cleaned_data['stock_name']
			quantity = form.cleaned_data['quantity']
			unit = form.cleaned_data['stock_unit']
			form.save()
			messages.success(request, 'Added ' + str(quantity) + " " + unit + " " +str(stock) + " Successfully")
			return redirect('add_stock')
		
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch.branch))
		unsent_mail_count = mail_count.count()
		context = {
			"status":status,
			"user": 'H',
			"form": form,
			"title": "Add Stock "+ hr_branch.branch,
			"main" : "Add Stock " + hr_branch.branch,
			"unsend_mail_count":unsent_mail_count
		}
	except:
		hr_branch = Receptionist.objects.get(username=status)
		print("Branch-----",hr_branch.branch,status)

		form = StockCreateForm(request.POST or None,request.FILES or None,initial = {'branch_name':hr_branch.branch},cat="Stock")
		if form.is_valid():
			stock = form.cleaned_data['stock_name']
			quantity = form.cleaned_data['quantity']
			unit = form.cleaned_data['stock_unit']
			form.save()
			messages.success(request, 'Added ' + str(quantity) + " " + unit + " " +str(stock) + " Successfully")
			return redirect('add_stock')
		
		
		context = {
			"status":status,
			"user": 'R',
			"form": form,
			"title": "Add Stock "+ hr_branch.branch,
			"main" : "Add Stock " + hr_branch.branch,			
		}
	return render(request, "add_stock.html", context)
@csrf_exempt
def bill_view(request,pk):

	status = False
	if request.user:
		status = request.user

	image_obj = Stock.objects.filter(id=pk)
	try:
		try:
			hr_branch = HR.objects.get(username = status)
			mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch.branch))
			unsent_mail_count = mail_count.count()

			context = {
				"image_obj":image_obj,
				"pk":pk	,
				"status":status,
				"user":"H",
				"unsend_mail_count":unsent_mail_count		
			}
		except:
			branch = Receptionist.objects.get(username = status)
			context = {
				"image_obj":image_obj,
				"pk":pk	,
				"status":status,
				"user":"R",						
			}
	except:
		context = {
			"image_obj":image_obj,
			"pk":pk	,
			"status":status,
			"user":"D",
				
		}
	return render(request,"view_bill.html",context)
@csrf_exempt
def all_stock_bills(request,pk):

	status = False
	if request.user:
		status = request.user
	
	all_bill_image = BillImageStock.objects.filter(stock__id=pk)
	vendor =  BillImageStock.objects.filter(stock__id=pk).last()	
	try:
		try:
			hr_branch = HR.objects.get(username = status)
			mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch.branch))
			unsent_mail_count = mail_count.count()			
			context={
				"images":all_bill_image,
				"unsend_mail_count":unsent_mail_count,
				"status":status,
				"user":"H",
				"vendor":vendor
			}
		except:
			user = Receptionist.objects.get(username=status)
			context={
				"images":all_bill_image,
				"status":status,
				"user":"R",
				"vendor":vendor
			}
	except:
		context = {
			"images":all_bill_image,			
			"status":status,
			"user":"D",	
			"vendor":vendor			
		}

	return render(request,"all_stock_bills.html",context)
@csrf_exempt
def test_function(request):
	status = False
	if request.user:
		status = request.user

	hr_obj = HR.objects.get(username= status)

	hr_branch = hr_obj.branch

	header = 'List of Stock'
	form = StockSearchForm(request.POST or None)
	vendor_cat = VendorCategory.objects.get(category="Stock")
	queryset = Stock.objects.filter(Q(branch_name = hr_branch) & Q(vendor__vendor_category=vendor_cat.id))

	order_check = []

	for q in queryset:
		order_history = PlaceOrderStock.objects.filter(stock_order__id=q.id)

		if order_history:
			last_order = order_history.last()
			if last_order.order_received_flag:
				order_check.append(None)
			else:
				order_check.append(last_order)
		else:
			order_check.append(None)
	
	stock_list = []
	for q in queryset:
		stock_list.append(q)

	new_zipped = list(zip(stock_list,order_check))

	p = Paginator(new_zipped,6)
	page = request.GET.get('page')
	datas = p.get_page(page)

	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
	unsent_mail_count = mail_count.count()

	context = {
			"header": header,
			"queryset": queryset,
			"form": form,
			"status":status,
			"user": 'H',
			"branch": hr_branch,
			"unsend_mail_count":unsent_mail_count,			
			# "new_zipped":new_zipped,
			"datas":datas,			
	}
	if form.is_valid():
			try:		
				stock_search = StockName.objects.get(name =form.cleaned_data['stock_name'])		
				queryset = Stock.objects.filter(Q(stock_name__product_name=stock_search) & Q(branch_name=hr_branch))
				list1 = []
				orders_check_new = []
				for q in queryset:
					list1.append(q)
					order_history = PlaceOrderStock.objects.filter(stock_order__id = q.id)
					if order_history:
						last_order = order_history.last()
						if last_order.order_received_flag:
							orders_check_new.append(None)
						else:
							orders_check_new.append(last_order)
					else:
						orders_check_new.append(None)


				new_zipped = list(zip(list1,orders_check_new))
				p = Paginator(new_zipped,6)
				page = request.GET.get('page')
				datas = p.get_page(page)
			except:
				pass
			form.save(commit=False)
			context = {
			"form": form,
			"header": header,
			"queryset": queryset,
			"branch": hr_branch,
			"status":status,
			"user": 'H',
			"unsend_mail_count":unsent_mail_count,
			"datas":datas,			
		}
	return render(request, "test.html", context)	
@csrf_exempt
def list_stock(request):

	status = False
	if request.user:
		status =  request.user

	try:
		hr_obj = HR.objects.get(username = status)

		hr_branch = hr_obj.branch

		header = 'List of Stock'
		form = StockSearchForm(request.POST or None)	
		vendor_cat = VendorCategory.objects.get(category="Stock")
		queryset = Stock.objects.filter(Q(branch_name = hr_branch) & Q(vendor__vendor_category=vendor_cat.id))
		
		# To check orders paralley for the stock in stock list for Blue , Green Buttons
		orders_check = []

		for q in queryset:
			order_history = PlaceOrderStock.objects.filter(stock_order__id = q.id)
			
			if order_history:
				last_order = order_history.last()
				if last_order.order_received_flag:
					orders_check.append(None)
				else:
					orders_check.append(last_order)
			else:
				orders_check.append(None)		

		stock_list =  []
		for q in queryset:
			stock_list.append(q)
		
		new_zipped = list(zip(stock_list,orders_check))

		p = Paginator(new_zipped,6)
		page = request.GET.get('page')
		datas = p.get_page(page)
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		context = {
			"header": header,
			"queryset": queryset,
			"form": form,
			"status":status,
			"user": 'H',
			"branch": hr_branch,
			"unsend_mail_count":unsent_mail_count,			
			"new_zipped":new_zipped,
			"datas":datas,			
		}
		if form.is_valid():
			try:		
				stock_search = StockName.objects.get(name =form.cleaned_data['stock_name'])		
				queryset = Stock.objects.filter(Q(stock_name__product_name=stock_search) & Q(branch_name=hr_branch))
				list1 = []
				orders_check_new = []
				for q in queryset:
					list1.append(q)
					order_history = PlaceOrderStock.objects.filter(stock_order__id = q.id)
					if order_history:
						last_order = order_history.last()
						if last_order.order_received_flag:
							orders_check_new.append(None)
						else:
							orders_check_new.append(last_order)
					else:
						orders_check_new.append(None)


				new_zipped = zip(list1,orders_check_new)

				p = Paginator(new_zipped,6)
				page = request.GET.get('page')
				datas = p.get_page(page)
			except:
				pass
			form.save(commit=False)
			context = {
			"form": form,
			"header": header,
			"queryset": queryset,
			"branch": hr_branch,
			"status":status,
			"user": 'H',
			"unsend_mail_count":unsent_mail_count,
			"new_zipped":new_zipped,
			"datas":datas,
			
		}
	except:
		hr_obj = Receptionist.objects.get(username = status)

		hr_branch = hr_obj.branch

		header = 'List of Stock'
		form = StockSearchForm(request.POST or None)	
		vendor_cat = VendorCategory.objects.get(category="Stock")
		queryset = Stock.objects.filter(Q(branch_name = hr_branch) & Q(vendor__vendor_category=vendor_cat.id))
		orders_check = []

		for q in queryset:
			order_history = PlaceOrderStock.objects.filter(stock_order__id = q.id)
			
			if order_history:
				last_order = order_history.last()
				if last_order.order_received_flag:
					orders_check.append(None)
				else:
					orders_check.append(last_order)
			else:
				orders_check.append(None)		

		stock_list =  []
		for q in queryset:
			stock_list.append(q)

		
		new_zipped = list(zip(stock_list,orders_check))

		p = Paginator(new_zipped,6)
		page =  request.GET.get('page')
		datas=p.get_page(page)
		
		context = {
			"header": header,
			"queryset": queryset,
			"form": form,
			"status":status,
			"user": 'R',
			"branch": hr_branch,
			"new_zipped":new_zipped,
			"datas":datas,			
		}
		if form.is_valid():
			try:		
				stock_search = StockName.objects.get(name =form.cleaned_data['stock_name'])		
				queryset = Stock.objects.filter(Q(stock_name__product_name=stock_search) & Q(branch_name=hr_branch))
				list1 = []
				for q in queryset:
					list1.append(q)
					list1 = []
				orders_check_new = []
				for q in queryset:
					list1.append(q)
					order_history = PlaceOrderStock.objects.filter(stock_order__id = q.id)
					if order_history:
						last_order = order_history.last()
						if last_order.order_received_flag:
							orders_check_new.append(None)
						else:
							orders_check_new.append(last_order)
					else:
						orders_check_new.append(None)

				new_zipped = list(zip(list1,orders_check_new))
				p = Paginator(new_zipped,6)
				page =  request.GET.get('page')
				datas= p.get_page(page)
			except:
				pass
			form.save(commit=False)
			context = {
			"form": form,
			"header": header,
			"queryset": queryset,
			"branch": hr_branch,
			"status":status,
			"user": 'R',
			"new_zipped":new_zipped,
			"datas":datas,			
		}
	return render(request, "list_stock_new.html", context)

@csrf_exempt
def delete_stock(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Deleted ' + str(queryset.quantity) + " " + queryset.stock_unit + " " + str(queryset.stock_name)+' Successfully.')
		return redirect('/list-stock/')
	return render(request, 'delete_stock.html')

@csrf_exempt
def stock_management(request, pk):

	status = False
	if request.user:
		status = request.user	

	queryset = Stock.objects.get(id=pk)
	try:		
		hr_branch = HR.objects.get(username = status).branch
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		context = {		
			"queryset": queryset,
			"header": hr_branch +" Store ",
			"stock_name": queryset.stock_name.product_name.name.upper(),
			"status":status,
			"user":"H",
			"unsend_mail_count":unsent_mail_count,
		}
	except:
		hr_branch = Receptionist.objects.get(username=status).branch
		context = {		
			"queryset": queryset,
			"header": hr_branch +" Store ",
			"stock_name": queryset.stock_name.product_name.name.upper(),
			"status":status,
			"user":"R",
			
		}
	return render(request, "stock_management.html", context)

@csrf_exempt
def issue_stock(request, pk):

	status = False
	if request.user:
		status = request.user

	queryset = Stock.objects.get(id=pk)
	print(queryset.approval_flag_updtate)
	form = StockIssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.receive_quantity = 0
		instance.quantity -= instance.issue_quantity
		if instance.approval_flag_updtate:
			instance.approval_flag_updtate = False				
		messages.success(request, "Issued "+ str(queryset.issue_quantity)+ " "+ str(instance.stock_unit) + " "+ str(instance.stock_name) +" SUCCESSFULLY . " + str(instance.quantity) + " "+ str(instance.stock_unit) + " " + str(instance.stock_name) + " now left in Store")
		instance.save()
		return redirect('/stock-management/'+str(instance.id))

	try:
		user = HR.objects.get(username=status)
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=queryset.branch_name))
		unsent_mail_count = mail_count.count()		

		context = {
			"title": 'Issue ' + str(queryset.stock_name),
			"queryset": queryset,
			"form": form,
			"status":status,
			"user":"H",	
			"unsend_mail_count":unsent_mail_count	
		}
	except:
		user = Receptionist.objects.get(username=status)
		context = {
			"title": 'Issue ' + str(queryset.stock_name),
			"queryset": queryset,
			"form": form,
			"status":status,
			"user":"R",				
		}
	return render(request, "add_stock.html", context)


# Receive Stock
@csrf_exempt
def receive_stock(request, pk):

	status = False
	if request.user:
		status = request.user

	queryset = Stock.objects.get(id=pk)
	form = StockReceiveForm(request.POST or None, request.FILES or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.issue_quantity = 0
		instance.quantity += instance.receive_quantity
		if instance.approval_flag_receive:
			instance.approval_flag_receive = False
		if 'upload_stock_bill_image' in request.FILES:
			instance.upload_stock_bill_image = request.FILES['upload_stock_bill_image']

		obj = BillImageStock.objects.create(stock=queryset,stock_image= request.FILES['upload_stock_bill_image'])
		instance.save()
		messages.success(request, "Received "+  str(instance.receive_quantity) + " " + str(instance.stock_unit) + " " + str(instance.stock_name) +" SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.stock_unit) + " " + str(instance.stock_name) +" now in Store")
		return redirect('/stock-management/'+str(instance.id))
	
	try:
		user = HR.objects.get(username=status)
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=queryset.branch_name))
		unsent_mail_count = mail_count.count()		
			
		context = {
				"title": 'Receive ' + str(queryset.stock_name),
				"instance": queryset,
				"form": form,
				"status":status,
				"user":"H",	
				"unsend_mail_count":unsent_mail_count		
			}
	except:
		user = Receptionist.objects.get(username=status)
		context = {
				"title": 'Receive ' + str(queryset.stock_name),
				"instance": queryset,
				"form": form,
				"status":status,
				"user":"R",							
			}
	return render(request, "add_stock.html", context)

#  Reorder Stock
@csrf_exempt
def reorder_stock(request, pk):

	status = False
	if request.user:
		status = request.user

	queryset = Stock.objects.get(id=pk)
	form = StockReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.stock_name) + " is updated to " + str(instance.reorder_level))
		return redirect("/list-stock/")
	
	try:
		user = HR.objects.get(username=status)
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=queryset.branch_name))
		unsent_mail_count = mail_count.count()
		context = {
				"instance": queryset,
				"form": form,
				"title": "Set Reorder Level for  " + str(queryset.stock_name),
				"status":status,
				"user":"H",
				"unsend_mail_count":unsent_mail_count
			}
	except:
		context = {
			"instance": queryset,
			"form": form,
			"title": "Set Reorder Level for  " + str(queryset.stock_name),
			"status":status,
			"user":"R",			
		}
	return render(request, "add_stock.html", context)



# ON DOCTORS DASHBOARD
@csrf_exempt
def list_approval(request,branch):

	print("Branch",branch)
	status = False
	if request.user:
		status = request.user
	
	header = 'Approval of Items'
	form = StockSearchForm(request.POST or None)	
	# queryset = Stock.objects.filter(branch_name = branch)
	vendor_cat = VendorCategory.objects.get(category="Stock")
	queryset = Stock.objects.filter(Q(branch_name = branch) & Q(vendor__vendor_category=vendor_cat.id))
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
	unsent_mail_count = mail_count.count()
	

	context = {
		"header": header,
		"queryset": queryset,
		"form": form,
		"status":status,
		"user":"D",
		"branch":branch,
		'unsend_mail_count': unsent_mail_count,
	}

	if form.is_valid():	

		try:
			stock_search = StockName.objects.get(name =form.cleaned_data['stock_name'])	
			queryset = Stock.objects.filter(Q(stock_name__product_name=stock_search) & Q(branch_name=branch))	
		except:
			pass
		# queryset = Stock.objects.filter(Q(stock_name__product_name=stock_search) & Q(branch_name=branch))
		form.save(commit=False)	
		context = {
		"form": form,
		"header": header,
		"queryset": queryset,
		"status":status,
		"user":"D",
		"branch":branch,
		'unsend_mail_count': unsent_mail_count,
	}
	return render(request, "list_approval.html", context)

@csrf_exempt
def approve_new_stock(request,pk):
	
	data = Stock.objects.get(id=pk)
	# print(data.approval_flag_new)

	if data.approval_flag_new:
		data.approval_flag_new = False
		data.save()
	return redirect('/list-approval/'+data.branch_name)
@csrf_exempt
def approve_issue_stock(request,pk):
	
	data = Stock.objects.get(id=pk)
	
	if data.approval_flag_updtate == False:
		data.approval_flag_updtate = True
		data.save()
	return redirect('/list-approval/'+data.branch_name)
@csrf_exempt
def approve_receive_stock(request,pk):
	
	data = Stock.objects.get(id=pk)
	
	if data.approval_flag_receive == False:
		data.approval_flag_receive = True
		data.save()
	return redirect('/list-approval/'+data.branch_name)


""""MEDICINE STOCK MANAGEMENT CODE"""

# ADD NEW MEDICINE NAME
@csrf_exempt
def add_medicine_name_hr(request):

	status = False
	if request.user:
		status = request.user

	

	form = AddMedicineHRForm(request.POST or None)
	if form.is_valid():
		medicine_name = form.cleaned_data['medicine_name']
		obj = form.save(commit=False)
		if medicine_name.title():
			obj.save()
		else:
			obj.name = medicine_name.title()
			obj.save()

		messages.success(request,"Successfully added " + str(medicine_name) + " to the Medicine Name list")
		return redirect('add_medicine_name_hr')
	try:
		hr_branch = HR.objects.get(username = status).branch
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		
		context = {
			'form':form,
			'status':status,
			'user':'H',
			"title":"Add New Medicine Name",
			"unsend_mail_count":unsent_mail_count,
		}
	except:
		user = Receptionist.objects.get(username=status)
		context = {
			'form':form,
			'status':status,
			'user':'R',
			"title":"Add New Medicine Name",
			
		}


	return render(request,"add_medicine_name_hr.html",context)

#  ADD NEW POTENCY NAME
@csrf_exempt
def add_potency_name_hr(request):

	status = False
	if request.user:
		status = request.user

	

	form = AddPotencyHRForm(request.POST or None)
	if form.is_valid():
		potency_name = form.cleaned_data['potency_name']
		obj = form.save(commit=False)
		if potency_name.title():
			obj.save()
		else:
			obj.name = potency_name.title()
			obj.save()

		messages.success(request,"Successfully added " + str(potency_name) + " to the Potency list")
		return redirect('add_potency_name_hr')
	try:	
		hr_branch = HR.objects.get(username = status).branch
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		
		context = {
			'form':form,
			'status':status,
			'user':'H',
			"title":"Add New Potency",
			"unsend_mail_count":unsent_mail_count,
		}
	except:
		user = Receptionist.objects.get(username=status)
		context = {
			'form':form,
			'status':status,
			'user':'R',
			"title":"Add New Potency",
			
		}

	return render(request,"add_medicine_name_hr.html",context)

#  ADD MEDICINE ,POTENCY , QUANTITY TO STOCK OF DIFFERENT BRANCH
@csrf_exempt
def add_medicine_stock_hr(request):

	status = False
	if request.user:
		status=request.user
	
	try:
		hr_branch = HR.objects.get(username = status)

		# print("Branch",hr_branch.branch)

		form = MedicineStockListCreateForm(request.POST or None,request.FILES or None,initial = {'branch':hr_branch.branch},cat="Medicine")
		if form.is_valid():
			medicine = form.cleaned_data['medicine']
			quantity = form.cleaned_data['quantity']
			potency = form.cleaned_data['potency']
			form.save()
			messages.success(request, 'Added ' + str(quantity) + " " + str(medicine) + " " +str(potency) + " potency Successfully")
			return redirect('add_medicine_stock_hr')
		
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch.branch))
		unsent_mail_count = mail_count.count()
		context = {
			"status":status,
			"user": 'H',
			"form": form,
			"title": "Add Medicine Stock "+ hr_branch.branch,
			"main" : "Add Medicine Stock " + hr_branch.branch,
			"unsend_mail_count":unsent_mail_count
		}
	except:
			hr_branch = Receptionist.objects.get(username = status)

			# print("Branch",hr_branch.branch)

			form = MedicineStockListCreateForm(request.POST or None,request.FILES or None,initial = {'branch':hr_branch.branch},cat="Medicine")
			if form.is_valid():
				medicine = form.cleaned_data['medicine']
				quantity = form.cleaned_data['quantity']
				potency = form.cleaned_data['potency']
				form.save()
				messages.success(request, 'Added ' + str(quantity) + " " + str(medicine) + " " +str(potency) + " potency Successfully")
				return redirect('add_medicine_stock_hr')			
			
			context = {
				"status":status,
				"user": 'R',
				"form": form,
				"title": "Add Medicine Stock "+ hr_branch.branch,
				"main" : "Add Medicine Stock " + hr_branch.branch,
				
			}
	return render(request, "add_medicine_stock_hr.html", context)
@csrf_exempt
def load_medicines(request):

	vendor_id = request.GET.get('vendor_id')	
	medicine = VendorMedicine.objects.filter(vendor_id=vendor_id)
	print(medicine.values())	
	return render(request, 'medicine_dropdown_list_options.html', {'medicine': medicine})
@csrf_exempt
def med_bill_view(request,pk):

	status = False
	if request.user:
		status = request.user

	image_obj = MedicineStockList.objects.filter(id=pk)
	try:
		try:
			hr_branch = HR.objects.get(username = status)
			mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch.branch))
			unsent_mail_count = mail_count.count()

			context = {
				"image_obj":image_obj,
				"pk":pk	,
				"status":status,
				"user":"H",
				"unsend_mail_count":unsent_mail_count		
			}
		except:
			hr_branch = Receptionist.objects.get(username = status)
			

			context = {
				"image_obj":image_obj,
				"pk":pk	,
				"status":status,
				"user":"R",						
			}
	except:
		context = {
			"image_obj":image_obj,
			"pk":pk	,
			"status":status,
			"user":"D",				
		}
	return render(request,"view_bill_med.html",context)

def all_med_bills(request,pk):

	status = False
	if request.user:
		status = request.user
	
	all_bill_image = BillImageMedicine.objects.filter(medicine__id=pk)	

	vendor = BillImageMedicine.objects.filter(medicine__id=pk).last()
	print("vendor",vendor.medicine.medicine.vendor.vendor_name)
	try:
		try:
			hr_branch = HR.objects.get(username = status)
			mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch.branch))
			unsent_mail_count = mail_count.count()			
			context={
				"images":all_bill_image,
				"unsend_mail_count":unsent_mail_count,
				"status":status,
				"user":"H",
				"vendor":vendor
			}
		except:
			user = Receptionist.objects.get(username=status)
			context={
				"images":all_bill_image,
				"status":status,
				"user":"R",
				"vendor":vendor
			}
	except:
		context = {
			"images":all_bill_image,			
			"status":status,
			"user":"D",	
			"vendor":vendor			
		}

	return render(request,"all_med_bills.html",context)

#  LIST STOCK OF ADDED MEDICINE ,POTENCY, QUANTITY
@csrf_exempt
def medicine_stock_list_hr(request):

	status = False
	if request.user:
		status =  request.user

	try:
		hr_obj = HR.objects.get(username = status)

		hr_branch = hr_obj.branch
			
		header = 'Medicine Stock Enquiry ' + hr_branch
		form = MedicineStockListSearchForm(request.POST or None)	
		queryset = MedicineStockList.objects.filter(branch = hr_branch)

		# To check orders parallely for the medicine in the medicine list for blue, green buttons
		orders_check = []
		for q in queryset:
			order_history = PlaceOrderMedicineNew.objects.filter(medicine_order__id = q.id)

			if order_history:
				last_order = order_history.last()
				if last_order.order_received_flag:
					orders_check.append(None)
				else:
					orders_check.append(last_order)
			else:
				orders_check.append(None)
		
		medicine_list = []
		for q in queryset:
			medicine_list.append(q)
		
		new_zipped = list(zip(medicine_list,orders_check))

		p = Paginator(new_zipped,10)
		page = request.GET.get('page')
		datas = p.get_page(page)		

		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		context = {
			"header": header,
			"queryset": queryset,
			"form": form,
			"status":status,
			"user": 'H',
			"branch": hr_branch,
			"unsend_mail_count":unsent_mail_count,
			"new_zipped":new_zipped,
			"datas":datas,
		}
		if form.is_valid():
			try:
				print("medicine",form.cleaned_data['medicine'])	
				print("potency",form.cleaned_data['potency'])		
				medicine_search = AddMedicineHR.objects.get(medicine_name =form.cleaned_data['medicine'])
				potency_search = AddPotencyHR.objects.get(potency_name =form.cleaned_data['potency'])		
				queryset = MedicineStockList.objects.filter(Q(medicine__medicine=medicine_search) & Q(branch=hr_branch) & Q(potency__potency_name=potency_search))
				list1 = []
				orders_check_new = []
				for q in queryset:
					list1.append(q)
					order_history = PlaceOrderMedicineNew.objects.filter(medicine_order__id = q.id)
					if order_history:
						last_order = order_history.last()
						if last_order.order_received_flag:
							orders_check_new.append(None)
						else:
							orders_check_new.append(last_order)
					else:
						orders_check_new.append(None)	

				new_zipped = list(zip(list1,orders_check_new))
				p = Paginator(new_zipped,3)
				page = request.GET.get('page')
				datas = p.get_page(page)			
			except:
				pass
			form.save(commit=False)
			context = {
			"form": form,
			"header": header,
			"queryset": queryset,
			"branch": hr_branch,
			"status":status,
			"user": 'H',
			"unsend_mail_count":unsent_mail_count,
			"new_zipped":new_zipped,
			"datas":datas,
				}
	except:
		hr_obj = Receptionist.objects.get(username = status)
		hr_branch = hr_obj.branch			
		header = 'Medicine Stock Enquiry ' + hr_branch
		form = MedicineStockListSearchForm(request.POST or None)	
		queryset = MedicineStockList.objects.filter(branch = hr_branch)
		orders_check = []
		for q in queryset:
			order_history = PlaceOrderMedicineNew.objects.filter(medicine_order__id = q.id)
			if order_history:
				last_order = order_history.last()
				if last_order.order_received_flag:
					orders_check.append(None)
				else:
					orders_check.append(last_order)
			else:
				orders_check.append(None)
		
		medicine_list = []
		for q in queryset:
			medicine_list.append(q)
		
		new_zipped = list(zip(medicine_list,orders_check))
		p = Paginator(new_zipped,3)
		page =  request.GET.get('page')
		datas = p.get_page(page)

		context = {
			"header": header,
			"queryset": queryset,
			"form": form,
			"status":status,
			"user": 'R',
			"branch": hr_branch,
			"new_zipped":new_zipped,
			"datas":datas,			
		}
		if form.is_valid():	
			try:	
				medicine_search = AddMedicineHR.objects.get(medicine_name =form.cleaned_data['medicine'])
				potency_search = AddPotencyHR.objects.get(potency_name =form.cleaned_data['potency'])		
				queryset = MedicineStockList.objects.filter(Q(medicine__medicine=medicine_search) & Q(branch=hr_branch) & Q(potency__potency_name=potency_search))
				list1 = []
				orders_check_new = []
				for q in queryset:
					list1.append(q)
					order_history = PlaceOrderMedicineNew.objects.filter(medicine_order__id = q.id)
					if order_history:
						last_order = order_history.last()
						if last_order.order_received_flag:
							orders_check_new.append(None)
						else:
							orders_check_new.append(last_order)
					else:
						orders_check_new.append(None)
				new_zipped = list(zip(list1,orders_check_new))
				p = Paginator(new_zipped,3)
				page = request.GET.get('page')
				datas= p.get_page(page)						
			except:
				pass
			form.save(commit=False)
			context = {
			"form": form,
			"header": header,
			"queryset": queryset,
			"branch": hr_branch,
			"status":status,
			"user": 'R',
			"new_zipped":new_zipped,
			"datas":datas,			
		}
	return render(request, "medicine_stock_list_new.html", context)

@csrf_exempt
def add_reorder_medicine(request,pk):

	data = get_object_or_404(MedicineStockList,id=pk)
	data.order_status = True
	data.save()
	return redirect('medicine_stock_list_hr')

from django.forms import modelformset_factory
@csrf_exempt
def place_reorder_medicine_modelformset(request):

	status = False
	if request.user:
		status = request.user
	
	try:
		hr_obj = HR.objects.get(username = status)

		hr_branch = hr_obj.branch
		queryset = MedicineStockList.objects.filter(Q(branch= hr_branch) & Q(order_status = True))
		order_check = []
		for q in queryset:
			if q.quantity <= q.reorder_level:
				
				order_history = OrderMedicineItem.objects.filter(Q(vendor=q.vendor) & Q(ordered_med__medicine_order_id=q.id) & Q(ordered_med__medicine_order__branch = hr_branch))
				if order_history:
					last_order = order_history.last()
					if last_order.order_receive_flag:
						order_check.append(None)
					else:
						order_check.append(last_order)
				else:
					order_check.append(None)

		medicine_list = []
		for q in queryset:
			if q.quantity <= q.reorder_level:
				medicine_list.append(q)

		new_zipped = list(zip(medicine_list,order_check))
		count_new_zipped = len(new_zipped)

		OrderFormSet = modelformset_factory(PlaceOrderMedicineOne, form=OrderMedicineOneForm, extra=count_new_zipped)
		if request.method == 'POST':
			formset = OrderFormSet(request.POST, queryset=PlaceOrderMedicineOne.objects.none())		
			if formset.is_valid():			
				formset.save()
				messages.success(request,"Orders Placed Successfully")
				return redirect('/place-reorder-medicine-hr/')
		else:
			items_data = [
			{
				'medicine_order':item1,
				'potency':item1.potency,
				'order_quantity': 1
			}
			for item1,item2 in new_zipped	]		
			formset = OrderFormSet(queryset=PlaceOrderMedicineOne.objects.none(),initial=items_data)	

		zipped_three = list(zip(medicine_list,order_check,formset))

		placed_orders = PlaceOrderMedicineOne.objects.filter(Q(order_timestamp=date.today()) & Q(medicine_order__branch = hr_branch))

		ordered_items = OrderMedicineItem.objects.filter(Q(ordered_med__order_timestamp = date.today()) & Q(ordered_med__medicine_order__branch = hr_branch))

		ordered_items_vendor_temp = []
		for i in ordered_items:
			ordered_items_vendor_temp.append(i.vendor)

		ordered_items_vendor = []
		ordered_items_medicine = []
		for v in list(set(ordered_items_vendor_temp)):
			ordered_items_vendor.append(v)
			data = OrderMedicineItem.objects.filter(Q(vendor=v) & Q(ordered_med__order_timestamp=date.today()) & Q(ordered_med__medicine_order__branch=hr_branch))
			ordered_items_medicine.append(data)
		
		vendor_medicine_list = list(zip(ordered_items_vendor,ordered_items_medicine))

		context = {
			"status" : status,
			"user" : "H",
			"new_zipped": new_zipped,
			"formset":formset,	
			"zipped_three":zipped_three,
			'placed_orders':placed_orders,
			'vendor_medicine_list': vendor_medicine_list,
			'today':date.today(),
		}
	except:
		hr_obj = Receptionist.objects.get(username = status)
		hr_branch = hr_obj.branch
		queryset = MedicineStockList.objects.filter(Q(branch= hr_branch) & Q(order_status = True))
		order_check = []
		for q in queryset:
			if q.quantity <= q.reorder_level:
				
				order_history = OrderMedicineItem.objects.filter(Q(vendor=q.vendor) & Q(ordered_med__medicine_order_id=q.id) & Q(ordered_med__medicine_order__branch = hr_branch))
				if order_history:
					last_order = order_history.last()
					if last_order.order_receive_flag:
						order_check.append(None)
					else:
						order_check.append(last_order)
				else:
					order_check.append(None)

		medicine_list = []
		for q in queryset:
			if q.quantity <= q.reorder_level:
				medicine_list.append(q)

		new_zipped = list(zip(medicine_list,order_check))
		count_new_zipped = len(new_zipped)

		OrderFormSet = modelformset_factory(PlaceOrderMedicineOne, form=OrderMedicineOneForm, extra=count_new_zipped)
		if request.method == 'POST':
			formset = OrderFormSet(request.POST, queryset=PlaceOrderMedicineOne.objects.none())		
			if formset.is_valid():			
				formset.save()
				messages.success(request,"Orders Placed Successfully")
				return redirect('/place-reorder-medicine-hr/')
		else:
			items_data = [
			{
				'medicine_order':item1,
				'potency':item1.potency,
				'order_quantity': 1
			}
			for item1,item2 in new_zipped	]		
			formset = OrderFormSet(queryset=PlaceOrderMedicineOne.objects.none(),initial=items_data)	

		zipped_three = list(zip(medicine_list,order_check,formset))

		placed_orders = PlaceOrderMedicineOne.objects.filter(Q(order_timestamp=date.today()) & Q(medicine_order__branch = hr_branch))

		ordered_items = OrderMedicineItem.objects.filter(Q(ordered_med__order_timestamp = date.today()) & Q(ordered_med__medicine_order__branch = hr_branch))

		ordered_items_vendor_temp = []
		for i in ordered_items:
			ordered_items_vendor_temp.append(i.vendor)

		ordered_items_vendor = []
		ordered_items_medicine = []
		for v in list(set(ordered_items_vendor_temp)):
			ordered_items_vendor.append(v)
			data = OrderMedicineItem.objects.filter(Q(vendor=v) & Q(ordered_med__order_timestamp=date.today()) & Q(ordered_med__medicine_order__branch=hr_branch))
			ordered_items_medicine.append(data)
		
		vendor_medicine_list = list(zip(ordered_items_vendor,ordered_items_medicine))

		context = {
			"status" : status,
			"user" : "R",
			"new_zipped": new_zipped,
			"formset":formset,	
			"zipped_three":zipped_three,
			'placed_orders':placed_orders,
			'vendor_medicine_list': vendor_medicine_list,
			'today':date.today(),
		}
	return render(request,"place_reorder_medicine_test.html",context)
@csrf_exempt
def remove_reorder_medicine(request,pk):
	
	print('pk',pk)
	data = get_object_or_404(MedicineStockList,id=pk)
	data.order_status = False
	data.save()
	return redirect('place_reorder_medicine')
@csrf_exempt
def vendor_med_mail(request,pk):

	med_data = OrderMedicineItem.objects.filter(Q(vendor__id=pk) & Q (ordered_med__order_timestamp=date.today()))
	for flag in med_data:
		email_flag = get_object_or_404(OrderMedicineItem,pk=flag.id)
		email_flag.email_status = True
		email_flag.save()
	vendor_data = AddVendorStock.objects.get(id=pk)

	template = render_to_string('mail_order_medicine.html',{'med_data':med_data,'vendor_data': vendor_data})
	email_id = vendor_data.email
	mylist = []
	mylist.append(email_id)

	email = EmailMessage('Order Details',
					  template,
					  settings.EMAIL_HOST_USER,
					  mylist
					)
	email.fail_silently = True
	email.send()
	return redirect('place_reorder_medicine')
	
	
	# return render(request,'mail_order_medicine.html',{'med_data':med_data,'vendor_data': vendor_data})
@csrf_exempt
def medicine_order_history(request):

	status = False
	if request.user:
		status = request.user

	try:
		hr_obj = HR.objects.get(username= status)
	# print("hr_obj",hr_obj)
	
		hr_branch = hr_obj.branch
		ordered_medicine = OrderMedicineItem.objects.filter(ordered_med__medicine_order__branch = hr_branch)
		order_date_temp = []
		order_vendor_temp = []
		for dat in ordered_medicine:
			order_date_temp.append(dat.ordered_med.order_timestamp)

		for vendor in ordered_medicine:
			order_vendor_temp.append(vendor.vendor)


		orders_list = []
		for dat in list(set(order_date_temp)):
			for vendor in list(set(order_vendor_temp)):
				orders_date_wise = OrderMedicineItem.objects.filter(Q(ordered_med__order_timestamp=dat) & Q(vendor=vendor) & Q(email_status=True) & Q(ordered_med__medicine_order__branch=hr_branch))
				if orders_date_wise:
					orders_list.append(orders_date_wise)
		
		
		# print("LIST : ",orders_list)
		context = {
			'status':status,
			'user':'H',
			'orders_list': orders_list,
			'today':date.today(),
		}
	except:
		hr_obj = Receptionist.objects.get(username = status)
	
		hr_branch = hr_obj.branch
		ordered_medicine = OrderMedicineItem.objects.filter(ordered_med__medicine_order__branch = hr_branch)
		order_date_temp = []
		order_vendor_temp = []
		for dat in ordered_medicine:
			order_date_temp.append(dat.ordered_med.order_timestamp)

		for vendor in ordered_medicine:
			order_vendor_temp.append(vendor.vendor)


		orders_list = []
		for dat in list(set(order_date_temp)):
			for vendor in list(set(order_vendor_temp)):
				orders_date_wise = OrderMedicineItem.objects.filter(Q(ordered_med__order_timestamp=dat) & Q(vendor=vendor) & Q(email_status=True) & Q(ordered_med__medicine_order__branch=hr_branch))
				if orders_date_wise:
					orders_list.append(orders_date_wise)
		
		
		# print("LIST : ",orders_list)
		context = {
			'status':status,
			'user':'R',
			'orders_list': orders_list,
			'today':date.today(),
		}

	return render(request,'medicine_order_history.html',context)
@csrf_exempt
def dom_med_order_history(request):

	status = False
	if request.user:
		status =  request.user

	
	ordered_medicine = OrderMedicineItem.objects.filter(Q(ordered_med__medicine_order__branch = "Dombivali"))
	order_date_temp = []
	order_vendor_temp = []
	for dat in ordered_medicine:
		order_date_temp.append(dat.ordered_med.order_timestamp)

	for vendor in ordered_medicine:
		order_vendor_temp.append(vendor.vendor)


	orders_list = []
	for dat in list(set(order_date_temp)):
		for vendor in list(set(order_vendor_temp)):
			orders_date_wise = OrderMedicineItem.objects.filter(Q(ordered_med__order_timestamp=dat) & Q(vendor=vendor) & Q(email_status=True) & Q(ordered_med__medicine_order__branch="Dombivali"))
			if orders_date_wise:
				orders_list.append(orders_date_wise)
	
	
	print("LIST : ",orders_list)
	context = {
		'status':status,
		'user':'D',
		'orders_list': orders_list,
		'today':date.today(),
	}

	return render(request,'dom_med_order_history.html',context)
@csrf_exempt
def view_medicine_order_bill(request,pk):

	status = False
	if request.user:
		status = request.user
	try:
		hr_obj = HR.objects.get(username = status)
		hr_branch = hr_obj.branch
		data = BillOrderMedicineImage.objects.filter(Q(ordered_med_id=pk) & Q(ordered_med__ordered_med__medicine_order__branch = hr_branch))
		order_summary = OrderMedicineItem.objects.get(id=pk)
		orders_obj = OrderMedicineItem.objects.filter(Q(vendor=order_summary.vendor) & Q(ordered_med__order_timestamp=order_summary.ordered_med.order_timestamp))
		context = {
		'status':status,
		'user':'H',
		'data':data,
		'orders_obj':orders_obj,
	}

	except:
		data = BillOrderMedicineImage.objects.filter(Q(ordered_med_id=pk) & Q(ordered_med__ordered_med__medicine_order__branch = "Dombivali"))
		order_summary = OrderMedicineItem.objects.get(id=pk)
		orders_obj = OrderMedicineItem.objects.filter(Q(vendor=order_summary.vendor) & Q(ordered_med__order_timestamp=order_summary.ordered_med.order_timestamp))
		context = {
		'status':status,
		'user':'D',
		'data':data,
		'orders_obj':orders_obj,
	}




	

	return render(request,'view_medicine_order_bill.html',context)
@csrf_exempt
def doc_verify_med_order(request,pk):

	data = get_object_or_404(OrderMedicineItem,id=pk)
	data.is_verified = True
	data.save()
	return redirect('dom_med_order_history')
@csrf_exempt
def medicine_order_receive(request,pk):	
	
	if request.method == 'POST':
		data = OrderMedicineItem.objects.get(id=pk)
		# print("POSt DATa",request.POST['order_received'])
		# print("data----- : ",data.ordered_med.medicine_order,":",data.ordered_med.medicine_order.id)
		data.order_received = request.POST['order_received']		
		data.order_balance = int(data.ordered_med.order_quantity) - int(request.POST['order_received'])
		data.order_receive_flag = True		
		medicine_stock = MedicineStockList.objects.get(id=data.ordered_med.medicine_order.id)
		# print("medicne_stock", medicine_stock, medicine_stock.quantity)
		# print("received quantity (2) :", request.POST['order_received'])
		medicine_stock.quantity += int(request.POST['order_received'])
		print("---------------")
		print("flag",medicine_stock.approval_flag_receive)
		medicine_stock.issue_quantity = 0				
		medicine_stock.approval_flag_receive = False
		medicine_stock.save()
		data.save()
		# print(data.order_received,data.order_receive_flag)
	return redirect('medicine_order_history')
@csrf_exempt
def bill_medicine_order_receive(request,pk):

	if request.method == 'POST':
		data = OrderMedicineItem.objects.get(id=pk)
		print("Image :",request.FILES.getlist('bill_images'))
		print("DATa:", data)
		uploaded_images = request.FILES.getlist('bill_images')
		for image in uploaded_images:
			uploaded_image = BillOrderMedicineImage(ordered_med=data,bill_images=image)
			uploaded_image.save()
		# if 'bill_image' in request.FILES:
		# 	data.bill_image = request.FILES['bill_image']
		# else:
		# 	pass
		# data.save()
		messages.success(request,"Bill Image Uploaded")
		return redirect('medicine_order_history')
@csrf_exempt
def delete_all_placed_med(request):
	
	data = PlaceOrderMedicineOne.objects.all().delete()
	return redirect('place_reorder_medicine')


@csrf_exempt
def place_reorder_medicine(request):

	status = False
	if request.user:
		status = request.user

	hr_obj = HR.objects.get(username = status)

	hr_branch = hr_obj.branch

	queryset = MedicineStockList.objects.filter(branch= hr_branch)

	order_check = []
	for q in queryset:
		if q.quantity <= q.reorder_level:
			order_history = PlaceOrderMedicineNew.objects.filter(medicine_order__id = q.id)
			if order_history:
				last_order = order_history.last()
				if last_order.order_received_flag:
					order_check.append(None)
				else:
					order_check.append(last_order)
			else:
				order_check.append(None)

	medicine_list = []
	for q in queryset:
		if q.quantity <= q.reorder_level:
			medicine_list.append(q)

	new_zipped = list(zip(medicine_list,order_check))
	medicine = []
	for item1,item2 in new_zipped:
		medicine.append(item1)

	
	form = OrderMedicineOneForm(request.POST or None,initial={'order_quantity':1,'medicine_order':medicine})
	if form.is_valid():
		form.save()
		messages.success(request,"Order Placed Successfully.")
		return redirect('place_reorder_medicine')	
	
	context = {
		"status" : status,
		"user" : "H",
		"new_zipped": new_zipped,
		"form":form,		
	}

	return render(request,"place_reorder_medicine.html",context)
@csrf_exempt
def delete_medicine_stock_hr(request, pk):
	queryset = MedicineStockList.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Deleted ' + str(queryset.quantity) + " " + str(queryset.medicine) + " " + str(queryset.potency)+' Successfully.')
		return redirect('/medicine-stock-list-hr/')
	return render(request, 'delete_medicine_stock_hr.html')

@csrf_exempt
def medicine_stock_management_hr(request, pk):

	status = False
	if request.user:
		status = request.user

	try:
		hr_branch = HR.objects.get(username = status).branch
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()

		queryset = MedicineStockList.objects.get(id=pk)
		context = {		
			"queryset": queryset,
			"header": hr_branch +" Medicine Store ",
			"med_name": queryset.medicine.medicine.medicine_name.upper(),
			"status":status,
			"user":"H",
			"unsend_mail_count":unsent_mail_count,
		}
	except:
		hr_branch = Receptionist.objects.get(username = status).branch
		queryset = MedicineStockList.objects.get(id=pk)
		context = {		
			"queryset": queryset,
			"header": hr_branch +" Medicine Store ",
			"med_name": queryset.medicine.medicine.medicine_name.upper(),
			"status":status,
			"user":"R",			
		}
	return render(request, "medicine_stock_management_hr.html", context)
@csrf_exempt
def issue_medicine_hr(request, pk):

	status = False
	if request.user:
		status = request.user

	queryset = MedicineStockList.objects.get(id=pk)
	# print(queryset.approval_flag_updtate)
	form = MedicineIssueHRForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.receive_quantity = 0
		instance.quantity -= instance.issue_quantity
		if instance.approval_flag_updtate:
			instance.approval_flag_updtate = False				
		messages.success(request, "Issued "+ str(queryset.issue_quantity)+ " "+ str(instance.medicine) + " ("+ str(instance.potency) +") SUCCESSFULLY . " + str(instance.quantity) + " "+ str(instance.medicine) + " (" + str(instance.potency) + ") now left in Store")
		instance.save()
		return redirect('/medicine-stock-management-hr/'+str(instance.id))

	try:
		user = HR.objects.get(username=status)
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=queryset.branch))
		unsent_mail_count = mail_count.count()		

		context = {
			"title": 'Issue ' + str(queryset.medicine) + ' - ' +str(queryset.potency),
			"queryset": queryset,
			"form": form,
			"status":status,
			"user":"H",	
			"unsend_mail_count":unsent_mail_count	
		}
	except:
		user = Receptionist.objects.get(username=status)
		context = {
			"title": 'Issue ' + str(queryset.medicine) + ' - ' +str(queryset.potency),
			"queryset": queryset,
			"form": form,
			"status":status,
			"user":"R"				
		}
	return render(request, "add_medicine_stock_hr.html", context)

@csrf_exempt
def receive_medicine_hr(request, pk):

	status = False
	if request.user:
		status = request.user

	queryset = MedicineStockList.objects.get(id=pk)
	form = MedicineReceiveHRForm(request.POST or None,request.FILES or None ,instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.issue_quantity = 0
		instance.quantity += instance.receive_quantity
		print("Instance Flag",instance.approval_flag_receive)
		if instance.approval_flag_receive:
			instance.approval_flag_receive = False
		# if 'upload_medicine_bill_image' in request.FILES:
		# 	instance.upload_medicine_bill_image = request.FILES['upload_medicine_bill_image']		
		# obj = BillImageMedicine.objects.create(medicine=queryset,stock_image=request.FILES['upload_medicine_bill_image'])
		instance.save()
		messages.success(request, "Received "+  str(instance.receive_quantity) + " " + str(instance.medicine) + " (" + str(instance.potency) +") SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.medicine) + " (" + str(instance.potency) +") now in Store")
		return redirect('/medicine-stock-management-hr/'+str(instance.id))	
	
	try:
		user = HR.objects.get(username=status)
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=queryset.branch))
		unsent_mail_count = mail_count.count()		
		
		context = {
				"title": 'Receive ' + str(queryset.medicine) + " - " + str(queryset.potency),
				"instance": queryset,
				"form": form,
				"status":status,
				"user":"H",	
				"unsend_mail_count":unsent_mail_count		
			}
	except:
		user =Receptionist.objects.get(username=status)
		context = {
				"title": 'Receive ' + str(queryset.medicine) + " - " + str(queryset.potency),
				"instance": queryset,
				"form": form,
				"status":status,
				"user":"R",							
			}
	return render(request, "add_medicine_stock_hr.html", context)
@csrf_exempt
def reorder_medicine_hr(request, pk):

	status = False
	if request.user:
		status = request.user

	queryset = MedicineStockList.objects.get(id=pk)
	form = MedicineReorderLevelHRForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.medicine) + " is updated to " + str(instance.reorder_level))
		return redirect("/medicine-stock-list-hr/")
	
	try:
		user = HR.objects.get(username=status)
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=queryset.branch))
		unsent_mail_count = mail_count.count()
		context = {
				"instance": queryset,
				"form": form,
				"title": "Set Reorder Level for  " + str(queryset.medicine) + " " + str(queryset.potency),
				"status":status,
				"user":"H",
				"unsend_mail_count":unsent_mail_count
			}
	except:
		user = Receptionist.objects.get(username=status)
		context = {
				"instance": queryset,
				"form": form,
				"title": "Set Reorder Level for  " + str(queryset.medicine) + " " + str(queryset.potency),
				"status":status,
				"user":"R",				
			}
	return render(request, "add_medicine_stock_hr.html", context)


# ON DOCTORS DASHBOARD
@csrf_exempt
def medicine_stock_approval(request,branch):

	print("Branch",branch)
	status = False
	if request.user:
		status = request.user
	
	header = 'Approval of Medicines'
	form =MedicineStockListSearchForm(request.POST or None)	
	queryset = MedicineStockList.objects.filter(branch = branch)
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
	unsent_mail_count = mail_count.count()
	

	context = {
		"header": header,
		"queryset": queryset,
		"form": form,
		"status":status,
		"user":"D",
		"branch":branch,
		'unsend_mail_count': unsent_mail_count,
	}

	if form.is_valid():	

		medicine_search = AddMedicineHR.objects.get(medicine_name =form.cleaned_data['medicine'])
		potency_search = AddPotencyHR.objects.get(potency_name =form.cleaned_data['potency'])		
		queryset = MedicineStockList.objects.filter(Q(medicine__medicine=medicine_search) & Q(branch=branch) & Q(potency__potency_name=potency_search))
		form.save(commit=False)	
		context = {
		"form": form,
		"header": header,
		"queryset": queryset,
		"status":status,
		"user":"D",
		"branch":branch,
		'unsend_mail_count': unsent_mail_count,
	}
	return render(request, "medicine_stock_approval.html", context)
@csrf_exempt
def approve_new_med_hr(request,pk):
	
	data = MedicineStockList.objects.get(id=pk)
	# print(data.approval_flag_new)

	if data.approval_flag_new:
		data.approval_flag_new = False
		data.save()
	return redirect('/medicine-stock-approval/'+data.branch)
@csrf_exempt
def approve_issue_med_hr(request,pk):
	
	data = MedicineStockList.objects.get(id=pk)
	
	if data.approval_flag_updtate == False:
		data.approval_flag_updtate = True
		data.save()
	return redirect('/medicine-stock-approval/'+data.branch)
@csrf_exempt
def approve_receive_med_hr(request,pk):
	
	data = MedicineStockList.objects.get(id=pk)
	
	if data.approval_flag_receive == False:
		data.approval_flag_receive = True
		data.save()
	return redirect('/medicine-stock-approval/'+data.branch)

@csrf_exempt
def add_vendor_stock(request):

	status = False
	if request.user:
		status = request.user
	form = AddVendorStockForm(request.POST or None)
	
	if form.is_valid():
		vendor_name = form.cleaned_data['vendor_name']		
		form.save()
		messages.success(request, 'Added '+ vendor_name + ' to the Vendors list Successfully')
		return redirect('add_vendor_stock')
	try:
		hr_branch = HR.objects.get(username=status).branch
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		context = {
			"form": form,
			"title": "Add Vendor Details",
			"main_one" : "Add Vendor Details",
			"status":status,
			"user":"H",
			"unsend_mail_count":unsent_mail_count,
		}
	except:
		context = {
			"form": form,
			"title": "Add Vendor Details",
			"main_one" : "Add Vendor Details",
			"status":status,
			"user":"R",			
		}
	return render(request, "add_stock.html", context)

@csrf_exempt
def vendor_stock_list(request):

	status = False
	if request.user:
		status=request.user	
	
	header = 'List of Vendors '
	form = VendorStockSearchForm(request.POST or None)	
	queryset = AddVendorStock.objects.all()
	# queryset = AddVendorStock.objects.filter(vendor_branch="Dombivali")
	try:
		hr_branch = HR.objects.get(username=status).branch	
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()

		context = {
			"header": header,
			"queryset": queryset,
			"form": form,
			"status":status,
			"user":"H",
			"unsend_mail_count":unsent_mail_count,
		}
	except:
		context = {
			"header": header,
			"queryset": queryset,
			"form": form,
			"status":status,
			"user":"R",			
		}

	if form.is_valid():
		try:	
			queryset = AddVendorStock.objects.filter(Q(vendor_name__icontains=form.cleaned_data['vendor_name']) & Q(mobile_number__icontains=form.cleaned_data['mobile_number']))
		except:
			try:
				queryset = AddVendorStock.objects.filter(vendor_name__icontains=form.cleaned_data['vendor_name'])
				# queryset = AddVendorStock.objects.filter(Q(vendor_name__icontains=form.cleaned_data['vendor_name']) & Q(vendor_branch="Dombivali"))

			except:
				queryset = AddVendorStock.objects.filter(mobile_number__icontains=form.cleaned_data['mobile_number'])
		form.save(commit=False)	
	try:
			context = {
			"form": form,
			"header": header,
			"queryset": queryset,
			"status":status,
			"user":"H",
			"unsend_mail_count":unsent_mail_count,
		}
	except:
		context = {
			"form": form,
			"header": header,
			"queryset": queryset,
			"status":status,
			"user":"R",
			
		}
	return render(request, "vendor_stock_list.html", context)

@csrf_exempt
def add_product_vendor_stock(request,pk):

	status = False
	if request.user:
		status = request.user

	vendor_data = AddVendorStock.objects.get(id=pk)
	# print("Vendor_category",vendor_data.vendor_category.category,type(vendor_data.vendor_category.category))
	category = vendor_data.vendor_category.category
	if category == "Stock":
		form = VendorStockProductForm(request.POST or None,initial = {'vendor':vendor_data},cat=category)
		if form.is_valid():		
			form.save()
			messages.success(request, 'Added  to the Product list Successfully')
			return redirect('/add-product-vendor-stock/'+str(pk)+'/')
		
		list_products = VendorStockProduct.objects.filter(vendor = vendor_data)
		try:
			hr_branch = HR.objects.get(username=status).branch	
			mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
			unsent_mail_count = mail_count.count()

			
			context = {
				"form": form,
				"title": "Add Product",
				"main_product" : "Add Product",
				"vendor_data":vendor_data,
				"queryset": list_products,
				"status":status,
				"user":"H",
				"unsend_mail_count":unsent_mail_count
				
			}
		except:
			context = {
				"form": form,
				"title": "Add Product",
				"main_product" : "Add Product",
				"vendor_data":vendor_data,
				"queryset": list_products,
				"status":status,
				"user":"R"			
			}
		return render(request, "add_stock.html", context)		
	elif category == 'Medicine':
		form = VendorMedicineForm(request.POST or None,initial = {'vendor':vendor_data},cat=category)
		if form.is_valid():		
			form.save()
			messages.success(request, 'Added  to the Medicine list Successfully')
			return redirect('/add-product-vendor-stock/'+str(pk)+'/')
		
		list_products = VendorMedicine.objects.filter(vendor = vendor_data)
		try:
			hr_branch = HR.objects.get(username=status).branch	
			mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
			unsent_mail_count = mail_count.count() 

			context = {
				"form": form,
				"title": "Add Medicine",
				"main_product" : "Add Medicine",
				"vendor_data":vendor_data,
				"queryset": list_products,
				"status":status,
				"user":"H",
				"unsend_mail_count":unsent_mail_count
				
			}
		except:
			context = {
				"form": form,
				"title": "Add Medicine",
				"main_product" : "Add Medicine",
				"vendor_data":vendor_data,
				"queryset": list_products,
				"status":status,
				"user":"R",				
				
			}
		return render(request, "add_stock_medicine.html", context)
		
	
# AJAX 
@csrf_exempt
def load_products(request):

	vendor_id = request.GET.get('vendor_id')	
	product = VendorStockProduct.objects.filter(vendor_id=vendor_id)	
	return render(request, 'product_dropdown_list_options.html', {'product': product})

@csrf_exempt
def place_order_stock(request, pk):

	status = False
	if request.user:
		status = request.user

	# pk-stock_id , filtering the Stock and take out vendor_id
	queryset = Stock.objects.get(id=pk)


	# filter stock basis of vendor_id , applying for condition of reorder level	
	place_order = Stock.objects.filter(vendor=queryset.vendor_id)

	print("Stock_per_vendor",place_order)

	reorder_now = []

	for pal in place_order:
		if pal.quantity <= pal.reorder_level:
			order_placed_previous = PlaceOrderStock.objects.filter(stock_order_id = pal.id).last()
			if order_placed_previous is None or order_placed_previous.order_received_flag==True:
				reorder_now.append(Stock.objects.get(id=pal.id))

	count_reorder_stock = 0
	for count in place_order:
		if count.quantity <= count.reorder_level:
			count_reorder_stock += 1

	no_previous_order = []
	previous_order_delivered = []
	order_not_delivered = []
	order_date = []
	stock_ordered = []	
	for p in place_order:
		if p.quantity <= p.reorder_level:			
			obj = PlaceOrderStock.objects.filter(stock_order_id = p.id)
			if obj:
				for o in obj:
					if o.order_received_flag:						
						previous_order_delivered.append(o.order_received_flag)
					else:						
						order_not_delivered.append(o.order_received_flag)
						order_date.append(o.order_timestamp)
						stock_ordered.append(o)
			else:				
				no_previous_order.append('x')	

	form = PlaceOrderForm(request.POST or None,initial={'email':queryset.vendor.email},vendor_id=queryset.vendor_id)
	if form.is_valid():
		instance = form.save(commit=False)
		messages.success(request,"Order Details Added")
		instance.save()
		return redirect('/place-order-stock/'+str(queryset.id)+'/')
	
	order_details = PlaceOrderStock.objects.filter(Q(stock_order__vendor_id =queryset.vendor_id) & Q(order_timestamp__date=date.today()) )

	order_info = order_details.last()	
	try:
		hr_branch = HR.objects.get(username=status).branch	
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		try:
			context = {		
				"queryset": queryset,
				"place_order":reorder_now,
				"order_info":order_info,
				"header": "Place Order",
				"stock_name": queryset.stock_name.product_name.name.upper(),
				'form':form,
				'order_details':order_details,
				"status":status,
				"user":"H",
				"unsend_mail_count":unsent_mail_count,
				"pk":pk,
				'date1':date.today(),
				'current_order': len(order_not_delivered),
				'order_date': order_date[0].date(),
				'stock_ordered':stock_ordered,
				'length_order':len(stock_ordered),
				'count_reorder_stock':count_reorder_stock,
			}
		except:
			context = {		
			"queryset": queryset,
			"place_order":reorder_now,
			"order_info":order_info,
			"header": "Place Order",
			"stock_name": queryset.stock_name.product_name.name.upper(),
			'form':form,
			'order_details':order_details,
			"status":status,
			"user":"H",
			"unsend_mail_count":unsent_mail_count,
			"pk":pk,
			'date1':date.today(),
			'current_order': len(order_not_delivered),			
		}	
	except:
		user = Receptionist.objects.get(username=status)
		try:
			context = {		
				"queryset": queryset,
				"place_order":reorder_now,
				"order_info":order_info,
				"header": "Place Order",
				"stock_name": queryset.stock_name.product_name.name.upper(),
				'form':form,
				'order_details':order_details,
				"status":status,
				"user":"R",
				"pk":pk,
				'date1':date.today(),
				'current_order': len(order_not_delivered),
				'order_date': order_date[0].date(),
				'stock_ordered':stock_ordered,
				'length_order':len(stock_ordered),
				'count_reorder_stock':count_reorder_stock,			
			}
		except:
			context = {		
				"queryset": queryset,
				"place_order":reorder_now,
				"order_info":order_info,
				"header": "Place Order",
				"stock_name": queryset.stock_name.product_name.name.upper(),
				'form':form,
				'order_details':order_details,
				"status":status,
				"user":"R",
				"pk":pk,
				'date1':date.today(),
				'current_order': len(order_not_delivered),					
			}
			
	return render(request, "place_order_stock.html", context)
@csrf_exempt
def order_placed_vendor_stockinfo(request,pk):

	status = False
	if request.user:
		status = request.user

	
	queryset = Stock.objects.get(id=pk)
	form = PlacedOrderStockSearchFrom(request.POST or None,vendor_id=queryset.vendor_id)	
	order_details = PlaceOrderStock.objects.filter(stock_order__vendor_id =queryset.vendor_id )
	try:
		hr_branch = HR.objects.get(username=status).branch	
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()	
		context = {
			'status':status,
			'user':'H',
			"form":form,
			'order_details':order_details,
			'unsend_mail_count':unsent_mail_count,	
			'pk':pk,
			'branch':hr_branch		
		}

		if form.is_valid():
			order_details = PlaceOrderStock.objects.filter(stock_order__stock_name__product_name__name = form.cleaned_data['stock_order']) 
			form.save(commit=False)
			context = {
			'status':status,
			'user':'H',
			"form":form,
			'order_details':order_details,
			'unsend_mail_count':unsent_mail_count,	
			'pk':pk,
			'branch':hr_branch		
		}
	except:
		user=Receptionist.objects.get(username=status)
		context = {
			'status':status,
			'user':'R',
			'form':form,
			'order_details':order_details,
			'pk':pk,
			'branch':user.branch
			}
		if form.is_valid():
			order_details = PlaceOrderStock.objects.filter(stock_order__stock_name__product_name__name = form.cleaned_data['stock_order']) 
			form.save(commit=False)

		context = {
			'status':status,
			'user':'R',
			'form':form,
			'order_details':order_details,
			'pk':pk,
			'branch':user.branch
			}
		

	return render(request,"order_placed_vendor_stockinfo.html",context)

@csrf_exempt
def order_summary_stock(request,pk):

	status = False
	if request.user:
		status = request.user

	queryset = Stock.objects.get(id=pk)

	order_details = PlaceOrderStock.objects.filter(Q(stock_order__vendor_id =queryset.vendor_id) & Q(order_timestamp__date=date.today()) )
	order_info = order_details.last()

	try:
		hr_branch = HR.objects.get(username=status).branch	
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		context = {
			'status': status,
			'user':'H',
			"order_info":order_info,
			'order_details':order_details,
			'pk':pk,
			'unsend_mail_count':unsent_mail_count,
		}
	except:
		user = Receptionist.objects.get(username=status)
		context = {
			'status': status,
			'user':'R',
			"order_info":order_info,
			'order_details':order_details,
			'pk':pk,
		}
	return render(request,"order_summary_stock.html",context)

@csrf_exempt
def delete_order_stock(request,pk):

	queryset= PlaceOrderStock.objects.get(id=pk)
	queryset.delete()	
	return redirect('/place-order-stock/'+str(queryset.stock_order_id)+'/')

@csrf_exempt	
def mail_order_stock(request,pk):

	queryset = Stock.objects.get(id=pk)

	order_details = PlaceOrderStock.objects.filter(Q(stock_order__vendor_id =queryset.vendor_id) & Q(order_timestamp__date=date.today()) )
	order_info = order_details.last()

	template =  render_to_string('mail_order_stock.html',{'order_details':order_details,'order_info':order_info})
	email_id = order_info.email
	mylist = []
	mylist.append(email_id)

	email = EmailMessage(
		'Order Placed Details',
		template,
		settings.EMAIL_HOST_USER,
		mylist
	)

	email.fail_silently = True
	email.send()

	for order in order_details:
		print("before---",order.stock_order,order.email_placed_flag)
		email_flag_change = order
		email_flag_change.email_placed_flag = True
		email_flag_change.save()
		print("after---",order.stock_order,order.email_placed_flag)


	# email_flag_change = get_object_or_404(PlaceOrderStock,id=pk)
	# email_flag_change.email_placed_flag = True
	# email_flag_change.save(update_fields=['email_placed_flag'])
	messages.success(request,"Email Sent Successfully !")
	return redirect('/order-summary-stock/'+str(pk)+'/')
	 
@csrf_exempt	
def mail_stock_vendor(request,pk):

	status = False
	if request.user:
		status = request.user

	order_details = PlaceOrderStock.objects.get(id=pk)
	try:
		hr_branch = HR.objects.get(username=status).branch	
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		context = {'order_details':order_details,
				'status':status,
				'user':"H",
				"unsend_mail_count":unsent_mail_count}
	except:
		user = Receptionist.objects.get(username=status)
		context = {'order_details':order_details,
				'status':status,
				'user':"R",
				}

	return render(request,"mail_stock_vendor.html",context)

@csrf_exempt	
def orders_placed_all(request):

	status = False
	if request.user:
		status = request.user
	form = PlacedOrderStockSearchFrom(request.POST or None)
	try:
		hr_branch = HR.objects.get(username=status).branch
		order_details = PlaceOrderStock.objects.filter(stock_order__branch_name = hr_branch)
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()

		p = Paginator(order_details,5)
		page = request.GET.get('page')
		datas = p.get_page(page)

		context = {
			'order_details':order_details,
			'status':status,
			'user':'H',
			'unsend_mail_count':unsent_mail_count,
			'form':form,
			'datas':datas,
		}
		if form.is_valid():
			order_details = PlaceOrderStock.objects.filter(stock_order__stock_name__product_name__name = form.cleaned_data['stock_order']) 
			form.save(commit=False)
			p = Paginator(order_details,5)
			page = request.GET.get('page')
			datas = p.get_page(page)			
			context = {
			'order_details':order_details,
			'status':status,
			'user':'H',
			'unsend_mail_count':unsent_mail_count,
			'form':form,
			'datas':datas,
		}
	except:
		hr_branch = Receptionist.objects.get(username=status).branch
		order_details = PlaceOrderStock.objects.filter(stock_order__branch_name = hr_branch)
		p = Paginator(order_details,5)
		page = request.GET.get('page')
		datas = p.get_page(page)
		context = {
			'order_details':order_details,
			'status':status,
			'user':'R',	
			'form':form,		
		}
		if form.is_valid():
			order_details = PlaceOrderStock.objects.filter(stock_order__stock_name__product_name__name = form.cleaned_data['stock_order']) 
			form.save(commit=False)
			p = Paginator(order_details,5)
			page = request.GET.get('page')
			datas = p.get_page(page)
			context = {
			'order_details':order_details,
			'status':status,
			'user':'R',	
			'form':form,
			'datas':datas,		
		}

	return render(request,"orders_placed_all.html",context)

@csrf_exempt
def mark_stock_delivered(request,pk):

	delivered = get_object_or_404(PlaceOrderStock,id=pk)
	delivered.order_received_flag  = True
	delivered.save(update_fields=['order_received_flag'])
	pre_url = request.META.get('HTTP_REFERER')
	obj =pre_url.split('/')	
	if obj[3] == 'order-placed-vendor-stockinfo':
		return redirect('/order-placed-vendor-stockinfo/'+str(obj[4])+'/')
	elif obj[3] == 'stock-orders-placed':
		return redirect('/stock-orders-placed/')

@csrf_exempt
def mark_medicine_delivered(request,pk):

	delivered = get_object_or_404(PlaceOrderMedicineNew,id=pk)
	delivered.order_received_flag  = True
	delivered.save(update_fields=['order_received_flag'])

	pre_url = request.META.get('HTTP_REFERER')
	obj = pre_url.split('/')
	print("obj",obj[3])
	if obj[3] == 'medicine-orders-placed':
		return redirect('/medicine-orders-placed/')
	elif obj[3] == 'order-placed-vendor-medicineinfo':
		return redirect('/order-placed-vendor-medicineinfo/'+str(obj[4])+'/')

	


@csrf_exempt
def place_order_medicine(request, pk):

	status = False
	if request.user:
		status = request.user

	queryset = MedicineStockList.objects.get(id=pk)

	"""filter medicine stock basis of vendor_id , applying for condition of reorder level	"""

	place_order = MedicineStockList.objects.filter(vendor=queryset.vendor_id)
	print("place order",place_order)
	reorder_now = []

	for pal in place_order:
		if pal.quantity <= pal.reorder_level:
			order_placed_previous = PlaceOrderMedicineNew.objects.filter(medicine_order_id = pal.id).last()
			if order_placed_previous is None or order_placed_previous.order_received_flag:
				reorder_now.append(MedicineStockList.objects.get(id=pal.id))	

	print("Reorder Now",reorder_now)
	count_reorder_stock = 0
	for count in place_order:
		if count.quantity <= count.reorder_level:
			count_reorder_stock += 1

	no_previous_order = []
	previous_order_delivered = []
	order_not_delivered = []
	order_date = []
	stock_ordered = []
	for p in place_order:
		if p.quantity <= p.reorder_level:			
			obj = PlaceOrderMedicineNew.objects.filter(medicine_order_id = p.id)
			if obj:
				for o in obj:
					if o.order_received_flag:						
						previous_order_delivered.append(o.order_received_flag)
					else:						
						order_not_delivered.append(o.order_received_flag)
						order_date.append(o.order_timestamp)
						stock_ordered.append(o)
			else:				
				no_previous_order.append('x')			

	
	form = PlaceMedicineOrderForm(request.POST or None,initial={'email':queryset.vendor.email},vendor_id=queryset.vendor_id)
	if form.is_valid():
		instance = form.save(commit=False)
		messages.success(request,"Medicine Order Details Added")
		instance.save()
		return redirect('/place-order-medicine/'+str(queryset.id)+'/')	
	
	order_details = PlaceOrderMedicineNew.objects.filter(Q(medicine_order__vendor_id =queryset.vendor_id) & Q(order_timestamp=date.today()) )
	order_info = order_details.last()
	try:
		hr_branch = HR.objects.get(username=status).branch	
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		try:
			context = {		
				"queryset": queryset,
				"place_order":place_order,
				"order_info":order_info,			
				"header": "Place Order",
				"stock_name": queryset.medicine.medicine.medicine_name.upper(),
				'form':form,
				'order_details':order_details,
				"status":status,
				"user":"H",
				"unsend_mail_count":unsent_mail_count,
				"pk":pk,
				'order_date': order_date[0],
				'stock_ordered':stock_ordered,
				'length_order':len(stock_ordered),
				'count_reorder_stock':count_reorder_stock,
				'current_order': len(order_not_delivered),
				'date1':date.today(),
			}
		except:
			context = {		
			"queryset": queryset,
			"place_order":place_order,
			"order_info":order_info,
			"header": "Place Order",
			"stock_name": queryset.medicine.medicine.medicine_name.upper(),
			'form':form,
			'order_details':order_details,
			"status":status,
			"user":"H",
			"unsend_mail_count":unsent_mail_count,
			"pk":pk,
			'date1':date.today(),
			'current_order': len(order_not_delivered),
						
		}

	except:
		user= Receptionist.objects.get(username=status)
		try:
			context = {		
				"queryset": queryset,
				"place_order":place_order,
				"order_info":order_info,
				"header": "Place Order",
				"stock_name": queryset.medicine.medicine.medicine_name.upper(),
				'form':form,
				'order_details':order_details,
				"status":status,
				"user":"R",
				'pk':pk,
				'date1':date.today(),
				'current_order': len(order_not_delivered),
				'order_date': order_date[0],
				'stock_ordered':stock_ordered,
				'length_order':len(stock_ordered),
				'count_reorder_stock':count_reorder_stock,
				}
		except:
			context = {		
				"queryset": queryset,
				"header": "Place Order",
				"place_order":place_order,
				"order_info":order_info,
				"stock_name": queryset.medicine.medicine.medicine_name.upper(),
				'form':form,
				'order_details':order_details,
				"status":status,
				"user":"R",
				'pk':pk,
				'date1':date.today(),
				'current_order': len(order_not_delivered),
			}


	return render(request, "place_order_medicine_change.html", context)

@csrf_exempt
def place_order_medicine_vendors(request, pk):

	status = False
	if request.user:
		status = request.user

	queryset = MedicineStockList.objects.get(id=pk)
	vendors = VendorMedicine.objects.filter(medicine_id=queryset.medicine.medicine_id)
	for v in vendors:
		print(v.vendor,v.medicine)

	context = {
		"status":status,
		"user":"H",
		"pk":pk,
		"vendors":vendors,	
	}
	return render(request, "place_order_medicine_vendors.html",context)

@csrf_exempt
def order_here_medicine(request,pk):

	status = False
	if request.user:
		status = request.user
	
	queryset = VendorMedicine.objects.get(id=pk)

	print("-------------")
	print(queryset.vendor,queryset.medicine)

	data = MedicineStockList.objects.filter(medicine__medicine__medicine_name = queryset.medicine).last()
	print("data",data)


	form = PlaceMedicineOrderForm(request.POST or None,initial = {'vendor_order':queryset.vendor,'medicine_order':data,'potency':queryset.potency,'email':queryset.vendor.email})
	if form.is_valid():
		instance = form.save(commit=False)
		messages.success(request,"Medicine Order Details Added")
		instance.save()
		return redirect('/order-medicine/'+str(pk)+'/')	
	

	context = {
		"status":status,
		"user":"H",
		"form":form,
	}

	return render(request, "order_here_medicine.html",context)

@csrf_exempt
def order_placed_vendor_medicineinfo(request,pk):

	status = False
	if request.user:
		status = request.user

	queryset = MedicineStockList.objects.get(id=pk)
	order_details = PlaceOrderMedicineNew.objects.filter(medicine_order__vendor_id =queryset.vendor_id)

	# for order in order_details:
	# 	print("--",order,order.id,order.medicine_order_id,order.order_timestamp.date())

	try:
		hr_branch = HR.objects.get(username=status).branch	
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()	
		context = {
			'status':status,
			'user':'H',			
			'order_details':order_details,
			'unsend_mail_count':unsent_mail_count,	
			'pk':pk,
			'branch':hr_branch		
		}
	except:
		user = Receptionist.objects.get(username=status)
		context = {
			'status':status,
			'user':'R',			
			'order_details':order_details,
			'pk':pk,
			'branch':user.branch
			}
	return render(request,"order_placed_vendor_medicineinfo.html",context)

@csrf_exempt
def order_medicine_summary(request,pk):

	status = False
	if request.user:
		status = request.user

	vendor = PlaceOrderMedicineNew.objects.get(id=pk)

	print("vendor",vendor.vendor_order_id)
	order_details = PlaceOrderMedicineNew.objects.filter(Q(vendor_order_id =vendor.vendor_order_id) & Q(order_timestamp=date.today()) )
	print("Order_details",order_details)
	order_info = order_details.last()
	print('order info',order_info,order_info.vendor_order.email,'--')

	context = {
		"status": status ,
		"user": "H",
		"order_details":order_details,
		"order_info":order_info,
		"pk":pk,

	}	

	return render(request,"order_medicine_summary.html",context)


@csrf_exempt
def order_summary_medicine(request,pk):

	status = False
	if request.user:
		status = request.user
	
	queryset = MedicineStockList.objects.get(id=pk)

	order_details = PlaceOrderMedicineNew.objects.filter(Q(medicine_order__vendor_id =queryset.vendor_id) & Q(order_timestamp=date.today()) )
	order_info = order_details.last()

	try:
		hr_branch = HR.objects.get(username=status).branch	
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		context = {
			'status': status,
			'user':'H',
			"order_info":order_info,
			'order_details':order_details,
			'pk':pk,
			'unsend_mail_count':unsent_mail_count,
		}
	except:
		user = Receptionist.objects.get(username=status)
		context = {
			'status': status,
			'user':'R',
			"order_info":order_info,
			'order_details':order_details,
			'pk':pk,
		}
	return render(request,"order_summary_medicine.html",context)

@csrf_exempt
def mail_order_medicine_new(request,pk):

	# queryset = MedicineStockList.objects.get(id=pk)
	# order_details = PlaceOrderMedicineNew.objects.filter(Q(medicine_order__vendor_id =queryset.vendor_id) & Q(order_timestamp=date.today()) )
	# order_info = order_details.last()
	vendor = PlaceOrderMedicineNew.objects.get(id=pk)
	order_details = PlaceOrderMedicineNew.objects.filter(Q(vendor_order_id =vendor.vendor_order_id) & Q(order_timestamp=date.today()) )
	order_info = order_details.last()

	print("order_info-----",order_info.email)


	template =  render_to_string('mail_order_medicine.html',{'order_details':order_details,'order_info':order_info})
	email_id = order_info.email
	mylist = []
	mylist.append(email_id)

	email = EmailMessage(
		'Order Placed Details',
		template,
		settings.EMAIL_HOST_USER,
		mylist
	)

	email.fail_silently = True
	email.send()
	for order in order_details:
		print("before---",order.medicine_order,order.email_placed_flag)
		email_flag_change = order
		email_flag_change.email_placed_flag = True
		email_flag_change.save()
		print("after---",order.medicine_order,order.email_placed_flag)

	messages.success(request,"Email Sent Successfully !")
	return redirect('/order_medicine_summary/'+str(pk)+'/')

@csrf_exempt
def delete_order_medicine(request,pk):

	queryset = PlaceOrderMedicineNew.objects.get(id=pk)
	queryset.delete()
	return redirect('/place-order-medicine/'+str(queryset.medicine_order_id)+'/')

@csrf_exempt
def mail_order_medicine(request,pk):

	order_details = PlaceOrderMedicineNew.objects.get(id=pk)
	template =  render_to_string('mail_order_med.html',{'order_details':order_details})
	email_id = order_details.email
	mylist = []
	mylist.append(email_id)

	email = EmailMessage(
		'Order Placed Details',
		template,
		settings.EMAIL_HOST_USER,
		mylist
	)

	email.fail_silently = True
	email.send()

	email_flag_change = get_object_or_404(PlaceOrderMedicineNew,id=pk)
	email_flag_change.email_placed_flag = True
	email_flag_change.save(update_fields=['email_placed_flag'])
	return redirect('/place-order-medicine/'+str(order_details.medicine_order_id)+'/')

@csrf_exempt
def mail_medicine_vendor(request,pk):

	status = False
	if request.user:
		status = request.user

	order_details = PlaceOrderMedicineNew.objects.get(id=pk)
	try:
		hr_branch = HR.objects.get(username=status).branch	
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		context = {'order_details':order_details,
				'status':status,
				'user':"H",
				"unsend_mail_count":unsent_mail_count}
	except:
		context = {'order_details':order_details,
				'status':status,
				'user':"R",
				}
		
	return render(request,"mail_medicine_vendor.html",context)


@csrf_exempt
def orders_placed_medicine(request):

	status = False
	if request.user:
		status = request.user

	try:
		hr_branch = HR.objects.get(username=status).branch
		order_details = PlaceOrderMedicineNew.objects.filter(medicine_order__branch = hr_branch)
		mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False) & Q(patient__branch=hr_branch))
		unsent_mail_count = mail_count.count()
		context = {
			'order_details':order_details,
			'status':status,
			'user':'H',
			'unsend_mail_count':unsent_mail_count
		}
	except:
		hr_branch = Receptionist.objects.get(username=status).branch
		order_details = PlaceOrderMedicineNew.objects.filter(medicine_order__branch = hr_branch)
		context = {
			'order_details':order_details,
			'status':status,
			'user':'R',			
		}

	return render(request,"orders_placed_medicine.html",context)

@csrf_exempt
def edit_home_page(request):

	status = False
	if request.user:
		status = request.user

	appointmentform = ForAppointmentHomePageForm(request.POST or None, request.FILES or None)
	if appointmentform.is_valid():
		appointmentform.save()
		messages.success(request,'Successfully Added a Branch')
		return redirect('edit_home_page')
	branches_details = ForAppointmentHomePage.objects.all()

	portfolio_images = OurPortfolioImages.objects.all()
	context = {
		'status':status,
		'user': 'D',		
		'appointmentform':appointmentform,
		'branches_details':branches_details,
		'portfolio_images' : portfolio_images,
	}
		
	return render(request,'edit_home_page_adjust.html',context)

@csrf_exempt
def update_branch_numbers(request,pk):

	if request.method == 'POST':
		data = ForAppointmentHomePage.objects.get(id=pk)
		# print(data)
		data.contact_number_one = request.POST['contact_number_one']		
		data.contact_number_two = request.POST['contact_number_two']
		data.save()
		messages.success(request,"Updated Successfully")
		return redirect('edit_home_page')

@csrf_exempt	
def delete_branch_numbers(request,pk):

	data = ForAppointmentHomePage.objects.get(id=pk)
	data.delete()
	messages.success(request,"Branch Deleted Successfully")
	return redirect('edit_home_page')

@csrf_exempt
def add_portfolio_images(request):

	if request.method == 'POST':
		images = request.FILES.getlist('images')
		for image in images:
			data = OurPortfolioImages.objects.create(images=image)
		messages.success(request,"Portfolio Images Uploaded")
		return redirect('edit_home_page')

@csrf_exempt	
def delete_portfolio_images(request,pk):

	data = OurPortfolioImages.objects.get(id=pk)
	data.delete()
	messages.success(request,"Portfolio Image Deleted Successfully")
	return redirect('edit_home_page')


 ######   ITEMS INVENTORY  FINAL CODE  ################
@csrf_exempt
def items_inventory_home(request):

	status = False
	if request.user:
		status = request.user

	try:
		find_branch = Receptionist.objects.get(username=status)
	except:
		find_branch = HR.objects.get(username=status)

	items_inventory = ItemUnitInventory.objects.filter(branch= find_branch.branch)

	search_form = ItemUnitInventorySearchForm(request.GET)
	filtered_items_inventory = items_inventory

	if search_form.is_valid():
		item = search_form.cleaned_data.get('item')

		if item:
			filtered_items_inventory = filtered_items_inventory.filter(item__item_name__icontains= item)
	
	general = Appointment.objects.filter(Q(patientid__branch = find_branch.branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = find_branch.branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = find_branch.branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=find_branch.branch))
	unsent_mail_count = str(mail_count.count())
	
	try:
		if Receptionist.objects.get(username=status):
			context = {
				'status':status,
				'user':'R',
				'filtered_items_inventory':filtered_items_inventory,
				'search_form':search_form,
				'branch':find_branch.branch,
				
				
			}
	except:
		context = {
			'status':status,
			'user':'H',
			'filtered_items_inventory':filtered_items_inventory,
			'search_form':search_form,
			'branch':find_branch.branch,
			'general':count_general,
			'repeat': count_repeat,
			'courier':count_courier,
			'unsend_mail_count': unsent_mail_count,
			
													

		}

	return render(request, 'COMMON_APP/items_inventory_home_adjust.html',context)

@csrf_exempt
def issue_items_inventory(request,id):

	queryset = ItemUnitInventory.objects.get(id=id)
	form = IssueItemsInventoryForm(request.POST or None,instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.receive_quantity = 0
		instance.quantity -= instance.issue_quantity
		instance.approval_flag_issue = True
		messages.success(request, f' {queryset.issue_quantity} {queryset.unit} {queryset.item} Over, {queryset.quantity} {queryset.unit} {queryset.item} now LEFT in Inventory')
		instance.save()
		return HttpResponseRedirect(reverse('issue_items_inventory',kwargs={'id':id}))



	context = {
		'queryset':queryset,
		'form':form,
	}

	return render(request,"COMMON_APP/issue_items_inventory.html",context)

@csrf_exempt
def reorder_level_items(request,id):

	queryset = ItemUnitInventory.objects.get(id=id)
	form = ReorderLevelItemInventoryForm(request.POST or None,instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,f'Reorder Level for {instance.item} is updated to {instance.reorder_level} {instance.unit}')
		return HttpResponseRedirect(reverse('reorder_level_items',kwargs={'id':id}))
	
	context = {
		'form':form,
		'queryset':queryset,
 	}

	return render(request,"COMMON_APP/reorder_level_items.html",context)

@csrf_exempt
def add_items_unit(request):

	status = False
	if request.user:
		status = False

	if request.method == 'POST':
		item_name = request.POST.get('item_name','').strip()
		unit_name = request.POST.get('unit_name','').strip()

		if item_name:
			item_name = item_name.upper()
			AddItems.objects.get_or_create(item_name=item_name)
			messages.success(request,f'Successfully added {item_name} to Items List.')
		
		if unit_name:
			unit_name = unit_name.upper()
			AddUnits.objects.get_or_create(unit_name=unit_name)
			messages.success(request,f'Successfully added {unit_name} to Unit List.')

	items_data = AddItems.objects.all()
	units_data = AddUnits.objects.all()

	search_form = AddItemsSearchForm(request.GET)
	search_form_two = AddUnitSearchForm(request.GET)	

	filtered_items = items_data
	filtered_units = units_data	

	if search_form.is_valid():
		item = search_form.cleaned_data.get('item')
		if item:
			filtered_items = filtered_items.filter(item_name__icontains=item)
	
	if search_form_two.is_valid():
		unit = search_form_two.cleaned_data.get('unit')
		if unit:
			filtered_units = filtered_units.filter(unit_name__icontains=unit)
				

	context = {
		'status': status,
		'user' : 'R',
		"filtered_items":filtered_items,
        "filtered_units":filtered_units,
        "search_form":search_form,
        "search_form_two":search_form_two,
	}

	return render(request,"COMMON_APP/add_items_unit.html",context)

@csrf_exempt
def items_vendors(request):

	form = ItemsVendorDetailsForm(request.POST or None)
	if form.is_valid():
		name = form.cleaned_data['vendor_name']
		number = form.cleaned_data['mobile_number']
		email = form.cleaned_data['email']
		address = form.cleaned_data['address']
		form.save(commit=False)
		ItemsVendorDetails.objects.get_or_create(vendor_name=name.upper(),mobile_number=number,email=email,address=address.upper())
		messages.success(request,f'Successfully Added {name.upper()} as a VENDOR for ITEMS')
		return redirect('items_vendors')
	
	vendor_details = ItemsVendorDetails.objects.all()
	context = {
		'form':form,
		'vendor_details':vendor_details,
	}
	return render(request,'COMMON_APP/items_vendors.html',context)

@csrf_exempt
def items_vendor_update(request,id):

	queryset = ItemsVendorDetails.objects.get(id=id)
	form = ItemsVendorDetailsForm(request.POST or None,instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.vendor_name = instance.vendor_name.upper()
		instance.mobile_number = instance.mobile_number
		instance.email = instance.email
		instance.address = instance.address.upper()
		messages.success(request,f'Successfully Updated')
		instance.save()
		return HttpResponseRedirect(reverse('items_vendor_update',kwargs={'id':id}))
	
	context = {
		'form':form,
	}

	return render(request,'COMMON_APP/items_update_vendor.html',context)

@csrf_exempt
def add_items_inventory(request):

	status = False
	if request.user:
		status = request.user
	# print("status",status)
	try:
		defined_branch = Receptionist.objects.get(username=status)
	except:
		defined_branch = HR.objects.get(username=status)

	form = ItemUnitInventoryCreateForm(request.POST or None,initial={'branch':defined_branch.branch})
	if form.is_valid():
		item = form.cleaned_data['item']
		unit = form.cleaned_data['unit']
		receive_quantity = form.cleaned_data['receive_quantity']
		branch = form.cleaned_data['branch']
		form.save(commit=False)
		ItemUnitInventory.objects.get_or_create(item=item,unit=unit,branch=branch,quantity = receive_quantity)
		messages.success(request,f'Successfully Added {receive_quantity} {unit} {item} to Items Inventory.')
		return redirect('add_items_inventory')
	
	context ={'form':form}
	return render(request,'COMMON_APP/add_items_inventory.html',context)

@csrf_exempt
def place_order_items(request):

	status = False
	if request.user:
		status = request.user

	try:
		find_branch = Receptionist.objects.get(username=status)
	except:
		find_branch = HR.objects.get(username=status)

	items_to_order = ItemUnitInventory.objects.filter(Q(quantity__lte=F('reorder_level')) & Q(branch=find_branch.branch) & Q(is_order_able=True))

	reorder_list = []
	for item in items_to_order:
		check_last = ReceiveOrderItems.objects.filter(Q(order__order_items=item) & Q(order__order_items__branch=find_branch.branch))
		# print("check",check_last)
		if check_last:
			last_order = check_last.last()
			if last_order.order_receive_flag:
				reorder_list.append(ItemUnitInventory.objects.get(id=last_order.order.order_items.id))
		else:
			reorder_list.append(item)
	# print("reorder_list",reorder_list)

	PlacedOrderFormset = modelformset_factory(PlacedOrderItems,form=PlacedOrderItemsForm,extra=len(reorder_list))
	if request.method == 'POST':
			formset = PlacedOrderFormset(request.POST, queryset=PlacedOrderItems.objects.none())

			if formset.is_valid():
				for form in formset:
					if form.is_valid() and form.has_changed():
						form.save()                
				messages.success(request,f'Orders Placed Successfully')
				return redirect('place_order_items')  # Redirect to a success page or another view after placing orders.
			else:
				messages.success(request,f'Fill the form details')
	else:
		initial_form = [
				{
					'order_items': med,
					'ordered_quantity': 1,
					'med_id': med.id,
				}
			for med in reorder_list            
			]
		formset = PlacedOrderFormset(queryset=PlacedOrderItems.objects.none(),initial=initial_form)
	
	item_id = []
	for item in reorder_list:
		item_id.append(item)
	
	zipped_one = list(zip(item_id,formset))

	order_details = ReceiveOrderItems.objects.all()

	order_date_temp = []
	order_vendor_temp = []
	for data in order_details:
		order_date_temp.append(data.order.order_date)
		order_vendor_temp.append(data.vendor)

	orders_list = []

	for dat in list(set(order_date_temp)):
		for ven in list(set(order_vendor_temp)):
			orders_date_wise = ReceiveOrderItems.objects.filter(Q(order__order_date=dat) & Q(vendor=ven))
			if orders_date_wise:
				orders_list.append(orders_date_wise)

	# print('orders_list', orders_list)	
	
	context= {
		'formset':formset,
		'zipped_one':zipped_one,
		'orders_list': orders_list,
	}
    
	return render(request,"COMMON_APP/place_order_items.html",context)

@csrf_exempt
def remove_order_items(request):
	if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
		order_id = request.POST.get('order_id')
        # print("order_id-- :",order_id)
		try:
			order = ItemUnitInventory.objects.get(id=order_id)
			order.is_order_able = False
			order.save()
			return JsonResponse({'message': 'Order removed successfully'})
		except ItemUnitInventory.DoesNotExist:
			return JsonResponse({'message': 'Order not found'}, status=404)
	return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt
def upload_bill_items(request,id):

	if request.method == 'POST':
		receive_item = ReceiveOrderItems.objects.get(id=id)
		upload_images = request.FILES.getlist('bill_images')
		for image in upload_images:
			OrderItemsBillImage.objects.create(item=receive_item,images=image)
		messages.success(request,f'Successfully Uploaded Bill Images')
		return HttpResponseRedirect(reverse('upload_bill_items',kwargs={'id':id}))

	context = {
		'id':id,
	}

	return render(request,"COMMON_APP/upload_bill_items.html",context)

@csrf_exempt
def receive_order_items(request,id):

	if request.method == 'POST':
		receive_order = ReceiveOrderItems.objects.get(id=id)
		receive_order.received_quantity = request.POST['order_received']
		receive_order.order_balance = int(receive_order.order.ordered_quantity) - int(request.POST['order_received'])
		receive_order.order_receive_flag = True
		receive_order.save()

		add_item_stock = ItemUnitInventory.objects.get(id=receive_order.order.order_items.id)
		add_item_stock.quantity += int(request.POST['order_received'])
		add_item_stock.issue_quantity = 0
		add_item_stock.receive_quantity = int(request.POST['order_received'])
		add_item_stock.approval_flag_receive = True
		add_item_stock.save()
	return redirect('place_order_items')

@csrf_exempt
def view_bill_items(request,id):

    # print("Id",id)
    order_bill = OrderItemsBillImage.objects.filter(item_id=id)
    # print("Order_bill",order_bill)

    last_image_details = order_bill.last()

    # print("vendor",last_image_details.medicine.vendor)
    # print("date",last_image_details.medicine.order.order_date)

    order_details = ReceiveOrderItems.objects.filter(Q(vendor=last_image_details.item.vendor) & Q(order__order_date=last_image_details.item.order.order_date))

    # print("Order_details--",order_details.count(),order_details)

    context = {"order_bill":order_bill,
               "order_details":order_details,
               "last_details":last_image_details}
    return render(request,'COMMON_APP/view_bill_items.html',context)

@csrf_exempt
def approve_items_doctor(request,branch):

	status = False
	if request.user:
		status = request.user

	items_inventory = ItemUnitInventory.objects.filter(branch=branch)
	search_form = ItemUnitInventorySearchForm(request.GET)
	filtered_items_inventory = items_inventory

	if search_form.is_valid():
		item = search_form.cleaned_data.get('item')

		if item:
			filtered_items_inventory = filtered_items_inventory.filter(item__item_name__icontains= item)
	
	

	context = {
		'status':status,
		'user':'D',
		'filtered_items_inventory':filtered_items_inventory,
		'search_form':search_form,		
		'branch':branch,
	}

	return render(request,'COMMON_APP/approve_items_doctor_adjust.html',context)

@csrf_exempt
def approve_flag_new_items(request,id):

	approve_new_item = ItemUnitInventory.objects.get(id=id)
	formatted_timestamp = approve_new_item.timestamp.strftime('%d-%b-%Y')
	approve_new_item.approval_flag_new = False
	approve_new_item.save()
	messages.success(request,f'Approved  NEW ITEM {approve_new_item} - RECEIVED {approve_new_item.quantity} ON {formatted_timestamp}') 
	return HttpResponseRedirect(reverse('approve_items_doctor',kwargs={'branch':approve_new_item.branch})) 


@csrf_exempt
def approve_flag_issue_items(request,id):

	approve_issue_item = ItemUnitInventory.objects.get(id=id)
	formatted_last_updated = approve_issue_item.last_updated.strftime('%d-%b-%Y')
	approve_issue_item.approval_flag_issue = False
	approve_issue_item.save()
	messages.success(request,f'Approved  ISSUED ITEM {approve_issue_item} - {approve_issue_item.issue_quantity} OVER, {approve_issue_item.quantity} LEFT IN STORE ON {formatted_last_updated }') 
	return HttpResponseRedirect(reverse('approve_items_doctor',kwargs={'branch':approve_issue_item.branch})) 

@csrf_exempt
def approve_flag_receive_items(request,id):

	approve_receive_items = ItemUnitInventory.objects.get(id=id)
	formatted_last_updated = approve_receive_items.last_updated.strftime('%d-%b-%Y')
	approve_receive_items.approval_flag_receive = False
	approve_receive_items.save()
	messages.success(request,f'Approved  RECEIVED ITEM {approve_receive_items} - {approve_receive_items.receive_quantity} RECEIVED, {approve_receive_items.quantity}  IN STORE ON {formatted_last_updated }')
	return HttpResponseRedirect(reverse('approve_items_doctor',kwargs={'branch':approve_receive_items.branch}))

@csrf_exempt
def order_history_items(request,branch):

	order_details = ReceiveOrderItems.objects.filter(order__order_items__branch = branch)
	
	order_date_temp = []
	order_vendor_temp = []
	for data in order_details:
		order_date_temp.append(data.order.order_date)
		order_vendor_temp.append(data.vendor)

	orders_list = []

	for dat in list(set(order_date_temp)):
		for ven in list(set(order_vendor_temp)):
			orders_date_wise = ReceiveOrderItems.objects.filter(Q(order__order_date=dat) & Q(vendor=ven) & Q(order__order_items__branch =branch))
			if orders_date_wise:
				orders_list.append(orders_date_wise)
	
	context = {
		'order_details':order_details,
		'orders_list':orders_list,
		'branch':branch,
	}
	return render(request,'COMMON_APP/order_history_items.html',context) 

@csrf_exempt
def approve_bills_items(request,id):

    order_bill = OrderItemsBillImage.objects.filter(item_id=id)
    last_image_details = order_bill.last()
    
    order_details = ReceiveOrderItems.objects.filter(Q(vendor=last_image_details.item.vendor) & Q(order__order_date=last_image_details.item.order.order_date))
    context = {"order_bill":order_bill,
               "order_details":order_details,
               "id":id,
               "last_details":last_image_details}

    return render(request,'COMMON_APP/approve_bills_items.html',context)

@csrf_exempt
def add_transaction_details_items(request,id):

    if request.method == 'POST':
        details = OrderItemsBillImage.objects.filter(item_id=id)

        add_transaction = details.last()
        
        receive_obj = ReceiveOrderItems.objects.get(id=add_transaction.item.id)
        receive_obj.is_approved = True
        receive_obj.save()

        add_transaction.payment_method =  request.POST['payment_method']
        add_transaction.transaction_detail = request.POST['transaction_detail']
        add_transaction.remark = request.POST['remark']
        if 'images_two' in request.FILES:            
            add_transaction.image_two = request.FILES['images_two']
        
        add_transaction.save()
        messages.success(request,"Transaction Details Added Successfully")
        return HttpResponseRedirect(reverse('add_transaction_details_items',kwargs={'id':id}))
		
    return render(request,'COMMON_APP/add_transaction_details_items.html')
	
 ######   MEDICINES INVENTORY  FINAL CODE  ################
@csrf_exempt
def medicines_inventory_home(request):

	status = False
	if request.user:
		status = request.user

	try:
		find_branch = Receptionist.objects.get(username=status)
	except:
		find_branch = HR.objects.get(username=status)

	medicine_stock = MedicinePotencyStock.objects.filter(branch=find_branch.branch)
	search_form = MedicinePotencyStockSearchForm(request.GET)
	filtered_medicine_stock = medicine_stock
	if search_form.is_valid():
		medicine = search_form.cleaned_data.get('medicine')
		potency = search_form.cleaned_data.get('potency')

		if medicine:
			 filtered_medicine_stock = filtered_medicine_stock.filter(medicine__medicine_name__icontains=medicine)
		if potency:
			filtered_medicine_stock = filtered_medicine_stock.filter(potency__potency_name__icontains=potency)
	
	general = Appointment.objects.filter(Q(patientid__branch = find_branch.branch) & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = True) & Q(notification_flag = False))	
	count_general = str(general.count())
	repeat_medicine = Appointment.objects.filter(Q(patientid__branch = find_branch.branch) & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_repeat = str(repeat_medicine.count())
	courier = Appointment.objects.filter(Q(patientid__branch = find_branch.branch) & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = True) & Q(notification_flag = False))
	count_courier = str(courier.count())
	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False)  &Q(patient__branch=find_branch.branch))
	unsent_mail_count = str(mail_count.count())
	

	
	try:
		if Receptionist.objects.get(username=status):
			context = {
			'status':status,
			'user':'R',
			'branch':find_branch.branch,
			'filtered_medicine_stock': filtered_medicine_stock,
			'search_form': search_form,
		}
	except:
		context = {
			'status':status,
			'user':'H',
			'branch':find_branch.branch,
			'filtered_medicine_stock': filtered_medicine_stock,
			'search_form': search_form,
			'general':count_general,
			'repeat': count_repeat,
			'courier':count_courier,
			'unsend_mail_count': unsent_mail_count,
		}

	
	
	return render(request,'COMMON_APP/medicines_inventory_home_adjust.html',context)

@csrf_exempt
def add_medicines_potency(request):

	if request.method == 'POST':
		medicine_name = request.POST.get('medicine_name', '').strip()
		potency_name = request.POST.get('potency_name', '').strip()
		if medicine_name:
			medicine_name = medicine_name.upper()
			AddMedicineList.objects.get_or_create(medicine_name=medicine_name)
			messages.success(request,f'Successfully Added {medicine_name} to MEDICINES LIST')
			return redirect('add_medicines_potency')
		if potency_name:
			potency_name=potency_name.upper()
			AddPotencyList.objects.get_or_create(potency_name=potency_name)
			messages.success(request,f'Successfully Added {potency_name} to POTENCY LIST')

	medicine_data = AddMedicineList.objects.all()
	potency_data = AddPotencyList.objects.all()

	search_form = AddMedicineSearchForm(request.GET)
	search_form_two = AddPotencySearchForm(request.GET)

	filtered_medicine = medicine_data
	filtered_potency = potency_data

	if search_form.is_valid():
		medicine = search_form.cleaned_data.get('medicine')
		if medicine:
			filtered_medicine = filtered_medicine.filter(medicine_name__icontains=medicine)

	if search_form_two.is_valid():
		potency = search_form_two.cleaned_data.get('potency')
		if potency:
			filtered_potency = filtered_potency.filter(potency_name__icontains =potency)
	
	context = {
		'filtered_medicine':filtered_medicine,
		'filtered_potency':filtered_potency,
		'search_form':search_form,
		'search_form_two':search_form_two,
	}
	return render(request,'COMMON_APP/add_medicines_potency.html',context)

@csrf_exempt
def medicines_vendors(request):

	form = MedicinesVendorDetailsForm(request.POST or None)
	if form.is_valid():
		name = form.cleaned_data['vendor_name']
		number = form.cleaned_data['mobile_number']
		email = form.cleaned_data['email']
		address = form.cleaned_data['address']
		form.save(commit=False)
		MedicinesVendorDetails.objects.get_or_create(vendor_name=name.upper(),mobile_number=number,email=email,address=address.upper())
		messages.success(request,f'Successfully Added {name.upper()} as a VENDOR for MEDICINE')
		return redirect('medicines_vendors')

	vendor_details = MedicinesVendorDetails.objects.all()

	context = {
		'form':form,
		'vendor_details':vendor_details,
	}



	return render(request,'COMMON_APP/medicines_vendors.html',context)

@csrf_exempt
def medicines_vendors_update(request,id):

	queryset = MedicinesVendorDetails.objects.get(id=id)
	form = MedicinesVendorDetailsForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.vendor_name = instance.vendor_name.upper()
		instance.mobile_number = instance.mobile_number
		instance.email = instance.email
		instance.address = instance.address.upper()
		messages.success(request,f'Successfully Updated')
		instance.save()
		return HttpResponseRedirect(reverse('medicines_vendors_update',kwargs={'id':id}))
	
	return render(request,'COMMON_APP/medicines_vendors_update.html',{'form':form})

@csrf_exempt
def add_medicines_inventory(request):

	status = False
	if request.user:
		status =  request.user

	try:
		find_branch = Receptionist.objects.get(username=status)
	except:
		find_branch = HR.objects.get(username=status)


	form = MedicinePotencyStockCreateForm(request.POST or None,initial = {'branch':find_branch.branch})
	if form.is_valid():
		medicine = form.cleaned_data['medicine']
		receive_quantity = form.cleaned_data['receive_quantity']
		potency = form.cleaned_data['potency']
		branch = form.cleaned_data['branch']
		form.save(commit=False)
		MedicinePotencyStock.objects.get_or_create(medicine=medicine,potency=potency,branch=branch,quantity=receive_quantity)
		messages.success(request,"Successfully Added " + str(receive_quantity) + " "+ str(medicine) + " - "+str(potency) +" to Medicine Inventory")
		return redirect('add_medicines_inventory')

	return render(request,'COMMON_APP/add_medicines_inventory.html',{'form':form})

@csrf_exempt
def reorder_medicine(request,id):

	queryset = MedicinePotencyStock.objects.get(id=id)
	form = ReorderLevelMedicineForm(request.POST or None,instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.medicine) + " is updated to " + str(instance.reorder_level))
		return HttpResponseRedirect(reverse('reorder_medicine',kwargs={'id':id}))
	
	context = {
        'form':form,
        'queryset':queryset,
    }

	return render(request,'COMMON_APP/reorder_medicine.html',context)

@csrf_exempt
def issue_medicine_inventory(request,id):

	queryset = MedicinePotencyStock.objects.get(id=id)
	form = IssueMedicinePotencyStockForm(request.POST or None,instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.receive_quantity = 0
		instance.quantity -= instance.issue_quantity
		instance.approval_flag_issue = True
		messages.success(request, "Issued "+ str(queryset.issue_quantity)+ " "+ str(instance.medicine) + " ("+ str(instance.potency) +") SUCCESSFULLY . " + str(instance.quantity) + " "+ str(instance.medicine) + " (" + str(instance.potency) + ") now left in Store")
		instance.save()
		return HttpResponseRedirect(reverse('issue_medicine_inventory',kwargs={'id':id}))
	
	context = {
        'form':form,
        'queryset':queryset,
    }

	return render(request,'COMMON_APP/issue_medicine_inventory.html',context)

@csrf_exempt
def order_medicines_inventory(request):

	status = False
	if request.user:
		status = request.user

	try:
		find_branch = Receptionist.objects.get(username=status)
	except:
		find_branch = HR.objects.get(username=status)

	medicines_to_order = MedicinePotencyStock.objects.filter(Q(quantity__lte=F('reorder_level')) & Q(branch=find_branch.branch) & Q(is_order_able=True))

	reorder_list = []
	for medicine in medicines_to_order:
		check_last = ReceiveOrderMedicine.objects.filter(Q(order__order_items=medicine) & Q(order__order_items__branch=find_branch.branch))
		if check_last:
			last_order = check_last.last()
			if last_order.order_receive_flag:
				reorder_list.append(MedicinePotencyStock.objects.get(id=last_order.order.order_items.id))
		else:
			reorder_list.append(medicine)

	PlacedOrderFormSet = modelformset_factory(PlacedOrderMedicine, form=PlacedOrderMedicineForm,extra=len(reorder_list))

	if request.method == 'POST':
		formset = PlacedOrderFormSet(request.POST, queryset=PlacedOrderMedicine.objects.none())
		if formset.is_valid():
			formset.save()
			messages.success(request,f'Orders Placed Successfully')
			return redirect('order_medicines_inventory')
		else:
			messages.success(request,f'Fill the form details')

	else:
		initial_form = [
				{
					'order_items': med,
					'ordered_quantity': 1,
					'med_id': med.id,
				}
			for med in reorder_list            
			]
		formset = PlacedOrderFormSet(queryset=PlacedOrderMedicine.objects.none(),initial=initial_form)

	medicine_id = []
	for med in reorder_list:
		medicine_id.append(med)
	
	zipped_one = list(zip(medicine_id,formset))

	order_details = ReceiveOrderMedicine.objects.filter(order__order_items__branch=find_branch.branch)

	order_date_temp = []
	order_vendor_temp = []

	for data in order_details:
		order_date_temp.append(data.order.order_date)
		order_vendor_temp.append(data.vendor)
	
	orders_list = []
	for dat in list(set(order_date_temp)):
		for ven in list(set(order_vendor_temp)):
			orders_date_wise = ReceiveOrderMedicine.objects.filter(Q(order__order_date=dat) & Q(vendor=ven) & Q(order__order_items__branch=find_branch.branch))
			if orders_date_wise:
				orders_list.append(orders_date_wise)
						
	context = {
		'formset':formset,
		'zipped_one':zipped_one,
		'orders_list': orders_list,
	}
	return render(request,'COMMON_APP/order_medicines_inventory.html',context)

@csrf_exempt
def remove_order(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        order_id = request.POST.get('order_id')
        # print("order_id-- :",order_id)
        try:
            order = MedicinePotencyStock.objects.get(id=order_id)
            order.is_order_able = False
            order.save()
            return JsonResponse({'message': 'Order removed successfully'})
        except MedicinePotencyStock.DoesNotExist:
            return JsonResponse({'message': 'Order not found'}, status=404)
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt
def upload_bills_medicine(request,id):

	if request.method == 'POST':
		receive_medicine = ReceiveOrderMedicine.objects.get(id=id)
		upload_images = request.FILES.getlist('bill_images')
		for image in upload_images:
			OrderMedicinesBillImage.objects.create(medicine=receive_medicine,images=image)
			messages.success(request,f'Successfully Uploaded Bill Images')
			return HttpResponseRedirect(reverse('upload_bills_medicine',kwargs={'id':id}))

	return render(request,'COMMON_APP/upload_bills_medicine.html', {'id':id})

@csrf_exempt
def receive_order_medicines(request,id):

	if request.method == 'POST':
		receive_order = ReceiveOrderMedicine.objects.get(id=id)
		receive_order.received_quantity = request.POST['order_received']
		receive_order.order_balance = int(receive_order.order.ordered_quantity) - int(request.POST['order_received'])
		receive_order.order_receive_flag = True
		receive_order.actual_delivery_date = request.POST['receive_date']
		receive_order.save()

		add_medicine_stock = MedicinePotencyStock.objects.get(id=receive_order.order.order_items.id)
		add_medicine_stock.quantity += int(request.POST['order_received'])
		add_medicine_stock.issue_quantity = 0
		add_medicine_stock.receive_quantity = int(request.POST['order_received'])
		add_medicine_stock.approval_flag_receive = True
		add_medicine_stock.save()
	return redirect('order_medicines_inventory')

@csrf_exempt
def view_bill_medicines(request,id):
    
	order_bill = OrderMedicinesBillImage.objects.filter(medicine_id=id)
	last_image_details = order_bill.last()
	order_details = ReceiveOrderMedicine.objects.filter(Q(vendor=last_image_details.medicine.vendor) & Q(order__order_date=last_image_details.medicine.order.order_date))
	context = {"order_bill":order_bill,
               "order_details":order_details,
               "last_details":last_image_details}



	return render(request,'COMMON_APP/view_bill_medicine.html',context)

@csrf_exempt
def approve_medicines_doctor(request,branch):

	status = False
	if request.user:
		status = request.user

	
	medicine_stock = MedicinePotencyStock.objects.filter(branch=branch)
	search_form = MedicinePotencyStockSearchForm(request.GET)
	filtered_medicine_stock = medicine_stock
	if search_form.is_valid():
		medicine = search_form.cleaned_data.get('medicine')
		potency = search_form.cleaned_data.get('potency')

		if medicine:
			filtered_medicine_stock = filtered_medicine_stock.filter(medicine__medicine_name__icontains=medicine)
		if potency:
			filtered_medicine_stock = filtered_medicine_stock.filter(potency__potency_name__icontains=potency)

	context = {
		'status' : status,
		'user' : 'D',
		'branch' : branch,		
		'filtered_medicine_stock': filtered_medicine_stock,
        'search_form': search_form,
	}

	return render(request,'COMMON_APP/approve_medicines_doctor_adjust.html',context)

@csrf_exempt
def approve_flag_new_medicine(request,id):

    approve_new = MedicinePotencyStock.objects.get(id=id)
    # print("approve_new_flag",approve_new.approval_flag_new)
    formatted_timestamp = approve_new.timestamp.strftime('%d-%b-%Y')
    approve_new.approval_flag_new = False
    approve_new.save()
    messages.success(request,f'Approved  NEW MEDICNE {approve_new} - RECEIVED {approve_new.quantity} ON {formatted_timestamp}') 
    return redirect(f'/approve-medicines-doctor/{approve_new.branch}/')

@csrf_exempt
def approve_flag_issue_medicine(request,id):

    approve_issue = MedicinePotencyStock.objects.get(id=id)
    print("approve_issue",approve_issue.approval_flag_issue)
    formatted_last_updated = approve_issue.last_updated.strftime('%d-%b-%Y')
    approve_issue.approval_flag_issue = False
    approve_issue.save()
    messages.success(request,f'Approved  ISSUED MEDICNE {approve_issue} - {approve_issue.issue_quantity} OVER, {approve_issue.quantity} LEFT IN STORE ON {formatted_last_updated }') 
    return redirect(f'/approve-medicines-doctor/{approve_issue.branch}/')

@csrf_exempt
def approve_flag_receive_medicine(request,id):

    approve_receive = MedicinePotencyStock.objects.get(id=id)
    # print("approve_receive",approve_receive.approval_flag_receive)
    formatted_last_updated = approve_receive.last_updated.strftime('%d-%b-%Y')
    approve_receive.approval_flag_receive = False
    approve_receive.save()
    messages.success(request,f'Approved  RECEIVED MEDICNE {approve_receive} - {approve_receive.receive_quantity} RECEIVED, {approve_receive.quantity}  IN STORE ON {formatted_last_updated }') 
    return redirect(f'/approve-medicines-doctor/{approve_receive.branch}/')

@csrf_exempt
def order_history_medicines(request,branch):

	order_details = ReceiveOrderMedicine.objects.filter(order__order_items__branch = branch)

	order_date_temp = []
	order_vendor_temp = []
	for data in order_details:
		order_date_temp.append(data.order.order_date)
		order_vendor_temp.append(data.vendor)

	orders_list = []

	for dat in list(set(order_date_temp)):
		for ven in list(set(order_vendor_temp)):
			orders_date_wise = ReceiveOrderMedicine.objects.filter(Q(order__order_date=dat) & Q(vendor=ven) & Q(order__order_items__branch =branch))
			if orders_date_wise:
				orders_list.append(orders_date_wise)	



	context = {
		'order_details':order_details,
		'orders_list':orders_list,
		'branch':branch,
	}

	return render(request,'COMMON_APP/order_history_medicines.html',context)

@csrf_exempt
def approve_bill_medicines(request, id):

	order_bill = OrderMedicinesBillImage.objects.filter(medicine_id=id)
	last_image_details = order_bill.last()
	order_details = ReceiveOrderMedicine.objects.filter(Q(vendor=last_image_details.medicine.vendor) & Q(order__order_date=last_image_details.medicine.order.order_date))
	context = {"order_bill":order_bill,
               "order_details":order_details,
               "id":id,
               "last_details":last_image_details}

	return render(request,'COMMON_APP/approve_bill_medicines.html',context)

@csrf_exempt
def add_transaction_medicines(request,id):


	if request.method == 'POST':
		details = OrderMedicinesBillImage.objects.filter(medicine_id=id)

		add_transaction = details.last()


        # print("Add transaction",add_transaction)
        # print("Receive",add_transaction.medicine.id)
		receive_obj = ReceiveOrderMedicine.objects.get(id=add_transaction.medicine.id)
		receive_obj.is_approved = True
		receive_obj.save()

		add_transaction.payment_method =  request.POST['payment_method']
		add_transaction.transaction_detail = request.POST['transaction_detail']
		add_transaction.remark = request.POST['remark']
		if 'images_two' in request.FILES:            
			add_transaction.image_two = request.FILES['images_two']

        
		add_transaction.save()
		messages.success(request,"Transaction Details Added Successfully")
		return HttpResponseRedirect(reverse('add_transaction_medicines',kwargs={'id':id})) 


	return render(request,'COMMON_APP/add_transaction_medicines.html')

@csrf_exempt
def order_balances_medicines(request,branch):

	orders_balance = ReceiveOrderMedicine.objects.filter(Q(order_balance__gt=0) & Q(order__order_items__branch=branch))
	context = {
        'orders_balance':orders_balance,
		'branch':branch
    }
	return render(request,'COMMON_APP/order_balances_medicines.html',context)

@csrf_exempt
def order_balances_items(request,branch):

	orders_balance = ReceiveOrderItems.objects.filter(Q(order_balance__gt=0) & Q(order__order_items__branch=branch))
	context = {
        'orders_balance':orders_balance,
		'branch':branch
    }


	return render(request,'COMMON_APP/order_balances_items.html',context)

@csrf_exempt
def balance_list(request,branch):

	status = False
	if request.user:
		status=request.user

	
	patient_details = Patient.objects.filter(branch=branch)

	balance_due_list = []
	appointment_type = []
	for p in patient_details:
		appoint = Appointment.objects.filter(Q(patientid=p)).last()
		if appoint is not None:
			try:
				balance_amount = Balance.objects.filter(patient=appoint.patientid).last()
				if balance_amount is not None and balance_amount.balance_amt > 0:
					balance_due_list.append(balance_amount)
					appointment_type.append(appoint)
			except:
				pass




	# balance_due_list = []
	# patient_info = []
	# appointment_type = []

	# balance_due = Balance.objects.filter(Q(patient__branch=branch))

	# for bal in balance_due:
	# 	patient_info.append(bal.patient)

	# print("patient_info",list(set(patient_info)))

	# for pat in list(set(patient_info)):
	# 	data = Balance.objects.filter(Q(patient__branch=branch) & Q(patient=pat)).last()

	# 	if data is not None and data.balance_amt > 0:
	# 		balance_due_list.append(data)
	# 		today_date = date.today().strftime("%Y-%m-%d")
	# 		appoint = Appointment.objects.filter(Q(patientid__branch=branch) & Q(patientid=data.patient)).exclude(date=today_date).last()
	# 		if appoint is not None:
	# 			appointment_type.append(appoint)
				
				
			
					
	
	# print("Balance_list",balance_due_list)	

	
	zipped_list = list(zip(balance_due_list,appointment_type))

	# if request.GET.get('appointment_type', None):
	# 	filtered_appointment_type = request.GET.get('appointment_type', None)
	# 	type_list = []
	# 	new_list = []
	# 	for x in appointment_type:
	# 		if x.stat == filtered_appointment_type:
	# 			type_list.append(x)
	# 			for bal in balance_due_list:
	# 				for p in type_list:
	# 					if p.patientid == bal.patient:
	# 						new_list.append(bal)

		

		

		# zipped_list = list(zip(new_list,[ x for x in appointment_type if x.stat == filtered_appointment_type]))	

	# zipped_list = zip(balance_due_list, [balance.appointment_type for balance in balance_due_list])
	context = {
		'status':status,
		'user':'D',		
		'branch':branch,
		# 'balance_due_list':balance_due_list,
		'zipped_list':zipped_list,
	}

	return render(request,'COMMON_APP/balance_list_adjust.html',context)

@method_decorator(csrf_exempt, name='dispatch')
class Balance_list_pdf(View):

	def get(self,request,*args,**kwargs):
		branch =  self.kwargs['branch']
	
		balance_due_list = []
		patient_info = []
		appointment_type = []

		balance_due = Balance.objects.filter(Q(patient__branch=branch))

		for bal in balance_due:
			patient_info.append(bal.patient)

		for pat in list(set(patient_info)):
			data = Balance.objects.filter(Q(patient__branch=branch) & Q(patient=pat)).last()
			
			if data is not None and data.balance_amt > 0:
				balance_due_list.append(data)
				today_date = date.today().strftime("%Y-%m-%d")
				appoint = Appointment.objects.filter(Q(patientid__branch=branch) & Q(patientid=data.patient)).exclude(date=today_date).last()
				
				if appoint is not None:
					appointment_type.append(appoint)			
		
		zipped_list = list(zip(balance_due_list,appointment_type))	

		
		data = {
			'branch':branch,
			'zipped_list':zipped_list,
		}

		pdf= render_to_pdf('COMMON_APP/balance_list_pdf.html',data)
		return HttpResponse(pdf, content_type='application/pdf')
	
# def place_new_order_doctor(request):

# 	status = False
# 	if request.user:
# 		status =  request.user

# 	general_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
# 	count_general_dom = str(general_dom.count())
# 	general_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="General") & Q(doctor_notification = False))
# 	count_general_mul = str(general_mul.count())
    
# 	repeat_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
# 	count_repeat_dom = str(repeat_medicine_dom.count())
# 	repeat_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Repeat Medicine") & Q(doctor_notification = False))
# 	count_repeat_mul = str(repeat_medicine_mul.count())
    
# 	courier_medicine_dom = Appointment.objects.filter(Q(patientid__branch = 'Dombivali') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
# 	count_courier_dom = str(courier_medicine_dom.count())
# 	courier_medicine_mul = Appointment.objects.filter(Q(patientid__branch = 'Mulund') & Q(date=date.today()) & Q(stat="Courier Medicine") & Q(doctor_notification = False))
# 	count_courier_mul = str(courier_medicine_mul.count())

# 	mail_count = CourierDetails.objects.filter(Q(date=date.today()) & Q(email_flag=False))
# 	unsent_mail_count = mail_count.count()

# 	if request.method == 'POST':
# 		form = PlaceOrderDoctorForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			messages.success(request,f'Order Placed Successfully.')
# 			return redirect('place_new_order_doctor')
		
# 	else:
# 		form = PlaceOrderDoctorForm()

# 	orders = PlaceOrderDoctor.objects.all()

# 	order_date_temp = []
# 	order_vendor_temp = []
# 	for data in orders:
# 		order_date_temp.append(data.order_date)
# 		order_vendor_temp.append(data.vendors)

# 	orders_list = []

# 	for dat in list(set(order_date_temp)):
# 		for ven in list(set(order_vendor_temp)):
# 			orders_date_wise = PlaceOrderDoctor.objects.filter(Q(order_date=dat) & Q(vendors=ven))
# 			if orders_date_wise:
# 				orders_list.append(orders_date_wise)

	

# 	context = {
# 		'status':status,
# 		'user':'D',
# 		'unsend_mail_count': unsent_mail_count,
# 		'count_general_dom':count_general_dom,
# 		'count_general_mul':count_general_mul,
# 		'count_repeat_dom':count_repeat_dom,
# 		'count_repeat_mul':count_repeat_mul,
# 		'count_courier_dom':count_courier_dom,
# 		'count_courier_mul':count_courier_mul,
# 		'form':form,
# 		'orders':orders,
# 		'orders_list':orders_list,
		
# 	}


# 	return render(request,'COMMON_APP/place_new_order_doctor.html',context)

@csrf_exempt
def homeo_book(request):

	status = False
	if request.user:
		status = request.user


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

	if request.method == 'POST':
			form = HomeoBookMedicineForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request,f"Successfully Added Medicine's Description to Homeo Bhagwat Gita" )
				return redirect('homeo_book')
	else:
		form = HomeoBookMedicineForm()

	medicine_detail = HomeBookMedicine.objects.all().order_by('medicine_name')
	items_per_page = 10
	paginator = Paginator(medicine_detail, items_per_page)
	page_number = request.GET.get('page')
	page = paginator.get_page(page_number)

		

	context = {
		'status':status,
		'user':'D',
		'unsend_mail_count': unsent_mail_count,
		'count_general_dom':count_general_dom,
		'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
		'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,
		'count_courier_mul':count_courier_mul,
		'form':form,
		'medicine_detail':medicine_detail,
		'page': page,
	}


	return render(request,'COMMON_APP/homeo_book_adjust.html',context)

@csrf_exempt
def homeo_book_update(request,id):

	queryset = HomeBookMedicine.objects.get(id=id)
	form = HomeoBookMedicineForm(request.POST or None,instance=queryset)
	if form.is_valid():
		form.save()
		messages.success(request,f'Successfully Updated')
		return HttpResponseRedirect(reverse('homeo_book_update',kwargs={'id':id}))


	return render(request,'COMMON_APP/homeo_book_update.html',{'form':form})

@csrf_exempt
def homeo_book_delete(request,id):

	data = HomeBookMedicine.objects.get(id=id).delete()
	messages.success(request,f'Deleted Successfully')
	return redirect('homeo_book')

@csrf_exempt
def homeo_book_disease(request):

	status = False
	if request.user:
		status = request.user


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

	if request.method == 'POST':
			form = HomeoBookDiseaseForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request,f"Successfully Added Disease's Description to Homeo Bhagwat Gita" )
				return redirect('homeo_book_disease')
	else:
		form = HomeoBookDiseaseForm()

	disease_detail = HomeBookDisease.objects.all().order_by('disease_name')	

	context = {
		'status':status,
		'user':'D',
		'unsend_mail_count': unsent_mail_count,
		'count_general_dom':count_general_dom,
		'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
		'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,
		'count_courier_mul':count_courier_mul,
		'form':form,
		'disease_detail':disease_detail,
	}

	return render(request,'COMMON_APP/homeo_book_disease_adjust.html',context)

@csrf_exempt
def homeo_book_update_disease(request,id):

	queryset = HomeBookDisease.objects.get(id=id)
	form = HomeoBookDiseaseForm(request.POST or None,instance=queryset)
	if form.is_valid():
		form.save()
		messages.success(request,f'Successfully Updated')
		return HttpResponseRedirect(reverse('homeo_book_update_disease',kwargs={'id':id}))

	return render(request,'COMMON_APP/homeo_book_update_disease.html',{'form':form})

@csrf_exempt
def home_book_delete_disease(request,id):

	data = HomeBookDisease.objects.get(id=id).delete()
	messages.success(request,f'Deleted Successfully')
	return redirect('homeo_book_disease')

@csrf_exempt
def home_book_redline_symptoms(request):


	status = False
	if request.user:
		status = request.user


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

	if request.method == 'POST':
			form = HomeoBookRedlineForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request,f"Successfully Added Redline Symptoms Description to Homeo Bhagwat Gita" )
				return redirect('home_book_redline_symptoms')
	else:
		form = HomeoBookRedlineForm()

	disease_detail = HomeBookRedline.objects.all().order_by('redline_symptoms')

	context = {
		'status':status,
		'user':'D',
		'unsend_mail_count': unsent_mail_count,
		'count_general_dom':count_general_dom,
		'count_general_mul':count_general_mul,
		'count_repeat_dom':count_repeat_dom,
		'count_repeat_mul':count_repeat_mul,
		'count_courier_dom':count_courier_dom,
		'count_courier_mul':count_courier_mul,
		'form':form,
		'disease_detail':disease_detail,
	}

	return render(request,'COMMON_APP/redline_symptoms_adjust.html',context)

@csrf_exempt
def homeo_book_update_redline(request,id):

	queryset = HomeBookRedline.objects.get(id=id)
	form = HomeoBookRedlineForm(request.POST or None,instance=queryset)
	if form.is_valid():
		form.save()
		messages.success(request,f'Successfully Updated')
		return HttpResponseRedirect(reverse('homeo_book_update_redline',kwargs={'id':id}))

	return render(request,'COMMON_APP/homeo_book_update_disease.html',{'form':form})

@csrf_exempt
def home_book_delete_redline(request,id):

	data = HomeBookRedline.objects.get(id=id).delete()
	messages.success(request,f'Deleted Successfully')
	return redirect('home_book_redline_symptoms')



# def place_order_doctor_mail(request,id):

# 	order_temp = PlaceOrderDoctor.objects.get(id=id)

# 	# print("order",order_temp.vendors.email)
# 	orders_list = []
# 	orders_date_wise = PlaceOrderDoctor.objects.filter(Q(order_date=order_temp.order_date) & Q(vendors=order_temp.vendors))
# 	if orders_date_wise:
# 		orders_list.append(orders_date_wise)

# 	# print("LIST :",orders_list)
# 	template =  render_to_string('COMMON_APP/place_order_doctor_mail.html',{'orders_list':orders_list})
# 	email_id = order_temp.vendors.email
# 	mylist = []
# 	mylist.append(email_id)

# 	email = EmailMessage(
# 		'Order Placed Details',
# 		template,
# 		settings.EMAIL_HOST_USER,
# 		mylist
# 	)

# 	email.fail_silently = True
# 	email.send()
# 	for order in orders_date_wise:
# 		flag = order
# 		flag.email_status = True
# 		flag.save()
# 	messages.success(request,f'Mail Successfully Sent')
# 	return redirect('place_new_order_doctor')

# def new_order_history(request):

# 	status = False
# 	if request.user:
# 		status = request.user

# 	find_branch = Receptionist.objects.get(username=status)

# 	orders = PlaceOrderDoctor.objects.filter(branch=find_branch.branch)
# 	order_date_temp = []
# 	order_vendor_temp = []
# 	for data in orders:
# 		order_date_temp.append(data.order_date)
# 		order_vendor_temp.append(data.vendors)

# 	orders_list = []

# 	for dat in list(set(order_date_temp)):
# 		for ven in list(set(order_vendor_temp)):
# 			orders_date_wise = PlaceOrderDoctor.objects.filter(Q(order_date=dat) & Q(vendors=ven))
# 			if orders_date_wise:
# 				orders_list.append(orders_date_wise)


	
# 	context = {
# 		'status':status,
# 		'user':'R',
# 		'orders_list':orders_list,
# 	}


# 	return render(request,'COMMON_APP/new_order_history.html',context)
@method_decorator(csrf_exempt, name='dispatch')
class Homeo_pdf(View):

	def get(self,request,*args,**kwargs):
		pre_url = request.META.get('HTTP_REFERER')
		obj =pre_url.split('/')

		if obj[3] == 'homeo-book-medicine':
			medicine_detail = HomeBookMedicine.objects.all().order_by('medicine_name')
			data = {
				'header': 'Medicines Description',
				'medicine_detail':medicine_detail,
			}			
			pdf= render_to_pdf('COMMON_APP/home_pdf.html',data)
			return HttpResponse(pdf, content_type='application/pdf')
		elif obj[3] == 'homeo-book-disease':
			disease_detail = HomeBookDisease.objects.all().order_by('disease_name')	
			data = {
				'header': 'Diseases Description',
				'disease_detail':disease_detail,
			}
			pdf= render_to_pdf('COMMON_APP/home_pdf.html',data)
			return HttpResponse(pdf, content_type='application/pdf')
		elif obj[3] == 'homeo-book-redline-symptoms':
			disease_detail = HomeBookRedline.objects.all().order_by('redline_symptoms')
			data = {
				'header': 'Redline Symptoms Description',
				'redline_detail':disease_detail,
			}
			pdf= render_to_pdf('COMMON_APP/home_pdf.html',data)
			return HttpResponse(pdf, content_type='application/pdf')

@method_decorator(csrf_exempt, name='dispatch')
class Homeo_pdf_id(View):

	def get(self,request,*args,**kwargs):
		id =  self.kwargs['id']
		pre_url = request.META.get('HTTP_REFERER')		
		obj =pre_url.split('/')
		
		if obj[3] == 'homeo-book-medicine':
			medicine_detail = HomeBookMedicine.objects.filter(id=id)
			data = {
				'header': 'Medicines Description',
				'medicine_detail':medicine_detail,
			}			
			pdf= render_to_pdf('COMMON_APP/home_pdf.html',data)
			return HttpResponse(pdf, content_type='application/pdf')
		elif obj[3] == 'homeo-book-disease':
			disease_detail = HomeBookDisease.objects.filter(id=id)
			data = {
				'header': 'Diseases Description',
				'disease_detail':disease_detail,
			}
			pdf= render_to_pdf('COMMON_APP/home_pdf.html',data)
			return HttpResponse(pdf, content_type='application/pdf')
		elif obj[3] == 'homeo-book-redline-symptoms':
			disease_detail = HomeBookRedline.objects.filter(id=id)
			data = {
				'header': 'Redline Symptoms Description',
				'redline_detail':disease_detail,
			}
			pdf= render_to_pdf('COMMON_APP/home_pdf.html',data)
			return HttpResponse(pdf, content_type='application/pdf')

@csrf_exempt
def assign_tasks(request):

	if request.method == 'POST':
		form = AssignTaskForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			messages.success(request,f'Assigned Task Successfully to {instance.assign_To} ')
			instance.save()
			return redirect('assign_tasks')
	else:
		form = AssignTaskForm()
	
	task_details = AssignTask.objects.all().order_by('-created_at')
	context = {
		'form':form,
		'task_details':task_details}
	

	return render(request,'COMMON_APP/assign_tasks.html',context)

@csrf_exempt
def delete_task(request,id):

	data = AssignTask.objects.get(id=id)
	data.delete()
	messages.success(request,f'Task Successfully Deleted')
	return redirect('assign_tasks')
@csrf_exempt
def task_details(request):

	status = False
	if request.user:
		status = request.user

	task_details = AssignTask.objects.filter(assign_To=status)

	return render(request,'COMMON_APP/task_details.html',{'task_details':task_details})

@csrf_exempt
def task_complete(request,id):

	task =  AssignTask.objects.get(id=id)
	task.completed = True
	task.save()
	messages.success(request,f'Task Completed Successfully!')
	return redirect('task_details')

@csrf_exempt
def place_new_order_medicine(request):

	PlacedOrderFormSet = modelformset_factory(PlacedOrderMedicine, form=PlacedOrderMedicineForm,extra=1)

	if request.method == 'POST':
		formset = PlacedOrderFormSet(request.POST, queryset=PlacedOrderMedicine.objects.none())
		if formset.is_valid():
			formset.save()
			messages.success(request,f'Orders Placed Successfully')
			return redirect('place_new_order_medicine')
		else:
			messages.success(request,f'Fill the form details')

	else:
		formset = PlacedOrderFormSet(queryset=PlacedOrderMedicine.objects.none())

	context = {
		'formset':formset,
	}
	

	return render(request,'COMMON_APP/place_new_order_medicine.html',context)

from django.db.models.functions import ExtractMonth, ExtractYear
import calendar
@csrf_exempt
def apply_leave(request):

	status = False
	if request.user:
		status = request.user

	app_user = User.objects.get(username=request.user)
	print('app_user',app_user)



	if request.method == 'POST':
		form = LeaveRequestForm(request.POST,initial={'staff':app_user})
		if form.is_valid():
			form.save()
			messages.success(request,"Leave Applied Successfully, Approval Status Pending")
			return redirect('apply_leave')
	else:
		form = LeaveRequestForm(initial={'staff':app_user})


	leave_details = LeaveRequest.objects.filter(staff=app_user).order_by('-id')
	# print("Leave_details",leave_details)

	data = LeaveRequest.objects.filter(Q(staff=status) & Q(is_approved=True))

	leaves_data = data.annotate(year=ExtractYear('start_date'), month=ExtractMonth('start_date')).values('year', 'month').annotate(total_duration=models.Sum('duration')).order_by('year', 'month')	
	month_names = {i: calendar.month_name[i] for i in range(1, 13)}
	for data in leaves_data:
		data['month'] = month_names.get(data['month'])

	items_per_page = 10
	paginator = Paginator(leave_details, items_per_page)
	page_number = request.GET.get('page')
	page = paginator.get_page(page_number)

	items_per_page_two = 12
	paginator_two = Paginator(leaves_data, items_per_page_two)
	page_number_two = request.GET.get('page')
	page_two = paginator_two.get_page(page_number_two)

	context = {
		'form':form,
		'leave_details':leave_details,
		'leaves_data':leaves_data,
		'page':page,
		'page_two':page_two,
	}

	return render(request,'COMMON_APP/apply_leave.html',context)

@csrf_exempt
def approve_leaves(request):

	leave_details = LeaveRequest.objects.all().order_by('-id')
	items_per_page = 10
	paginator = Paginator(leave_details, items_per_page)
	page_number = request.GET.get('page')
	page = paginator.get_page(page_number)

	return render(request,'COMMON_APP/approve_leaves.html',{'page':page})

@csrf_exempt
def is_approved_leave(request,id):

	data = LeaveRequest.objects.get(id=id)
	data.is_approved = True
	data.save()
	messages.success(request,f'Leave Approved')
	return redirect('approve_leaves')

@csrf_exempt
def leave_details(request,user):

	app_user = User.objects.get(username=user)

	leave_detail = LeaveRequest.objects.filter(staff=app_user).order_by('-id')

	data = LeaveRequest.objects.filter(Q(staff=app_user) & Q(is_approved=True))
	leaves_data = data.annotate(year=ExtractYear('start_date'), month=ExtractMonth('start_date')).values('year', 'month').annotate(total_duration=models.Sum('duration')).order_by('year', 'month')	
	month_names = {i: calendar.month_name[i] for i in range(1, 13)}
	for data in leaves_data:
		data['month'] = month_names.get(data['month'])

	items_per_page = 10
	paginator = Paginator(leave_detail, items_per_page)
	page_number = request.GET.get('page')
	page = paginator.get_page(page_number)

	items_per_page_two = 12
	paginator_two = Paginator(leaves_data, items_per_page_two)
	page_number_two = request.GET.get('page')
	page_two = paginator_two.get_page(page_number_two)	

	context = {
		'user':user,
		'page':page,
		'page_two':page_two,
	}

	return render(request,'COMMON_APP/leave_details_doc.html',context)

@csrf_exempt
def doctor_diagnose_history(request):

	status = False
	if request.user:
		status =  request.user
	
	query = request.GET.get('query')

	if query:    
            data = prescription.objects.filter( Q(diagnose__icontains=query) | Q(medicine__icontains=query) | Q(patientid__case__icontains=query.upper()))

	else:
		data = ""

	context = {
		'status':status,
		'user':'D',		
		'data':data,
		
	}

	return render(request,'COMMON_APP/doctor_diagnose_history_adjust.html',context)

@method_decorator(csrf_exempt, name='dispatch')
class Doctor_diagnose_pdf(View):

	def get(self,request,*args,**kwargs):

		query = request.GET.get('query')
		if query:
			data = prescription.objects.filter(Q(diagnose__icontains=query) | Q(medicine__icontains=query) | Q(patientid__case__icontains=query.upper()))
		else:
			data = []
		
		context = {'data':data}
		pdf = render_to_pdf('COMMON_APP/doctor_diagnose_pdf.html',context)
		return HttpResponse(pdf, content_type='application/pdf')

@method_decorator(csrf_exempt, name='dispatch')
class Doctor_pdf(View):

	def get(self,request,*args,**kwargs):
		pk = self.kwargs['pk']

		data = prescription.objects.filter(patientid__id=pk).order_by('-date')
		history_details = ExampleModel.objects.filter(patient_id=pk).order_by('-signature_date')
		present_complaints = PresentComplaintsNew.objects.filter(patient__id=pk)
		obj_chief_complaints = NewCaseModel.objects.filter(Q(patient_id=pk) & Q(category=7) )
		past_history = PatientHistoryNEW.objects.filter(Q(patient__id=pk) )
		question = Question1.objects.filter(category__id=9)
		obj_personal_history = NewCaseModel.objects.filter(Q(patient_id=pk) & Q(category=9))
		table_data = FamilyMedicalHistory.objects.filter(Q(patient__id=pk))
		my_list = []
		for t in table_data:
			x = t.list_of_disease
			x = x.replace("[","").replace("'","").replace("]","")
			my_list.append(x)
		
		zipped_list = zip(table_data,my_list)

		table_data1 = MentalCausativeRecord.objects.filter(Q(patient__id=pk) )
		my_list1 = []
		for t in table_data1:
			x = t.factors
			x = x.replace("[","").replace("'","").replace("]","")
			my_list1.append(x)		

		table_data2 = MentalPersonalityRecord.objects.filter(Q(patient__id=pk) )
		my_list2 = []
		for t in table_data2:
			x = t.characters
			x = x.replace("[","").replace("'","").replace("]","")
			my_list2.append(x)

		mental_personality = NewCaseModel.objects.filter(Q(patient_id=pk) & Q(category=11))
		bms_question = Question1.objects.filter(category__id=12)
		bms_view = NewCaseModel.objects.filter(Q(patient_id=pk) & Q(category=12))

		thermal_question = Question1.objects.filter(category__id=13)
		thermal_view = obj = NewCaseModel.objects.filter(Q(patient_id=pk) & Q(category=13))

		table_data3 =MiasmRecords.objects.filter(Q(patient__id=pk))
		my_list3 = []
		for t in table_data3:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list3.append(x)

		table_data4 =ThermalReactionRecords.objects.filter(Q(patient__id=pk))
		my_list4 = []
		for t in table_data4:
			x = t.records
			x = x.replace("[","").replace("'","").replace("]","")
			my_list4.append(x)	
		mental_caustative = NewCaseModel.objects.filter(Q(patient_id=pk) & Q(category=10))
		context = {
			'pk':pk,
			'data':data,
			'history_details':history_details,
			'table1':present_complaints,
                'table2':obj_chief_complaints,
                'table3': past_history,
                'question':question,
                'personal_history':obj_personal_history,
                'list':zipped_list,
                'my_list1':my_list1,
                'mental':mental_caustative,
                'my_list2':my_list2,
                'personality':mental_personality,
                'bms':bms_question,
                'bms_view':bms_view,
                'thermal':thermal_question,
                'thermal_view':thermal_view,
                'my_list3':my_list3,                
                'my_list4':my_list4,
                
		
		}

		pdf = render_to_pdf('COMMON_APP/doctor_pdf.html',context)
		return HttpResponse(pdf, content_type='application/pdf')		