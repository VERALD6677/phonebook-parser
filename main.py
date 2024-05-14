import re
from pprint import pprint
import csv

def format_phone(phone):
    numbers = re.findall(r'\d', phone)
    formatted_phone = f'+7({"".join(numbers[-10:-7])}){"".join(numbers[-7:-4])}-{"".join(numbers[-4:-2])}-{"".join(numbers[-2:])}'
    if 'доб' in phone:
        ext = re.search(r'доб\.\s?(\d+)', phone).group(1)
        formatted_phone += f' доб.{ext}'
    return formatted_phone

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for contact in contacts_list:
    if len(contact[0].split()) == 3:
        contact[0], contact[1], contact[2] = contact[0].split()
    contact[5] = format_phone(contact[5])

contacts_dict = {}
for contact in contacts_list:
    key = f"{contact[0]} {contact[1]} {contact[2]}"
    if key in contacts_dict:
        contacts_dict[key] = [contacts_dict[key][0]] + [item if item else contacts_dict[key][idx] for idx, item in enumerate(contact[3:])]
    else:
        contacts_dict[key] = contact

contacts_list = list(contacts_dict.values())

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

pprint(contacts_list)


