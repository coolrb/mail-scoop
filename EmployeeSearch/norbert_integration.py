import requests
import csv
import json

# Here's a quick sample Python code that implements the algorithm :

NorbertAPI_TOKEN = 'b8fc1282-6c0d-4679-b8b7-18424c23afb1'

first_names = []
last_names = []
domains = []

with open('EmployeeInput.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        domains.append(row[0])
        first_names.append(row[1])
        last_names.append(row[2])

for index in range(0, len(domains)):
    req = requests.post(
    'https://api.voilanorbert.com/2016-01-04/search/name',
    auth=('any_string', NorbertAPI_TOKEN),
    data = {
        'name': first_names[index] + ' ' + last_names[index],
        'domain': domains[index]
        }
    )

    result = req.json()

    while True:
        contact_r = requests.get('https://api.voilanorbert.com/2016-01-04/contacts/{0}'.format(result['id']), auth=('any_string', NorbertAPI_TOKEN))
        if contact_r.status_code == 200:
            contact = contact_r.json()

        if contact['searching'] is False:
            # TODO : Update your database here
            if contact['email']:
                # Email found !
                print (contact['email']['email'], contact['email']['score'])
            else:
                print "Email not found!"
            break
