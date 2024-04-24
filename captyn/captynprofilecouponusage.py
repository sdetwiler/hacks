#!/usr/bin/env python3

import csv


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

# CSV Fields for export from Captyn Coupon Usage
# (Home/Settings/<Program Offering> Settings/Coupons)
captyn_coupon_usage_cols = [
    'Coupon Name',
    'Coupon Code',
    'Coupon Amount',
    'Item Amount',
    'Account First Name',
    'Account Last Name',
    'Registration',
    'Participant First Name',
    'Participant Last Name',
    'Program',
    'Subtitle',
    'Tags',
    'Start Date',
    'End Date',
    'Days/Times/Locations'
]


def load_captyn_coupon_usage_by_account_name(captyn_coupon_usage_filename):
    '''Returns a dictionary of all Captyn coupon usage indexed by account name.

        captyn_coupon_usage_filename: Filename containing CSV of Captyn coupon usage.
    '''

    captyn_coupon_usage_by_name = {}
    captyn_file = open(captyn_coupon_usage_filename, 'r')
    captyn = csv.DictReader(captyn_file)
    for captyn_row in captyn:
        k = '{} {}'.format(captyn_row['Account First Name'], captyn_row['Account Last Name'])
        captyn_coupon_usage_by_name[k] = captyn_row

    return captyn_coupon_usage_by_name


def load_captyn_profiles_by_account_name(captyn_profiles_filename):
    '''Returns a dictionary of all Captyn profiles indexed by account name.

        captyn_profiles_filename: Filename containing CSV of Captyn profiles.
    '''

    captyn_profiles_by_name = {}
    captyn_file = open(captyn_profiles_filename, 'r')
    captyn = csv.DictReader(captyn_file)
    for captyn_row in captyn:
        k = captyn_row['Attached Account']
        if k not in captyn_profiles_by_name:
            captyn_profiles_by_name[k] = []
        
        captyn_profiles_by_name[k].append(captyn_row)

    return captyn_profiles_by_name


def captyn_coupon_usage_by_participant(captyn_profiles_filename, captyn_coupon_usage_filename):
    '''Generates a CSV file that contains AAU registrations using an exported Captyn membership CSV file.

    '''

    captyn_profiles_by_account_name = load_captyn_profiles_by_account_name(captyn_profiles_filename)
    captyn_coupon_usage_by_account_name = load_captyn_coupon_usage_by_account_name(captyn_coupon_usage_filename)


    print('coupon_pct,participant_first_name,participant_last_name')

    for k, v in captyn_profiles_by_account_name.items():
        if k in captyn_coupon_usage_by_account_name:
            coupon_usage = captyn_coupon_usage_by_account_name[k]

            coupon_name = coupon_usage['Coupon Name']

            if coupon_name[-1] == '%':
                coupon_pct = int(coupon_name.split(' ')[-1][:-1])
            else:
                coupon_pct = 100


            if coupon_pct >= 75:
                for profile in v:
                    print('{},{},{}'.format(coupon_pct, profile['First Name'], profile['Last Name']))




def main():
    captyn_profiles_filename = 'data/captyn_Profiles-Export-2024-04-24-0832.csv'
    captyn_coupon_usage_filename = 'data/Coupon_Usage-2024-04-24-2014.csv'

    captyn_coupon_usage_by_participant(captyn_profiles_filename, captyn_coupon_usage_filename)

if __name__ == '__main__':
    main()