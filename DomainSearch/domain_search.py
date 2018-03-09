import requests
import json
import csv

HunterAPI_Key = ""

domains = []

with open('DomainInput.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        domains.append(row[0])

with open('DomainOutput.csv', 'w') as DomainData:
    for company in domains:
        hunter = "https://api.hunter.io/v2/domain-search?domain=" + company + "&api_key=" + HunterAPI_Key

        response_hunter = requests.get(hunter)
        response_hunter_parsed = json.loads(response_hunter.text)
        emp_data_hunter = response_hunter_parsed["data"]["emails"]

        empWriter = csv.writer(DomainData, delimiter=',')
        for y in range(0, len(emp_data_hunter)):
            empWriter.writerow([emp_data_hunter[y]["first_name"]] + [emp_data_hunter[y]["last_name"]] + [emp_data_hunter[y]["value"]] + [emp_data_hunter[y]["position"]])

DomainData.close()


#print json.dumps(emp_data, indent=4)
