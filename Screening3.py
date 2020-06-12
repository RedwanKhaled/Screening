import re
import lxml
import requests
from bs4 import BeautifulSoup
import string
from string import punctuation

def parse_address(address):
    street_address = None
    zip_code = None
    city_name = None
    state = None
    pobox_info = None

    splited_address = address.strip(punctuation+' ').split('\n')
    splited_address = list(filter(lambda x: x!='', splited_address))
    # print splited_address

    po_box_regex = r'([Pp][\. ]?[Oo][\. ][ ]?[Bb][Oo][Xx][ ]?\d+)'
    po_box = re.search(po_box_regex, splited_address[0])
    if po_box and po_box.groups():
        pobox_info = po_box.groups()[0]
    else:
        street_address = splited_address[0].strip()

    if len(splited_address)>1:
        # parse city name
        get_cityname_pattern = r'[A-Z]{2} \d{5}(-\d{4})?'
        city_regex = re.split(get_cityname_pattern, splited_address[-1])
        if city_regex:
            city_name = city_regex[0].strip(punctuation+' ')
        # parse zip_code
        zip_code_regex = re.search(r'.*(\d{5}(\-\d{4})?)$', splited_address[-1])
        if zip_code_regex and zip_code_regex.groups():
            zip_code = zip_code_regex.groups()[0]

        state_regex = re.search(r'([A-Z]{2})', splited_address[-1])
        if state_regex and state_regex.groups():
            state = state_regex.groups()[0]

    return {
        'street_address': str(street_address),
        'city': str(city_name),
        'state': str(state),
        'zip_code': str(zip_code),
        'pobox': str(pobox_info)
    }

def parse_office_name(name):
    if not name:
        return {}
    # print name
    splited_name = name.split('-')
    splited_name[0] = splited_name[0].strip(punctuation+' ')
    return {
        "office_name": str(splited_name[0])
    }

def parse_office_address(address):
    
    address_dict = parse_address(address)

    return {
        "office_address": address_dict.get('street_address', None),
        "office_city": address_dict.get('city', None),
        "office_zip": address_dict.get('zip_code', None),
        "office_state": address_dict.get('state', None),
    }

def parse_mailing_address(address):

    address_dict = parse_address(address)

    return {
        "mailing_address": address_dict.get('street_address', None),
        "mailing_pobox": address_dict.get('pobox', None),
        "mailing_city": address_dict.get('city', None),
        "mailing_zip": address_dict.get('zip_code', None),
        "mailing_state": address_dict.get('state', None),
    }
    return {}


def parse_phone_number(contact_info):
    phone_number = None
    regex = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4})'
    phone_numbers = re.search(regex, contact_info)
    if phone_numbers and phone_numbers.groups():
        phone_number = str(phone_numbers.groups()[0].strip().replace('(','').replace(') ','-'))
    
    return {"office_phone": phone_number}


def main():
    url = 'https://dot.ca.gov'
    response = requests.get(url + '/contact-us')
    contents = response.text
    soup = BeautifulSoup(contents, 'lxml')
    tables = soup.find_all('table')
    result = []

    # file = open("result",'w')
    for tr in tables[0].find_all('tr'):
        td = tr.find_all('td')
        if not td:
            continue
        org = {}
        links = td[0].find_all('a')
        org['office_link'] = url
        for link in links:
            org['office_link'] = url+link.get('href')

        org.update(parse_office_name(td[0].text))
        org.update(parse_office_address(td[1].text))
        org.update(parse_mailing_address(td[2].text))
        org.update(parse_phone_number(td[3].text))
        result.append(org)

    print result
    # file.close()

if __name__ == '__main__':
    main()
