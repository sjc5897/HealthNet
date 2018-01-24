from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import View
from django.utils import timezone
import operator
from .models import *
from .forms import *
from django.db.models import Q

"""
This creates the index/homepage of Healthnet.
This is where initial navigation happens
"""
def index(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return redirect('home:administrator')
        if request.user.user_type() == 'doctor':
            return redirect('home:dDetail',request.user.username)
        if request.user.user_type() == 'nurse':
            return redirect('home:nDetail',request.user.username)
        if request.user.user_type() == 'patient':
            return redirect('home:pDetail',request.user.username)
    else:
        return render(request, "home/indexes/NotLogged.html")

#======List Views=======================================================================================================
"""
A Class representing a generic list of all patients in the system
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
def PatientView(request):
   template_name = 'home/patient/patient.html'
   if request.user.is_authenticated():
       user_type = request.user.user_type()
       if user_type == 'doctor':
           doctor = Doctor.objects.filter(user = request.user)
           doctor = doctor[0]
           hospital_name = doctor.hospital.name
           context = Patient.objects.filter(hospital = doctor.hospital)
       elif user_type == 'nurse':
           nurse = Nurse.objects.filter(user=request.user)
           nurse = nurse[0]
           hospital_name = nurse.hospital.name
           context = Patient.objects.filter(hospital=nurse.hospital)
       elif user_type == 'patient':
           user = Patient.objects.filter(user=request.user)
           user = user[0]
           hospital_name = user.hospital.name
           context = Patient.objects.filter(hospital=user.hospital)
       else:
           context = Patient.objects.all()
           hospital_name = None
       return render(request, template_name,{'hospital': hospital_name, 'patient_list': context.order_by('last_name'), 'search':False})
   else:
       return render(request, 'home/indexes/NotLogged.html')

"""
A Class representing a generic list of all admin in the system
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
class AdministratorView(generic.ListView):
    template_name = 'home/administrator.html'
    context_object_name = "administrator_list"
    """
    This method gets and returns all administrators
    """
    def get_queryset(self):
        return User.objects.filter(is_superuser = True)
"""
A Class representing a generic list of all Doctors in the system
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
def DoctorView(request):
    if request.user.is_authenticated():
        user_type = request.user.user_type()
        if user_type == 'doctor' or request.user.is_superuser:
            context = Doctor.objects.all()
            return render(request, 'home/doctor/doctor.html',
                          {'hospital': None, 'doctor_list': context, 'search': False})
        elif user_type == 'nurse':
            nurse = Nurse.objects.filter(user=request.user)
            if nurse:
                nurse = nurse[0]
                hospital_name = nurse.hospital.name
                context = Doctor.objects.filter(hospital=nurse.hospital)
            else:
                return Http404
        elif user_type == 'patient':
            user = Patient.objects.filter(user=request.user)
            if user:
                user = user[0]
                hospital_name = user.hospital.name
                context = Doctor.objects.filter(hospital=user.hospital)
            else:
                return Http404
        else:
            context = Patient.objects.all()
            hospital_name = None
        return render(request, 'home/doctor/doctor.html', {'hospital': hospital_name, 'doctor_list': context.order_by('last_name'), 'search': False})
    else:
        return render(request, 'home/indexes/NotLogged.html')
"""
A Class representing a generic list of all Nurses in the system
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
def NurseView(request):
    if request.user.is_authenticated():
        user_type = request.user.user_type()
        if request.user.is_superuser:
            context = Nurse.objects.all()
            return render(request, 'home/nurse/nurse.html',
                          {'hospital': None, 'nurse_list': context, 'search': False})
        elif user_type == 'doctor':
            user = Doctor.objects.filter(user=request.user)
            if user:
                user = user[0]
                context = Nurse.objects.filter(hospital = user.hospital)
                hospital_name = user.hospital.name
            else:
                return Http404
        elif user_type == 'nurse':
            nurse = Nurse.objects.filter(user=request.user)
            if nurse:
                nurse = nurse[0]
                hospital_name = nurse.hospital.name
                context = Nurse.objects.filter(hospital=nurse.hospital)
            else:
                return Http404
        elif user_type == 'patient':
            user = Patient.objects.filter(user=request.user)
            if user:
                user = user[0]
                hospital_name = user.hospital.name
                context = Nurse.objects.filter(hospital=user.hospital)
            else:
                return Http404
        else:
            context = Patient.objects.all()
            hospital_name = None
        return render(request, 'home/nurse/nurse.html', {'hospital': hospital_name, 'nurse_list': context.order_by('last_name'), 'search': False})
    else:
        return render(request, 'home/indexes/NotLogged.html')

class HospitalView(View):
    template_name = 'home/hospital.html'
    def get(self,request):
        if request.user.is_authenticated():
            if request.user.user_type() == 'doctor' or request.user.user_type() == 'nurse':
                if request.user.user_type() == 'doctor':
                    owner = Doctor.objects.get(user = request.user)
                elif request.user.user_type() == 'nurse':
                    owner = Nurse.objects.get(user=request.user)
                return render(request,self.template_name,{'owner': owner})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, "home/indexes/NotLogged.html")
"""
A Class representing a generic list of all Activities in the Activity Log
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
def ActivityView(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            today = timezone.now()
            template_name = 'home/activities.html'
            activities = Activity.sortTable(Activity)
            context = {
                "activity_list": activities
            }
            return render(request,template_name,context)
        else:
            return render(request, 'home/indexes/InvalidPer.html')
    else:
        return render(request, "home/indexes/NotLogged.html")

class PrescriptionView(View):
    template_name = "home/prescription/prescriptionList.html"

    def get(self,request,username):
        if request.user.is_authenticated():
            user = Patient.objects.filter(username = username)[0]
            if request.user.user_type() == 'nurse' or request.user.user_type()=='doctor' or request.user.username == username:
                prescription=  Prescription.objects.filter(user_ID = user)
                return render(request,self.template_name, {"prescription_list":prescription})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, "home/indexes/NotLogged.html")
class MessagesView(View):
    def get(self,request):
        if request.user.is_authenticated:
            Receiver_ID = request.user.username
            message_list = Messages.objects.filter(Receiver_ID=Receiver_ID)
            message_list = message_list.filter(ReceiverDelete = False).order_by('-timestamp')
            return render(request, "home/messages/messages.html",{'message_list':message_list})
        else:
            return render(request, "home/indexes/NotLogged.html")

def OutboxView(request):
    Sender_ID = request.user.username
    message_list = Messages.objects.filter(Sender_ID=Sender_ID)
    message_list = message_list.filter(SenderDelete = False).order_by('-timestamp')
    return render(request, "home/messages/outbox.html",{'message_list':message_list})

def Delete(request,message_id):
    message = get_object_or_404(Messages,pk = message_id)
    message.deleteMsg(request.user.username)
    return redirect('home:messages')

def HospitalList(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            Hospital_list = Hospital.objects.all()
            return render(request,'home/hopsitalList.html',{"Hospital_list":Hospital_list.order_by('name')})
        else:
            return render(request, 'home/indexes/InvalidPer.html')
    else:
        return render(request, "home/indexes/NotLogged.html")
class HospitalEdit(View):
    def get(self,request,hospital_id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                h = get_object_or_404(Hospital,pk = hospital_id)
                form = editHospitalForm(initial= {'address':h.address,'city':h.city,'zip':h.zip,'state':h.state})
                return render(request,'home/hospitalEdit.html',{'hospital_form':form,'h':h})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, "home/indexes/NotLogged.html")
    def post(self,request,hospital_id):
        h = get_object_or_404(Hospital, pk=hospital_id)
        form = editHospitalForm(request.POST)
        if form.is_valid():
            form_clean = form.cleaned_data
            h = h.edit(form_clean)
            Activity.createActivity(timezone.now(),"edited hospital",h,request.user.username,h,"")
            return redirect('home:hospitalList')
        else:
            return render(request, 'home/hospitalEdit.html', {'hospital_form': form, 'h':h})

def DrugList(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'patient':
            return render(request, 'home/indexes/InvalidPer.html')
        else:
            d = Drug.objects.all()
            return render(request,'home/prescription/DrugList.html',{'drug_list':d})
    else:
        return render(request, "home/indexes/NotLogged.html")
class DrugEdit(View):
    def get(self,request,drug_id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                d = get_object_or_404(Drug,pk=drug_id)
                form = editDrugForm(initial={'price':d.price})
                return render(request,'home/prescription/EditDrug.html',{'form':form,'d':d})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, "home/indexes/NotLogged.html")
    def post(self,request,drug_id):
        d = get_object_or_404(Drug, pk=drug_id)
        form = editDrugForm(request.POST)
        if form.is_valid():
            form_clean = form.cleaned_data
            d.updatePrice(form_clean['price'],request.user.username)
            return redirect('home:drugList')
        else:
            return render(request, 'home/prescription/EditDrug.html', {'form': form})
def deleteDrug(request,drug_id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            d = get_object_or_404(Drug,pk = drug_id)
            Activity.createActivity(timezone.now(),'deleted drug',d.name,request.user.username,None,"")
            d.delete()
            return redirect('home:drugList')
        else:
            return render(request, 'home/indexes/InvalidPer.html')
    else:
        return render(request, "home/indexes/NotLogged.html")

class EditNurse(View):
    temlt = 'home/nurse/editNurse.html'
    def get(self,request,username):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                n = Nurse.objects.filter(username = username)
                if n:
                    n = n[0]
                    user_form = UserEditForm(initial={'first_name':n.first_name, 'email':n.user.email,'last_name':n.user.last_name})
                    nurse_form = NurseForm(initial={'hospital':n.hospital,'phone':n.phone})
                    return render(request,self.temlt,{'user_form':user_form,'nurse_form':nurse_form,'n':n})
                else:
                    return Http404
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, "home/indexes/NotLogged.html")
    def post(self,request,username):
        user_form = UserEditForm(request.POST)
        nurse_form = NurseForm(request.POST)
        n = Nurse.objects.filter(username=username)[0]
        if user_form.is_valid() and nurse_form.is_valid():
            user_clean = user_form.cleaned_data
            nurse_clean = nurse_form.cleaned_data
            n = n.edit(nurse_clean, user_clean)
            Activity.createActivity(timezone.now(),'edited nurse profile',n.username,request.user.username,n.hospital,"")
            return redirect('home:nDetail',n.username)
        else:
            return render(request, self.temlt, {'user_form': user_form, 'nurse_form': nurse_form, 'n': n})
class EditDoctor(View):
    temlt = 'home/doctor/editDoctor.html'
    def get(self, request, username):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                d = Doctor.objects.filter(username=username)
                if d:
                    d=d[0]
                    user_form = UserEditForm(
                        initial={'first_name': d.first_name, 'email': d.user.email, 'last_name': d.user.last_name})
                    doctor_form = DoctorForm(initial={'hospital': d.hospital, 'phone': d.phone,'specialty':d.specialty,
                                             'office_hours_start':d.office_hours_start,'office_hours_end':d.office_hours_end,'office':d.office})
                    return render(request, self.temlt, {'user_form': user_form, 'doctor_form': doctor_form, 'd': d})

                else:
                    return Http404
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, "home/indexes/NotLogged.html")

    def post(self, request, username):
        user_form = UserEditForm(request.POST)
        Doctor_form = DoctorForm(request.POST)
        d = Doctor.objects.filter(username=username)[0]
        if user_form.is_valid() and Doctor_form.is_valid():
            user_clean = user_form.cleaned_data
            Doctor_clean = Doctor_form.cleaned_data
            d = d.edit(Doctor_clean,user_clean)
            Activity.createActivity(timezone.now(), 'edited doctor profile', d.username, request.user.username,
                                    d.hospital, "")
            return redirect('home:dDetail', d.username)
        else:
            return render(request, self.temlt, {'user_form': user_form, 'doctor_form': Doctor_form, 'd': d})
#======End List Views===================================================================================================

#======Detail Views=====================================================================================================
"""
This view is used when a user clicks on a patient's username
It gets all relevant User information and renders it using the context below
:arg
    patient_id: The id number of the patient, used to gather the information
:returns: a render of the user information page
"""
def pDetail(request,username):
    if request.user.is_authenticated():
        patient = Patient.objects.filter(username=username)
        if patient:
            patient = patient[0]
            if request.user.user_type() == 'nurse':
                n = Nurse.objects.filter(username = request.user.username)[0]
                if n.hospital != patient.hospital:
                    return render(request, 'home/indexes/InvalidPer.html')
            #gets the patient
            phone = patient.contact.phone
            phone = "%s%s%s-%s%s%s-%s%s%s%s" % tuple(phone) #formats phone
            weight = patient.medical.weight + " lb"
            #these 4 lines are used to format the hieght
            height1 = patient.medical.height_feet +"'"
            height2 = str(patient.medical.height_inches) +'"'
            context = {
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'username': patient.username,
                'DOB': patient.DOB,
                'address': patient.contact.address,
                'city': patient.contact.city,
                'state': patient.contact.state,
                'zip': patient.contact.zip,
                'phone': phone,
                'email': patient.user.email,
                'patient': patient,
                'weight': weight,
                'height1': height1,
                'height2': height2
            }
            Activity.createActivity(timezone.now(), " viewed information for ", patient.username, request.user, patient.hospital, "ViewInformation")
            return render(request, "home/patient/patientDetail.html", context)
        else:
            return Http404
    else:
        return render(request, 'home/indexes/NotLogged.html')
"""
This View is used to when a user clicks a Doctor's ID number
This displays all relevant class information
:arg
    doctor_id: the id number of the doctor
:returns: a render of the doctors info
"""
def dDetail(request,username):
    if request.user.is_authenticated():
        doctorUser = User.objects.filter(username = username)
        doctor = Doctor.objects.filter(user = doctorUser)
        if doctor:
            doctor = doctor[0]
            if request.user.user_type() == 'nurse':
                n = Nurse.objects.filter(username = request.user.username)[0]
                if n.hospital != doctor.hospital:
                    return render(request, 'home/indexes/InvalidPer.html')
            phone = doctor.phone
            phone = "%s%s%s-%s%s%s-%s%s%s%s" % tuple(phone)  # formats phone
            return render(request,"home/doctor/doctorDetail.html", {'doctor': doctor, 'phone': phone})
        else:
            raise Http404
    else:
        return render(request, 'home/indexes/NotLogged.html')
"""
This View is used to when a user clicks on a scheduled appointment
This displays all relevant class information
:arg
    appointment_id: the appointment's identification number
:returns: a render of the appointment information
"""
def AppointmentDetail(request, appointment_id):
    if request.user.is_authenticated():
        appointment = get_object_or_404(Appointment,pk = appointment_id)
        doctorUser = User.objects.filter(username = appointment.doctor_ID )
        doctor = Doctor.objects.filter(user = doctorUser)[0]
        patient = Patient.objects.filter(username = appointment.patient_ID)[0]
        if request.user.user_type() == 'nurse' or request.user.username == patient.username or request.user.username == doctor.user.username:
            return render(request,"home/appointment/aDetail.html",context={"app": appointment, 'doc': doctor, "patient": patient})
        else:
            return render(request, 'home/indexes/InvalidPer.html')
    else:
        return render(request, 'home/indexes/NotLogged.html')
"""
This View is used to when a user clicks a Nurse's ID number
This displays all relevant class information
:arg
    nurse_id: the id number of the doctor
:returns: a render of the nurse's info
"""
def nDetail(request,username):
    if request.user.is_authenticated():
        nurseU = User.objects.filter(username = username)
        nurse = Nurse.objects.filter(user = nurseU)
        if nurse:
            nurse = nurse[0]
            phone = nurse.phone
            phone = "%s%s%s-%s%s%s-%s%s%s%s" % tuple(phone)  # formats phone
            return render(request,"home/nurse/nDetail.html", {'nurse': nurse, 'phone': phone})
        else:
            return Http404
    else:
        return render(request, 'home/indexes/NotLogged.html')

class PrescriptionDetail(View):
    template_name = "home/prescription/prescriptionDetail.html"

    def get(self, request, prescription_id):
        prescription = get_object_or_404(Prescription, pk = prescription_id)
        if request.user.is_authenticated():
            if request.user.user_type()=='doctor' or request.user.user_type() == 'nurse' or request.user.username == prescription.user_ID.username:
                price = prescription.drug.price * prescription.quantity
                timeRefill = prescription.lastRefill + timezone.timedelta(days=30)
                showRefill = timeRefill < timezone.now()
                isExpired  = prescription.expiration < timezone.now()
                return render(request, self.template_name,
                              {"price":price                          , "timeRefill":timeRefill,
                               "showRefill":showRefill                , "prescription":prescription,
                               "patient":prescription.user_ID.username, "isExpired":isExpired})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')
class MessageDetail(View):
    template_name = "home/messages/messageDetail.html"
    def get(self,request, message_id):
        if request.user.is_authenticated():
            message = get_object_or_404(Messages,pk=message_id)
            if request.user.username == message.Sender_ID or request.user.username == message.Receiver_ID:
                return render(request,self.template_name,{"message":message})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

class MessageDetail2(View):
    template_name = "home/messages/messageDetail2.html"
    def get(self,request, message_id):
        if request.user.is_authenticated():
            message = get_object_or_404(Messages,pk=message_id)
            if request.user.username == message.Receiver_ID or request.user.username == message.Sender_ID:
                return render(request,self.template_name,{"message":message})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')


#======End Detail Views=================================================================================================

#======Registration and Update Views====================================================================================
"""
This view represents the registration, which is used to register a new user (patient)
"""
class RegistrationForm(View):
    template_name='home/patient/register.html'
    # Displays signup form
    def get(self,request):
        if request.user.is_authenticated():
            user_form= UserForm
            patient_form = PatientUserForm()
            if request.user.user_type() == 'doctor':
                d = Doctor.objects.filter(username = request.user.username)[0]
                patient_form.fields['hospital'].queryset = Hospital.objects.filter(name = d.hospital.name)
            elif request.user.user_type() == 'nurse':
                d = Nurse.objects.filter(username=request.user.username)[0]
                patient_form.fields['hospital'].queryset = Hospital.objects.filter(name = d.hospital.name)
            contact_form = ContactUserForm
            medical_form = MedicalUserForm
            return render(request, self.template_name,{'user_form': user_form, 'patient_form': patient_form, 'contact_form':contact_form, 'medical_form': medical_form})
        else:
            user_form = UserForm()
            patient_form = PatientUserForm()
            patient_form.fields['hospital'].queryset = Hospital.objects.all()
            contact_form = ContactUserForm()
            medical_form = MedicalUserForm()
            return render(request, self.template_name,
                          {'user_form': user_form, 'patient_form': patient_form, 'contact_form': contact_form,
                           'medical_form': medical_form})

    #regesters a user
    def post(self,request):
        user_form = UserForm(request.POST)
        patient_form = PatientUserForm(request.POST)
        contact_form = ContactUserForm(request.POST)
        medical_form = MedicalUserForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid() and contact_form.is_valid() and medical_form.is_valid():
            user_form_cleaned =  user_form.cleaned_data
            patient_form_cleaned = patient_form.cleaned_data
            contact_form_cleaned = contact_form.cleaned_data
            medical_form_cleaned  = medical_form.cleaned_data
            patient = Patient.createPatient(user_form_cleaned, patient_form_cleaned, contact_form_cleaned, medical_form_cleaned,request.user.username)
            patient.save()
            if request.user.is_authenticated():
                return redirect('home:pDetail', patient.username)
            else:
                return redirect('home:login')
        else:
            return render(request, self.template_name, {'user_form': user_form, 'patient_form': patient_form, 'contact_form': contact_form, 'medical_form': medical_form})

class DoctorReg(View):
    template_name = 'home/doctor/registration.html'
    def get(self, request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                user_form = UserForm()
                doctor_form = DoctorForm()
                return render(request, self.template_name, {'user_form': user_form, 'doctor_form':doctor_form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self,request):
        user_form = UserForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user_form_clean = user_form.cleaned_data
            doctor_form_clean = doctor_form.cleaned_data
            doctor = Doctor.createDoctor(user_form_clean,doctor_form_clean,request.user)
            return redirect('home:dDetail', doctor.username)
        else:
            return render(request, self.template_name, {'user_form': user_form, 'doctor_form': doctor_form})

class NurseReg(View):
    template_name = 'home/nurse/registration.html'
    def get(self,request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                user_form = UserForm()
                nurse_form = NurseForm()
                return render(request, self.template_name, {'user_form': user_form, 'nurse_form':nurse_form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self, request):
        user_form = UserForm(request.POST)
        nurse_form = NurseForm(request.POST)
        if user_form.is_valid() and nurse_form.is_valid():
            user_form_clean = user_form.cleaned_data
            nurse_form_clean = nurse_form.cleaned_data
            nurse = Nurse.createNurse(user_form_clean, nurse_form_clean, request.user)
            return redirect('home:nDetail', nurse.username)
        else:
            return render(request, self.template_name, {'user_form': user_form, 'nurse_form': nurse_form})

class AdminReg(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                form = UserForm
                return render(request,'home/AdminReg.html',{'form':form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self,request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_clean = user_form.cleaned_data
            admin = User.objects.create_superuser(user_clean['username'],user_clean['email'],user_clean['password'])
            admin.save()
            Activity.createActivity(timezone.now(),'created new admin:',admin, request.user,None,"AdminCreation")
            return redirect('home:administrator')
        else:
            return render(request, 'home/AdminReg.html', {'form': user_form})
"""
This view represents the contact edit, which is used to edit a user's contact information
:atrb: template_name    the name/location of the html template associated with updating the user's contact info
"""
class ContactEditForm(View):
    template_name = 'home/patient/contactU.html'

    def get(self,request,patient_id):
        if request.user.is_authenticated():
            patient = get_object_or_404(Patient, pk=patient_id)
            if request.user.username == patient.username:
                contact_form = ContactUserForm(initial={
                    "address": patient.contact.address, "city": patient.contact.city, "state": patient.contact.state,
                    "zip": patient.contact.zip, 'phone': patient.contact.phone})
                return render(request, self.template_name,{'contact_form': contact_form, 'patient': patient})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self,request,patient_id):
            patient = get_object_or_404(Patient, pk=patient_id)
            contact_form = ContactUserForm(request.POST)
            if contact_form.is_valid():
                contact_form_clean = contact_form.cleaned_data
                patient = patient.UpdateContact(contact_form_clean,request.user.username)
                patient.save()
                return redirect('home:pDetail', patient.user.username)
            else:
                return render(request, self.template_name,
                              {'contact_form': contact_form, 'patient': patient})
"""
This view represents the medical edit, which is used to edit a user's medical information
:atrb: template_name    the name/location of the html template associated with updating the user's medical info
"""
class MedicalEditForm(View):
    template_name = 'home/patient/updateM.html'

    def get(self, request, patient_id):
        if request.user.is_authenticated:
            if request.user.user_type()=='doctor' or request.user.user_type()=='nurse':
                patient = get_object_or_404(Patient, pk=patient_id)
                medical_form = MedicalUserForm(initial={
                    "sex": patient.medical.sex, "height_feet": patient.medical.height_feet,"height_inches": patient.medical.height_inches, "weight": patient.medical.weight,
                    "blood_Type": patient.medical.blood_Type})
                return render(request, self.template_name, {'medical_form': medical_form, 'patient': patient})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self, request, patient_id):
        # if request.user.is_authenticated:
        patient = get_object_or_404(Patient, pk=patient_id)
        medical_form = MedicalUserForm(request.POST)
        if medical_form.is_valid():
            medical_form_clean = medical_form.cleaned_data
            patient = patient.UpdateMedical(medical_form_clean,request.user.username)
            patient.save()
            return redirect('home:pDetail', patient.user.username)
        else:
            return render(request, self.template_name,
                          {'medical_form': medical_form, 'patient': patient})


#======End Registration and Update Views================================================================================

#======Login and Logout Views===========================================================================================
"""
This view represents the login page, which is used to log in to a user's profile
:atrb: template_name    the name/location of the html template associated with the user login page
"""
class LoginView(View):
    template_name = 'home/login/login.html'
    def get(self,request):
        login_info = LoginForm()
        return render(request,self.template_name,{'form': LoginForm})
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        HttpResponse()
        user = authenticate(username = username,password = password)
        if user is not None:
            Activity.createActivity(timezone.now(), "Logged in:",username, "", None, "LogIn")
            login(request,user)
            return redirect('home:index')
        else:
            return render(request,'home/login/failure.html',{'login_form':LoginForm})
"""
This view represents the logout function, which is used to log out of a user's profile
"""
class LogOutView(View):
    def get(self,request):
        Activity.createActivity(timezone.now(), "Logged out:", request.user.username, "", None, "LogOut")
        logout(request)
        return redirect('home:index')
#======End Login and Logout Views=======================================================================================
#======Start of Appoinment Views========================================================================================
"""
This view represents the creation of a new appointment
:atrb: template_name    the html appointment form
"""
class newAppointment(View):
    template_name = 'home/appointment/appointmentForm.html'
    def get(self,request,username):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                return render(request, 'home/indexes/InvalidPer.html')
            else:
                user = User.objects.filter(username = username)
                owner = Doctor.objects.filter(user = user)
                oT = 'd'
                if len(owner) == 0:
                    oT = 'p'
                    owner = Patient.objects.filter(user = user)
                    if len(owner) == 0:
                        raise Http404("User doesn't exist")
                    else:
                        owner = owner[0]
                else:
                    owner = owner[0]
                user = request.user
                type = user.user_type()
                appointment_form = AppointmentForm()
                if type == 'doctor':
                    doctor = Doctor.objects.filter(user = request.user)[0]
                    appointment_form.fields['doctor_ID'].queryset = Doctor.objects.filter(user=request.user)
                    appointment_form.fields['patient_ID'].queryset = Patient.objects.filter(hospital = doctor.hospital )
                elif type == 'patient':
                    patient = Patient.objects.filter(username=request.user.username)[0]
                    appointment_form.fields['patient_ID'].queryset = Patient.objects.filter(user=request.user)
                    appointment_form.fields['doctor_ID'].queryset = Doctor.objects.filter(hospital=patient.hospital)

                # if oT == "d" and type == 'patient':
                #
                #     appointment_form.fields['patient_ID'].queryset = Patient.objects.filter(username = request.user.username)
                #
                elif oT == "p":
                    appointment_form.fields['patient_ID'].queryset = Patient.objects.filter(username=username)



                else:
                    appointment_form = AppointmentForm()

                return render(request, self.template_name, {'appointment_form': appointment_form, 'owner': owner,'type': type,})
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self, request, username):
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment_form_cleaned = appointment_form.cleaned_data
            appointment = Appointment.createAppoinment(appointment_form_cleaned)

            Activity.createActivity(timezone.now(),"created an appointment with", appointment.doctor_ID, request.user.username,
                                    Doctor.objects.filter(user = User.objects.filter(username = appointment.doctor_ID)[0])[0].hospital,
                                    "CreateAppointment")
            appointment.save()

            return redirect('home:appointmentCal',username)
        else:
            return render(request, self.template_name, {'appointment_form': appointment_form, 'error': True})
"""
This view represents the doctor calendar view, which is currently the default/only calendar view available
:atrb: template_name    location/name of calendar html template
"""
class CalendarView(View):

    def get(self,request,username):
        if request.user.is_authenticated():
            Ruser = User.objects.filter(username=username)
            Ruser = Ruser[0]
            if (Ruser.user_type() == 'patient'):
                p = Patient.objects.filter(user = Ruser)[0]
                if request.user.user_type() == 'patient' and request.user.username != username:
                    return render(request, 'home/indexes/InvalidPer.html')
                elif request.user.user_type() == 'nurse':
                    d = Nurse.objects.filter(username=request.user.username)[0]
                    if p.hospital != d.hospital:
                        return render(request, 'home/indexes/InvalidPer.html')
                template_name = 'home/appointment/calendar.html'
                owner = Patient.objects.filter(user = Ruser)
                owner = owner[0]
                hospital = owner.hospital
            elif (Ruser.user_type() == 'nurse'):
                template_name = 'home/appointment/nCalendar.html'
                owner = Nurse.objects.filter(user = Ruser)
                owner = owner[0]
                hospital = owner.hospital
                if owner.hospital == hospital:
                    return render(request, template_name, {'appointments': owner.getAppointmentsToday(), "owner": owner, "hospital":
                        hospital,'week':False})
                else:
                    return render(request, 'home/indexes/InvalidPer.html')
            elif (Ruser.user_type() == 'doctor'):
                template_name = 'home/appointment/calendar.html'
                owner = Doctor.objects.filter(user = Ruser)
                owner = owner[0]
                hospital = owner.hospital
                if request.user.user_type() == 'nurse':
                    d = Nurse.objects.filter(username=request.user.username)[0]
                    if hospital != d.hospital:
                        return render(request, 'home/indexes/InvalidPer.html')
            return render(request,template_name, {'appointments': owner.getAppointments().order_by('date'),"owner":owner, "hospital":
                hospital})
        else:
            return render(request, 'home/indexes/NotLogged.html')

class nCal7(View):
    def get(self,request, username):
        if request.user.is_authenticated():
            if request.user.user_type() == 'nurse':
                Ruser = User.objects.filter(username=username)
                Ruser = Ruser[0]
                template_name = 'home/appointment/nCalendar.html'
                owner = Nurse.objects.filter(user=Ruser)
                owner = owner[0]
                hospital = owner.hospital
                return render(request, template_name, {'appointments': owner.getAppointmentsToday7(), "owner": owner, "hospital":
                    hospital,'week':True})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')
"""
This view represents the editing / updating of an existing appointment
:atrb: template_name    name/location of appointment form (html)
"""
class EditAppointment(View):
    template_name = 'home/appointment/appointmentForm.html'
    def get(self, request,appointment_id):
        if request.user.is_authenticated():
            appointment = get_object_or_404(Appointment,pk = appointment_id)
            if request.user.user_type() == 'nurse' or request.user.username==appointment.patient_ID or request.user.username==appointment.doctor_ID:
                patient = Patient.objects.filter(username = appointment.patient_ID)[0]
                doctor = Doctor.objects.filter(username = appointment.doctor_ID)[0]
                appointment_form = AppointmentForm(initial={'patient_ID': patient,
                                                            'doctor_ID': doctor, 'office': appointment.office,
                                                            'description': appointment.description,
                                                            'date': appointment.date})
                return render(request, self.template_name, {'appointment_form': appointment_form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')


    def post(self, request, appointment_id):
        appointment_form = AppointmentForm(request.POST)
        appointment = get_object_or_404(Appointment,pk = appointment_id)
        appointment.delete()
        if appointment_form.is_valid():
            appointment_form_cleaned = appointment_form.cleaned_data
            appointment = Appointment.createAppoinment(appointment_form_cleaned)
            Activity.createActivity(timezone.now(),"edited an appointment with",appointment.doctor_ID, request.user.username,
                                    Doctor.objects.filter(user = User.objects.filter(username = appointment.doctor_ID)[0])[0].hospital,
                                    "EditAppointment")
            appointment.save()
            return redirect('home:AppointmentDetails',appointment.id)
        else:
            return render(request, self.template_name, {'appointment_form': appointment_form, 'error': True})
"""
This view represents the canceling/ deletion of a pre-existing appointment
"""
class CancelAppointment(View):
    def get(self,request,appointment_id):
        if request.user.is_authenticated():
            appointment = get_object_or_404(Appointment,pk = appointment_id)
            if request.user.username == appointment.patient_ID or request.user.username == appointment.doctor_ID:
                appointment.cancelA()
                Activity.createActivity(timezone.now(),'canceled appoinment', request.user.username,"",
                                        Doctor.objects.filter(user = User.objects.filter(username = appointment.doctor_ID)[0])[0].hospital,
                                        "CancelAppointment")
                return redirect('home:doctor')
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')
#======End Appointment Views=======================================================================================
#=======Start of Search Classes=========================================================================================
class FilterPatientView(View):
    templatename = 'home/patient/patientFilter.html'
    def get(self, request):
        if request.user.is_authenticated():
            if request.user.user_type() != 'patient':
                patient_form = FilterPatientForm
                return render(request,self.templatename,{'patient_form': patient_form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self,request):
        # user_form = FilterUserForm(request.POST)
        patient_form = FilterPatientForm(request.POST)
        # user_clean = user_form.cleaned_data
        if patient_form.is_valid():
            patient_clean = patient_form.cleaned_data
            results = self.getQuery(patient_clean)
            return render(request,'home/patient/patient.html',{'patient_list': results, 'search': True,})
        else:
            return render(request, 'home/patient/patient.html',
                          {'patient_list': None, 'search': True})

    def getQuery(self,patient_clean):
        ans = Patient.objects.all()
        if patient_clean['Username'] != '':
            ans = ans.filter(username__icontains = patient_clean['Username'])
        if patient_clean['first_name'] != '':
            ans = ans.filter(first_name__icontains  = patient_clean['first_name'])
        if patient_clean['last_name']!= '':
            ans = ans.filter(last_name__icontains=patient_clean['last_name'])
        if patient_clean['Hospital'] != None:
            ans = ans.filter(hospital =patient_clean['Hospital'])
        return ans
class FilterActivity(View):
    templatename = 'home/filterActivities.html'

    def get(self,request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                activity_form = FilterActivityForm()
                return render(request,self.templatename,{'activities': activity_form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self, request):
        activity_form = FilterActivityForm(request.POST)
        if activity_form.is_valid():
            activity_form = activity_form.cleaned_data
            results = self.getQuery(activity_form)
            return render(request, 'home/activities.html', {'activity_list': results})
        else:
            return render(request, 'home/activities.html',
                          {'activites_list': None, 'search': True})

    def getQuery(self, activity_form):
        ans = Activity.objects.all()
        if activity_form['User'] != '':
            ans = ans.filter(Q(User_ID__icontains=activity_form['User'])|Q (Effected_ID__icontains=activity_form['User']))
        if activity_form['From'] != None and activity_form['to'] != None:
            to = activity_form['to'] + timezone.timedelta(days=1)
            ans = ans.filter(timestamp__range = [activity_form['From'],to])
        if activity_form['Hospital'] != None:
            ans = ans.filter(Hospital=activity_form['Hospital'])
        return ans.order_by("-timestamp")

class FilterStatistics(View):
    def get(self, request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                stat_form = FilterStatisticsForm()
                return render(request, 'home/statistics/filterStats.html', {'stat_form':stat_form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self, request):
        stat_form   = FilterStatisticsForm(request.POST)
        if stat_form.is_valid():
            stat_form = stat_form.cleaned_data
            activities  = self.getQuery(stat_form)
            PatientReg  = activities.filter(Activity_Type = "CreatePatient").count()
            NurseCreate = activities.filter(Activity_Type = "CreateNurse").count()
            DoctorCreate= activities.filter(Activity_Type = "CreateDoctor").count()
            AdminCreate = activities.filter(Activity_Type = "AdminCreation").count()
            HosCreate   = activities.filter(Activity_Type = "HospitalCreated").count()
            PresCreated = activities.filter(Activity_Type = "CreatePrescription").count()
            PresDeleted = activities.filter(Activity_Type = "DeletePrescription").count()
            PresRefill  = activities.filter(Activity_Type = "RefillPrescription").count()
            DrugCreated = activities.filter(Activity_Type = "CreateDrug").count()
            AppCreated  = activities.filter(Activity_Type = "CreateAppointment").count()
            AppEdited   = activities.filter(Activity_Type = "EditAppointment").count()
            AppCanceled = activities.filter(Activity_Type = "CancelAppointment").count()
            Logins      = activities.filter(Activity_Type = "LogIn").count()
            MessageSent = activities.filter(Activity_Type = "MessageSent").count()
            Transfers   = activities.filter(Activity_Type = "Transfer").count()
            Admitted    = activities.filter(Activity_Type = "Admit")
            admittedAll = Activity.objects.all().filter(Activity_Type = "Admit")
            end = stat_form['end'] + timezone.timedelta(days=1)
            admittedAll = admittedAll.filter(timestamp__lte = end)
            discharged  = Activity.objects.all().filter(Activity_Type = "Discharge")
            discharged  = discharged.filter(timestamp__lte = end)
            if stat_form['Hospital'] != None:
                admittedAll = admittedAll.filter(Hospital = stat_form['Hospital'])
                discharged  =  discharged.filter(Hospital = stat_form['Hospital'])
            admitDict   = {}
            totalTime   = timezone.timedelta(minutes=0)
            admittedAll.order_by("timestamp")
            discharged.order_by("timestamp")
            discharged = list(discharged)
            for admit in Admitted:
                reason = admit.Activity_Details.split()[-1]
                if reason in admitDict.keys():
                    admitDict[reason] += 1
                else:
                    admitDict[reason] = 1
            totalPatients = 0.0
            for admit in admittedAll:
                for discharge in discharged:
                    if admit.Effected_ID == discharge.Effected_ID:
                        if timezone.datetime.date(discharge.timestamp) >= stat_form["start"]:
                            if timezone.datetime.date(admit.timestamp) <= stat_form["start"]:
                                totalTime += timezone.datetime.date(discharge.timestamp) - stat_form["start"]
                                totalPatients += 1
                            else:
                                totalTime += timezone.datetime.date(discharge.timestamp) - timezone.datetime.date(admit.timestamp)
                                totalPatients += 1
                        discharged.remove(discharge)
                        break
                    elif discharged[-1] == discharge:
                        if timezone.datetime.date(admit.timestamp) < stat_form["start"]:
                            totalTime += stat_form["end"] - stat_form["start"]
                            totalPatients += 1
                        else:
                            totalTime += stat_form["end"] - timezone.datetime.date(admit.timestamp)
                            totalPatients += 1
            Reasons = []
            count = 0
            for key in admitDict.keys():
                if admitDict[key] == count:
                    if key == "Care":
                        Reasons.append("Intensive Care")
                    else:
                        Reasons.append(key)
                elif admitDict[key] > count:
                    if key == "Care":
                        Reasons = ["Intensive Care"]
                    else:
                        Reasons = [key]
                    count = admitDict[key]
            Admitted = Admitted.count()
            AvgTime = timezone.timedelta(minutes=0)
            if totalPatients != 0:
                AvgTime = totalTime / totalPatients

            return render(request, "home/statistics/stats.html",
                          {"PReg" : PatientReg , "PresC": PresCreated , "PresD": PresDeleted, "PresR" : PresRefill ,
                           "DrugC": DrugCreated, "AppCr": AppCreated  , "AppE" : AppEdited  , "AppCa" : AppCanceled,
                           "Login": Logins     , "Msg"  : MessageSent , "Trans": Transfers  , "Admit" : Admitted   ,
                           "NReg" : NurseCreate, "DReg" : DoctorCreate, "AvgTm": AvgTime    , "Reason": Reasons    ,
                           "HosC" : HosCreate  , "AReg" : AdminCreate})
        else:
            return render(request, 'home/statistics/filterStats.html', {'stat_form': stat_form})
    def getQuery(self, stat_form):
        ans = Activity.objects.all()
        end = stat_form['end'] + timezone.timedelta(days = 1)
        ans = ans.filter(timestamp__range = [stat_form['start'],end])
        if stat_form['Hospital'] != None:
            ans = ans.filter(Hospital = stat_form['Hospital'])
        return ans



#=======End of Search Classes===========================================================================================
#=======Start of Admission and Discharge and Transfer Views=============================================================
class HospitalReg(View):
    templateName = 'home/hospitalReg.html'
    def get(self,request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                form = HospitalRegForm()
                return render(request,self.templateName,{'hospital_form': form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')

        else:
            return render(request, 'home/indexes/NotLogged.html')
    def post(self,request):
        form = HospitalRegForm(request.POST)
        if form.is_valid():
            form_clean = form.cleaned_data
            h = Hospital.create(form_clean)
            Activity.createActivity(timezone.now(),"created a new hospital",h,request.user,h,"HospitalCreated")
            return redirect('home:hospitalList')
        else:
            return render(request, self.templateName, {'hospital_form': form})

class Transfer(View):
    def get(self,request,username):
        if request.user.is_authenticated():
            p = Patient.objects.filter(username = username)[0]
            if request.user.user_type() == 'doctor':
                doctor = Doctor.objects.filter(user = request.user)[0]
                if doctor.hospital == p.hospital:
                    return render(request,'home/transfer.html',{'issue': True, 'Cuser': doctor, 'patient': p, 'form':None})
                else:
                    return render(request, 'home/transfer.html', {'issue': False, 'Cuser': doctor, 'patient': p, 'form':None})
            elif request.user.is_superuser:
                form = TransferForm()
                return render(request, 'home/transfer.html', {'issue': True, 'Cuser': request.user, 'patient': p, 'form': form})
            else:
                return render(request, 'home/transfer.html', {'issue': True, 'user': request.user, 'patient': p})
        else:
            return render(request, 'home/indexes/NotLogged.html')


    def post(self,request,username):
        p = Patient.objects.filter(username=username)[0]
        if request.user.user_type() == 'doctor':
            doctor = Doctor.objects.filter(user=request.user)[0]
            p.PatientTransfer(doctor.hospital)
            return redirect('home:pDetail', username)
        elif request.user.is_superuser:
            form = TransferForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                hospital = form['hospital']
                p.PatientTransfer(hospital)
                return redirect('home:pDetail', username)
        else:
            return HttpResponse("SPOOKY ERROR")

class Admit(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.user_type() == 'doctor' or request.user.user_type() == 'nurse':
                if request.user.user_type() == 'doctor':
                    Cuser = Doctor.objects.filter(user = request.user)[0]
                elif request.user.user_type() == 'nurse':
                    Cuser = Nurse.objects.filter(user=request.user)[0]
                Uform = AdmitUser()
                po =  Patient.objects.filter(hospital = Cuser.hospital)
                Uform.fields['username'].queryset = po.filter(admit = False)
                Aform = AdmitForm()
                return render(request,'home/admit/admit.html',{'Uform':Uform,'Aform':Aform})
            else:
                return render(request,'home/indexes/InvalidPer.html')
        else:
            return render(request,'home/indexes/NotLogged.html')
    def post(self,request):
        UForm = AdmitUser(request.POST)
        Aform = AdmitForm(request.POST)
        if UForm.is_valid() and Aform.is_valid():
            UForm = UForm.cleaned_data
            Aform = Aform.cleaned_data
            user = UForm['username']
            patient = Patient.objects.filter(username = user.username)[0]
            patient.AdmitPatient(Aform['admitReason'],timezone.now(),request.user.username)
            return redirect('home:admitted')
        else:
            if request.user.user_type() == 'doctor':
                Cuser = Doctor.objects.filter(user=request.user)[0]
            elif request.user.user_type() == 'nurse':
                Cuser = Nurse.objects.filter(user=request.user)[0]
            UForm.fields['username'].queryset = Patient.objects.filter(hospital=Cuser.hospital)
            return render(request,'home/admit/admit.html',{'Uform':UForm,'Aform':Aform})

def Discharge(request,username):
    if request.user.is_authenticated():
        if request.user.user_type() == 'doctor' or request.user.user_type() == 'nurse' or request.user.is_superuser:
            patient = Patient.objects.filter(username = username)[0]
            patient.Discharge()
            return redirect('home:admitted')
        else:
            return render(request, 'home/indexes/InvalidPer.html')
    else:
        return render(request, "home/indexes/NotLogged.html")
class AdmittedView(View):
    template_name = 'home/admit/addmitted.html'

    def get(self, request):
        if request.user.is_authenticated():
            if request.user.user_type() == 'doctor' or request.user.user_type() == 'nurse':
                if request.user.user_type() == 'doctor':
                    Cuser = Doctor.objects.get(user=request.user)
                elif request.user.user_type() == 'nurse':
                    Cuser = Nurse.objects.get(user=request.user)
                Patients = Patient.objects.filter(hospital = Cuser.hospital)
                Patients = Patients.filter(admit = True)
                return render(request, self.template_name, {'owner': Cuser, "patients": Patients.order_by('last_name')})
            elif  request.user.is_superuser:
                Patients = Patient.objects.filter(admit = True)
                return render(request, self.template_name, {'owner': request.user, "patients": Patients.order_by('last_name')})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, "home/indexes/NotLogged.html")

#=======End of Admission and Discharge and Transfer Views===============================================================
#=======Start of Prescription Views=====================================================================================
class Refill(View):
    def get(self, request, prescription_id):
        if request.user.is_authenticated():
            prescription = get_object_or_404(Prescription, pk=prescription_id)
            prescription.refill(request.user.username)
            prescription.save()
            return redirect('home:prescriptionDetail', prescription_id)
        else:
            return render(request, 'home/indexes/NotLogged.html')

class NewDrug(View):
    def get(self,request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                form = DrugForm()
                return render(request,'home/prescription/createDrug.html',{"form":form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')
    def post(self,request):
        form = DrugForm(request.POST)
        if form.is_valid():
            form_clean = form.cleaned_data
            Drug.createNewDrug(form_clean,request.user)
            return redirect('home:drugList')
        else:
            return render(request, 'home/prescription/createDrug.html', {"form": form})


class NewPrescription(View):
    template_name = "home/prescription/newPrescription.html"

    def get(self, request):
        if request.user.is_authenticated():
            if request.user.user_type() == 'doctor':
                d = Doctor.objects.filter(user = request.user)[0]
                prescription_form = PrescriptionForm()
                prescription_form.fields['user_ID'].queryset = Patient.objects.filter(hospital = d.hospital)
                return render(request, self.template_name, {"prescription_form":prescription_form})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')

    def post(self, request):
        prescription_form = PrescriptionForm(request.POST)
        if prescription_form.is_valid():
            prescription_form_clean = prescription_form.cleaned_data
            prescription = Prescription.createPrescription(prescription_form_clean, request.user.username)
            prescription.save()
            return redirect('home:prescriptions', prescription.user_ID.username)
        else:
            return render(request, self.template_name, {"prescription_form":prescription_form})

class DeletePrescriptionConfirmation(View):
    def get(self, request, prescription_id):
        if request.user.user_type() == "doctor":
            prescription = get_object_or_404(Prescription, pk=prescription_id)
            return render(request, 'home/prescription/prescriptionDelete.html', {"prescription":prescription})
        else:
            return render(request, 'home/indexes/InvalidPer.html')

class DeletePrescription(View):
    def get(self, request, prescription_id):
        if request.user.user_type() == "doctor":
            prescription = get_object_or_404(Prescription, pk=prescription_id)
            patient      = prescription.user_ID.username
            prescription.removePrescription(request.user.username)
            return redirect("home:prescriptions", patient)
        else:
            return render(request, 'home/indexes/InvalidPer.html')

#=======End of Prescription Views=======================================================================================
#=======Start of Message Views=====================================================================================
class NewMessage(View):
    template_name = "home/messages/newmessage.html"
    def get(self,request):
        if request.user.is_authenticated:
            new_message = MessageForm()
            return render(request,self.template_name, {'message_form':new_message})
        else:
            return render(request, 'home/indexes/NotLogged.html')
    def post(self,request):
        new_message = MessageForm(request.POST)
        if new_message.is_valid():
            new_message_clean = new_message.cleaned_data
            message = Messages.sendMsg(new_message_clean,request.user.username)
            message.save()
            return redirect("home:messages")
        else:
            return render(request,self.template_name, {'message_form':new_message})
class Reply(View):
    template_name = "home/messages/newmessage.html"
    def get(self, request,message_id):
        if request.user.is_authenticated:
            new_message = ReplyForm()
            return render(request, self.template_name, {'message_form': new_message})
        else:
            return render(request, "home/indexes/NotLogged.html")

    def post(self,request,message_id):
        message = ReplyForm(request.POST)
        repling = get_object_or_404(Messages, pk = message_id)
        if message.is_valid():
            message_clean = message.cleaned_data
            Messages.reply(message_clean,repling)
            return redirect("home:messages")
        else:
            return render(request, self.template_name, {'message_form': message})
#=======End of Message Views=======================================================================================
#=======Start of Upload Patient Information Views=============================================================
class Export(View):
    def get(self,request,test_id):
        test = get_object_or_404(MedTest,pk = test_id)
        if request.user.is_authenticated:
            if test.patient_ID == request.user.username:
                return render(request,'home/Export.html',{'medtest':test})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')
    def post(self,request,test_id):
        test = get_object_or_404(MedTest,pk = test_id)
        filename = test.attachedFiles.name.split('/')[-1]
        response = HttpResponse(test.attachedFiles, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response



def List(request, username):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form_cleaned = form.cleaned_data
            newdoc = MedTest(attachedFiles=request.FILES['attachedFiles'],
                             patient_ID = username, comments = form_cleaned['comments'],
                             released = request.POST.get('released', False))
            newdoc.save()

            p = Patient.objects.filter(username=username)[0]
            d = Doctor.objects.filter(username = request.user.username)[0]
            Activity.createActivity(timezone.now(), ' uploaded information for', username, d.user, p.hospital, "UploadFiles" )
            if newdoc.released:
                Activity.createActivity(timezone.now(), ' released information for', username, d.user, p.hospital,
                                        "ReleaseFiles")

            # Redirect to the document list after POST

            # Load documents for the list page
            documents = MedTest.objects.filter(patient_ID=username)
            id = username

            return render(request, 'home/patient/list.html', {'documents': documents, 'form': form, 'id': id})
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    if request.user.is_authenticated:
        documents = MedTest.objects.filter(patient_ID=username)
        id = username
        p = Patient.objects.filter(username = id)[0]
        if request.user.username == username:
            # Render list page with the documents and the form
            return render(
                request,
                # 'home/list.html',
                'home/patient/list.html',
                {'documents': documents, 'form': form, 'id': id}
            )
        elif request.user.user_type() == 'doctor':
            d = Doctor.objects.filter(username = request.user.username)[0]
            if d.hospital == p.hospital:
                return render(
                    request,
                    # 'home/list.html',
                    'home/patient/list.html',
                    {'documents': documents, 'form': form, 'id': id}
                )
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        elif request.user.user_type() == 'nurse':
            d = Nurse.objects.filter(username=request.user.username)[0]
            if d.hospital == p.hospital:
                return render(
                    request,
                    # 'home/list.html',
                    'home/patient/list.html',
                    {'documents': documents, 'form': form, 'id': id}
                )
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/InvalidPer.html')

    else:
        return render(request, 'home/indexes/NotLogged.html')

def test(request,username):
    if request.user.is_authenticated:
        tests = MedTest.objects.filter(patient_ID = username)
        id = username
        p = Patient.objects.filter(username = id)[0]
        if username == request.user.username:
            return render(request,'home/patient/tests.html',{"tests":tests, "id": p, 'Cuser':p})
        elif request.user.user_type() == 'doctor':
            d = Doctor.objects.filter(username = request.user.username)[0]
            return render(request, 'home/patient/tests.html', {"tests": tests, "id": p, 'Cuser': d})
        elif request.user.user_type() == 'nurse':
            n = Nurse.objects.filter(username = request.user.username)[0]
            return render(request, 'home/patient/tests.html', {"tests": tests, "id": p, 'Cuser': n})
        else:
            return render(request, 'home/indexes/InvalidPer.html')
    else:
        return render(request, 'home/indexes/NotLogged.html')

def release(request, test_id, username):
    test = get_object_or_404(MedTest, pk = test_id)
    test.release_test()
    d = Doctor.objects.filter(username=request.user.username)[0]
    p = Patient.objects.filter(username=username)[0]
    Activity.createActivity(timezone.now(), ' released information for', username, d.user, p.hospital, "ReleaseFiles")
    return redirect('home:test', username)

#=======End of Upload Patient Information Views=========================================================================
#=======Start of Statistics View========================================================================================
class Statistics(View):
    def get(self, request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                activities  = Activity.objects.all()
                PatientReg  = activities.filter(Activity_Type = "CreatePatient").count()
                NurseCreate = activities.filter(Activity_Type = "CreateNurse").count()
                DoctorCreate= activities.filter(Activity_Type = "CreateDoctor").count()
                AdminCreate = activities.filter(Activity_Type = "AdminCreation").count()
                HosCreate   = activities.filter(Activity_Type = "HospitalCreated").count()
                PresCreated = activities.filter(Activity_Type = "CreatePrescription").count()
                PresDeleted = activities.filter(Activity_Type = "DeletePrescription").count()
                PresRefill  = activities.filter(Activity_Type = "RefillPrescription").count()
                DrugCreated = activities.filter(Activity_Type = "CreateDrug").count()
                AppCreated  = activities.filter(Activity_Type = "CreateAppointment").count()
                AppEdited   = activities.filter(Activity_Type = "EditAppointment").count()
                AppCanceled = activities.filter(Activity_Type = "CancelAppointment").count()
                Logins      = activities.filter(Activity_Type = "LogIn").count()
                MessageSent = activities.filter(Activity_Type = "MessageSent").count()
                Transfers   = activities.filter(Activity_Type = "Transfer").count()
                Admitted    = activities.filter(Activity_Type = "Admit")
                discharged  = activities.filter(Activity_Type = "Discharge")
                admitDict   = {}
                totalTime   = timezone.timedelta(minutes = 0)
                Admitted.order_by("timestamp")
                discharged.order_by("timestamp")
                discharged = list(discharged)
                AvgTime = timezone.timedelta(minutes=0)
                for admit in Admitted:
                    reason = admit.Activity_Details.split()[-1]
                    if reason in admitDict.keys():
                        admitDict[reason] += 1
                    else:
                        admitDict[reason] = 1
                    for discharge in discharged:
                        if admit.Effected_ID == discharge.Effected_ID:
                            totalTime += discharge.timestamp - admit.timestamp
                            AvgTime = AvgTime + totalTime
                            discharged.remove(discharge)
                            break
                        elif discharged[-1] == discharge:
                            totalTime += timezone.now() - admit.timestamp
                            AvgTime = AvgTime + totalTime
                Reasons = []
                count   = 0
                for key in admitDict.keys():
                    if admitDict[key] == count:
                        if key == "Care":
                            Reasons.append("Intensive Care")
                        else:
                            Reasons.append(key)
                    elif admitDict[key] > count:
                        if key == "Care":
                            Reasons = ["Intensive Care"]
                        else:
                            Reasons = [key]
                        count   = admitDict[key]
                Admitted = Admitted.count()

                if Admitted != 0:
                    AvgTime = totalTime/Admitted
                return render(request, "home/statistics/stats.html",
                              {"PReg" :PatientReg , "PresC":PresCreated , "PresD":PresDeleted, "PresR" :PresRefill ,
                               "DrugC":DrugCreated, "AppCr":AppCreated,
                               "Login":Logins     , "Msg"  :MessageSent , "Trans":Transfers  , "Admit" :Admitted   ,
                               "NReg" :NurseCreate, "DReg" :DoctorCreate, "AvgTm":AvgTime    , "Reason":Reasons    ,
                               "AReg" :AdminCreate + 1})
            else:
                return render(request, 'home/indexes/InvalidPer.html')
        else:
            return render(request, 'home/indexes/NotLogged.html')


