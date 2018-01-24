from django.db import models
from django.utils import timezone
from .hospital import Hospital


"""
This class represents appointment objects. Appointments are created by patients, doctors and nurses, but can only
be edited by patients or doctors.
:atrb: date          the date of the appointment
:atrb: time          the time the appointment is scheduled for
:atrb: office        the location of the appointment
:atrb: patient_ID    the patient's unique identifier
:atrb: doctor_ID     the doctor's unique identifier
:atrb: description   the (optional) description of the purpose for the appointment
"""
class Appointment(models.Model):
    date = models.DateTimeField(blank= False,)        #appointment date and time
    office = models.IntegerField('Room number:')    #office number of the doctor
    patient_ID = models.CharField(max_length=100, default='')    #patient user ID
    doctor_ID = models.CharField(max_length=100, default='')     #doctor user ID
    hospital = models.ForeignKey(Hospital, default= None)
    description = models.TextField(max_length=500, default='')  #description for the appointment
    #edits a pre-existing appointment with values from the applicable form

    def editAppointment(self,form):
        self.date = form['date']
        self.description = form['description']
        self.office = form['office']
        self.patient_ID = form['patient_ID'].username
        self.doctor_ID = form['doctor_ID'].user.username
    #creates a new appointment via the appointment_form, currently cannot perform unique date/time validation

    def createAppoinment(appointment_form):
        patient = appointment_form['patient_ID']
        doctor = appointment_form['doctor_ID']
        appointment = Appointment(
            date=appointment_form['date'],
            office=appointment_form['office'],
            patient_ID=patient.username,
            doctor_ID=doctor.user.username,
            description=appointment_form['description'],
            hospital = doctor.hospital
        )
        # appointment.
        appointment.save()
        return appointment
    #cancels / deletes a pre-existing appointment
    def cancelA(self):
        self.delete()

    def __str__(self):
        tostr = ""
        tostr += self.date + self.time + " at office No." + self.office + "\n"
        tostr += " Patient ID: " + self.patient_ID + "\n Doctor ID: " + self.doctor_ID + "\n"
        tostr += "  Description: " + self.description
        return tostr
