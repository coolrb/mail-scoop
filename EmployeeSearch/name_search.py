import requests
import json
import csv

HunterAPI_Token = "ae4f979860e00b77649e67369a77064e75f58fff"
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

with open('EmployeeOutput.csv', 'w') as employData:

    empWriter = csv.writer(employData, delimiter=',')
    empWriter.writerow(["First Name"] + ["Last Name"] + ["Hunter Email"] + ["Hunter Score"] + ["VoilaNorbert Email"] + ["VoilaNorbert Score"])

    for index in range(0, len(domains)):

        # Hunter Search Script
        hunter = "https://api.hunter.io/v2/email-finder?domain=" + domains[index] + "&first_name=" + first_names[index] + "&last_name=" + last_names[index] + "&api_key=" + HunterAPI_Token

        response_hunter = requests.get(hunter)
        response_hunter_parsed = json.loads(response_hunter.text)
        emp_data_hunter = response_hunter_parsed["data"]

        #Voila Norbert Search Script
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
                    emp_data_norbert = contact['email']
                else:
                    print "Email not found!"
                break

        empWriter.writerow(
            [emp_data_hunter["first_name"]]
            + [emp_data_hunter["last_name"]]
            + [emp_data_hunter["email"]]
            + [emp_data_hunter["score"]]
            + [emp_data_norbert["email"]]
            + [emp_data_norbert["score"]]
            )

employData.close()


#print json.dumps(emp_data, indent=4)
