import json
import sched
import time

import gspread
import yaml

from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"
         ]

print("---------------------------sheet schedular server started -----------------------")
with open('config.yml', 'r') as json_data_file:
    json_credentials = yaml.safe_load(json_data_file)
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_credentials, scope)

# authorize the clientsheet
client = gspread.authorize(creds)

s = sched.scheduler(time.time, time.sleep)


def store_templates_locally(file_names=None):
    # get the instance of the Spreadsheet
    if file_names is None:
        file_names = []
    for item in file_names:
        print(item)
        # sheet = client.open('Shriram prod responses')
        sheet = client.open('Shriram Housing Finance')
        # get the first sheet of the Spreadsheet
        sheet_instance = sheet.worksheet(item)
        result1 = sheet_instance.get_all_records(head=1)
        print("-----------------Templates updated locally--------------")
        with open("../{}.json".format(item), "w+", encoding='utf-8') as f:
            json.dump(result1, f, indent=4, ensure_ascii=False)

    s.enter(5, 1, store_templates_locally, (files_required,))


files_required = ["customer_details"]
# files_required = ["Sheet1"]
s.enter(5, 1, store_templates_locally, (files_required,))
s.run()
