import datetime
from email import utils
import time 

from actions.utils.common_imports import *
from actions.utils.helper import *
from datetime import timedelta, date
helper = Helper()

class PtpReminder(FormAction):
    def name(self):
        return "ptp_reminder_form"

    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        payment_confirmation = tracker.get_slot("payment_confirmation")
        availability_status = tracker.get_slot("availability_status")
        ask_delay_reason = tracker.get_slot("ask_delay_reason")
        if stop_conversation == "TRUE":
            return []
        if payment_confirmation == "ask_delay_reason":
            return ["ask_delay_reason"]
        if availability_status == "ask_delay_reason":
            return ["ask_delay_reason"]
        if availability_status == "payment_confirmation":
            return ["payment_confirmation"]
        return ["availability_status"]

    def get_delay_reason(self,value=None):
        return [
            self.from_intent(intent="business_loss", value=value),
            # self.from_intent(intent="cycle_date_issue", value=value),
            self.from_intent(intent="insufficient_funds", value=value),
            self.from_intent(intent="job_loss", value=value),
            self.from_intent(intent="salary_issue", value=value),
            # self.from_intent(intent="medical_issue", value=value),
            # self.from_intent(intent="foreclosing_through_own_funds", value=value),
            # self.from_intent(intent="branch_issue", value=value),
            self.from_intent(intent="family_dispute", value=value),
            # self.from_intent(intent="account_not_working", value=value),
            # self.from_intent(intent="change_account_for_deduction", value=value),
            self.from_intent(intent="personal_issue",value=value),
            # self.from_intent(intent="will_pay_late_fee",value=value),
            self.from_intent(intent="death_in_family",value=value),
            # self.from_intent(intent="technical_issue",value=value),   
        ]

    def slot_mappings(self):
        return{
            "availability_status": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="agree_to_proceed"),
                self.from_intent(intent = "inform",value = "TRUE"),
                self.from_intent(intent = "deny", value="deny"),
                self.from_intent(intent = "disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent = "inform_call_later", value="disagree_to_proceed"),
                self.from_intent(intent = "inform_wrong_info", value="inform_wrong_info"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "will_pay_late_fee", value="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="deny"),
                self.from_intent(intent = "bye", value="bye"),
                self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_method", value="TRUE"),
                # self.from_intent(intent = "pay_via_branch", value="TRUE"),
                # self.from_intent(intent = "pay_via_online", value="TRUE"),
                self.from_intent(intent = "ask_partial_payment",value = "FALSE"),
                self.from_intent(intent = "inform_payment_done",value = "inform_payment_done"),
            ] + self.get_delay_reason(value="decline_reason"),
            "payment_confirmation": [
                self.from_intent(intent = "affirm", value="TRUE"),  
                self.from_intent(intent = "agree_to_proceed", value="FALSE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent = "inform_call_later", value="inform_call_later"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "agree_to_pay", value="agree_to_pay"),
                self.from_intent(intent = "inform_wrong_info", value="inform_wrong_info"),
                # self.from_intent(intent = "pay_via_agent", value="TRUE"),
                self.from_intent(intent = "will_pay_late_fee", value="FALSE"),
                # self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                # self.from_intent(intent = "ask_payment_link", value="TRUE"),
                # self.from_intent(intent = "ask_payment_method", value="TRUE"),
                self.from_intent(intent = "ask_partial_payment", value = "FALSE"),
                self.from_intent(intent = "inform_payment_done", value = "inform_payment_done"),
            ] + self.get_delay_reason(value = "decline_reason"),
            "ask_delay_reason": [
                self.from_intent(intent = "affirm", value="agree_to_pay"),
                self.from_intent(intent = "agree_to_proceed", value="agree_to_pay"),
                self.from_intent(intent = "inform",value = "agree_to_pay"),
                self.from_intent(intent = "agree_to_pay", value="agree_to_pay"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent = "inform_call_later", value="disagree_to_proceed"),
                self.from_intent(intent = "inform_wrong_info", value="inform_wrong_info"),
                self.from_intent(intent = "will_pay_late_fee", value="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                # self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                # self.from_intent(intent = "ask_payment_link", value="TRUE"),
                # self.from_intent(intent = "ask_payment_method", value="TRUE"),
                self.from_intent(intent = "ask_partial_payment",value = "FALSE"),
                self.from_intent(intent = "inform_payment_done",value = "inform_payment_done"),
            ] + self.get_delay_reason(value="decline_reason"),
        }
    @staticmethod
    def _should_request_slot(tracker,slot_name):
        return tracker.get_slot(slot_name) is None
    
    def request_next_slot(
        self,
        dispatcher:"CollectingDispatcher",
        tracker:"Tracker",
        domain:Dict[Text,Any]
        ):
        for slot in self.required_slots(tracker):
            trail_count = tracker.get_slot("trail_count")
            if self._should_request_slot(tracker,slot):
                total_loans = get_total_loan(tracker)
                total_emi_amount,due_date,sheet_name,emi_flow,loan_id,ReferenceNo = get_emi_details(tracker,total_loans)
                print(total_emi_amount,due_date,sheet_name,emi_flow,"total_emi_amount,due_date,sheet_name,emi_flow")
                if slot == "availability_status":
                    if trail_count is None:
                        dispatcher.utter_template("utter_greet_reminder",tracker,monthly_emi=str(total_emi_amount))
                        print("EMI Flow in Availability Slot>>>>>>>>>>>>", emi_flow)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="pic")
                    else:
                        dispatcher.utter_template("utter_greet_reminder_trim",tracker, monthly_emi = str(total_emi_amount))
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="pic",emi_flow = emi_flow)
                if slot == "payment_confirmation":
                    if trail_count is None:
                        dispatcher.utter_template("utter_RTP_reminder",tracker)
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_RTP_reminder_trim",tracker, monthly_emi = str(total_emi_amount))
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="pic",emi_flow = emi_flow)
                
                if slot == "ask_delay_reason":
                    if trail_count is None:
                       dispatcher.utter_template("utter_RTP_2_reminder", tracker)
                       send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_RTP_2_reminder_trim",tracker, monthly_emi = str(total_emi_amount))
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="pic",emi_flow = emi_flow)
                
                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1) if trail_count is not None else None]
    
    
    @staticmethod
    def validate_availability_status(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any],
    ):
        print("The value comes to this function is, ",value)
        total_loans = get_total_loan(tracker)
        total_emi_amount,due_date,sheet_name,emi_flow,loan_id,ReferenceNo = get_emi_details(tracker,total_loans)
        if value == "disagree_to_proceed":
            dispatcher.utter_template("utter_not_available_to_talk_2_reminder", tracker, monthly_emi = str(total_emi_amount))
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="disagree to proceed",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}

        elif value == "FALSE":
            print("Coming this disagree to pay1")
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="rtp",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"availability_status": "payment_confirmation", "trail_count": None}

        elif value == "deny" or value == "agree_to_proceed":
            print("Coming this disagree to pay1")
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="rtp",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"availability_status": "payment_confirmation", "trail_count": None}

        elif value == "TRUE" :
            user_message = tracker.latest_message.get("text")
            entities = tracker.latest_message["entities"]
            now = datetime.datetime.now()
            intent = tracker.latest_message.get("intent").get("name")
            if entities:
                if intent in date_check_intents:
                    # TODO store the promise to pay date, and need to add payment link response also
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                due_date=datetime.datetime.strptime(due_date[0],"%d-%m-%Y").date()
                                no_of_days = given_date.date() - datetime.datetime.now().date()
                                print("no of days", no_of_days)
                                if no_of_days.days == 0:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_PTP_today_reminder",tracker, monthly_emi = str(total_emi_amount))
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="SDP",
                                                                    flag=TIMEOUT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                                    return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}
                                elif no_of_days.days <= 1:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_PTP_today_reminder",tracker, monthly_emi = str(total_emi_amount))
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                                    return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}
                                else:
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="PTP", flag=DEFAULT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                                    return {"availability_status": "payment_confirmation", "trail_count": None}
            
            else:
                now = datetime.datetime.now()
                given_date = now.strftime("%d %B %Y")
                dispatcher.utter_template("utter_PTP_today_reminder",tracker, monthly_emi = str(total_emi_amount))
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="SDP",
                                                                    flag=TIMEOUT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}

        elif value == "inform_wrong_info":
            dispatcher.utter_template("utter_agent_will_connect_common", tracker)
            dispatcher.utter_template("utter_bye_common", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"availability_status": value, "stop_conversation": "TRUE"}
        
        elif value == "inform_payment_done":
            dispatcher.utter_template("utter_bye_common",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                        disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"availability_status": value, "stop_conversation": "TRUE"}
        elif value=="bye":
            dispatcher.utter_template("utter_bye_common",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="bye",emi_flow=emi_flow)
            return {"stop_conversation":"TRUE"}

        elif value == "decline_reason":
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            entities = tracker.latest_message["entities"]
            if entities:
                for entity in entities:
                    if entity.get("entity", None) == "date":
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                        given_date = given_date.strftime("%d %B %Y")
                        intent = tracker.latest_message.get("intent").get("name")
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=DEFAULT_FLAG,emi_flow=emi_flow)
                        return {"availability_status": "payment_confirmation", "trail_count":None}
                    else:
                        intent = tracker.latest_message.get("intent").get("name")
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=DEFAULT_FLAG,emi_flow=emi_flow)
                        return {"availability_status": "payment_confirmation", "trail_count":None}
            else:
                intent = tracker.latest_message.get("intent").get("name")
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=DEFAULT_FLAG,emi_flow=emi_flow)
                return {"availability_status": "payment_confirmation", "trail_count":None}
        return{"availability_status":None}

    @staticmethod
    def validate_payment_confirmation(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any], 
    ):
        total_loans = get_total_loan(tracker)
        total_emi_amount,due_date,sheet_name,emi_flow,loan_id,ReferenceNo = get_emi_details(tracker,total_loans)
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE" or value == "agree_to_pay":
            user_message = tracker.latest_message.get("text")
            entities = tracker.latest_message["entities"]
            now = datetime.datetime.now()
            intent = tracker.latest_message.get("intent").get("name")
            if entities:
                if intent in date_check_intents:
                    # TODO store the promise to pay date, and need to add payment link response also
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                due_date=datetime.datetime.strptime(due_date[0],"%d-%m-%Y").date()
                                no_of_days = given_date.date() - datetime.datetime.now().date()
                                print("no of days", no_of_days)
                                if no_of_days.days == 0:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_PTP_today_reminder",tracker, monthly_emi = str(total_emi_amount))
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="SDP",
                                                                    flag=TIMEOUT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                                    return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}
                                if no_of_days.days <= 1:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_PTP_today_reminder",tracker, monthly_emi = str(total_emi_amount))
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                                    return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}
                                else:
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="PTP", flag=DEFAULT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                                    return {"payment_confirmation": "ask_delay_reason", "trail_count": None}
            else:
                Date_req = date.today() + timedelta(days=1)
                given_date = Date_req.strftime("%d %B %Y")
                dispatcher.utter_template("utter_agree_to_pay_2_reminder", tracker, monthly_emi = str(total_emi_amount))
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                                disposition_id="PTP", flag=TIMEOUT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                return {"payment_confirmation":value,"trail_count":None,"stop_conversation": "TRUE"}

        elif value == "FALSE":
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="rtp", flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation": "ask_delay_reason","trail_count":None}

        elif value == "decline_reason":
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            entities = tracker.latest_message["entities"]
            if entities:
                for entity in entities:
                    if entity.get("entity", None) == "date":
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                        given_date = given_date.strftime("%d %B %Y")
                        intent = tracker.latest_message.get("intent").get("name")
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=DEFAULT_FLAG,emi_flow=emi_flow)
                        return {"payment_confirmation": "ask_delay_reason","trail_count":None}
                    else:
                        intent = tracker.latest_message.get("intent").get("name")
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=DEFAULT_FLAG,emi_flow=emi_flow)
                        return {"payment_confirmation": "ask_delay_reason","trail_count":None}

            else:
                intent = tracker.latest_message.get("intent").get("name")
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=DEFAULT_FLAG,emi_flow=emi_flow)
                return {"payment_confirmation": "ask_delay_reason","trail_count":None}

        elif value == "inform_wrong_info":
            dispatcher.utter_template("utter_agent_will_connect", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}

        elif value == "inform_payment_done":
            dispatcher.utter_template("utter_already_paid_due_date",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                        disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"trail_count":None,"payment_confirmation":value,"stop_conversation":"TRUE"}
        
        return{"payment_confirmation":None}


    @staticmethod
    def validate_ask_delay_reason(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any]
    ):
        total_loans = get_total_loan(tracker)
        total_emi_amount,due_date,sheet_name,emi_flow,loan_id,ReferenceNo = get_emi_details(tracker,total_loans)
        user_message = tracker.latest_message.get("text")
        if value  == "FALSE":
            dispatcher.utter_template("utter_reason_unaccepted_reminder",tracker)
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ask_delay_reason":value,"stop_conversation":"TRUE","trail_count": None}
        elif value == "agree_to_pay":
            intent = tracker.latest_message.get("intent").get("name")
            dispatcher.utter_template("utter_agree_to_pay_2_reminder",tracker, monthly_emi = str(total_emi_amount))
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"stop_conversation": "TRUE", "trail_count": None, "ask_delay_reason": value}

        elif value == "inform_payment_done":
            dispatcher.utter_template("utter_already_paid_due_date", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}

        elif value == "decline_reason":
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            entities = tracker.latest_message["entities"]
            dispatcher.utter_template("utter_reason_unaccepted_reminder", tracker)
            if entities:
                for entity in entities:
                    if entity.get("entity", None) == "date":
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                        given_date = given_date.strftime("%d %B %Y")
                        intent = tracker.latest_message.get("intent").get("name")
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                    else:
                        intent = tracker.latest_message.get("intent").get("name")
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)

            else:
                intent = tracker.latest_message.get("intent").get("name")
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}

        return {"ask_delay_reason":None}
        
        

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any]
    ) -> List[EventType]:
        return [FollowupAction("action_listen"), AllSlotsReset()] 