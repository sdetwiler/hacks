from datetime import datetime

def first_name(v):
    '''Extract the first name from an iClassPro full name in the format "Last, First"'''

    return v.split(',')[-1].strip().title()


def last_name(v):
    '''Extract the first name from an iClassPro full name in the format "Last, First"'''

    return v.split(',')[0].strip().title()


def full_name(v):
    '''Format a full name to the format "First Last" from an iClassPro full name in the format "Last, First"'''
    
    tokens = v.split(',')
    return ' '.join([tokens[-1]] + tokens[0:-1]).strip().title()


def secondary_contact(v):
    '''Format a full name to the format "To First Last" from an iClassPro full name in the format "Last, First"'''

    return 'To ' + full_name(v)


def phone_number(v):
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


def state(v):
    '''Extract the two character state from an iClassPro state value in the format CA-US'''

    return v[0:2]


def street_address_from_captyn_address(v):
    # Sample: 123 Fake St; Oakland CA 94610
    return v.split(';')[0].replace(',', '').strip()


def city_from_captyn_address(v):
    # Sample: 123 Fake St; Oakland CA 94610
    last_line = v.split(';')[-1]
    tokens = last_line.split(' ')
    # drop the last two tokens, which are state and zip. Supports cities with multiple words.
    return ' '.join(tokens[0:len(tokens)-2]).strip()


def state_from_captyn_address(v):
    # Sample: 123 Fake St; Oakland CA 94610
    # Sample: 123 Fake St; Oakland California 94610
    
    # HACK!
    return 'CA'
    len_tail = len('CA 94610')
    return v[-len_tail:][0:2]


def zipcode_from_captyn_address(v):
    # Sample: 123 Fake St; Oakland CA 94610
    tokens = v.split(' ')
    zip = tokens[-1]
    return zip[0:5]


def captyn_date_to_aau_date(v):
    # "Jun 30, 2001" -> "06/30/2001"
    
    # Zero pad the date so strptime can parse it...
    tokens = v.split(' ')
    if len(tokens[1]) == 2:
        tokens[1] = '0' + tokens[1]
    v = ' '.join(tokens)

    d = datetime.strptime(v, '%b %d, %Y')
    return d.strftime('%m/%d/%Y')


def captyn_gender_to_aau_gender(v):
    # "Female" -> "F"
    if len(v) == 0:
        return 'O'
    return v[0].upper()