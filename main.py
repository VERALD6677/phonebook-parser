import re
from pprint import pprint
import csv

def format_phone(phone):
    phone_pattern = (
        r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
        r"(\s*\(?доб\.\s*(\d+)\)?)?"
    )
    phone_replace = r"+7(\2)\3-\4-\5"
    match = re.match(phone_pattern, phone)
    if match and match.group(7):
        return f"{re.sub(phone_pattern, phone_replace, phone)} доб.{match.group(7)}"
    else:
        return re.sub(phone_pattern, phone_replace, phone)

def process_name(contact):
    full_name = ' '.join(contact[:3]).split()
    while len(full_name) < 3:
        full_name.append('')
    contact[:3] = full_name
    return contact

def merge_contacts(existing_contact, new_contact):
    return [new if new else old for old, new in zip(existing_contact, new_contact)]

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for contact in contacts_list:
    contact = process_name(contact)
    contact[5] = format_phone(contact[5])

contacts_dict = {}
for contact in contacts_list:
    key = f"{contact[0]} {contact[1]}"
    if key in contacts_dict:
        contacts_dict[key] = merge_contacts(contacts_dict[key], contact)
    else:
        contacts_dict[key] = contact

contacts_list = list(contacts_dict.values())

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

pprint(contacts_list)

