import datetime
from email import utils
import time 

from actions.utils.common_imports import *
from actions.utils.helper import *

helper = Helper()

class preEmiSriram(FormAction):
    def name(self):
        return "sriram_pre_emi_form"

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
            self.from_intent(intent="cycle_date_issue", value=value),
            self.from_intent(intent="insufficient_funds", value=value),
            self.from_intent(intent="job_loss", value=value),
            self.from_intent(intent="foreclosing_through_own_funds", value=value),
            self.from_intent(intent="branch_issue", value=value),
            self.from_intent(intent="account_not_working", value=value),
            self.from_intent(intent="change_account_for_deduction", value=value),
            self.from_intent(intent="personal_issue",value=value)
        ]

    def slot_mappings(self):
        return{
            "availability_status": [
                
                self.from_intent(intent = "ask_payment_link",value = "TRUE"),
                self.from_intent(intent = "pay_online",value = "TRUE"),
                self.from_intent(intent = "pay_via_branch",value = "TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="TRUE"),
                self.from_intent(intent = "affirm", value="agree_to_pay"),
                self.from_intent(intent = "inform",value = "agree_to_pay"),
                self.from_intent(intent = "agree_to_pay", value="agree_to_pay"),
                self.from_intent(intent = "deny", value="deny"),
                self.from_intent(intent = "insufficient_funds", value="deny"),
                self.from_intent(intent = "disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent = "inform_wrong_info", value="inform_wrong_info"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "bye", value="bye"),
                # self.from_intent(intent = "ask_partial_payment",value = "disagree_to_pay"),
            ] + self.get_delay_reason(value="decline_reason"),
            "payment_confirmation": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="TRUE"),
                self.from_intent(intent = "ask_payment_link",value = "TRUE"),
                self.from_intent(intent = "pay_via_branch",value = "TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                # self.from_intent(intent = "ask_partial_payment",value = "disagree_to_pay"),
            ] + self.get_delay_reason(value="decline_reason"),
            "ask_delay_reason": [
                self.from_intent(intent = "affirm", value="+1"),
                self.from_intent(intent = "agree_to_proceed", value="+1"),
                self.from_intent(intent = "inform",value = "TRUE"),
                self.from_intent(intent = "agree_to_pay", value="agree_to_pay"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                # self.from_intent(intent = "ask_partial_payment",value = "disagree_to_pay"),
            ] + self.get_delay_reason(value="decline_reason")
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
                total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
                print(total_emi_amount,due_date,sheet_name,emi_flow,"total_emi_amount,due_date,sheet_name,emi_flow")
                if slot == "availability_status":
                    print("http://localhost:13214/nlg",trail_count)
                    if trail_count is None:
                        trail_count = 0
                        day_time = helper.get_daytime()
                        print("The due date value is",due_date)
                        # date = due_date[0].date()
                        # value = datetime.strptime(due_date[0],'%d/%m/%Y')
                        emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
                        ptp_date = emi_date.strftime("%d %B %Y")
                        print("The value of date ",emi_date)
                        # ptp_date = value.strftime("%d %B, %Y").replace(",","")
                        dispatcher.utter_template("utter_greet_predue",tracker,monthly_emi = total_emi_amount,monthly_emi_date=ptp_date)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="pic",emi_amount=total_emi_amount,
                                        emi_flow="pre_emi")
                    if trail_count >=1:
                        emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
                        ptp_date = emi_date.strftime("%d %B %Y")
                        print("The value of date ",emi_date)
                        dispatcher.utter_template("utter_repeat_ask_payment_pre_due",tracker)
                        return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time())]
                if slot == "payment_confirmation":
                    if trail_count is None:
                        dispatcher.utter_template("utter_disagree_to_pay",tracker)
                    else:
                        dispatcher.utter_template("utter_disagree_to_pay",tracker)
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                disposition_id="pic",emi_flow="pre_emi")
                if slot == "ask_delay_reason":
                    dispatcher.utter_template("utter_disagree_to_pay_disagree", tracker)
                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time())]
    
    
    
    @staticmethod
    def validate_availability_status(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any],
    ):
        print("The value comes to this function is, ",value)
        if value ==  "TRUE":
            dispatcher.utter_template("utter_agree_to_pay",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="PTP",flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}

        if value == "disagree_to_proceed":
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
            emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
            ptp_date = emi_date.strftime("%d %B %Y")
            user_details = get_user_details(tracker)
            dispatcher.utter_template("utter_not_avail_talk", tracker,monthly_emi = total_emi_amount,monthly_emi_date = ptp_date)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="disagree to proceed",flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"availability_status": value, "trail_count": None,"stop_conversation":"TRUE"}

        if value == "FALSE":
            print("Coming this disagree to pay1")
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="rtp",flag=DEFAULT_FLAG,emi_flow="pre_emi")
            return {"availability_status": "payment_confirmation", "trail_count": None}
        elif value == "deny":
            # dispatcher.utter_template("utter_diagree_to_pay",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, 
                    user_message=user_message,disposition_id="deny",flag=DEFAULT_FLAG,emi_flow="pre_emi")
            return {"availability_status": "payment_confirmation", "trail_count": None}
        elif value == "agree_to_pay" or value =="inform":
            print("value is getting matched")
            entities = tracker.latest_message["entities"]
            intent = tracker.latest_message.get("intent").get("name")
            user_message = tracker.latest_message.get("text")
            print("The captured entities are ",entities)
            given_date = ""
            if entities:
                for entity in entities:
                    if entity.get("entity", None) == "date":
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                        print("given date", given_date)
                        if given_date:
                            no_of_days = given_date.date() - datetime.datetime.now().date()
                        if no_of_days.days<=2:
                            given_date = given_date.strftime("%d %B %Y")
                        if no_of_days>2:
                            given_date = given_date.strftime("%d %B %Y")
            dispatcher.utter_template("utter_agree_to_pay",tracker)
            if given_date ==  "": 
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                            user_message=user_message,disposition_id="agree to pay",flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            else:
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                            user_message=user_message,disposition_id="PTP",flag=TIMEOUT_FLAG,emi_flow="pre_emi",ptp_date=given_date)
                                
            return {"availability_status":value,"stop_conversation":"TRUE","trail_count":None}
        elif value == "inform_wrong_info":
            dispatcher.utter_template("utter_agent_will_connect_common", tracker)
            dispatcher.utter_template("utter_bye", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="wrong info",user_message=user_message,flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"availability_status": value, "stop_conversation": "TRUE"}
        elif value == "+1":
            dispatcher.utter_template("utter_confirm_again", tracker)
            return {"availability_status": value}
        elif value == "decline_reason":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"availability_status": value, "stop_conversation": "TRUE"}
        elif value=="bye":
            dispatcher.utter_template("utter_bye_common",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="bye",emi_flow="pre_emi")
            return {"stop_conversation":"TRUE"}
        return{"availability_status":None}

    @staticmethod
    def validate_payment_confirmation(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any], 
    ):
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            dispatcher.utter_template("utter_disagree_to_pay_agree",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                            flag=TIMEOUT_FLAG,emi_flow="pre_emi",)
            return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}
        elif value == "FALSE":
            # dispatcher.utter_template("utter_diagree_to_pay", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="rtp", flag=DEFAULT_FLAG,emi_flow="pre_emi")
            return {"payment_confirmation": "ask_delay_reason"}
        elif value == "decline_reason":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}
        elif value == "inform_wrong_info":
            dispatcher.utter_template("utter_agent_will_connect", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="wrong info",user_message=user_message,flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}
        # elif value== "disagree_to_pay":
        #     dispatcher.utter_template("utter_disagree_to_pay_disagree",tracker)
        #     user_message=tracker.latest_message.get("text")
        #     send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="rtp", 
        #         flag=DEFAULT_FLAG,emi_flow="pre_emi")
        #     return {"payment_confirmation": value, "trail_count": None}
        # elif value == "agree_to_pay":
        #     dispatcher.utter_template("utter_disagree_to_pay_agree",tracker)
        #     return {"payment_confirmation": value, "stop_conversation": "TRUE"}        
        elif value == "inform_payment_done":
            dispatcher.utter_template("utter_bye",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                        disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"trail_count":None,"payment_confirmation":value,"stop_conversation":"TRUE"}
        
        if value == "disagree_to_proceed":
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
            emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
            ptp_date = emi_date.strftime("%d %B %Y")
            user_details = get_user_details(tracker)
            dispatcher.utter_template("utter_not_avail_talk", tracker,monthly_emi = total_emi_amount,monthly_emi_date = ptp_date)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="disagree to proceed",flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}


    @staticmethod
    def validate_ask_delay_reason(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any]
    ):
        if value  == "FALSE":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted",tracker)
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"ask_delay_reason":value,"stop_conversation":"TRUE"}
        elif value == "agree_to_pay":
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            dispatcher.utter_template("utter_disagree_to_pay_agree",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                        flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"ask_delay_reason":value,"stop_conversation":"TRUE","trail_count":None}
        elif value == "decline_reason":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            # dispatcher.utter_template("utter_bye",tracker)
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay_reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"ask_delay_reason": value, "stop_conversation": "TRUE"}  
        elif value == "+1":
            dispatcher.utter_template("utter_apology", tracker)
            dispatcher.utter_template("utter_confirm_again", tracker)
            return {"ask_delay_reason": None, "trail_count": get_trail_count(tracker)}
        elif value == "+2":
            dispatcher.utter_template("utter_send_payment_link", tracker)
            dispatcher.utter_template("utter_thank_you", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="PTP", flag=TIMEOUT_FLAG,emi_flow="post_emi",)
            return {"trail_count": None, "ask_delay_reason": value,"stop_conversation": "TRUE"}
        elif value == "inform_payment_done":
            dispatcher.utter_template("utter_bye", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}

        elif value == "cycle_date_issue":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="pre_emi",delay_reason="cycle date issue")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        elif value == "business_loss":
            dispatcher.utter_template("utter_disagree_to_pay_reason_accepted",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="pre_emi",delay_reason="business loss")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        elif value == "insufficient_funds":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="pre_emi",delay_reason="insufficient funds")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        
        elif value == "family_dispute":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="pre_emi",delay_reason="family dispute")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        
        elif value == "change_account_for_deduction":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="pre_emi",delay_reason="change account for deduction")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}

        elif value == "account_not_working":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="pre_emi",delay_reason="account not working")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}

        elif value == "foreclosing_through_own_funds":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="pre_emi",delay_reason="foreclosing through own funds")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        
        if value == "disagree_to_proceed":
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
            emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
            ptp_date = emi_date.strftime("%d %B %Y")
            user_details = get_user_details(tracker)
            dispatcher.utter_template("utter_not_avail_talk", tracker,monthly_emi = total_emi_amount,monthly_emi_date = ptp_date)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="disagree to proceed",flag=TIMEOUT_FLAG,emi_flow="pre_emi")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}

        return {"ask_delay_reason":None}

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any]
    ) -> List[EventType]:
        return [FollowupAction("action_listen"), AllSlotsReset()]    