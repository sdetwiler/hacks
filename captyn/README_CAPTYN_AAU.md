# Captyn AAU
Captyn Membership synchronization for AAU Swimming


# Setup
Create a Membership in Captyn for AAU Swimming

AAU Swimming charges $22/year for the extended coverage option and renews every September 1st.


## captynprofile2membership
Generates a CSV file that can be manually given to Captyn to add all Captyn Profiles as members to a Captyn Membership.

This is used to initially load all profiles into the AAU membership.


## captyngroup2membership
Generates a CSV file that can be manually given to Captyn to add all Captyn Group offering members to a Captyn Membership.

This is used to load all group members into the AAU membership.


## captyn2aau
Generates a CSV file that can be loaded into AAU from a Captyn membership CSV export.

Use this to load all members from the Captyn AAU Swimming Membership into AAU to keep them in sync.



# Creating AAU Memberships From Captyn Data
This is used to register all swimmers for AAU Swimming that have the Captyn AAU Membership 

Export the Membership list for the AAU Swimming membership that was created in Captyn


AAU Club Code: W3D794

Importing participants that already exist is ok... AAU detects and notes they're in the system 

Need to add to Captyn Export
* Gender
* Birthdate


X a. First Name
X b. Middle Name (field may be left blank)
X c. Last Name
d. Date of Birth (mm/dd/yyyy)
e. Gender (M-Male, F-Female)
X f. 10 digit Phone Number
X g. Email Address (field may be left blank)
X h. Street Address
X i. City
X j. 2 digit State code
X k. 5 digit Zip Code



Upload CSV to AAU https://play.aausports.org/joinaau/importathletememberships.aspx


# Creating Captyn Membership Enrollments from AAU Data
This is needed if swimmers first register in AAU Swimming and that needs to be connected in Captyn

In AAU export the team roster



Capytn to AAU input
AAU to Captyn input
