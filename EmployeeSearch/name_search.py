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

    for index in range(0, len(domains)):

        # Hunter Search Script
        hunter = "https://api.hunter.io/v2/email-finder?domain=" + domains[index] + "&first_name=" + first_names[index] + "&last_name=" + last_names[index] + "&api_key=" + HunterAPI_Token

        response_hunter = requests.get(hunter)
        response_hunter_parsed = json.loads(response_hunter.text)
        emp_data_hunter = response_hunter_parsed["data"]

        #Voila Norbert Search Script
        

        empWriter = csv.writer(employData, delimiter=',')
        empWriter.writerow([emp_data_hunter["first_name"]] + [emp_data_hunter["last_name"]] + [emp_data_hunter["email"]] + [emp_data_hunter["score"]])

employData.close()


#print json.dumps(emp_data, indent=4)
