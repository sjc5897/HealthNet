from django.conf.urls import url
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='home'
urlpatterns = [
    # ex: /home/
    url(r'^$', views.index, name='index'),
    # ex: /home/patient/
    url(r'^patient/$', views.PatientView, name='patient'),
    # ex: /home/messages/
    url(r'^messages/$', views.MessagesView.as_view(), name='messages'),
    url(r'^messages/delete/(?P<message_id>[0-9]+)/$',views.Delete, name = 'delete'),
    # ex: /home/outbox/
    url(r'^outbox/$', views.OutboxView, name='outbox'),
    # ex: /home/messages/newmessage/
    url(r'^messages/newmessage$', views.NewMessage.as_view(), name='newmessage'),
    url(r'^messages/(?P<message_id>[0-9]+)/reply/$', views.Reply.as_view(), name='reply'),
    # ex: /home/messages/messagedetail/
    url(r'^messages/(?P<message_id>[0-9]+)/$', views.MessageDetail.as_view(), name='messageDetail'),
    # ex: /home/messages/messagedetail2/
    url(r'^messages2/(?P<message_id>[0-9]+)/$', views.MessageDetail2.as_view(), name='messageDetail2'),
    # ex: /home/administrator# ex: /home/administrator
    url(r'^administrator/$', views.AdministratorView.as_view(), name='administrator'),
    # ex: /home/doctor/
    url(r'doctor/$', views.DoctorView, name='doctor'),
    url(r'doctor/create/$', views.DoctorReg.as_view(), name='DoctorReg'),
    url(r'nurse/create/$', views.NurseReg.as_view(), name='NurseReg'),
    url(r'hospital/create/$', views.HospitalReg.as_view(), name='HospitalReg'),
    url(r'admin/create/$', views.AdminReg.as_view(), name='AdminReg'),
    # ex: /home/nurse
    url(r'^nurse/$',views.NurseView, name='nurse'),
    # ex: home/patient/unique_username
    url(r'^patient/(?P<username>.+)/$', views.pDetail, name='pDetail'),
    # ex: home/doctor/unique_username
    url(r'^doctor/(?P<username>.+)/$', views.dDetail, name='dDetail'),
    # ex: home/nurse/unique_username
    url(r'^nurse/(?P<username>.+)$', views.nDetail, name='nDetail'),
    # ex: 1/appointmentDetail
    url(r'^(?P<appointment_id>[0-9]+)/appointmentDetail/$', views.AppointmentDetail, name='AppointmentDetails'),
    # ex: home/register/
    url(r'register/', views.RegistrationForm.as_view(), name='register'),
    # ex: home/activities/
    url(r'activities/', views.ActivityView, name='activities'),
    # ex: /unique_username/contact
    url(r'^(?P<patient_id>[0-9]+)/contact/$',views.ContactEditForm.as_view(), name='contact'),
    # ex: /unique_username/medical
    url(r'^(?P<patient_id>[0-9]+)/medical/$',views.MedicalEditForm.as_view(), name='medical'),
    # ex: login/
    url(r'login/$', views.LoginView.as_view(),name='login'),
    # ex: logout/
    url(r'logout/$', views.LogOutView.as_view(),name='logout'),
    # ex: /unique_username/appointmentCal/
    url(r'^(?P<username>.+)/appointmentCal/$', views.CalendarView.as_view(), name='appointmentCal'),
    # ex: /unique_username/appointmentCal7/
    url(r'^(?P<username>.+)/appointmentCal7/$', views.nCal7.as_view(), name='nCal7'),
    # ex: /unique_username/appointmentCal/CreateAppointment
    url(r'^(?P<username>.+)/appointmentCal/CreateAppointment/$', views.newAppointment.as_view(), name="CreateAppointment"),
    # ex: 1/appointmentEdit/
    url(r'^(?P<appointment_id>[0-9]+)/appointmentEdit/$',views.EditAppointment.as_view(), name="EditAppointment"),
    # ex: 1/cancelAppointment/
    url(r'^(?P<appointment_id>[0-9]+)/cancelAppointment/$',views.CancelAppointment.as_view(), name="CancelAppointment"),
    # ex: /filterPatient
    url(r'filterPatient/$',views.FilterPatientView.as_view(),name = 'FilterPatients'),
    url(r'filterActivity/$',views.FilterActivity.as_view(),name = 'FilterActivity'),
    url(r'tests/(?P<username>.+)/$',views.test, name = 'test'),
    url(r'createDrug',views.NewDrug.as_view(), name = 'NewDrug'),
    # ex: unique_username/transfer
	url(r'^(?P<username>.+)/transfer/$',views.Transfer.as_view(),name = 'Transfer'),
    url(r'^(?P<username>.+)/prescriptions/$', views.PrescriptionView.as_view(), name = 'prescriptions'),
    url(r'^(?P<prescription_id>[0-9]+)/$', views.PrescriptionDetail.as_view(), name = "prescriptionDetail"),
    url(r'^(?P<prescription_id>[0-9]+)/refill/$', views.Refill.as_view(), name = "refill"),
    url(r'^newPrescription/$', views.NewPrescription.as_view(), name = "newPrescription"),
    url(r'^(?P<prescription_id>[0-9]+)/deleteConfirmation/$', views.DeletePrescriptionConfirmation.as_view(), name = "deletePrescriptionConfirmation"),
    url(r'^(?P<prescription_id>[0-9]+)/delete/$', views.DeletePrescription.as_view(), name = "deletePrescription"),
    url(r'hospital/$', views.HospitalView.as_view(), name='hospital'),
    # url(r'^list/$', views.list, name='list'),
    url(r'list/(?P<username>.+)/$', views.List, name='list'),
    url(r'^admit/$', views.Admit.as_view(), name = 'admit'),
    url(r'^admitted/$', views.AdmittedView.as_view(), name='admitted'),
    url(r'^(?P<username>.+)/discharge$', views.Discharge, name = 'Discharge'),
    url(r'release/(?P<test_id>[0-9]+)/(?P<username>.+)', views.release, name = 'release'),
    url(r'export/(?P<test_id>[0-9]+)/$',views.Export.as_view(), name = 'export'),
    url(r'statistics/$', views.Statistics.as_view(), name = "statistics"),
    url(r'filterStatistics/$', views.FilterStatistics.as_view(), name = "filterStatistics"),
    url(r'^hospitalList/$',views.HospitalList,name = 'hospitalList'),
    url(r'^hospitalList/(?P<hospital_id>[0-9]+)$',views.HospitalEdit.as_view(),name = 'editHospital'),
    url(r'^drugList/$',views.DrugList,name='drugList'),
    url(r'^drugList/(?P<drug_id>[0-9]+)/$',views.DrugEdit.as_view(),name='editDrug'),
    url(r'^drugList/(?P<drug_id>[0-9]+)/delete$',views.deleteDrug,name='drugDelete'),
    url(r'^Nedit/(?P<username>.+)/$',views.EditNurse.as_view(),name = 'editNurse'),
    url(r'^Dedit/(?P<username>.+)/$',views.EditDoctor.as_view(),name = 'editDoctor')
]