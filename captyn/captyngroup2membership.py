#!/usr/bin/env python3

import csv
import transform


captyn_group_cols = {
    'Department',
    'Program',
    'Title',
    'Ages','Dates',
    'Price',
    'Class Times','Tags',
    'Participant First Name',
    'Participant Last Name',
    'Status',
    'Account First Name',
    'Account Last Name',
    'Account Email',
    'Account Phone',
    'Account Address',
    'Emergency Contact',
    'Emergency Contact Phone',
    'Date of Registration',
    'Date of Approval',
    'Medical Notes',
    'Oaklantis can use photos and video of my swimmer for marketing and promotional purposes.', # Custom
    'Have you applied for financial aid?',  # Custom
    'Liability Waiver & USA Swimming Registration',  # Custom
    'Billing Authorization' # Custom
}


captyn_membership_cols = [
    'Offering ID',
    'Account',
    'Participant First Name',
    'Participant Last Name',
    'Status',
    'Renewal Date'
]


def create_captyn_membership(captyn_group_row, offering_id, renewal_date):
    '''Returns a row containing a Captyn membership to be used by a csv.DictWriter.

    captyn_group_row: A csv.DictReader row containing a Captyn group record.
    '''

    captyn_membership_row = {
        'Offering ID': offering_id,
        'Account': captyn_group_row['Account Email'],
        'Participant First Name': captyn_group_row['Participant First Name'],
        'Participant Last Name': captyn_group_row['Participant Last Name'],
        'Status':'Enrolled',
        'Renewal Date': renewal_date
    }

    return captyn_membership_row


def create_captyn_memberships(captyn_group_filename, captyn_memberships_filename, offering_id, renewal_date):
    '''Generates a CSV file that contains Captyn memberships using an exported Captyn group CSV file

    The output file can be provided to Captyn to bulk add all entries as a members to a Membership.
    '''

    memberships_count = 0

    captyn_memberships_file = open(captyn_memberships_filename, 'w', newline='')
    captyn_memberships = csv.DictWriter(captyn_memberships_file, fieldnames=captyn_membership_cols)
    captyn_memberships.writeheader()

    captyn_group_file = open(captyn_group_filename, 'r')
    captyn_group = csv.DictReader(captyn_group_file)
    next(captyn_group) # skip first row, which contains Captyn membership pricing data.
    for captyn_group_row in captyn_group:
        captyn_membership_row = create_captyn_membership(captyn_group_row, offering_id, renewal_date)
        if captyn_membership_row:
            captyn_memberships.writerow(captyn_membership_row)
            memberships_count+=1

    captyn_memberships_file.close()

    print('Saved {}\nMemberships: {}'.format(captyn_memberships_filename, memberships_count))


def main():
    captyn_group_filename = 'data/captyn_Group_Registrations_Export-2024-04-22-2159.csv'
    captyn_memberships_filename = 'data/captyn_membership.csv'

    offering_id = '12345678'
    renewal_date = '09/01/2024'

    create_captyn_memberships(captyn_group_filename, captyn_memberships_filename, offering_id, renewal_date)


if __name__ == '__main__':
    main()