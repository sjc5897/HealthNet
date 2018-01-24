from django.db import models
from django.conf import settings
from .patient import Patient
import os

class MedTest(models.Model):
    # attributes
    patient_ID = models.CharField(max_length=20, default='')  # patient user ID

    comments = models.CharField(max_length=140, default='')  # doctor comments regarding patient test results

    attachedFiles = models.FileField(upload_to='documents/%Y/%m/%d')  # TODO

    released = models.BooleanField(default = False)  # release status - True if released, False otherwise

    @property
    def filename(self):
        return os.path.basename(self.attachedFiles.name)

    def __str__(self):
        return self.patient_ID + self.comments

    # Methods
    def release_test(self):
        self.released = True
        self.save()
