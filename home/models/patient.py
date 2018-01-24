from django.db import models
from django.contrib.auth.models import User
from .activity import Activity
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from .calendar import Appointment
from .hospital import Hospital

"""
This file is the model for the patient in the Healthnet website
It houses the patient class, medicalInfo class, contact info class and their methods
Author: Stephen Cook
Language: Python 3.4.3 and Django 1.9.1
"""


def user_data(self):
    if hasattr(self, 'patient'): return self.patient
    if hasattr(self, 'doctor' ): return self.doctor
    if hasattr(self, 'nurse'  ):
        return self.nurse
    else:
        return "invalid_user"

def user_type(self):
    if hasattr(self, 'patient'): return 'patient'
    if hasattr(self, 'doctor' ): return 'doctor'
    if hasattr(self, 'nurse'  ):
        return 'nurse'
    else:
        return "invalid_user"


User.add_to_class('user_data', user_data)
User.add_to_class('user_type', user_type)


"""
This is a class representing all important contact information for a patient
:atrb: Patient_ID:  The ID of the patient
:atrb: address:     The patient's current address
:atrb: phone:       The patient's phone number
:atrb: c_states:    The possible choices for states
:atrb: state:       The patient's current state. Not Healthnet currently only supports American Users
:atrb: zip:         The patient's zip code
:atrb: city:        The city or town of the user
"""
class ContactInfo(models.Model):
    Patient_ID = models.CharField(max_length=20 , default='')
    address    = models.CharField(max_length=100, default='')
    phone      = models.CharField(max_length=10 , default='')
    c_states = (
        ('AK', 'Alaska'),
        ('AL', 'Alabama'),
        ('AR', 'Arkansas'),
        ('AS', 'American Samoa'),
        ('AZ', 'Arizona'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DC', 'District of Columbia'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('GU', 'Guam'),
        ('HI', 'Hawaii'),
        ('IA', 'Iowa'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('MA', 'Massachusetts'),
        ('MD', 'Maryland'),
        ('ME', 'Maine'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MO', 'Missouri'),
        ('MP', 'Northern Mariana Islands'),
        ('MS', 'Mississippi'),
        ('MT', 'Montana'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('NE', 'Nebraska'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NV', 'Nevada'),
        ('NY', 'New York'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('PR', 'Puerto Rico'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VA', 'Virginia'),
        ('VI', 'Virgin Islands'),
        ('VT', 'Vermont'),
        ('WA', 'Washington'),
        ('WI', 'Wisconsin'),
        ('WV', 'West Virginia'),
        ('WY', 'Wyoming')
    )
    state = models.CharField(max_length=20 , choices=c_states, default="")
    zip   = models.CharField(max_length= 5 , default="")
    city  = models.CharField(max_length= 30, default="")

    """
    A too string used to quickly reference information
    """
    def __str__(self):
        return self.Patient_ID + " contact"
    """
       Creates a Contact Information class from cleaned data
       :arg
            contact_form: cleaned data used to represent the new contact information
            username:     The associated users username
    """
    def createContact(contact_form,username):
        contact = ContactInfo(
            Patient_ID=username,
            address=contact_form['address'],
            phone=contact_form['phone'],
            state=contact_form['state'],
            zip=contact_form['zip'],
            city=contact_form['city']
        )
        # saves the contact
        contact.save()
        return contact
    """
    Updates the current patient's contact information. Current version replaces all aspects of contact information
    :arg
        contact_from:   cleaned_data from the ContactUserForm representing the users new contact information
    """
    def Update(self,contact_form):
            self.address = contact_form['address']
            self.phone   = contact_form['phone'  ]
            self.state   = contact_form['state'  ]
            self.zip     = contact_form['zip'    ]
            self.city    = contact_form['city'   ]
            self.save()

"""
This is a class representing all important medical information for a patient
:atrb: medical_ID:  The associated ID of a patient
:atrb: c_sex:       The choices for sex
:atrb: blood_Type_c The choice for blood type
:atrb: sex:         The patients sex
:atrb: weight:      The patient's weight
:atrb: height:      The patinet's hieght
:atrb: blood_Type:  The patient's blood type
"""
class MedicalInfo(models.Model):
    medical_ID = models.CharField(max_length=20, default='')
    c_sex = (
        ("M", "Male"  ),
        ("F", "Female")
    )
    c_admit = (
        ("Appointment", "Appointment"),("Checkup","Checkup"),("In Labor","In Labor"),("Intensive Care","Intensive Care"),
        ("Observation","Observation"),("Surgery","Surgery"),
        ("Other", "Other"),
    )
    blood_Type_c = (
        ("A+","A+"), ("A-" ,"A-" ),("B+" ,"B+" ),
        ("B-","B-"), ("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-")
    )
    sex           = models.CharField(max_length = 1, choices = c_sex, default = '')
    weight        = models.CharField(max_length = 3, default = '')
    height_feet   = models.CharField(max_length = 1, default = '')
    height_inches = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(11)])
    blood_Type    = models.CharField(max_length = 3, choices = blood_Type_c, default = '')
    admit = models.NullBooleanField(blank = True)
    admitReason = models.CharField(max_length=20, choices=c_admit, default='Not', blank=True, null=True)
    DateAdmission = models.DateTimeField(blank= True, default= timezone.now,null= True)

    """
        Creates a medical info class from cleaned data
        Called in the patient creation class
        """

    def createMedical(medical_form, username):
        medical = MedicalInfo(
            medical_ID=username,
            sex=medical_form['sex'],
            weight=medical_form['weight'],
            height_feet=medical_form['height_feet'],
            height_inches=medical_form['height_inches'],
            blood_Type=medical_form['blood_Type'],
            admit = False,
            admitReason = None,
            DateAdmission = None
        )
        medical.save()
        return medical
    """
    Updates medical information via the medical_form
    """
    def Update(self,medical_form):
        self.blood_Type = medical_form['blood_Type']
        self.weight     = medical_form['weight'    ]
        self.height_feet= medical_form['height_feet']
        self.height_inches = medical_form['height_inches']
        self.sex        = medical_form['sex'       ]
        self.save()

    def Admit(self,reason,date):
        self.admit = True
        self.admitReason = reason
        self.DateAdmission = date
        self.save()

    def Discharge(self):
        self.admit = False
        self.admitReason = None
        self.DateAdmission = None
        self.save()
    """
    Returns a string for admin
    """
    def __str__(self):
        return self.medical_ID + " medical"

"""
A class used to represent the Patient.
:atrb: name:        The name of the Patient.
:atrb: username:    The patients username, used to easily describe info
:atrb: DOB:         Users date of Birth
:atrb: hospital:    The name of the hospital the user is in
:atrb: contact:     The users contact information
:atrb: medical:     The users medical information
"""
class Patient(models.Model):
    user     = models.OneToOneField(User,on_delete = models.CASCADE, default = None)
    username = models.CharField    (max_length = 100, default = "")
    first_name = models.CharField  (blank=False,max_length= 25, default= "")
    last_name  = models.CharField    (blank = False   , default = "", max_length = 50)
    DOB      = models.DateField    (blank = False   )
    hospital = models.ForeignKey   (Hospital, default = None)
    admit = models.NullBooleanField(blank=True)
    insurance= models.CharField    (blank=False, max_length=100,default='')
    PolicyNumber = models.CharField (blank=False, max_length=100,default='')
    #sets the contact information
    contact  = models.ForeignKey(
        ContactInfo,
        on_delete = models.CASCADE,
        default   = None,
        blank     = False
    )
    #sets a medical class
    medical = models.ForeignKey(
        MedicalInfo,
        on_delete = models.CASCADE,
        default   = None,
        blank     = False
    )

    """
    Creates a patient using form data. This allows the system to creates
    a patient with user info and associated to a user
    :arg
        user_form:      cleaned_data representing user info
        patient_form    cleaned_data representing patient info
        contact_form    cleaned_data representing contact info
        medical_form    cleaned_data representing medical info
    """
    def createPatient(user_form, patient_form, contact_form, medical_form,user):
        #Creates the user profile.
        credentials = User.objects.create_user(
            first_name    = user_form   ['first_name'   ],
            last_name     = user_form   ['last_name'    ],
            username      = user_form   ['username'     ],
            email         = user_form   ['email'        ],
            password      = user_form   ['password'     ],
        )
        #creates contact information
        contact = ContactInfo.createContact(contact_form, credentials.username)
        #creates a new medical information
        medical = MedicalInfo.createMedical(medical_form,credentials.username)
        #creates a new patient
        patient = Patient(
            user          = credentials,
            username      = credentials.username,
            first_name    = credentials.first_name,
            last_name     = credentials.last_name,
            DOB           = patient_form['DOB'       ],
            hospital      = patient_form['hospital'  ],
            insurance     = patient_form['insurance'],
            PolicyNumber  = patient_form['PolicyNumber'],
            contact       = contact,
            medical       = medical,
            admit = False

        )
        #saves the patient
        patient.save()
        if user == '':
            Activity.createActivity(timezone.now(), "User self registered: " , credentials.username,user,
                                    patient_form['hospital'], "CreatePatient")
        else:
            Activity.createActivity(timezone.now(), "created a new patient: ", credentials.username,
                                    user,patient_form['hospital'], "CreatePatient")
        return patient
    """
    Updates the contact information
    :arg
        contact_form:   the cleaned data representing the new contact information
    """
    def UpdateContact(self,contact_form,user):
        self.contact.Update(contact_form)
        Activity.createActivity(timezone.now(),"Updated contact information: ",self.username,'', self.hospital, "UpdateProfile")
        return self

    """
    Updates the medical information
    :arg
        medical_form:   the cleaned data representing the new medical information
    """
    def UpdateMedical(self,medical_form,user):
        self.medical.Update(medical_form)
        Activity.createActivity(timezone.now(),"updated medical for",self.username,user,self.hospital, "UpdateProfile")
        return self

    def getAppointments(self):
        today = timezone.now()
        appointments = Appointment.objects.filter(patient_ID = self.username)
        oldappointments = appointments.filter(date__lt = timezone.now() )
        for appointment in oldappointments:
            appointment.delete()
        appointments = Appointment.objects.filter(patient_ID=self.username)
        return appointments
    """
    Transfers a patient to a new hospital
    :arg
        hospital: the new hospital that the patient is going to
    """
    def PatientTransfer(self,hospital):
        self.hospital = hospital
        self.save()
        Activity.createActivity(timezone.now(),"transferred to", hospital,self.username,self.hospital, "Transfer")

    def AdmitPatient(self,reason,date,user):
        self.admit = True
        Activity.createActivity(date," admitted " + str(self.username) + " for " + str(reason), "", user, self.hospital, "Admit")
        self.medical.Admit(reason,date)
        self.save()

    def Discharge(self):
        self.admit = False
        Activity.createActivity(timezone.now(), "was discharged from", self.hospital, self.username,self.hospital, "Discharge")
        self.medical.Discharge()
        self.save()

    """
        Creates a to string
        """

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.user.username + ")"
