import csv
import re

def process_phone(phone):
    phone_pattern = re.compile(r'(\+?\d{1,2})?\s*?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{2})[\s.-]?(\d{2})\s*?(?:доб)?\.?\s*?(\d+)?')
    phone_match = phone_pattern.match(phone)
    if phone_match:
        phone = f'+7({phone_match.group(2)}){phone_match.group(3)}-{phone_match.group(4)}-{phone_match.group(5)}'
        if phone_match.group(6):
            phone += f' доб.{phone_match.group(6)}'
    return phone

def main():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    unique_contacts = {}

    for contact in contacts_list:
        name_parts = contact[0].split()
        if len(name_parts) == 3:
            lastname, firstname, surname = name_parts
        elif len(name_parts) == 2:
            lastname, firstname = name_parts
            surname = ''
        else:
            continue

        phone = process_phone(contact[5])

        key = f'{lastname}_{firstname}_{surname}'

        if key in unique_contacts:
            existing_contact = unique_contacts[key]
            updated_contact = [
                lastname or existing_contact[0],
                firstname or existing_contact[1],
                surname or existing_contact[2],
                contact[3] or existing_contact[3],  # Организация
                contact[4] or existing_contact[4],  # Должность
                phone or existing_contact[5],  # Телефон
                contact[6] or existing_contact[6],  # Email
            ]
            unique_contacts[key] = updated_contact
        else:
            unique_contacts[key] = [
                lastname,
                firstname,
                surname,
                contact[3],  # Организация
                contact[4],  # Должность
                phone,  # Телефон
                contact[6],  # Email
            ]

    contacts_list = [list(contact.values()) for contact in unique_contacts.values()]

    with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

if __name__ == "__main__":
    main()

