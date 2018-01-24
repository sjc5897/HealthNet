from django.db import models
from django.contrib.auth.models import User
from .hospital import Hospital
from django.utils import timezone
from .activity import Activity
from .calendar import Appointment

"""
This class represents a nurse
:atrb: user                  NUrse's username, used to uniquely identify a nurse
:atrb: name                  Nurse's (full) name
:atrb: phone                 Nurse's phone number
:atrb: email                 Nurse's e-mail address
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

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    username = models.CharField(max_length=50, default="")
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email    = models.CharField (max_length = 100, default = '')
    phone    = models.CharField (max_length = 10 , default = '')
    hospital = models.ForeignKey(Hospital,on_delete = models.CASCADE, default = None)

    def createNurse(user_form,nurse_form,user):
        credential = User.objects.create_user(
            username = user_form['username'],
            email = user_form['email'],
            password= user_form['password'],
            first_name = user_form['first_name'],
            last_name = user_form['last_name']
        )
        credential.save()
        nurse = Nurse(
            user = credential,
            username = credential.username,
            first_name = credential.first_name,
            last_name = credential.last_name,
            hospital = nurse_form['hospital'],
            email = credential.email,
            phone = nurse_form['phone'],
        )
        nurse.save()
        Activity.createActivity(timezone.now(),"has created a new nurse:", nurse.username, user.username, nurse.hospital, "CreateNurse")
        return nurse
        pass

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.user.username + ")"

    def getAppointmentsToday(self):
        now = timezone.now()
        frame = now + timezone.timedelta(days=1)
        ap = Appointment.objects.filter(hospital = self.hospital)
        ap = ap.filter(date__range = [now,frame])
        return ap.order_by("date")


    def getAppointmentsToday7(self):
        now = timezone.now()
        frame = now + timezone.timedelta(weeks=1)
        ap = Appointment.objects.filter(hospital=self.hospital)
        ap = ap.filter(date__range=[now, frame])
        return ap.order_by("date")


    def edit(self,nurse_form,user_form):
        self.user.email = user_form['email']
        self.email = user_form['email']
        self.user.first_name = user_form['first_name']
        self.first_name = user_form['first_name']
        self.user.last_name = user_form['last_name']
        self.last_name = user_form['last_name']
        self.hospital = nurse_form['hospital']
        self.phone = nurse_form['phone']
        self.user.save()
        self.save()
        return self