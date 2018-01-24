from .forms import *
from django.test import TestCase
from django.test import client
from .views import *
from .models import *
from django.test import RequestFactory

# Create your tests here.
def main():
    pass

#===================================FORM TEST CASES=================================================================#
class UserFormTestCase(TestCase):
    def test_forms(self):
        user_form = {'username':"ted",'password':"ted",'password_confirm':"ted",'email':"a@gmail.com",'first_name':"ted",'last_name':"cruise"}
        form = UserForm(data=user_form)
        self.assertTrue(form.is_valid())

"""
class PatientFormTestCase(TestCase):
    def test_forms(self):
        patient_form = {'DOB':"01-01-2000",'insurance':"test",'PolicyNumber':"1",'hospital':"a real hospital"}
        form = PatientUserForm(data=patient_form)
        self.assertTrue(form.is_valid())
"""
class MessageFormTestCase(TestCase):
    def test_forms(self):
        message_form = {'Receiver_ID':"ted",'Subject':"test",'Message':"Nothing"}
        form = MessageForm(data=message_form)
        self.assertTrue(form.is_valid())

#===================================END FORM TEST CASES=================================================================#

def regiTest():
    pass

def editTest():
    pass

class testHospital(TestCase):
    def createHospital(self):
        hospital = Hospital
