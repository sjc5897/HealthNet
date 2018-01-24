from django.db import models
from django.utils import timezone
from .activity import Activity
from .patient import Patient

class Drug( models.Model ):
    name  = models.CharField   ( default = ''  , max_length = 100                   )
    price = models.DecimalField( default = 0.00, decimal_places = 2, max_digits = 10)

    def createNewDrug(drug_form, user):
        drug = Drug(
            name  = drug_form['drug' ],
            price = drug_form['price']
        )
        drug.save()
        Activity.createActivity(timezone.now(), "added new drug to the database called ", drug.name, user, None, "CreateDrug")
        return drug

    def updatePrice(self, price, user):
        self.price = price
        self.save()
        Activity.createActivity(timezone.now(), "changed to price of " + self.name.__str__() + " to ", price, user, None, "UpdateDrug")

    def __str__(self):
        return self.name


"""
This Class represents a prescription given by a doctor
:atrb: expiration       the date that the prescription expires
:atrb: refills          the number of refills remaining
:atrb: quantity         the amount of the drug per refill
:atrb: drug             the name of the drug
:atrb: user_ID          the user ID that corresponds to this prescription
:atrb: directions       a set of instructions, describing how to use the drug
"""
class Prescription( models.Model ):
    drug       = models.ForeignKey   ( Drug   , on_delete = models.CASCADE, default = None)
    user_ID    = models.ForeignKey   ( Patient, on_delete = models.CASCADE, default = None)
    expiration = models.DateTimeField( default = timezone.now)
    lastRefill = models.DateTimeField( default = timezone.now)
    refills    = models.IntegerField ( default = 0           )
    quantity   = models.IntegerField ( default = 0           )
    directions = models.TextField    ( default = ''          )

    #creates a new prescription
    def createPrescription(prescription_form, user):
        prescription = Prescription(
            expiration = prescription_form['expiration'],
            refills    = prescription_form['refills'   ],
            quantity   = prescription_form['quantity'  ],
            drug       = prescription_form['drug'      ],
            user_ID    = prescription_form['user_ID'   ],
            directions = prescription_form['directions']
        )
        prescription.save()
        Activity.createActivity(timezone.now(), "Prescribed " + prescription.drug.name + " to ", prescription.user_ID, user,
                                Patient.objects.filter(user= prescription_form['user_ID'].user)[0].hospital, "CreatePrescription")
        return prescription

    #removes a prescription
    def removePrescription(self, user):
        Activity.createActivity(timezone.now(), "removed prescription for " + self.drug.name + " from ", self.user_ID,
                                user,Patient.objects.filter(user = self.user_ID.user)[0].hospital, "DeletePrescription")
        self.delete()

    #refills a prescription
    def refill(self, user):
        #if timezone.now() - timezone.timedelta(days = 30) < self.lastRefill:
        #    return
        #elif self.expiration > timezone.now():
        #    return
        #elif self.refills > 0:
        #    return
        #else:
        self.refills -= 1
        self.lastRefill = timezone.now()
        Activity.createActivity(timezone.now(), "refilled ", self.drug.name, user,
                                Patient.objects.filter(username = self.user_ID.user)[0].hospital, "RefillPrescription")

    def __str__(self):
        return self.drug.name