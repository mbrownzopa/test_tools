import codecs
import difflib
from selenium import webdriver
driver = webdriver.Firefox()
import os, sys
import requests

# Open the files to read and write. Require utf-8 encoding - remove any previous actuals file
if os.path.isfile('actual_results.txt'):
	os.remove('actual_results.txt')
expected = codecs.open('expected_results.txt', 'r', 'utf-8')
actuals = codecs.open('actual_results.txt', 'w', 'utf-8')

# Go to the Policy codes page
url = 'http://underwriting.uat.ldn.zopa.com/Policy'
driver.get(url)
print driver.current_url

# Find the codes embedded in the tables.
tables = driver.find_elements_by_xpath("//table[@id='underwriting-codes']")
#print tables

# Write the results to a file
for table in tables:
    #print table.text
    actuals.write("%s\n" % table.text)
actuals.close()

actuals = codecs.open('actual_results.txt', 'r', 'utf-8')

# Compare the files and flag any differences
x  = difflib.SequenceMatcher(None,expected.read(), actuals.read())
print x.ratio()

x = str(x.ratio())

if x != "1.0":
    print("mismatch")
    payload = {'color': 'red', 'message': 'UAT UW Policy Rules check ran and do not match @all', 'notify': 'true', 'message_format': 'text'}
    r = requests.post('https://api.hipchat.com/v2/room/2200616/notification?auth_token=g7wdJ7Qyijpd08iLTEdZH6Q74LgUYN6UQkG3eYQS', data=payload)
    os.system("winmergeu expected_results.txt actual_results.txt")
else:
    payload = {'color': 'green', 'message': 'UAT UW Policy Rules check ran and match', 'notify': 'true', 'message_format': 'text'}
    r = requests.post('https://api.hipchat.com/v2/room/2200616/notification?auth_token=g7wdJ7Qyijpd08iLTEdZH6Q74LgUYN6UQkG3eYQS', data=payload)

# Tidy up
actuals.close()
expected.close()
driver.quit()
