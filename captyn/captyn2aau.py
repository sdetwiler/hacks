#!/usr/bin/env python3

import csv
import transform

# CSV Fields for export from Captyn Profiles
# (Home/People/Profiles)
captyn_profiles_cols = [
    'Last Name',
    'First Name',
    'Age',
    'Birthdate',
    'Gender',
    'Medical Notes',
    'Participant Note',
    'Attached Account',
    'Attached Account Email'
]


# CSV Fields for export from Captyn Membership
# (Home/Membership Offerings/<Membership Name>/Memberships)
captyn_membership_cols = [
    'Department',
    'Title',
    'Price',
    'Participant First Name',
    'Participant Last Name',
    'Status',
    'Account First Name',
    'Account Last Name',
    'Account Email',
    'Account Phone',
    'Account Address',
    'Registration Date',
    'Renewal Date',
    'Expiration Date',
    'Emergency Contact',
    'Emergency Contact Phone',
    'AAU Membership ID' # Custom field added in Captyn
]


# CSV Fields for import to AAU 
aau_add_registration_cols = [
    'First Name',
    'Middle Name',
    'Last Name',
    'DOB mm/dd/yyyy',
    'Gender M or F',
    'Phone Number 123-123-1234',
    'Email Address',
    'Street Address',
    'City',
    'State',
    'Zipcode 12345'
]


def load_captyn_profiles_by_account_name(captyn_profiles_filename):
    '''Returns a dictionary of all Captyn profiles indexed by account name.

        captyn_profiles_filename: Filename containing CSV of Captyn profiles.
    '''

    captyn_profiles_by_name = {}
    captyn_file = open(captyn_profiles_filename, 'r')
    captyn = csv.DictReader(captyn_file)
    for captyn_row in captyn:
        k = captyn_row['First Name'] + captyn_row['Last Name']
        captyn_profiles_by_name[k] = captyn_row

    return captyn_profiles_by_name


def create_aau_registration(captyn_membership_row, captyn_profiles_by_name):
    '''Returns a row containing an AAU registration to be used by a csv.DictWriter.

        captyn_membership_row: A csv.DictReader row containing a Captyn membership record.
        captyn_profiles_by_name: A dict of Captyn profiles indexed by swimmer's concatinated first and last names. 
    '''

    k = captyn_membership_row['Participant First Name'] + captyn_membership_row['Participant Last Name']

    if k not in captyn_profiles_by_name:        
        raise KeyError('Membership account {} not found in Captyn profile export'.format(captyn_membership_row['Account Email']))

    captyn_profile = captyn_profiles_by_name[k]

    aau_row = {
        'First Name': captyn_membership_row['Participant First Name'],
        'Middle Name': '',
        'Last Name': captyn_membership_row['Participant Last Name'],
        'DOB mm/dd/yyyy': transform.captyn_date_to_aau_date(captyn_profile['Birthdate']),
        'Gender M or F': transform.captyn_gender_to_aau_gender(captyn_profile['Gender']),
        'Phone Number 123-123-1234': transform.phone_number(captyn_membership_row['Account Phone']),
        'Email Address': captyn_membership_row['Account Email'],
        'Street Address': transform.street_address_from_captyn_address(captyn_membership_row['Account Address']),
        'City': transform.city_from_captyn_address(captyn_membership_row['Account Address']),
        'State': transform.state_from_captyn_address(captyn_membership_row['Account Address']),
        'Zipcode 12345': transform.zipcode_from_captyn_address(captyn_membership_row['Account Address']),
    }

    return aau_row


def create_aau_registrations(captyn_profiles_filename, captyn_membership_filename, aau_registration_filename):
    '''Generates a CSV file that contains AAU registrations using an exported Captyn membership CSV file.

        The AAU CSV file should not include a header.
    '''

    captyn_profiles_by_account_email = load_captyn_profiles_by_account_name(captyn_profiles_filename)

    registrations_count = 0

    aau_file = open(aau_registration_filename, 'w', newline='')
    aau = csv.DictWriter(aau_file, fieldnames=aau_add_registration_cols)

    captyn_file = open(captyn_membership_filename, 'r')
    captyn = csv.DictReader(captyn_file)
    next(captyn) # skip first row, which contains Captyn membership pricing data.
    for captyn_row in captyn:
        aau_row = create_aau_registration(captyn_row, captyn_profiles_by_account_email)
        if aau_row:
            aau.writerow(aau_row)
            registrations_count+=1

    aau_file.close()

    print('Saved {}\nRegistrations: {}'.format(aau_registration_filename, registrations_count))


def main():
    # The memberships stored in Captyn that should be added to AAU.
    captyn_membership_filename = 'data/captyn_Memberships_Export-2024-04-22-2211.csv'
    
    # Full export of all Captyn profiles, used to obtain additional, required fields for AAU.
    captyn_profiles_filename = 'data/captyn_Profiles-Export-2024-04-24-0832.csv'
    
    # The output filename for the CSV that can be loaded into AAU
    aau_registration_filename = 'data/aau_add_registration.csv'

    create_aau_registrations(captyn_profiles_filename, captyn_membership_filename, aau_registration_filename)

if __name__ == '__main__':
    main()