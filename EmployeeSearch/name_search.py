import requests
import json
import csv

HunterAPI_Token = "f41b1f81cb0cad684f5eb7d80bad48b4178ba8d8"
NorbertAPI_TOKEN = "b8fc1282-6c0d-4679-b8b7-18424c23afb1"

first_names = []
last_names = []
domains = []
hunter_emails = []
hunter_scores = []
norbert_emails = []
norbert_scores = []
verify_results = []
verify_scores = []

#Open and import domains, first and last names.
with open('EmployeeInput.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        domains.append(row[0])
        first_names.append(row[1])
        last_names.append(row[2])

#Open output file to write to
with open('EmployeeOutput.csv', 'w', newline='') as employData:

    empWriter = csv.writer(employData, delimiter=',')
    empWriter.writerow(["Domain"] + ["First Name"] + ["Last Name"] + ["Hunter Email"] + ["Hunter Score"] + ["VoilaNorbert Email"] + ["VoilaNorbert Score"] + ["Deliverable?"] + ["Deliverability Score"])

#Loop through the imported domains and search for emails.

    for index in range(0, len(domains)):
    # Hunter Search Script
        hunter = "https://api.hunter.io/v2/email-finder?domain=" + domains[index] + "&first_name=" + first_names[index] + "&last_name=" + last_names[index] + "&api_key=" + HunterAPI_Token

        response_hunter = requests.get(hunter)
        response_hunter_parsed = json.loads(response_hunter.text)
        try:
            emp_data_hunter = response_hunter_parsed["data"]
        except KeyError:
            print("Invalid Response")
            break

        if emp_data_hunter["email"]:
            hunter_emails.append(emp_data_hunter["email"])
            hunter_scores.append(emp_data_hunter["score"])
        else:
            hunter_emails.append("No Email Found")
            hunter_scores.append("No score")

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
                    norbert_emails.append(emp_data_norbert["email"])
                    norbert_scores.append(emp_data_norbert["score"])
                else:
                    norbert_emails.append("No Email Found")
                    norbert_scores.append("No score")
                break

#Check Deliverability

    #Neither email was found
        if hunter_emails[index] == "No Email Found" and norbert_emails[index] == "No Email Found":
            verify_results.append("Not Applicable")
            verify_scores.append("Not Applicable")
    #Both emails were found and are the same.
        elif hunter_emails[index] == norbert_emails[index]:
            hunter_verify = requests.get("https://api.hunter.io/v2/email-verifier?email=" + hunter_emails[index] + "&api_key=" + HunterAPI_Token)
    #Hunter didn't return an email but Norbert did, lookup Norbert email
        elif hunter_emails[index] == "No Email Found":
            hunter_verify = requests.get("https://api.hunter.io/v2/email-verifier?email=" + norbert_emails[index] + "&api_key=" + HunterAPI_Token)
    #Norbert didn't return an email, but Hunter did, lookup Hunter email
        elif norbert_emails[index] == "No Email Found":
            hunter_verify = requests.get("https://api.hunter.io/v2/email-verifier?email=" + hunter_emails[index] + "&api_key=" + HunterAPI_Token)
    #Both returned emails, check both and save the deliverable one (assumes employees only have one functional email per domain)
        elif norbert_emails[index] != hunter_emails[index]:
            #Check hunter email
            hunter_verify = requests.get("https://api.hunter.io/v2/email-verifier?email=" + hunter_emails[index] + "&api_key=" + HunterAPI_Token)
            hunter_verify_parsed = json.loads(hunter_verify.text)
            verify_data = hunter_verify_parsed["data"]
            if verify_data["result"] == "deliverable":
                verify_results.append("Hunter Deliverable")
                verify_scores.append(verify_data["score"])
            #Check Norbert email
            hunter_verify = requests.get("https://api.hunter.io/v2/email-verifier?email=" + norbert_emails[index] + "&api_key=" + HunterAPI_Token)
            hunter_verify_parsed = json.loads(hunter_verify.text)
            verify_data = hunter_verify_parsed["data"]
            if verify_data["result"] == "deliverable":
                verify_results.append("Norbert Deliverable")
                verify_scores.append(verify_data["score"])

    #Write the result of whichever elif was satisfied to memory.
        hunter_verify_parsed = json.loads(hunter_verify.text)
        verify_data = hunter_verify_parsed["data"]
        verify_results.append("Hunter" + " " + verify_data["result"])
        verify_scores.append(verify_data["score"])

    #Write completed lists to CSV file.
        empWriter.writerow(
            [domains[index]]
            + [first_names[index]]
            + [last_names[index]]
            + [hunter_emails[index]]
            + [hunter_scores[index]]
            + [norbert_emails[index]]
            + [norbert_scores[index]]
            + [verify_results[index]]
            + [verify_scores[index]])

    #Close csv file.
employData.close()
