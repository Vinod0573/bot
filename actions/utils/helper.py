from code import interact
import csv
from sys import int_info

import pytz
import redis
import pickle
import json
import pandas as pd
import datetime
from rasa_sdk.forms import REQUESTED_SLOT
from ruamel import yaml
import time
import datetime
import requests
from rasa_sdk.events import SlotSet, FollowupAction
from actions.utils.common_imports import *
import numpy as np
from handle_bulk_data import red_customers

customer_informed_disagree_to_proceed = 0
customer_informed_agree_to_pay = 1
customer_informed_call_later = 2
customer_informed_decline_reason = 3
customer_informed_wrong_info = 4
customer_informed_bye = 5
customer_no_response = 18
customer_asked_human_handoff = 19
customer_informed_disagree_to_pay = 20
customer_says_hello_only = 21
customer_informed_not_audible = 22
customer_informed_partial_payment = 23
customer_informed_payment_done = 24
bot_unable_to_catch_partial_amount = 25
decline_reason_disposition_id = {
    "business_loss": "Lockdown Impact - No Income",
    "cycle_date_issue": "Cycle Date Issue",
    "insufficient_funds": "Funds Unavailable",
    "job_loss": "Loss of Job",
    "medical_issue": "Medical Expense Family/Self",
    "technical_issue": "Technical Issue",
    "family_dispute": "Family Dispute",
    "foreclosing_through_own_funds": "Foreclosing Through Own Funds",
    "branch_issue": "Branch Issue",
    "account_not_working": "Account Not Working",
    "change_account_for_deduction": "Change Account for Deduction",
    "transfer_to_another_hfc": "Transfer to another HFC",
    "salary_issue":"Salary Issue"
}
customer_informed_payment_not_done = 1
customer_informed_promise_to_pay_date_with_in_7_days = 2
customer_informed_promise_to_pay_date_after_7_days = 15
customer_informed_ptp_date_with_count_greater_than_2 = 16
customer_informed_payment_later = 3
customer_informed_payment_issue = 4
customer_informed_payment_link_issue = 6
customer_informed_human_hand_off = 7
customer_informed_pay_with_another_method = 10
customer_informed_payment_today = 12
bot_unable_to_understand = 14
customer_informed_do_not_call = 17
customer_informed_other_language = 19
language_issue = 20


# def send_message(tracker):
#     # TODO need to update the bot responses according to status of the message sent ->
#     #  means if message not sent update the bot responses
#     phone_number = str(tracker.user_id)
#     if not phone_number.startswith("91"):
#         phone_number = "91" + phone_number
#     user_details = get_user_details(tracker)
#     _user_details = {"loan_id": user_details.get("loan_id"),
#                      "customer_name": user_details.get("Employee Name") if user_details.get("Employee Name") else
#                      "customer ", "payment_link": "", "EMI Amount": "", "Due date": ""}
#     if not (user_details.get("EMI Amount") and user_details.get("Due date") and user_details.get("payment_link")):
#         return
#     else:
#         _user_details["Due date"] = user_details.get("Due date")
#         _user_details["EMI Amount"] = user_details.get("EMI Amount")
#         _user_details["payment_link"] = user_details.get("payment_link")
#     message = "Dear {customer_name}, Greetings from Avail Finance! Your CreditATM Loan ID: {loan_id}" \
#               " is due for: {emi_amount} on: {due_date}. Pay your dues today to reactivate your credit limit." \
#               " You can pay by clicking on the link {payment_link} or through the Avail app." \
#               " Not paying dues on time will result in late payment fees and also impact your credit score -Gamut".\
#         format(customer_name=_user_details.get("customer_name"), loan_id=_user_details.get("loan_id"),
#                emi_amount=_user_details.get("EMI Amount"), due_date=_user_details.get("Due date"),
#                payment_link=_user_details.get("payment_link"))
#     print("Sending message to phone number", phone_number)
#     headers = {
#         "api-key": "Ad9ba96c1c7d12ee451e01fe20dcc0fc3",
#     }

#     try:
#         data = {
#             "to": "+" + phone_number,
#             "source": "API",
#             "type": "TXN",
#             "sender": "GamutA",
#             "body": message,
#             "template_id": "1207162546311102546"
#         }
#         print(data)
#         start_time = datetime.datetime.now()
#         response_qs = requests.post(
#             "https://api.kaleyra.io/v1/HXIN1700984931IN/messages",
#             headers=headers,
#             data=data,
#         ).json()
#         end_time = datetime.datetime.now()
#         print("Time taken to send the message", end_time - start_time)
#         print(response_qs)
#         if response_qs.get("recipients"):
#             print(response_qs)
#     except Exception as e:
#         print(e)

customer_data=pd.read_csv("customer_details_new.csv")
customer_data.replace(np.nan,"",regex=True,inplace=True) 
def send_and_store_disposition_details(tracker=None, dispatcher=None, flag=702, disposition_id=None,
                                       user_message=None, ptp_date=None, partial_amount=None,delay_reason=None,emi_flow=None,language=None,outstanding_payment=None,customer_name=None,loan_id=None,
                                       due_date=None,payment_link=None,ptp_recheck=None,sheet_name=None,URNNO = None,total_emi_amount=None,last_unpaid_emi_date=None,count_of_days=None):
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    helper = Helper()
    total_emi_amount = tracker.get_slot("total_emi_amount")
    URNNO=tracker.get_slot("URNNO")
    due_date = tracker.get_slot("due_date")
    sheet_name = tracker.get_slot("sheet_name")
    emi_flow= tracker.get_slot("emi_flow")
    loan_id=tracker.get_slot("loan_id")
    language= tracker.get_slot("language")
    customer_name= tracker.get_slot("employee_name")
    last_unpaid_emi_date= tracker.get_slot("last_unpaid_emi_date")
    count_of_days= tracker.get_slot("count_of_days")
    helper.send_conversation_flag(flag, dispatcher, delay_reason=delay_reason, 
                                    message=user_message,
                                    disposition_id=disposition_id, 
                                    ptp_date=ptp_date,
                                    time=time,
                                    partial_amount=partial_amount,
                                    loan_id=loan_id,
                                    language=language,
                                    last_unpaid_emi_date=last_unpaid_emi_date,
                                    count_of_days=count_of_days,
                                    total_emi_amount=total_emi_amount,
                                    due_date=due_date,
                                    payment_link=payment_link,
                                    ptp_recheck=ptp_recheck,
                                    sheet_name=sheet_name,
                                    emi_flow=emi_flow,
                                    URNNO = URNNO,
                                    customer_name=customer_name
                                    )
    # store_call_log(disposition_id=disposition_id, tracker=tracker,user_message=user_message, ptp_date=ptp_date, partial_amount=partial_amount,delay_reason=delay_reason,emi_flow=emi_flow,language=language,outstanding_payment=outstanding_payment,time=time)


def store_call_log(disposition_id=None, tracker=None, user_message=None, ptp_date=None, partial_amount=None,delay_reason=None,emi_flow=None,language=None,outstanding_payment=None,time=None):
    # TODO need to handle the if phone number coming from tracker having string -> it leads to expection
    print("------------Store call getlog------------")
    phone_number = tracker.user_id
    try:
        with open('call_logs.csv', 'r+', newline='') as file:
            data = csv.reader(file)
            writer = csv.writer(file)
            current_date = datetime.datetime.now()
            if len(list(data)) == 0:
                writer.writerows(
                    [["date", "phone number", "disposition id", "user message", "ptp_date", "partial_amount","delay_reason","emi flow","time"], [
                        current_date.strftime("%d/%m/%Y"), phone_number, disposition_id, user_message, ptp_date,
                        partial_amount,delay_reason,emi_flow,time]])
            else:
                writer.writerow([current_date.strftime("%d/%m/%Y"), phone_number, disposition_id, user_message,
                                 ptp_date, partial_amount,delay_reason,emi_flow,time])
    except IOError:
        with open('call_logs.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            current_date = datetime.datetime.now()
            writer.writerows(
                [["date", "phone number", "disposition id", "user message", "ptp_date", "partial_amount","delay_reason","emi flow","time"], [
                    current_date.strftime("%d/%m/%Y"), phone_number, disposition_id, user_message, ptp_date,
                    partial_amount,delay_reason,emi_flow,time]])


def get_ptp_day_count(tracker):
    phone_number = tracker.user_id
    data = pd.read_csv("call_logs.csv")
    try:
        data["month"] = pd.to_datetime(data["date"], format="%d/%m/%Y").dt.month
        employee_records = data.loc[(data["phone number"] == int(phone_number)) &
                                    (data["month"] == datetime.datetime.now().month)]
        print(employee_records)
        return len(employee_records)
    except:
        return 0


def set_ptp_day_count(tracker):
    pass


def get_trail_count(tracker):
    trail_count = tracker.get_slot("trail_count")
    if trail_count is None:
        return 1
    else:
        try:
            trail_count = int(trail_count) + 1
            return trail_count
        except:
            return 1


def get_return_values(tracker):
    if tracker.active_form.get("name") is not None:
        # print("tracker.active_form.get()-1",tracker.active_form.get("name"))
        return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
        ]
    # print("tracker.active_form.get()",tracker.active_form.get("name"))
    return [FollowupAction("action_listen")]


def get_disposition_id(intent):
    disposition_id = None
    if intent == "deny" or intent == "disagree_to_pay":
        disposition_id = customer_informed_disagree_to_pay
    if intent == "disagree_to_proceed":
        disposition_id = customer_informed_disagree_to_proceed
    if intent == "pay_later":
        disposition_id = customer_informed_payment_later
    if intent == "inform_pay_with_other_method":
        disposition_id = customer_informed_pay_with_another_method
    if intent == "bye":
        disposition_id = customer_informed_bye
    if intent == "inform_wrong_info":
        disposition_id = customer_informed_wrong_info
    if intent == "inform_payment_going_on":
        disposition_id = customer_informed_wrong_info
    if intent == "inform_payment_done":
        disposition_id = customer_informed_payment_done
    return disposition_id


def get_user_details_2(tracker):
    phone_number = tracker.user_id
    user_details = requests.get("http://13.92.118.170/sheetapi/navi/userDetails?phone_number={}".format(phone_number))
    print(user_details)
    if user_details.status_code == 200:
        user_details = user_details.json()
        if user_details.get("status") == 200 and "response" in user_details:
            print(user_details["response"])
            if "response" in user_details["response"] and len(user_details["response"]["response"]) > 0:
                formatted_data = {"name": user_details["response"]["response"][0]["name"].lower(),
                                  "monthly_emi": user_details["response"]["response"][0]["emi_amt"],
                                  "language": user_details["response"]["response"][0]["custom_field_2"]}
                emi_date = user_details["response"]["response"][0]["emi_date"]
                if emi_date:
                    emi_date = datetime.datetime.strptime(emi_date, "%d-%m-%Y")
                formatted_data["monthly_emi_date"] = emi_date.strftime("%d %B %Y")
                print(emi_date)
                return formatted_data
    formatted_data = {"name": "", "language": "en",
                      "monthly_emi": 1000, "monthly_emi_date": datetime.datetime.now().strftime("%d %B %Y")}
    return formatted_data


def get_user_details(tracker):
    phone_number = tracker.user_id
    formatted_data = {"Employee Name": "", "language": "en",
                      "EMI Amount": 1000, "Due date": datetime.datetime.now().strftime("%d %B %Y"),"flow_type":"","payment_link":"","loan_id":""}
    with open("customer_details.json", "r+", encoding='utf-8') as f:
        customer_details = json.load(f)
    _customer = None
    for customer in customer_details:
        if "phone_number" in customer and str(customer["phone_number"]) == phone_number:
            _customer = customer
            formatted_data["Employee Name"] = customer.get("name")
            formatted_data["EMI Amount"] = customer.get("emi_amt")
            formatted_data["language"] = customer.get("custom_field_2")
            formatted_data["payment_link"] = customer.get("Payment link")
            formatted_data["loan_id"] = customer.get("Loan ID")
            formatted_data["flow_type"]=customer.get("flow_type")
            emi_date = customer.get("emi_date")
            if emi_date:
                emi_date = datetime.datetime.strptime(emi_date, "%d-%m-%Y")
                formatted_data["Due date"] = emi_date.strftime("%d %B %Y")
    if _customer is None:
        phone_number = "9851197922"
        for customer in customer_details:
            if "phone_number" in customer and str(customer["phone_number"]) == phone_number:
                formatted_data["Employee Name"] = customer.get("name")
                formatted_data["EMI Amount"] = customer.get("emi_amt")
                formatted_data["language"] = customer.get("custom_field_2")
                formatted_data["payment_link"] = customer.get("Payment link")
                formatted_data["loan_id"] = customer.get("Loan ID")
                formatted_data["flow_type"]=customer.get("flow_type")
                emi_date = customer.get("emi_date")
                if emi_date:
                    emi_date = datetime.datetime.strptime(emi_date, "%d-%m-%Y")
                    formatted_data["Due date"] = emi_date.strftime("%d %B %Y")

    return formatted_data

def get_total_loan(tracker):
    phone_number=tracker.user_id
    print("phone number:",phone_number)
    total_rows=customer_data.index[customer_data["phone_number"]==int(phone_number)].tolist()
    if len(total_rows)>0:
        return total_rows
    else:
        total_rows=customer_data.index[customer_data["phone_number"]==int(8618145405)].tolist()
        print(total_rows,phone_number)
        return total_rows

def get_emi_details(tracker,total_rows):
    print("total_rows>>>.",total_rows)
    phone_number=tracker.user_id
    print(phone_number)
    total_emi_amount=0
    due_date=[]
    sheet_name=''
    emi_flow=''
    URNNO = ''
    loan_id=''
    employee_name=''
    language=''
    last_unpaid_emi_date=''
    count_of_days=''
    for i in total_rows:
        total_emi_amount+=int(customer_data['emi_amt'][i])
        due_date = customer_data['emi_date'][i]
        sheet_name=customer_data['sheet_name'][i]
        emi_flow=customer_data['flow_type'][i]
        URNNO = customer_data['URNNO'][i]
        loan_id =customer_data["Loan ID"][i]
        employee_name=customer_data["name"][i]
        language=customer_data["custom_field_2"][i]
        last_unpaid_emi_date=customer_data["Last unpaid EMI date"][i]
        count_of_days=customer_data["count_of_days"][i]

        print("due_date...........",due_date)
    return total_emi_amount,due_date,sheet_name,emi_flow,URNNO,loan_id,employee_name,language,last_unpaid_emi_date,count_of_days
    
mapped_languages={
    "english":"en",
    "hindi":"hi",
    "tamil":"tam",
    "telugu":"tel",
    "kannada":"ka",
    "malayalam":"ml",
    "bangla":"bn",
    "marathi":"ma",
    "punjabi":"pa",
    "gujarati":"gu",

}

def get_user_details_redis(tracker):
    phone_number = tracker.user_id
    cust_details=red_customers.hgetall(phone_number)
    formatted_data = {"total_emi": "", "language": "en","URNNO":"","loan_id":"",
                      "sheet_name":"", "due_date": datetime.datetime.now().strftime("%d %B %Y"),"emi_flow":"","employee_name":"","user_id":"","account_no":"","total_loans":"","count_of_days":"","last_unpaid_emi_date":"","reference_no":"",}
    if len(cust_details)>0:
        formatted_data["total_emi"] = cust_details.get("emi_amt")
        lang = cust_details.get("language").lower()
        formatted_data["language"] = mapped_languages[lang]
        formatted_data["URNNO"] = cust_details.get("URNNO")
        formatted_data["loan_id"] = cust_details.get("Loan ID")
        formatted_data["sheet_name"] = cust_details.get("sheet_name")
        formatted_data["due_date"] = cust_details.get("emi_date")
        formatted_data["emi_flow"] = cust_details.get("flow_type")
        formatted_data["employee_name"]=cust_details.get("name")
        formatted_data["user_id"]=cust_details.get("user_id")
        formatted_data["account_no"]=cust_details.get("account_no")
        formatted_data["total_loans"]=cust_details.get("total_loans")
        formatted_data["count_of_days"]=cust_details.get("count_of_days")
        formatted_data["last_unpaid_emi_date"]=cust_details.get("Last unpaid EMI date")
        formatted_data["reference_no"]=cust_details.get("ReferenceNo")
        emi_date = cust_details.get("emi_date")
        if emi_date:
            emi_date = datetime.datetime.strptime(emi_date, "%d-%m-%Y")
            formatted_data["due_date"] = cust_details.get("emi_date")
    return formatted_data


class Helper:
    def __init__(self):
        pass

    def format_date(self, date):
        # Formats the date to readable format
        if date:
            date = str(date)[:-3]
            date_time = datetime.datetime.fromtimestamp(int(date)) + datetime.timedelta(hours=+8)
            date_string = date_time.strftime("%d/%m/%Y, %H:%M:%S")
            return date_string

    def send_conversation_flag(self, flag, dispatcher, 
                              message=None, 
                              time_limit=8, 
                              disposition_id=None,
                              language=None,
                              count_of_days=None,
                              last_unpaid_emi_date=None,
                              language_change=None,
                               delay_reason=None,
                               ptp_date=None,time=None,
                               partial_amount=None,
                               customer_name=None,
                               loan_id=None,
                                total_emi_amount=None,
                                due_date=None,
                                payment_link=None,
                                ptp_recheck=None,
                                sheet_name=None,
                                emi_flow=None,
                                URNNO = None):
        # Send Flags to backend.

        conv_flag = dict()
        conv_flag["status"] = flag
        if message:
            conv_flag["message"] = message
        # if disposition_id:
        conv_flag["disposition_id"] = disposition_id
        conv_flag["delay_reason"]=delay_reason
        conv_flag["ptp_date"]=ptp_date
        conv_flag["time_limit"] = time_limit
        conv_flag['response_time']=time
        conv_flag['partial_amount']=partial_amount
        conv_flag['customer_name']=customer_name
        conv_flag['loan_id']=loan_id
        conv_flag['emi_amt']=total_emi_amount
        conv_flag['due_date']=due_date
        conv_flag['payment_link']=payment_link
        conv_flag['ptp_recheck']=ptp_recheck
        conv_flag['sheet_name']=sheet_name
        conv_flag['flow_type']=emi_flow
        conv_flag["URNNO"] = URNNO
        conv_flag["language"] = language
        conv_flag["count_of_days"] = count_of_days
        conv_flag["last_unpaid_emi_date"] = last_unpaid_emi_date
        conv_flag["others"] = {
            "URNNO":URNNO
        }

        # conv_flag["others"] = {
        #     "URNNO":URNNO,
        #     "ReferenceNo":referenceNO
        # }
        dispatcher.utter_custom_json(conv_flag)

    @staticmethod
    def get_daytime():
        tz_NY = pytz.timezone('Asia/Kolkata')
        datetime_NY = datetime.datetime.now(tz_NY)
        current_time = int(datetime_NY.strftime("%H"))
        print("dsfasfsfs", current_time)
        daytime = 'good morning'
        if 12 <= int(current_time) < 17:
            daytime = 'good afternoon'
        elif int(current_time) >= 17:
            daytime = 'good evening'
        print(daytime)
        return daytime

# def customer_informed_promise_to_pay_date(value, dispatcher, tracker, helper):
#     now = datetime.datetime.now()
#     entities = tracker.latest_message["entities"]
#     if entities:
#         # TODO store the promise to pay date
#         for entity in entities:
#             if entity.get("entity", None) == "date":
#                 given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
#                 print("given date", given_date)
#                 if given_date:
#                     no_of_days = given_date - datetime.datetime.now()
#                     print("no of days", no_of_days)
#                     if 0 < no_of_days.days < 7:
#                         given_date = given_date.strftime("%d, %B, %Y")
#                         dispatcher.utter_template("utter_first_case_inform_payment_date", tracker,
#                                                   given_date=given_date)
#                     else:
#                         end_date = now + datetime.timedelta(days=1)
#                         end_date = end_date.strftime("%d, %B, %Y")
#                         dispatcher.utter_template("utter_first_case_inform_payment_date_1", tracker,
#                                                   end_date=end_date)
#                     helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher)
#                     return {"payment_status": value, "stop_conversation": "TRUE", "trail_count": None}