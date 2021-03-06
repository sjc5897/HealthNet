# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-05-09 10:17
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('User_ID', models.CharField(default='', max_length=100)),
                ('Effected_ID', models.CharField(default='', max_length=100)),
                ('Activity_Type', models.CharField(choices=[('CreatePatient', 'Patient Creation'), ('CreatePrescription', 'Prescription Creation'), ('CreateDrug', 'Drug Creation'), ('CreateAppointment', 'Appointment Creation'), ('AdminCreation', 'Admin Creation'), ('EditAppointment', 'Appointment Edits'), ('CancelAppointment', 'Appointment Cancellations'), ('LogIn', 'User Log In'), ('LogOut', 'User Log Out'), ('MessageSent', 'Messages Sent'), ('Transfer', 'Patient Transfer'), ('Admit', 'Patient Admitted to Hospital'), ('Discharge', 'Patient Discharged from Hospital'), ('UpdateProfile', 'Profile Information Updates'), ('UpdateDrug', 'Drug Price Updates'), ('DeletePrescription', 'Prescriptions Deleted'), ('RefillPrescription', 'Prescription Refills'), ('CreateDoctor', 'Doctor Creation'), ('CreateNurse', 'Nurse Creation'), ('HospitalCreated', 'Hospital Creation'), ('UploadFiles', 'Files Uploaded'), ('ReleaseFiles', 'Files Released'), ('ViewInformation', 'Information Viewed')], default='', max_length=100)),
                ('Activity_Details', models.TextField(default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('office', models.IntegerField(verbose_name='Room number:')),
                ('patient_ID', models.CharField(default='', max_length=100)),
                ('doctor_ID', models.CharField(default='', max_length=100)),
                ('description', models.TextField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Patient_ID', models.CharField(default='', max_length=20)),
                ('address', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=10)),
                ('state', models.CharField(choices=[('AK', 'Alaska'), ('AL', 'Alabama'), ('AR', 'Arkansas'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DC', 'District of Columbia'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('IA', 'Iowa'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('MA', 'Massachusetts'), ('MD', 'Maryland'), ('ME', 'Maine'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MO', 'Missouri'), ('MP', 'Northern Mariana Islands'), ('MS', 'Mississippi'), ('MT', 'Montana'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('NE', 'Nebraska'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NV', 'Nevada'), ('NY', 'New York'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VA', 'Virginia'), ('VI', 'Virgin Islands'), ('VT', 'Vermont'), ('WA', 'Washington'), ('WI', 'Wisconsin'), ('WV', 'West Virginia'), ('WY', 'Wyoming')], default='', max_length=20)),
                ('zip', models.CharField(default='', max_length=5)),
                ('city', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=10)),
                ('specialty', models.CharField(default='', max_length=100)),
                ('office_hours_start', models.TimeField(default=django.utils.timezone.now)),
                ('office_hours_end', models.TimeField(default=django.utils.timezone.now)),
                ('office', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=75)),
                ('address', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=30)),
                ('state', models.CharField(choices=[('AK', 'Alaska'), ('AL', 'Alabama'), ('AR', 'Arkansas'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DC', 'District of Columbia'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('IA', 'Iowa'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('MA', 'Massachusetts'), ('MD', 'Maryland'), ('ME', 'Maine'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MO', 'Missouri'), ('MP', 'Northern Mariana Islands'), ('MS', 'Mississippi'), ('MT', 'Montana'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('NE', 'Nebraska'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NV', 'Nevada'), ('NY', 'New York'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VA', 'Virginia'), ('VI', 'Virgin Islands'), ('VT', 'Vermont'), ('WA', 'Washington'), ('WI', 'Wisconsin'), ('WV', 'West Virginia'), ('WY', 'Wyoming')], default='', max_length=20)),
                ('zip', models.CharField(default='', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_ID', models.CharField(default='', max_length=20)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=1)),
                ('weight', models.CharField(default='', max_length=3)),
                ('height_feet', models.CharField(default='', max_length=1)),
                ('height_inches', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(11)])),
                ('blood_Type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], default='', max_length=3)),
                ('admit', models.NullBooleanField()),
                ('admitReason', models.CharField(blank=True, choices=[('Appointment', 'Appointment'), ('Checkup', 'Checkup'), ('In Labor', 'In Labor'), ('Intensive Care', 'Intensive Care'), ('Observation', 'Observation'), ('Surgery', 'Surgery'), ('Other', 'Other')], default='Not', max_length=20, null=True)),
                ('DateAdmission', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_ID', models.CharField(default='', max_length=20)),
                ('comments', models.CharField(default='', max_length=140)),
                ('attachedFiles', models.FileField(upload_to='documents/%Y/%m/%d')),
                ('released', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('Sender_ID', models.CharField(default='', max_length=100)),
                ('Receiver_ID', models.CharField(default='', max_length=100)),
                ('SenderDelete', models.BooleanField(default=False)),
                ('ReceiverDelete', models.BooleanField(default=False)),
                ('Subject', models.CharField(default='', max_length=100)),
                ('Message', models.TextField(default='', max_length=1250)),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('email', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=10)),
                ('hospital', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Hospital')),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('first_name', models.CharField(default='', max_length=25)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('DOB', models.DateField()),
                ('admit', models.NullBooleanField()),
                ('insurance', models.CharField(default='', max_length=100)),
                ('PolicyNumber', models.CharField(default='', max_length=100)),
                ('contact', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.ContactInfo')),
                ('hospital', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Hospital')),
                ('medical', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.MedicalInfo')),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiration', models.DateTimeField(default=django.utils.timezone.now)),
                ('lastRefill', models.DateTimeField(default=django.utils.timezone.now)),
                ('refills', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('directions', models.TextField(default='')),
                ('drug', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Drug')),
                ('user_ID', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='hospital',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Hospital'),
        ),
        migrations.AddField(
            model_name='activity',
            name='Hospital',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Hospital'),
        ),
    ]
