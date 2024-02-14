#!/usr/bin/env python3

import csv

'''
# iClassPro to Captyn Data Conversion

This tool converts account information from iClassPro to a CSV format that can be imported into Captyn.

# Usage Notes

    1. Export all columns from iClassPro to a CSV file.
    2. Edit the exported CSV and append numbers to the following column names to make them unique:
        Secondary Guardian Name -> 1,2,3,4
        Secondary Phone Number -> 1,2,3
        Secondary Email -> 1,2

    3. Ensure the iclass_event_to_captyn_offering table correctly reflects the mapping for your use.
    4. Add any custom columns to captyn_accounts_and_participants_cols
    5. Update any column mappings in iclass_to_captyn_account and iclass_to_captyn_participant
    6. in the main() function, edit the filename to match your iClassPro CSV export
    7. Run and enjoy.
'''


def transform_first_name(v):
    '''Extract the first name from an iClassPro full name in the format "Last, First"'''

    return v.split(',')[-1].strip().title()


def transform_last_name(v):
    '''Extract the first name from an iClassPro full name in the format "Last, First"'''

    return v.split(',')[0].strip().title()


def transform_full_name(v):
    '''Format a full name to the format "First Last" from an iClassPro full name in the format "Last, First"'''
    
    tokens = v.split(',')
    return ' '.join([tokens[-1]] + tokens[0:-1]).strip().title()


def transform_secondary_contact(v):
    '''Format a full name to the format "To First Last" from an iClassPro full name in the format "Last, First"'''

    return 'To ' + transform_full_name(v)

def transform_phone_number(v):
    '''
    Sanitize various phone number formats to a common format of 123-456-7890
    and retain any trailing string that might contain an extension or other information.
    '''
    
    v = v.replace('-', '')
    v = v.replace('(', '')
    v = v.replace(')', '')
    v = v.replace(' ', '')
    if len(v) == 0:
        return v
    
    # Remove country code escape prefix
    if v[0] == '+':
        v = v[1:]
    # Remove leading US country code 1 if it exists
    if v[0] == '1':
        v = v[1:]
    
    return v[0:3] + '-' + v[3:6] + '-' + v[6:10] + v[10:]


def transform_state(v):
    '''Extract the two character state from an iClassPro state value in the format CA-US'''

    return v[0:2]


# All columns as exported from iClassPro. Note the required manual modifications to make all column names unique.
iclass_cols = [
    'id',
    'Student Name',
    'Primary Guardian Name',
    'Primary Email',
    'Primary Phone Number',
    'Secondary Guardian Names',
    'Secondary Guardian Name 1', # Manually added the 1,2,3 suffix and edited exported CSV to match.
    'Secondary Guardian Name 2', #
    'Secondary Guardian Name 3', #
    'Secondary Guardian Name 4', #
    'Secondary Phone Numbers',
    'Secondary Phone Number 1',  # Manually added the 1,2,3 suffix and edited exported CSV to match.
    'Secondary Phone Number 2',  #
    'Secondary Phone Number 3',  #
    'Secondary Emails',
    'Secondary Email 1',         # Manually added the 1,2 suffix and edited exported CSV to match.
    'Secondary Email 2',         #
    'Balance Due',
    'Last Payment Date',
    'Last Payment Amount',
    'Primary Address',
    'Street 1',
    'Street 2',
    'City',
    'State',
    'Zip',
    'Association Id',
    'Gender',
    'Birthday',
    'Age',
    'Student Keywords',
    'Anniversary Charge Eligibility Date',
    'Anniversary Charge Eligibility Month',
    'Roll Sheet Comment',
    'Allergies Health Concerns',
    'Hospital Clinic Preference',
    'Insurance Carrier Company',
    'Policy Number',
    'Physician Name',
    'Physician Phone',
    'Medical Information',
    'Created Date',
    'Active Enrollment Count',
    'Class Enrollment Count',
    'Camp Enrollment Count',
    'Event Name',
    'Instructors'
]


# All columns for the Captyn accounts and participants CSV. Note the custom columns.
captyn_accounts_and_participants_cols = [
    'Type',
    'Email',
    'First Name',
    'Last Name',
    'Address 1',
    'Address 2',
    'City',
    'State',
    'Zip',
    'Phone',
    'Birthdate',
    'Gender',
    'Health',
    'Participant Note',
    'Emergency Name',
    'Emergency Phone',
    'Member Since',
    'Secondary Email 1',
    'Secondary Phone 1',
    'Secondary Email 2',
    'Secondary Phone 2',
    ### CUSTOM COLUMNS
    'Secondary Contact'

]


# All columns for the Captyn enrollment CSV.
captyn_enrollment_cols = [
    'Offering ID',
    'Account',
    'Participant First Name',
    'Participant Last Name',
    'Status',
    'Private'
]


# Column mapping between iClassPro and Captyn for a Captyn Account.
# Mappings can have an optional transform function to modify the iClassPro data before saving to Captyn.
iclass_to_captyn_account = [
    {'iclass':'Primary Email', 'captyn':'Email'},
    {'iclass':'Primary Guardian Name', 'captyn':'First Name', 'transform':transform_first_name},
    {'iclass':'Primary Guardian Name', 'captyn':'Last Name', 'transform':transform_last_name},
    {'iclass':'Street 1', 'captyn':'Address 1'},
    {'iclass':'Street 2', 'captyn':'Address 2'},
    {'iclass':'City', 'captyn':'City'},
    {'iclass':'State', 'captyn':'State', 'transform':transform_state},
    {'iclass':'Zip', 'captyn':'Zip'},
    {'iclass':'Primary Phone Number', 'captyn':'Phone', 'transform':transform_phone_number},
    {'iclass':'Allergies Health Concerns', 'captyn':'Health'},
    {'iclass':'Created Date', 'captyn':'Member Since'},
]


# Column mapping between iClassPro and Captyn for a Captyn Secondary Account.
# Mappings can have an optional transform function to modify the iClassPro data before saving to Captyn.
iclass_to_captyn_secondary_account = [
    {'iclass':'Secondary Email 1', 'captyn':'Email'},
    {'iclass':'Secondary Guardian Name 1', 'captyn':'First Name', 'transform':transform_first_name},
    {'iclass':'Secondary Guardian Name 1', 'captyn':'Last Name', 'transform':transform_last_name},
    {'iclass':'Secondary Phone Number 1', 'captyn':'Phone', 'transform':transform_phone_number},
    {'iclass':'Created Date', 'captyn':'Member Since'},
    {'iclass':'Student Name', 'captyn':'Secondary Contact', 'transform':transform_secondary_contact},
]


# Column mapping between iClassPro and Captyn for a Captyn Participant.
# Mappings can have an optional transform function to modify the iClassPro data before saving to Captyn.
iclass_to_captyn_participant = [
    {'iclass':'Primary Email', 'captyn':'Email'},
    {'iclass':'Student Name', 'captyn':'First Name', 'transform':transform_first_name},
    {'iclass':'Student Name', 'captyn':'Last Name', 'transform':transform_last_name},
    {'iclass':'Birthday', 'captyn':'Birthdate'},
    {'iclass':'Gender', 'captyn':'Gender'},
    {'iclass':'Primary Guardian Name', 'captyn':'Emergency Name', 'transform':transform_full_name},
    {'iclass':'Primary Phone Number', 'captyn':'Emergency Phone', 'transform':transform_phone_number},
    {'iclass':'Created Date', 'captyn':'Member Since'}
]


# Mapping of iClassPro event name to Captyn offering ID.
# This defines what offering each Participant will be enrolled in.
# This must be modified to match the Team's unique naming scheme.
iclass_event_to_captyn_offering = {
    '*Junior Team':{'name':'Mavericks Juniors', 'offering_id':'mavericks_juniors'},
    'Pre Team':{'name':'Mini Marauders', 'offering_id':'school_pre_team'},
    '*Junior Elite Team':{'name':'Mavericks Junior Elite', 'offering_id':'mavericks_junior_elite'},
    'Marauders':{'name':'Marauders', 'offering_id':'marauders'},
    'Mini Marauders':{'name':'Mini Marauders', 'offering_id':'mini_marauders'},
    '*Senior Developmental Team':{'name':'Mavericks Senior Developmental', 'offering_id':'maverics_senior_developmental'},
    '*Developmental Team':{'name':'Mavericks Developmental', 'offering_id':'mavericks_developmental'},
    '*Maverick Elite Team':{'name':'Mavericks Seniors', 'offering_id':'mavericks_seniors'},
    '*Armada Jr Elite':{'name':'Mavericks Junior Elite', 'offering_id':'mavericks_junior_elite'}
}


def populate_captyn_row(captyn_row, iclass_row, mappings):
    ''' Populates the captyn_row with values from the iclass_row using the provided mappings.

    captyn_row: A csv.DictWriter row containing Captyn record.
    iclass_row: A csv.DictReader row containing an iClassPro record.
    mappings: A mapping list that describes which iClassPro columns map to Captyn columns.
    '''
    for mapping in mappings:
        if 'transform' in mapping:
            v = mapping['transform'](iclass_row[mapping['iclass']])
        else:
            v = iclass_row[mapping['iclass']]

        # Filter out newlines.
        v = v.replace('\n', ' ')

        # Filter out iclass default empty string.
        if v != '--':
            captyn_row[mapping['captyn']] = v

    return captyn_row


def create_captyn_account(iclass_row):
    '''Returns a row containing a Captyn account to be used by a csv.DictWriter.
    
    iclass_row: A csv.DictReader row containing an iClassPro record.
    '''

    captyn_row = {'Type':'Account'}
    return populate_captyn_row(captyn_row, iclass_row, iclass_to_captyn_account)


def create_captyn_secondary_account(iclass_row):
    '''Returns a row containing a Captyn account to be used by a csv.DictWriter.
    
    iclass_row: A csv.DictReader row containing an iClassPro record with a Secondary Email 1.
    '''

    captyn_row = {'Type':'Account'}
    return populate_captyn_row(captyn_row, iclass_row, iclass_to_captyn_secondary_account)


def create_captyn_participant(iclass_row):
    '''Returns a row containing a Captyn participant to be used by a csv.DictWriter.
    
    iclass_row: A csv.DictReader row containing an iClassPro record.
    '''

    captyn_row = {'Type':'Participant'}
    return populate_captyn_row(captyn_row, iclass_row, iclass_to_captyn_participant)


def create_captyn_enrollment(iclass_row, event_id):
    ''' Returns a row containing a Captyn enrollment to be used by a csv.DictWriter.
    
    iclass_row: A csv.DictReader row containing an iClassPro record.
    event_id: A single event id from iClassPro that will be mapped to a Captyn offering.
    '''

    if event_id not in iclass_event_to_captyn_offering:
        print('  Unknown event from iClassPro: "{}".\n  Check iclass_event_to_captyn_offering to ensure your mappings are correct.\n'.format(event_id))
        return None

    captyn_row = {
        'Offering ID': iclass_event_to_captyn_offering[event_id]['offering_id'],
        'Account': iclass_row['Primary Email'],
        'Participant First Name':transform_first_name(iclass_row['Student Name']),
        'Participant Last Name':transform_last_name(iclass_row['Student Name']),
        'Status':'Enrolled'
    }

    return captyn_row


def create_captyn_accounts_and_participants(iclass_export_filename, captyn_accounts_and_participants_filename):
    '''Generates a CSV file that contains Captyn accounts and participants using an exported iClassPro CSV file.
    '''
    
    accounts_count = 0
    secondary_accounts_count = 0
    participants_count = 0
    accounts = []

    captyn_file = open(captyn_accounts_and_participants_filename, 'w', newline='')
    captyn = csv.DictWriter(captyn_file, fieldnames=captyn_accounts_and_participants_cols)
    captyn.writeheader()

    iclass_file = open(iclass_export_filename, 'r')
    iclass = csv.DictReader(iclass_file)
    for iclass_row in iclass:
        email = iclass_row['Primary Email']
        if email not in accounts:
            captyn_row = create_captyn_account(iclass_row)
            captyn.writerow(captyn_row)
            accounts.append(email)
            accounts_count+=1

        secondary_email = iclass_row['Secondary Email 1']
        if secondary_email == '--':
            secondary_email = ''
        if len(secondary_email) > 0:
            if secondary_email not in accounts:
                captyn_row = create_captyn_secondary_account(iclass_row)
                captyn.writerow(captyn_row)
                accounts.append(secondary_email)
                secondary_accounts_count+=1


        captyn_row = create_captyn_participant(iclass_row)            
        captyn.writerow(captyn_row)
        participants_count+=1

    captyn_file.close()
    print('Saved {}\nAccounts: {}\nSecondary Accounts: {}\nParticipants: {}'.format(captyn_accounts_and_participants_filename, accounts_count, secondary_accounts_count, participants_count))



def create_captyn_enrollments(iclass_export_filename, captyn_enrollments_filename):
    '''Generates a CSV file that contains Captyn enrollments using an exported iClassPro CSV file.
    '''
    
    enrollments_count = 0

    captyn_file = open(captyn_enrollments_filename, 'w', newline='')
    captyn = csv.DictWriter(captyn_file, fieldnames=captyn_enrollment_cols)
    captyn.writeheader()

    iclass_file = open(iclass_export_filename, 'r')
    iclass = csv.DictReader(iclass_file)
    for iclass_row in iclass:
        # iClassPro comma separates all classes the participant is enrolled in.
        # Split them apart and generate a separate enrollment for each value.
        event_ids = iclass_row['Event Name'].split(',')
        if len(event_ids) == 0:
            print('  Warning: No iClassPro enrollments for {}'.format(iclass_row['Student Name']))

        for event_id in event_ids:
            event_id = event_id.strip()
            captyn_row = create_captyn_enrollment(iclass_row, event_id)
            if captyn_row:
                captyn.writerow(captyn_row)
                enrollments_count+=1

    captyn_file.close()

    print('Saved {}\nEnrollments: {}'.format(captyn_enrollments_filename, enrollments_count))


def main():
    iclass_export_filename = 'iclass_20240207_export.csv'

    captyn_accounts_and_participants_filename = 'captyn_accounts_and_participants.csv'
    captyn_enrollments_filename = 'captyn_enrollments.csv'

    create_captyn_accounts_and_participants(iclass_export_filename, captyn_accounts_and_participants_filename)
    create_captyn_enrollments(iclass_export_filename, captyn_enrollments_filename)


if __name__ == '__main__':
    main()