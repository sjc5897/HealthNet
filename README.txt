Welcome to the Healthnet web application (Release 2). This application was built using Django 1.9.1 and Python 3.4.3 
Test Liaison: Stephen Cook sjc5897@g.rit.edu
Authors: 
    -Chris Letourneau
    -Georgiy Rozenshteyn
    -Oren Rosin
    -Stephen Cook
    -Xixiao Yue
HealthNet is a web application project intended to improve communication and ease of access of data by healthcare providers. 
HealthNet is geared towards enhancing the management of patient and employee-related information, as well as facilitation of day-to-day hospital business by focusing on ease of use and navigation. 
Special consideration will be given to the development of an intuitive front-end system allowing for straightforward transfer of data and providing a platform for effective communication between patients and healthcare professionals.

In Release 2, available functions include:
    -Patient Registration
    -Administrator Registration
    -Update Patient Profile Information
    -Update Patient Medical Information
    -Create, cancel or Update Patient Appointment
    -Patient Transfer
    -Prescriptions
    -Appointment Calendar
    -Viewing Patient Medical Information, Prescriptions and Tests and Results
    -Logging System Activity 
    -Viewing Activity Log 
    -Message system
    -Viewing system statistics
Preexisting Accounts:
Admin Accounts:
	Username: admin 		Password: HelloWorld
Doctor Accounts :
	Username: DrJohnLocke 	Password: HelloWorld
	Username: DrRMHouse	Password: HelloWorld
	Username: DrLeeTwy		Password: HelloWorld
Nurse Accounts
	Username: NurseJackie	Password: HelloWorld
	Username: NurseK		Password: HelloWorld
Patient Accounts:
	Username: StephenCook	Password: HelloWorld
	Username: StephenCookSen Password: HelloWorld
	Username: WeslyFoster	 Password: HelloWorld
	
	


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
How to use the application: 

Installation and Setup:
    1. Extract the contents of the zip file to the directory of your choice
    2. Make sure that the correct version of Django (1.9.1) is installed on the system
    3. To initialize creation, It is important to create a new superuser. The superuser is
       to create hospitals, doctors, patients, and drugs. For Doctors, Patients and Nurses
       to be created, a hospital must first be created

To run the server: 
    1. Make sure there is no software using the 127.0.0.1:8000 port. 
    2. Double click the Batch file "runserver.bat" in Release-2-Beta\Healthnet
    3. The server will run under localhost:8000/

To edit information as an administration:
    1. Login to the admin page.
    2. Go to the information page using the home bar
    3. Select the user to edit.
    4. Follow the instruction to edit the information and click "SAVE" to save the changes.
	
To add another administrator:
    1. Login as an administrator and fill the information under Add New Admin pages
  OR:  If the server is not started, there is another way to add administrator
    1. Double click the Batch file "create_super_user.bat" in "\HealthNet"
    2. Follow the instruction to setup username and password and other information
    3. In order to make sure the account is successfully registered, start the server and try to login with the new administrator account

To add a hosptial:
    1. as an admin select the create new hospital button in the home bar and fill information

To add a doctor:
    1. as an admin select the create new doctor button in the home bar and fill information

To add a nurse:
    1. as an admin select the create new nurse button in the home bar and fill information

To add a drug:
    1. as an admin select the create new drug button in the home bar and fill information

Uses of Filter:
    All forms in filter is optional. Just leave blank if you want to see all the results. 

To Transfer Patients:
    1. Be logged into an admin or doctor account and go to the desired profile
    2. Hit the transfer link on the patient's profile
    3. If an admin select the destination or if doctor choice is auto selected to doctors hospital
    4. Confirm intent to transfer patient 
	
To view and update patient's medical information:
    1. Make sure you are logged into the valid account. 
    2. Go to the home page and select "View Patient Profiles"
    3. Select the patient you want. 
    4. Select "Edit Medical Information" to change the information.
    5. Click "Save changes" to save the changes.
	
To add an appointment:
    1. Select Doctor list on home page
    2. Select  the doctor you want to have an appointment with
    3. Select "View Calendar"
    4. Select "Schedule an appointment" and edit the appointment information
    5. Select "save changes" and return

To view all patient in the system as a doctor:
  *By default the doctor will only view the patient in their own hospital, but you can still see all patients in the system by doing 
Select “Filter” in the Patient profile
Leave all blank and directly click search
All patient in the system will appear. 
	
To logout:
	1. Click username on the right corner to open the drop down menu
	2. Select "Logout". 
To Upload and Release Test:
	1. As a doctor go to a patient's profile page
	2. Select View test results, From here the Doctor will be able to view all test (Released or Not)
	3. To Release a test select Release Test
	4. The create a new test select upload test.
To Export a test:
	1. As a patient go to your profile and select test results
	2. Here you can view all test results that have been released.
	3. Select the export test result and confirm

To send or view messages:
	1. Logging to any account and select messages
	2. This will go to the inbox where the user can click a message to view the details
	3. After selecting a messages a user can reply by hitting reply or delete by hitting delete
	4. To create a new message go to the inbox or outbox and select create new messages and fill in the form
To admit a Patient:
	1. A doctor or nurse is to select view hospital
	2. click admit a patient and fill out the form
to discharge a patient:
	1. A doctor or nurse is to select view hospital
	2. click view admitted patient list
	3. select discharge next to the patient's name
to view Activity Log and System Statistics:
	1. Logging as in admin and select the respective button on the nav bar
TO create a Prescription:
	1. Make sure drugs exist in the drug database
	2. Logging as a doctor and go to the patient's profile page
	3. Select Prescriptions and and create new
TO Refill:
	1. Note: Prescription must be > 30 days old and not expired to Refill
	2. As a patient go to a prescription with the above conditions
	3. Select Refill


***Known Bugs and Issues***: 
    *If form for appointment edit page is invalid. Appointment gets deleted and user experiences a 404 error
    *System of Average Admit is in a weird format



