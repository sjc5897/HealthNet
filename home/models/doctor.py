from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .hospital import Hospital
from .calendar import Appointment
from .activity import Activity

"""
This class represents a doctor
:atrb: user                  Doctor's username, used to uniquely identify a doctor
:atrb: name                  Doctor's (full) name
:atrb: phone                 Doctor's phone number
:atrb: specialty             Specialty associated with doctor (e.g. pediatrician, optometrist, etc.)
:atrb: office_hours_start    Beginning of doctor's office hours
:atrb: office_hours_end      End of doctor's office hours
:atrb: office                Doctor's office room number
"""
def user_data(self):
    if hasattr(self, 'patient'): return self.patient
    if hasattr(self, 'doctor'): return self.doctor
    if hasattr(self,'nurse'): return self.nurse

    else:return "invalid_user"
def user_type(self):
    if hasattr(self, 'patient'): return 'patient'
    if hasattr(self, 'doctor'): return 'doctor'
    if hasattr(self,'nurse'): return 'nurse'
    else: return "invalid_user"

User.add_to_class('user_data',user_data)
User.add_to_class('user_type',user_type)

class Doctor(models.Model):
    # attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None,)
    username = models.CharField(max_length=50, default='', blank=False)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=10, default='')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, default=None)
    specialty = models.CharField(max_length=100,default='')
    office_hours_start = models.TimeField(default=timezone.now)
    office_hours_end = models.TimeField(default=timezone.now)
    office = models.CharField(max_length=100,default="")

    def createDoctor(user_form,doctor_form,user):
        credential = User.objects.create_user(
            username = user_form['username'],
            email = user_form['email'],
            password = user_form['password'],
            first_name = user_form['first_name'],
            last_name = user_form['last_name']
        )
        credential.save()
        doctor = Doctor(
            user = credential,
            username = credential.username,
            first_name = credential.first_name,
            last_name = credential.last_name,
            phone = doctor_form['phone'],
            hospital = doctor_form['hospital'],
            specialty = doctor_form['specialty'],
            office_hours_start = doctor_form['office_hours_start'],
            office_hours_end=doctor_form['office_hours_end'],
            office = doctor_form['office']
        )
        doctor.save()
        Activity.createActivity(timezone.now(),"has creted a new doctor:", doctor.username, user.username, doctor.hospital, "CreateDoctor")
        return doctor

    def getAppointments(self):
        appointments = Appointment.objects.filter(doctor_ID=self.username)
        oldappointments = appointments.filter(date__lt=timezone.now())
        for appointment in oldappointments:
            appointment.delete()
        appointments = Appointment.objects.filter(doctor_ID=self.username)
        return appointments

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.user.username + ")"

    def edit(self,doctor_form,user_form):
        self.user.email = user_form['email']
        self.user.first_name = user_form['first_name']
        self.user.last_name = user_form['last_name']
        self.first_name = user_form['first_name']
        self.last_name = user_form['last_name']
        self.phone = doctor_form['phone']
        self.hospital = doctor_form['hospital']
        self.specialty = doctor_form['specialty']
        self.office_hours_start = doctor_form['office_hours_start']
        self.office_hours_end = doctor_form['office_hours_end']
        self.office = doctor_form['office']
        self.user.save()
        self.save()
        return self