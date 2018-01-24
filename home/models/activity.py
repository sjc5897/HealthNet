from django.db import models
from django.utils import timezone
from .hospital import Hospital
import sqlite3

"""
This class represents activity objects. It stores information based on actions in other class methods.
:atrb: timestamp: Time when activity was done.
:atrb: User_ID: Identification of the user that performed the activity.
:atrb: Effected_ID: Identification of the user affected by the activity (can be same as User_ID)
:atrb: Activity_Details: Description of the action performed.
"""
class Activity(models.Model):
    c_activity_type = (
        ("CreatePatient"     , "Patient Creation"                ),
        ("CreatePrescription", "Prescription Creation"           ),
        ("CreateDrug"        , "Drug Creation"                   ),
        ("CreateAppointment" , "Appointment Creation"            ),
        ("AdminCreation"     , "Admin Creation"                  ),
        ("EditAppointment"   , "Appointment Edits"               ),
        ("CancelAppointment" , "Appointment Cancellations"       ),
        ("LogIn"             , "User Log In"                     ),
        ("LogOut"            , "User Log Out"                    ),
        ("MessageSent"       , "Messages Sent"                   ),
        ("Transfer"          , "Patient Transfer"                ),
        ("Admit"             , "Patient Admitted to Hospital"    ),
        ("Discharge"         , "Patient Discharged from Hospital"),
        ("UpdateProfile"     , "Profile Information Updates"     ),
        ("UpdateDrug"        , "Drug Price Updates"              ),
        ("DeletePrescription", "Prescriptions Deleted"           ),
        ("RefillPrescription", "Prescription Refills"            ),
        ("CreateDoctor"      , "Doctor Creation"                 ),
        ("CreateNurse"       , "Nurse Creation"                  ),
        ("HospitalCreated"   , "Hospital Creation"               ),
        ("UploadFiles"       , "Files Uploaded"                  ),
        ("ReleaseFiles"      , "Files Released"                  ),
        ("ViewInformation"   , "Information Viewed"              )
    )
    timestamp        = models.DateTimeField(default = timezone.now)
    User_ID          = models.CharField    (max_length = 100, default = '')
    Effected_ID      = models.CharField    (max_length = 100, default = '')
    Activity_Type    = models.CharField    (max_length = 100, default = '', choices = c_activity_type)
    Activity_Details = models.TextField    (default = "",null=True)
    Hospital         = models.ForeignKey   (Hospital, default = None, null=True)
    #Used to sort the database in time order such that the user can view the activity log by most recent date.
    def sortTable(self):
        today = timezone.now()
        return Activity.objects.filter(timestamp__year=today.year).order_by('-timestamp')
    #creates a new activity object for other methods to use
    def createActivity(time, details, User_ID, user, hospital, a_type):
        activity = Activity (
            Effected_ID      = User_ID,
            Hospital         = hospital,
            User_ID          = user,
            timestamp        = time,
            Activity_Details = details,
            Activity_Type    = a_type
        )
        activity.save()
    #creates a toString
    def __str__(self):
        return "Time: "+str(self.timestamp)+" | Message: "+str(self.Activity_Details)