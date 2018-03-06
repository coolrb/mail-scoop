import requests
import json
import csv


domains = []

with open('domains.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        domains.append(row[0])

with open('EmployData.csv', 'w') as employData:

    for company in domains:
        getter = "https://api.hunter.io/v2/domain-search?domain=" + company + "&api_key=ae4f979860e00b77649e67369a77064e75f58fff"
        response = requests.get(getter)
        response_parsed = json.loads(response.text)
        emp_data = response_parsed["data"]["emails"]
        empWriter = csv.writer(employData, delimiter=',')

        for y in range(0, len(emp_data)):
            empWriter.writerow([emp_data[y]["first_name"]] + [emp_data[y]["last_name"]] + [emp_data[y]["value"]] + [emp_data[y]["position"]])

#        employData.close()

#first_name = emp_data[0]["first_name"]
#last_name = emp_data[0]["last_name"]
#email = emp_data[0]["value"]
#position = emp_data[0]["position"]

#print(first_name)
#print(last_name)
#print(email)
#print(position)

#print json.dumps(emp_data, indent=4)
