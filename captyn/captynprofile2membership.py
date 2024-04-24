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


captyn_membership_cols = [
    'Offering ID',
    'Account',
    'Participant First Name',
    'Participant Last Name',
    'Status',
    'Renewal Date'
]


def create_captyn_membership(captyn_profile_row, offering_id, renewal_date):
    '''Returns a row containing a Captyn membership to be used by a csv.DictWriter.

    captyn_profile_row: A csv.DictReader row containing a Captyn profile record.
    '''

    captyn_membership_row = {
        'Offering ID': offering_id,
        'Account': captyn_profile_row['Attached Account Email'],
        'Participant First Name': captyn_profile_row['First Name'],
        'Participant Last Name': captyn_profile_row['Last Name'],
        'Status':'Enrolled',
        'Renewal Date': renewal_date
    }

    return captyn_membership_row


def create_captyn_memberships(captyn_profile_filename, captyn_memberships_filename, offering_id, renewal_date):
    '''Generates a CSV file that contains Captyn memberships using an exported Captyn profile CSV file

    The output file can be provided to Captyn to bulk add all entries as a members to a Membership.
    '''

    memberships_count = 0

    captyn_memberships_file = open(captyn_memberships_filename, 'w', newline='')
    captyn_memberships = csv.DictWriter(captyn_memberships_file, fieldnames=captyn_membership_cols)
    captyn_memberships.writeheader()

    captyn_profile_file = open(captyn_profile_filename, 'r')
    captyn_profile = csv.DictReader(captyn_profile_file)
    for captyn_profile_row in captyn_profile:
        captyn_membership_row = create_captyn_membership(captyn_profile_row, offering_id, renewal_date)
        if captyn_membership_row:
            captyn_memberships.writerow(captyn_membership_row)
            memberships_count+=1

    captyn_memberships_file.close()

    print('Saved {}\nMemberships: {}'.format(captyn_memberships_filename, memberships_count))


def main():
    captyn_profile_filename = 'data/captyn_Profiles-Export-2024-04-24-0832.csv'
    captyn_memberships_filename = 'data/captyn_membership.csv'

    offering_id = '12345678'
    renewal_date = '09/01/2024'

    create_captyn_memberships(captyn_profile_filename, captyn_memberships_filename, offering_id, renewal_date)


if __name__ == '__main__':
    main()