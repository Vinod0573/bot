import datetime
import time

from actions.utils.common_imports import *
from actions.utils.helper import *

helper = Helper()


class AvailFinancePostEMI(FormAction):
    def name(self):  # type: () -> Text
        return "post_emi_updated_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        payment_confirmation = tracker.get_slot("payment_confirmation")
        availability_status=tracker.get_slot("availability_status")
        if stop_conversation == "TRUE":
            return []
        # if payment_confirmation == "ask_partial_payment":
        #     return ["availability_status", "payment_confirmation", "partial_payment_status"]
        if availability_status == "ask_delay_reason":
            return ["ask_delay_reason"]
        return ["availability_status"]

    def get_delay_reason(self, value=None):
        return [
            self.from_intent(intent="business_loss", value=value),
            self.from_intent(intent="cycle_date_issue", value=value),
            self.from_intent(intent="insufficient_funds", value=value),
            self.from_intent(intent="job_loss", value=value),
            self.from_intent(intent="salary_issue",value=value),
            self.from_intent(intent="medical_issue", value=value),
            self.from_intent(intent="technical_issue", value=value),
            self.from_intent(intent="family_dispute", value=value),
            self.from_intent(intent="foreclosing_through_own_funds", value=value),
            self.from_intent(intent="branch_issue", value=value),
            self.from_intent(intent="account_not_working", value=value),
            self.from_intent(intent="change_account_for_deduction", value=value),
            self.from_intent(intent="personal_issue",value=value)
            # self.from_intent(intent="transfer_to_another_hfc", value=value),
        ]

    def slot_mappings(self):  # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        return {
            "availability_status": [
                self.from_intent(intent="affirm", value="TRUE"),
                self.from_intent(intent="agree_to_proceed", value="TRUE"),
                self.from_intent(intent="deny", value="deny"),
                self.from_intent(intent="disagree_to_proceed", value="deny"),
                self.from_intent(intent="inform_wrong_info", value="inform_wrong_info"),
                self.from_intent(intent="agree_to_pay", value="agree_to_pay"),
                self.from_intent(intent="ask_partial_payment", value="agree_to_pay"),
                self.from_intent(intent="disagree_to_pay", value="disagree_to_pay"),
                self.from_intent(intent="inform_payment_done", value="paid"),
                self.from_intent(intent="bye", value="bye"),
            ] + self.get_delay_reason(value="decline_reason"),
            # "payment_confirmation": [
            #     self.from_intent(intent="affirm", value="TRUE"),
            #     self.from_intent(intent="agree_to_proceed", value="TRUE"),
            #     self.from_intent(intent="deny", value="FALSE"),
            #     self.from_intent(intent="disagree_to_proceed", value="FALSE"),
            #     self.from_intent(intent="disagree_to_pay", value="FALSE"),
            #     self.from_intent(intent="inform_wrong_info", value="inform_wrong_info"),
            #     self.from_intent(intent="agree_to_pay", value="TRUE"),
            #     self.from_intent(intent="ask_partial_payment", value="TRUE"),
            #     self.from_intent(intent="inform", value="TRUE"),
            #     self.from_intent(intent="inform_payment_done", value="inform_payment_done"),
            # ] + self.get_delay_reason(value="decline_reason"),
            # "partial_payment_status": [
            #     self.from_intent(intent="affirm", value="TRUE"),
            #     self.from_intent(intent="agree_to_proceed", value="TRUE"),
            #     self.from_intent(intent="agree_to_pay", value="TRUE"),
            #     self.from_intent(intent="deny", value="FALSE"),
            #     self.from_intent(intent="disagree_to_proceed", value="FALSE"),
            #     self.from_intent(intent="disagree_to_pay", value="FALSE"),
            #     self.from_intent(intent="inform_wrong_info", value="inform_wrong_info"),
            #     self.from_intent(intent="ask_partial_payment", value="TRUE"),
            #     self.from_intent(intent="inform_payment_done", value="inform_payment_done"),
            # ] + self.get_delay_reason(value="decline_reason"),
            "ask_delay_reason": [
                self.from_intent(intent="affirm", value="+1"),
                self.from_intent(intent="agree_to_proceed", value="+1"),
                self.from_intent(intent="agree_to_pay", value="+2"),
                self.from_intent(intent="deny", value="FALSE"),
                self.from_intent(intent="disagree_to_proceed", value="FALSE"),
                self.from_intent(intent="disagree_to_pay", value="FALSE"),
                self.from_intent(intent="inform_wrong_info", value="FALSE"),
                self.from_intent(intent="ask_partial_payment", value="+2"),
                self.from_intent(intent="inform_payment_done", value="inform_payment_done"),
            ] + self.get_delay_reason(value="decline_reason")
        }

    @staticmethod
    def _should_request_slot(tracker, slot_name):  # type: (Tracker, Text) -> bool
        """Check whether form action should request given slot"""
        return tracker.get_slot(slot_name) is None

    def request_next_slot(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ):
        for slot in self.required_slots(tracker):
            trail_count = tracker.get_slot("trail_count")
            if self._should_request_slot(tracker, slot):
                if slot == "availability_status":
                    if trail_count is None:
                        day_time = helper.get_daytime()
                        # dispatcher.utter_template('utter_ask_capability', tracker, day_time=day_time)
                        total_loans=get_total_loan(tracker)
                        total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo=get_emi_details(tracker,total_loans)
                        if len(total_loans)>1:
                            dispatcher.utter_template("utter_greet_multiple_cred",tracker,total_emi=str(total_emi_amount),no_of_loans=str(len(total_loans)))
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="initial message",sheet_name=sheet_name,emi_flow=emi_flow)
                        else:
                            due_date=datetime.datetime.strptime(due_date,"%d-%m-%Y")
                            due_date=due_date.strftime("%d %B %Y")
                            print("Updated due date:",due_date)
                            dispatcher.utter_template("utter_greet_cred",tracker,monthly_emi=str(total_emi_amount),emi_date=due_date)
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="initial message",sheet_name=sheet_name,emi_flow=emi_flow)
                        dispatcher.utter_template("utter_ask_payment_confirmation",tracker)
                        # dispatcher.utter_template("utter_ask_capability", tracker)
                        # dispatcher.utter_template("utter_important",tracker)
                        # dispatcher.utter_template("utter_ask_availability", tracker)
                    else:
                        dispatcher.utter_template("utter_ask_payment_confirmation", tracker)
                        return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot)]
                if slot == "ask_delay_reason":
                    dispatcher.utter_template("utter_ask_delay_reason", tracker)
                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time()),SlotSet("sheet_name",sheet_name),SlotSet("emi_flow",emi_flow)]

    @staticmethod
    def validate_availability_status(
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ):
        # user_details = get_user_details(tracker)
        # if value == "TRUE":
        #     return {"availability_status": value, "trail_count": None}
        user_message = tracker.latest_message.get("text")
        sheet_name=tracker.get_slot("sheet_name")
        if value == "deny":
            dispatcher.utter_template("utter_disagree_to_pay_cred",tracker)
            dispatcher.utter_template("utter_thank_you",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="rtp", flag=TIMEOUT_FLAG, emi_flow="post_emi",sheet_name=sheet_name)
            return {"availability_status": value, "stop_conversation": "TRUE"}
        elif value=="disagree_to_pay":
            dispatcher.utter_template("utter_disagree_to_pay_cred",tracker)
            dispatcher.utter_template("utter_thank_you",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="rtp", flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
            return {"availability_status": value,"stop_conversation":"TRUE"}
        elif value=="agree_to_pay" or value=="TRUE":
            entities = tracker.latest_message["entities"]
            now = datetime.datetime.now()
            intent = tracker.latest_message.get("intent").get("name")
            # user_details = get_user_details(tracker)
            if entities:
                if intent in date_check_intents:
                    # TODO store the promise to pay date, and need to add payment link response also
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                no_of_days = given_date.date() - datetime.datetime.now().date()
                                # print("no of days", no_of_days)
                                # if no_of_days.days:
                                #     return {"payment_confirmation": "ask_partial_payment", "trail_count": None}
                                if no_of_days.days < 7:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_dpd_less_7",tracker,ptp_day=given_date)
                                    dispatcher.utter_template("utter_thank_you", tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG, ptp_date=given_date,emi_flow="post_emi",sheet_name=sheet_name)
                                    # send_message(tracker)
                                    return {"availability_status": value, "stop_conversation": "TRUE", "trail_count": None}
                                else:
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="PTP",
                                                                    flag=DEFAULT_FLAG, ptp_date=given_date,emi_flow="post_emi",sheet_name=sheet_name)
                                    # send_message(tracker)
                                    return {"availability_status": "ask_delay_reason", "trail_count": None}
                        else:
                            dispatcher.utter_template("utter_agree_to_pay_cred", tracker)
                            # send_message(tracker)
                            dispatcher.utter_template("utter_thank_you", tracker)
                            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                                            disposition_id="PTP", flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
                            return {"availability_status": value, "stop_conversation": "TRUE", "trail_count": None}
            else:
                dispatcher.utter_template("utter_agree_to_pay_cred", tracker)
                # send_message(tracker)
                # dispatcher.utter_template("utter_thank_you", tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                                disposition_id="PTP", flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
                return {"availability_status": value, "stop_conversation": "TRUE", "trail_count": None}
        elif value == "inform_wrong_info":
            dispatcher.utter_template("utter_agent_will_connect", tracker)
            send_and_store_disposition_details(tracker=tracker, disposition_id="wrong info human agent",dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
            return {"availability_status": value, "stop_conversation": "TRUE"}
        elif value == "decline_reason":
            dispatcher.utter_template("utter_disagree_to_pay_cred", tracker)
            dispatcher.utter_template("utter_thank_you", tracker)
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
            return {"availability_status": value, "stop_conversation": "TRUE"}
        elif value == "paid":
            dispatcher.utter_template("utter_bye", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
            return {"trail_count": None, "payment_confirmation": value, "stop_conversation": "TRUE"}
        elif value=="bye":
            dispatcher.utter_template("utter_disagree_to_pay_cred", tracker)
            dispatcher.utter_template("utter_thank_you", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message, flag=TIMEOUT_FLAG,disposition_id="bye",emi_flow="post_emi",sheet_name=sheet_name)
            return {"stop_conversation":"TRUE"}
        # return {"availability_status": None}

    # @staticmethod
    # def validate_payment_confirmation(
    #         value: Text,
    #         dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any],
    # ):
    #     user_message = tracker.latest_message.get("text")
    #     user_details = get_user_details(tracker)
    #     if value == "TRUE":
    #         # trail_count = tracker.get_slot("trail_count")
    #         # if trail_count is None:
    #         #     dispatcher.utter_template("utter_thank_you_2", tracker)
    #         #     send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
    #         #                                        disposition_id=customer_informed_agree_to_pay, flag=DEFAULT_FLAG)
    #         #     return {"payment_confirmation": None, "trail_count": get_trail_count(tracker)}
    #         # else:
    #         entities = tracker.latest_message["entities"]
    #         now = datetime.datetime.now()
    #         intent = tracker.latest_message.get("intent").get("name")
    #         if entities and intent in date_check_intents:
    #             # TODO store the promise to pay date, and need to add payment link response also
    #             for entity in entities:
    #                 if entity.get("entity", None) == "date":
    #                     given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
    #                     print("given date", given_date)
    #                     if given_date:
    #                         no_of_days = given_date.date() - datetime.datetime.now().date()
    #                         # print("no of days", no_of_days)
    #                         # if no_of_days.days:
    #                         #     return {"payment_confirmation": "ask_partial_payment", "trail_count": None}
    #                         if no_of_days.days == 0:
    #                             given_date = given_date.strftime("%d %B %Y")
    #                             dispatcher.utter_template("utter_inform_ptp_date_today", tracker)
    #                             dispatcher.utter_template("utter_send_payment_link_2", tracker,
    #                                                     monthly_emi=user_details.get("EMI Amount"))
    #                             dispatcher.utter_template("utter_thank_you", tracker)
    #                             send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
    #                                                             flag=TIMEOUT_FLAG, ptp_date=given_date,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi",
    #                                                             customer_name=user_details["Employee Name"],loan_id=user_details['loan_id'],emi_amount=user_details['EMI Amount'],due_date=user_details['Due date'],payment_link=user_details['payment_link'])
    #                             # send_message(tracker)
    #                             return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}
    #                         if 0 < no_of_days.days < 7:
    #                             given_date = given_date.strftime("%d %B %Y")
    #                             dispatcher.utter_template("utter_inform_ptp_date", tracker,
    #                                                     ptp_day=given_date)
    #                             dispatcher.utter_template("utter_send_payment_link_2", tracker,
    #                                                     monthly_emi=user_details.get("EMI Amount"))
    #                             dispatcher.utter_template("utter_thank_you", tracker)
    #                             send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
    #                                                             user_message=user_message,
    #                                                             disposition_id="PTP",
    #                                                             flag=TIMEOUT_FLAG, ptp_date=given_date,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi",
    #                                                             customer_name=user_details["Employee Name"],loan_id=user_details['loan_id'],emi_amount=user_details['EMI Amount'],due_date=user_details['Due date'],payment_link=user_details['payment_link'])
    #                             # send_message(tracker)
    #                             return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}
    #                         else:
    #                             given_date = given_date.strftime("%d %B %Y")
    #                             send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
    #                                                             user_message=user_message,
    #                                                             disposition_id="PTP",
    #                                                             flag=DEFAULT_FLAG, ptp_date=given_date,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi",
    #                                                             customer_name=user_details["Employee Name"],loan_id=user_details['loan_id'],emi_amount=user_details['EMI Amount'],due_date=user_details['Due date'],payment_link=user_details['payment_link'])
    #                             # send_message(tracker)
    #                             return {"payment_confirmation": "ask_delay_reason", "trail_count": None}
    #         dispatcher.utter_template("utter_send_payment_link", tracker,
    #                                     monthly_emi=user_details.get("EMI Amount"))
    #         # send_message(tracker)
    #         dispatcher.utter_template("utter_thank_you", tracker)
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
    #                                             disposition_id="PTP", flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi",
    #                                             customer_name=user_details["Employee Name"],loan_id=user_details['loan_id'],emi_amount=user_details['EMI Amount'],due_date=user_details['Due date'],payment_link=user_details['payment_link'])
    #         return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}
    #     elif value == "FALSE":
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
    #                                            disposition_id="rtp", flag=DEFAULT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi")
    #         return {"payment_confirmation": "ask_partial_payment", "trail_count": None}
    #     elif value == "decline_reason":
    #         dispatcher.utter_template("utter_inform_late_charges_2", tracker)
    #         user_message = tracker.latest_message.get("text")
    #         intent = tracker.latest_message.get("intent").get("name")
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
    #                                            delay_reason=decline_reason_disposition_id.get(intent),
    #                                            flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi")
    #         return {"payment_confirmation": value, "stop_conversation": "TRUE"}
    #     elif value == "inform_wrong_info":
    #         dispatcher.utter_template("utter_agent_will_connect", tracker)
    #         user_message = tracker.latest_message.get("text")
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi")
    #         return {"payment_confirmation": value, "stop_conversation": "TRUE"}
    #     elif value == "partial_payment":
    #         dispatcher.utter_template("utter_send_payment_link", tracker, monthly_emi=500)
    #         # TODO send payment link with amount
    #         dispatcher.utter_template("utter_thank_you", tracker)
    #         user_message = tracker.latest_message.get("text")
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
    #                                            disposition_id="Partial Payment Requested", flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi")
    #         return {"trail_count": None, "payment_confirmation": value, "stop_conversation": "TRUE"}
        # elif value == "inform_payment_done":
        #     dispatcher.utter_template("utter_bye", tracker)
        #     user_message = tracker.latest_message.get("text")
        #     send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
        #                                        disposition_id="Paid", flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi")
        #     return {"trail_count": None, "payment_confirmation": value, "stop_conversation": "TRUE"}
    #     return {"payment_confirmation": None}

    # @staticmethod
    # def validate_partial_payment_status(
    #         value: Text,
    #         dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any],
    # ):
    #     user_details = get_user_details(tracker)
    #     if value == "TRUE":
    #         partial_amount=500
    #         dispatcher.utter_template("utter_send_payment_link", tracker, monthly_emi=partial_amount)
    #         dispatcher.utter_template("utter_thank_you", tracker)
    #         user_message = tracker.latest_message.get("text")
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
    #                                            disposition_id="Partial PTP", flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi",partial_amount=partial_amount)
    #         return {"partial_payment_status": value, "stop_conversation": "TRUE", "trail_count": None}
    #     elif value == "FALSE":
    #         dispatcher.utter_template("utter_inform_late_charges_2", tracker)
    #         user_message = tracker.latest_message.get("text")
    #         intent = tracker.latest_message.get("intent").get("name")
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
    #                                            delay_reason=decline_reason_disposition_id.get(intent),
    #                                            flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi")
    #         return {"partial_payment_status": value, "stop_conversation": "TRUE"}
    #     elif value == "decline_reason":
    #         dispatcher.utter_template("utter_inform_late_charges_2", tracker)
    #         user_message = tracker.latest_message.get("text")
    #         intent = tracker.latest_message.get("intent").get("name")
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
    #                                            delay_reason=decline_reason_disposition_id.get(intent),
    #                                            flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi")
    #         return {"partial_payment_status": value, "stop_conversation": "TRUE"}
    #     elif value == "inform_wrong_info":
    #         dispatcher.utter_template("utter_agent_will_connect", tracker)
    #         user_message = tracker.latest_message.get("text")
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi")
    #         return {"partial_payment_status": value, "stop_conversation": "TRUE"}
    #     elif value == "inform_payment_done":
    #         dispatcher.utter_template("utter_bye", tracker)
    #         user_message = tracker.latest_message.get("text")
    #         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
    #                                            disposition_id="Paid", flag=TIMEOUT_FLAG,language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow="post_emi")
    #         return {"trail_count": None, "partial_payment_status": value, "stop_conversation": "TRUE"}
    #     return {"partial_payment_status": None}

    @staticmethod
    def validate_ask_delay_reason(
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ):
        user_message = tracker.latest_message.get("text")
        sheet_name=tracker.get_slot("sheet_name")
        if value == "FALSE":
            dispatcher.utter_template("utter_disagree_to_pay_cred", tracker)
            dispatcher.utter_template("utter_thank_you", tracker)
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               flag=TIMEOUT_FLAG, delay_reason=decline_reason_disposition_id.get(intent),emi_flow="post_emi",sheet_name=sheet_name)
            return {"ask_delay_reason": value, "stop_conversation": "TRUE"}
        elif value == "decline_reason":
            dispatcher.utter_template("utter_disagree_to_pay_cred", tracker)
            dispatcher.utter_template("utter_thank_you", tracker)
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               flag=TIMEOUT_FLAG, delay_reason=decline_reason_disposition_id.get(intent),emi_flow="post_emi",sheet_name=sheet_name)
            return {"ask_delay_reason": value, "stop_conversation": "TRUE"}
        elif value == "+1":
            dispatcher.utter_template("utter_apology", tracker)
            dispatcher.utter_template("utter_confirm_again", tracker)
            return {"ask_delay_reason": None, "trail_count": get_trail_count(tracker)}
        elif value == "+2":
            total_loans=get_total_loan(tracker)
            total_emi_amount,due_date=get_emi_details(tracker,total_loans)
            if len(total_loans)>1:
                dispatcher.utter_template("utter_greet_multiple_cred",tracker,total_emi=str(total_emi_amount),no_of_loans=str(len(total_loans)))
            else:
                due_date=datetime.datetime.strptime(due_date,"%d-%m-%Y")
                due_date=due_date.strftime("%d %B %Y")
                dispatcher.utter_template("utter_greet_cred",tracker,monthly_emi=str(total_emi_amount),emi_date=due_date)
            dispatcher.utter_template("utter_thank_you", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="PTP", flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
            return {"trail_count": None, "ask_delay_reason": value}
        elif value == "partial_payment":
            dispatcher.utter_template("utter_send_payment_link", tracker, monthly_emi=500)
            # TODO send payment link with amount
            dispatcher.utter_template("utter_thank_you", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="Partial Payment Requested", flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
            return {"trail_count": None, "ask_delay_reason": value}
        elif value == "inform_payment_done":
            dispatcher.utter_template("utter_bye", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        return {"ask_delay_reason": None}

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[EventType]:
        return [FollowupAction("action_listen"), AllSlotsReset()]