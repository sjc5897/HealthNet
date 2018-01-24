from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from .models import *
from django.utils import timezone
from django.contrib.admin import widgets



"""
This class represents the user form, which contains relevant user info
:atrb: password             The user's secure password
:atrb: password_confirm     User's secure confirmation of password (re-typed password)
"""
class UserForm(forms.ModelForm):
    password         = forms.CharField(widget = forms.PasswordInput)
    password_confirm = forms.CharField(widget = forms.PasswordInput)
    # if password != password_confirm:
    #     raise ValidationError("Passwords do not match")
    class Meta:
        model        = User
        fields       = ['username','password','password_confirm','email','first_name','last_name']
    def clean(self):
        clean = self.cleaned_data
        if 'password' and 'password_confirm' in clean.keys():
            if clean['password'] != clean['password_confirm']:
                raise forms.ValidationError("Passwords Do Not Match")
            if 'username' in clean.keys():
                if User.objects.filter(username = clean['username']).exists():
                    raise forms.ValidationError("Username is taken, selected new username")
                if clean['username'] == 'patient' or clean['username'] == 'doctor' or clean['username'] == 'nurse':
                    raise forms.ValidationError("Username is invalid please pick a new one")


"""
This class represents the patient user form, which contains only date of birth, currently
"""
class PatientUserForm(forms.ModelForm):
    DOB = forms.DateField(label='Date of Birth (MM-DD-YYYY)', input_formats=['%m-%d-%Y'])
    insurance = forms.CharField(label= 'Insurance Provider')
    PolicyNumber = forms.CharField(label='Insurance Policy Number')
    class Meta:
        model  = Patient
        fields = ['DOB','insurance','PolicyNumber','hospital']

class UserEditForm(forms.ModelForm):
    class Meta:
        model        = User
        fields       = ['email','first_name','last_name']

class DoctorForm(forms.ModelForm):
    office_hours_start = forms.TimeField(label = 'Office Hours Start (HH:MM AM/PM)',input_formats=['%I:%M %p'], initial="",widget=forms.DateInput(format='%I:%M %p'))
    office_hours_end = forms.TimeField(label = 'Office Hours End (HH:MM AM/PM)',input_formats=['%I:%M %p'], initial="",widget=forms.DateInput(format='%I:%M %p'))
    class Meta:
        model = Doctor
        fields = ['phone','hospital','specialty','office_hours_start','office_hours_end','office']

class NurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = ['phone','hospital']
"""
This class represents the appointment form, which is used when creating and editing an appointment
:atrb: patient_ID    patient's unique identifier (username)
:atrb: doctor_ID     doctor's unique identifier  (username)
"""
class AppointmentForm(forms.ModelForm):

    patient_ID = forms.ModelChoiceField(queryset=Patient.objects.all())
    doctor_ID  = forms.ModelChoiceField(queryset=Doctor.objects.all())
    date = forms.DateTimeField(label='Date (MM-DD-YYYY HH:MM AM/PM)', input_formats=['%m-%d-%Y %I:%M %p'],widget=forms.DateInput(format='%m-%d-%Y %I:%M %p'),)
    class Meta:
        model  = Appointment
        fields = ['patient_ID','doctor_ID', 'date', 'office', 'description']

    def clean(self):
        clean = self.cleaned_data
        if'date' in clean.keys():
                limit = timezone.now().date() + timezone.timedelta(days=1)
                if clean['date'].date()< limit:
                    raise forms.ValidationError("Appointments must be made a day in advance")
                Urange = clean['date'] + timezone.timedelta(minutes=30)
                Lrange = clean['date'] - timezone.timedelta(minutes=30)
                appointment = Appointment.objects.filter(date__range = [Lrange,Urange])
                appointment = appointment.filter(doctor_ID = clean['doctor_ID'].username)
                appointment = appointment.filter(patient_ID=clean['patient_ID'].username)
                if appointment :
                    raise forms.ValidationError("Another appointment during that time")
                return clean

"""
This class represents the contact form, which contains relevant contact info
:atrb: phone     a valid phone number, validated via regular expressions
:atrb: zip       a valid zip code, validated through regular expressions
"""
class ContactUserForm(forms.ModelForm):
    phone      = forms.RegexField(regex = r'^\+?1?\d{10}$')
    zip        = forms.RegexField(regex = r'^\+?1?\d{5}'  )
    class Meta:
        model  = ContactInfo
        fields = ['address','city','state','zip','phone']
"""
This class represents the medical form, which contains relevant medical info
:atrb: weight    patient's weight, must be between 1 and 3 digits in length
:atrb: height    patient's height, must be between 2 and 3 digits in length
"""
class MedicalUserForm(forms.ModelForm):
    weight        = forms.RegexField(regex = r'^\+?1?\d{1,3}')
    height_feet   = forms.RegexField(regex = r'^\+?1?\d{1}'  )
    class Meta:
        model     = MedicalInfo
        fields    = ['sex','weight','height_feet','height_inches','blood_Type']
"""
This class represents the login form, which contains relevant login info
:atrb: password    User's secure password
"""
class LoginForm(forms.ModelForm):
    password   = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model  = User
        fields = ['username','password']

class PrescriptionForm( forms.ModelForm ):
    """
    # checks that the patient is a valid patient
    def user_ID_exists(value):
        patient = Patient.objects.filter( username = value )
        if not patient:
            raise ValidationError('Must be A Patient')

    user_ID = forms.CharField(label = "patient_ID", required = True, validators = [user_ID_exists])
    """
    expiration = forms.DateTimeField(label='Expiration (MM-DD-YYYY HH:MM AM/PM )', input_formats=['%m-%d-%Y %I:%M %p', '%m/%d/%Y %I:%M %p'],
                           widget=forms.DateInput(format='%m-%d-%Y %I:%M %p'), required=False)
    class Meta:
        model  = Prescription
        fields = ['user_ID', 'drug', 'expiration', 'refills', 'quantity', 'directions']

class DrugForm( forms.ModelForm ):
    #checks that the new drug is not already in the system
    def checkDrug(value):
        drug = Drug.objects.filter( name = value )
        if drug:
            raise ValidationError('Drug must be unique')
    def checkPrice(value):
        if value <= 0.0:
            raise ValidationError('Drug has invalid price')
    drug = forms.CharField(label = 'Drug Name', required = True, validators = [checkDrug])
    price = forms.DecimalField(decimal_places = 2, max_digits = 10, label = 'Price per pill', required=True, validators=[checkPrice] )
    class Meta:
        model  = Drug
        fields = ['drug','price']

"""
This form provides a way to search and filter patients based of inputted information
"""

class FilterPatientForm(forms.Form):
    Username = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    Hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=False)

class DateInput(forms.DateInput):
    input_type = 'date'

class FilterActivityForm(forms.Form):
    User = forms.CharField(required=False)
    From = forms.DateField(label='From (MM-DD-YYYY )', input_formats=['%m-%d-%Y','%m/%d/%Y'],widget=forms.DateInput(format='%m-%d-%Y'),required=False)
    to = forms.DateField(label='To (MM-DD-YYYY)', input_formats=['%m-%d-%Y','%m/%d/%Y'],widget=forms.DateInput(format='%m-%d-%Y'),required=False)
    Hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=False)
    widgets = {
        'date': DateInput()
    }

class TransferForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['hospital']


class AdmitUser(forms.Form):
    username = forms.ModelChoiceField(queryset=Patient.objects.all())

class AdmitForm(forms.ModelForm):
    class Meta:
        model = MedicalInfo
        fields = ['admitReason']


class MessageForm(forms.ModelForm):

    # checks that the patient is a valid patient
    def user_ID_exists(value):
        user = User.objects.filter(username = value)
        if not user:
            raise ValidationError('Must be send to a valid user')

    Receiver_ID = forms.CharField(label = "To", required = True, validators = [user_ID_exists])
    class Meta:
        model = Messages
        fields = [ 'Receiver_ID', 'Subject', 'Message']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['Message']

class DocumentForm(forms.ModelForm):
    attachedFiles = forms.FileField(
        label='File\n'
    )
    released = forms.BooleanField(required=False)
    class Meta:
        model = MedTest
        fields = {"attachedFiles", 'comments', 'released'}

class FilterStatisticsForm(forms.Form):
    start = forms.DateField(label='Start (MM-DD-YYYY )', input_formats=['%m-%d-%Y', '%m/%d/%Y'],
                           widget=forms.DateInput(format='%m-%d-%Y'), required=True)
    end = forms.DateField(label='End (MM-DD-YYYY)', input_formats=['%m-%d-%Y', '%m/%d/%Y'],
                         widget=forms.DateInput(format='%m-%d-%Y'), required=True)
    Hospital = forms.ModelChoiceField(queryset = Hospital.objects.all(), required = False, label = "Hospital(optional)")

class HospitalRegForm(forms.ModelForm):
    name = forms.CharField(label= "Hospitals ID Name")
    zip = forms.RegexField(regex=r'^\+?1?\d{5}')
    class Meta:
        model = Hospital
        fields = {'name','address','city','zip','state'}
    def clean(self):
        clean = self.cleaned_data
        if 'name' in clean.keys():
            r = Hospital.objects.filter(name = clean['name'])
            if r:
                raise ValidationError("Hospital name must be unique")


class editHospitalForm(forms.ModelForm):
    zip = forms.RegexField(regex=r'^\+?1?\d{5}')
    class Meta:
        model = Hospital
        fields = {'address', 'city', 'zip', 'state'}

class editDrugForm(forms.ModelForm):
    def checkPrice(value):
        if value <= 0.0:
            raise ValidationError('Drug has invalid price')
    price = forms.DecimalField(decimal_places=2, max_digits=10, label='Price per pill', required=True,
                               validators=[checkPrice])

    class Meta:
        model = Drug
        fields = ['price']