from django.contrib import admin
from .models import *

admin.site.register(Nurse)
admin.site.register(Doctor)
admin.site.register(Activity)
admin.site.register(Hospital)
admin.site.register(Prescription)
admin.site.register(Drug)
admin.site.register(MedTest)
admin.site.register(Messages)