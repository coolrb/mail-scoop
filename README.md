# mail-scoop
Python lead generation script using multiple email scraping APIs.

The domain_search.py script acccepts domain names and returns emails scraped from their websites, it takes a .csv file
with a list of domains in the fist collumn.

The name_search.py script accepts a .csv file with the following collumns:
A) domain
B) first name
C) last name

It looks these up in both Hunter.io and Voila Norbert, compares the confidence of the emails returned, and then verifies
the more confident email for deliverability. All results are saved in the EmployeeOutput.csv file.
