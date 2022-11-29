from rasa_sdk import Action
from rasa_sdk.events import *
from typing import Dict, Text, Any, List, Union

from rasa_sdk import ActionExecutionRejection
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa.nlu.model import Interpreter
import requests
import json
import difflib
from ruamel import yaml
# from constants import ENV_CONSTANT_FILE
from actions.utils.helper import *
# import Levenshtein
import re, datetime

HANDOFF_FLAG = 703
TIMEOUT_FLAG = 701
HOLD_FLAG = 704
DTMF_CODE = 705
DEFAULT_FLAG = 702
WAIT_FLAG = 720

date_check_intents = ["agree_to_pay", "pay_later", "disagree_to_pay", "inform"]
person_details = {
    '9123090327': {
        'name': "Piyush ",
        'monthly_emi': '7800',
        'monthly_emi_date': '10 December 2020',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },
    '9172098085': {
        'name': "Yogesh ",
        'monthly_emi': '7800',
        'monthly_emi_date': '10 December 2020',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'chennai'
    },
    '9404711867': {
        'name': "Prathamesh ",
        'monthly_emi': '7800',
        'monthly_emi_date': '10 December 2020',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'mumbai'
    },

    '8618064285': {
        'name': "Vishwanath ",
        'monthly_emi': '7800',
        'monthly_emi_date': '10 December 2020',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },

    '8904065526': {
        'name': "Rakesh ",
        'monthly_emi': '7800',
        'monthly_emi_date': '10 December 2020',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'mumbai'
    },

    '8051011443': {
        'name': "Ankit ",
        'monthly_emi': '7800',
        'monthly_emi_date': '10 December 2020',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'pune'
    },

    'default': {
        'name': " ",
        'monthly_emi': '7800',
        'monthly_emi_date': '10 December 2020',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'pune'
    },
    '9494034885': {
        'name': "sudheer ",
        'monthly_emi': '7800',
        'monthly_emi_date': '10 December 2020',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },
    '9781269363': {
        'name': "Pallavi ",
        'monthly_emi': '9000',
        'monthly_emi_date': '10 April 2021',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },
    '7009092504': {
        'name': "Tanisha",
        'monthly_emi': '8000',
        'monthly_emi_date': '10 April 2021',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },
    '7506523129': {
        'name': "Anushka",
        'monthly_emi': '7000',
        'monthly_emi_date': '14 April 2021',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },
    '9980470220': {
        'name': "Anusha",
        'monthly_emi': '5000',
        'monthly_emi_date': '14 April 2021',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },
    '7978694806': {
        'name': "Papun",
        'monthly_emi': '9000',
        'monthly_emi_date': '14 April 2021',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },
    '9594928933': {
        'name': "Rutuja",
        'monthly_emi': '6000',
        'monthly_emi_date': '14 April 2021',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },
    '7894427533': {
        'name': "soumya",
        'monthly_emi': '6000',
        'monthly_emi_date': '14 April 2021',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    },
    '7977906861': {
        'name': "karan",
        'monthly_emi': '6000',
        'monthly_emi_date': '14 April 2021',
        'late_fee': '700 ',
        'total_loan_amt': '500000 ',
        'total_installments': '75 ',
        'paid_installments': '15 ',
        'remaining_amt': '385699 ',
        'principal_amt': '150000 ',
        'loan_end_date': '18 January 2038 ',
        'account_no': '1 0 1 1 0 0 0 1 1 0 2 2 ',
        'interest_paid': '1354532 ',
        'emi_interest': '14',
        'location': 'bangalore'
    }

}

