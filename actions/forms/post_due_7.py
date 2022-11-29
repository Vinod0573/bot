import datetime
import time
from datetime import timedelta, date
from actions.utils.common_imports import *
from actions.utils.helper import *

helper = Helper()


class AvailFinancePostEMI(FormAction):
    def name(self):  # type: () -> Text
        return "post_emi_7_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        payment_confirmation = tracker.get_slot("payment_confirmation")
        availability_status=tracker.get_slot("availability_status")
        if stop_conversation == "TRUE":
            return []
        # if payment_confirmation == "ask_partial_payment":
        #     return ["availability_status", "payment_confirmation", "partial_payment_status"]
        if payment_confirmation=="decline" or payment_confirmation=="ask_delay_reason":
            return ["ask_delay_reason"]
        if availability_status == "ask_delay_reason":
            return ["ask_delay_reason"]
        if availability_status=="confirm" or availability_status=="payment_confirmation":
            return ['payment_confirmation']
        return ["availability_status"]

    def get_delay_reason(self, value=None):
        return [
            self.from_intent(intent="business_loss", value=value),
            self.from_intent(intent="cycle_date_issue", value=value),
            self.from_intent(intent="insufficient_funds", value=value),
            self.from_intent(intent="job_loss", value=value),
            self.from_intent(intent="salary_issue",value=value),
            self.from_intent(intent="family_issue",value=value),
            self.from_intent(intent="family_dispute", value=value),
            # self.from_intent(intent="foreclosing_through_own_funds", value=value),
            self.from_intent(intent="branch_issue", value=value),
            self.from_intent(intent="account_not_working", value=value),
            # self.from_intent(intent="change_account_for_deduction", value=value),
            self.from_intent(intent="personal_issue",value=value)
        ]

    def slot_mappings(self):  # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        return {
            "availability_status": [
                self.from_intent(intent="affirm", value="TRUE"),
                self.from_intent(intent = "inform",value = "TRUE"),
                self.from_intent(intent="agree_to_proceed", value="TRUE"),
                # self.from_intent(intent = "pay_online",value = "TRUE"),
                self.from_intent(intent="deny", value="FALSE"),
                self.from_intent(intent="disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent="agree_to_pay", value="TRUE"),
                self.from_intent(intent="ask_partial_payment", value="FALSE"),
                self.from_intent(intent="disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "ask_payment_link",value = "TRUE"),
                # self.from_intent(intent = "pay_online",value = "TRUE"),
                # self.from_intent(intent = "pay_via_branch",value = "TRUE"),

            ] + self.get_delay_reason(value="decline_reason"),
            "payment_confirmation": [
                self.from_intent(intent="affirm", value="TRUE"),
                self.from_intent(intent = "inform",value = "TRUE"),
                self.from_intent(intent="agree_to_proceed", value="TRUE"),
                self.from_intent(intent="agree_to_pay", value="TRUE"),
                # self.from_intent(intent = "pay_online",value = "TRUE"),
                self.from_intent(intent = "ask_payment_link",value = "TRUE"),
                # self.from_intent(intent = "pay_online",value = "TRUE"),
                # self.from_intent(intent = "pay_via_branch",value = "TRUE"),
                self.from_intent(intent="deny", value="FALSE"),
                self.from_intent(intent="disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent="ask_partial_payment", value="FALSE"),
                self.from_intent(intent="disagree_to_pay", value="FALSE"),
            ] + self.get_delay_reason(value="decline_reason"),
            "ask_delay_reason": [
                self.from_intent(intent="affirm", value="+1"),
                self.from_intent(intent="agree_to_proceed", value="+1"),
                self.from_intent(intent = "inform",value = "TRUE"),
                self.from_intent(intent="agree_to_pay", value="+1"),
                self.from_intent(intent="deny", value="FALSE"),
                self.from_intent(intent="disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent="disagree_to_pay", value="FALSE"),
                self.from_intent(intent="ask_partial_payment", value="FALSE"),
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
                total_loans=get_total_loan(tracker)
                print("The total loans",total_loans)
                total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo=get_emi_details(tracker,total_loans)
                print("total_emi_amount,due_date,sheet_name,emi_flow",total_emi_amount,due_date,sheet_name,emi_flow)
                print("total_loans",total_loans)
                print("coming here -1")
                if slot == "availability_status":
                    # print("Entering insideavailability_status, ",trail_count)
                    if trail_count is None:
                        day_time = helper.get_daytime()
                        trail_count=0
                        # dispatcher.utter_template('utter_ask_capability', tracker, day_time=day_time)
                        if len(total_loans)>1:
                            print("The total loans",len(total_loans))
                            dispatcher.utter_template("utter_greet_ml_b_post_due",tracker,total_amount=str(total_emi_amount),no_of_loans=str(len(total_loans)))
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="pic",sheet_name=sheet_name,emi_flow=emi_flow)
                        else:
                            due_date=datetime.datetime.strptime(due_date[0],"%d-%m-%Y")
                            due_date=due_date.strftime("%d %B %Y")
                            print("Updated due date:",due_date)
                            dispatcher.utter_template("utter_greet_b_post_due",tracker,EMI_Amount=str(total_emi_amount))
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="pic",sheet_name=sheet_name,emi_flow=emi_flow)
                        return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),SlotSet("timestamp", time.time()),SlotSet("sheet_name",sheet_name),SlotSet("emi_flow",emi_flow),
                                SlotSet("trail_count",trail_count+1)]
                    else:
                        dispatcher.utter_template("utter_repeat_ask_payment_1_common", tracker)
                        return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot)]
                if slot=="payment_confirmation":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_persue_to_pay_post_due",tracker)
                        return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),SlotSet("timestamp", time.time()),SlotSet("sheet_name",sheet_name),SlotSet("emi_flow",emi_flow),
                                SlotSet("trail_count",trail_count+1)]
                    else:
                        dispatcher.utter_template("utter_repeat_ask_payment_1_common",tracker)
                if slot == "ask_delay_reason":
                    dispatcher.utter_template("utter_ask_reason_post_due", tracker)
                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time()),SlotSet("sheet_name",sheet_name),SlotSet("emi_flow",emi_flow)]

    @staticmethod
    def validate_availability_status(
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ):
        user_message = tracker.latest_message.get("text")
        sheet_name=tracker.get_slot("sheet_name")
        if value=="FALSE":
            print("Is it coming here1")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="rtp", flag=DEFAULT_FLAG,emi_flow="post_emi_0_7",sheet_name=sheet_name)
            return {"availability_status": "payment_confirmation","trail_count": None}
        elif value=="TRUE":
            entities = tracker.latest_message["entities"]
            now = datetime.datetime.now()
            # give_date = now.strftime("%d %B %Y")
            intent = tracker.latest_message.get("intent").get("name")

            if intent == "ask_payment_link":
                total_loans = get_total_loan(tracker)
                total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
                dispatcher.utter_template("utter_accepted_ptp_post_due",tracker,monthly_emi=total_emi_amount)
                dispatcher.utter_template("utter_bye_common",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    disposition_id="ask payment link",
                                                                    flag=TIMEOUT_FLAG,emi_flow="post_emi_0_7")
                                    # send_message(tracker)
                return {"availability_status": value, "stop_conversation": "TRUE", "trail_count": None}

            # user_details = get_user_details(tracker)
            if entities:
                print("here ****************1**")
                if intent in date_check_intents:
                    # TODO store the promise to pay date, and need to add payment link response also
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                no_of_days = given_date.date() - datetime.datetime.now().date()
                                print("no_of_days",no_of_days.days)
                                # print("no of days", no_of_days)
                                # if no_of_days.days:
                                #     return {"payment_confirmation": "ask_partial_payment", "trail_count": None}
                                if no_of_days.days==0:
                                    total_loans = get_total_loan(tracker)
                                    total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_accepted_ptp_post_due",tracker,monthly_emi=total_emi_amount)
                                    # dispatcher.utter_template("utter_bye_common",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG, ptp_date=given_date,emi_flow="post_emi_0_7",sheet_name=sheet_name)
                                    # send_message(tracker)
                                    return {"availability_status": value, "stop_conversation": "TRUE", "trail_count": None}
                                elif no_of_days.days<2:
                                    given_date = given_date.strftime("%d %B %Y")
                                    total_loans = get_total_loan(tracker)
                                    total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
                                    dispatcher.utter_template("utter_accepted_ptp_post_due",tracker,monthly_emi=total_emi_amount)
                                    # dispatcher.utter_template("utter_bye_common",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG, ptp_date=given_date,emi_flow="post_emi_0_7",sheet_name=sheet_name)
                                    # send_message(tracker)
                                    return {"availability_status": value, "stop_conversation": "TRUE", "trail_count": None}
                                else:
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="PTP",
                                                                    flag=DEFAULT_FLAG, ptp_date=given_date,emi_flow="post_emi_0_7",sheet_name=sheet_name)
                                    # send_message(tracker)
                                    return {"availability_status": "confirm", "trail_count": None}
                        else:
                            # dispatcher.utter_template("utter_pay_today_post_due8_15",tracker,ptp_day=given_date)
                            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                                disposition_id="agree to pay", flag=DEFAULT_FLAG,emi_flow="post_emi_0_7",sheet_name=sheet_name)
                            return {"availability_status": "confirm", "trail_count": None}
            else:
                print("here ******************")
                total_loans=get_total_loan(tracker)
                total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo=get_emi_details(tracker,total_loans)
                # dispatcher.utter_template("utter_persue_to_pay_post_due",tracker,emi_amount=total_emi_amount)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                                disposition_id="agree to pay", flag=DEFAULT_FLAG,emi_flow="post_emi_0_7",sheet_name=sheet_name)
                return {"availability_status": "confirm", "trail_count": None}
        elif value == "decline_reason":
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=DEFAULT_FLAG,emi_flow="post_emi_0_7",sheet_name=sheet_name)
            return {"availability_status": "confirm", "trail_count": None}
        
        if value == "disagree_to_proceed":
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
            user_details = get_user_details(tracker)
            dispatcher.utter_template("utter_not_available_to_talk", tracker,EMI_Amount = total_emi_amount)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="disagree to proceed",flag=TIMEOUT_FLAG,emi_flow="post_emi_0_7")
            return {"availability_status": value, "trail_count": None,"stop_conversation":"TRUE"}
        return {"availability_status": None}

    @staticmethod
    def validate_payment_confirmation(
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ):
        user_message = tracker.latest_message.get("text")
        sheet_name=tracker.get_slot("sheet_name")
        if value=="FALSE":
            print("Is it coming here2")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="rtp", flag=DEFAULT_FLAG,emi_flow="post_emi_0_7",sheet_name=sheet_name)
            return {"payment_confirmation": "ask_delay_reason","trail_count": None}
        elif value=="TRUE":
            print("Entering into True of payment conformation")
            entities = tracker.latest_message["entities"]
            # now = datetime.datetime.now()
            Date_req = date.today() + timedelta(days=1)
            give_date = Date_req.strftime("%d %B %Y")
            # now = datetime.datetime.now()
            # give_date = now.strftime("%d %B %Y")
            intent = tracker.latest_message.get("intent").get("name")
            # user_details = get_user_details(tracker)
            if intent == "ask_payment_link":
                total_loans = get_total_loan(tracker)
                total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
                dispatcher.utter_template("utter_accepted_ptp_post_due",tracker,monthly_emi=total_emi_amount)
                dispatcher.utter_template("utter_bye_common",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    disposition_id="ask payment link",
                                                                    flag=TIMEOUT_FLAG,emi_flow="post_emi_0_7")
                                    # send_message(tracker)
                return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}
            if entities:
                print("Entering into entities")
                if intent in date_check_intents:
                    # TODO store the promise to pay date, and need to add payment link response also
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                no_of_days = given_date.date() - datetime.datetime.now().date()
                                print("no of days ******", no_of_days.days)
                                # if no_of_days.days:
                                #     return {"payment_confirmation": "ask_partial_payment", "trail_count": None}
                                if no_of_days.days<2:
                                    print("Entering into less than 2")
                                    given_date = given_date.strftime("%d %B %Y")
                                    total_loans = get_total_loan(tracker)
                                    total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
                                    dispatcher.utter_template("utter_pay_today_post_due8_15",tracker,monthly_emi=total_emi_amount)
                                    # dispatcher.utter_template("utter_bye_common",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG, ptp_date=given_date,emi_flow="post_emi_0_7",sheet_name=sheet_name)
                                    # send_message(tracker)
                                    return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}
                                else:
                                    print("Enteriing into else part of the meeting")
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="PTP",
                                                                    flag=DEFAULT_FLAG, ptp_date=given_date,emi_flow="post_emi_0_7",sheet_name=sheet_name)
                                    # send_message(tracker)
                                    return {"payment_confirmation": "decline", "trail_count": None}
                        # else:
                        #     dispatcher.utter_template("utter_agree_to_pay_cred", tracker)
                        #     # send_message(tracker)
                        #     dispatcher.utter_template("utter_thank_you", tracker)
                        #     send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                        #                                     disposition_id="PTP", flag=TIMEOUT_FLAG,emi_flow="post_emi",sheet_name=sheet_name)
                        #     return {"availability_status": value, "stop_conversation": "TRUE", "trail_count": None}
            else:
                total_loans = get_total_loan(tracker)
                total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
                dispatcher.utter_template("utter_pay_today_post_due8_15",tracker,monthly_emi=total_emi_amount,emi_amount=total_emi_amount)
                # dispatcher.utter_template("utter_bye_common",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                user_message=user_message,
                                                disposition_id="PTP",
                                                flag=TIMEOUT_FLAG, emi_flow="post_emi_0_7",sheet_name=sheet_name,ptp_date=give_date)
                # send_message(tracker)
                return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}
        elif value == "decline_reason":
            dispatcher.utter_template("utter_not_accepted_reason_post_due", tracker)
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="post_emi_0_7",sheet_name=sheet_name)
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}
        

        if value == "disagree_to_proceed":
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
            user_details = get_user_details(tracker)
            dispatcher.utter_template("utter_not_available_to_talk", tracker,EMI_Amount = total_emi_amount)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="disagree to proceed",flag=TIMEOUT_FLAG,emi_flow="post_emi_0_7")
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}


    @staticmethod
    def validate_ask_delay_reason(
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ):  
        print("ENTERING INTO ASK DELAY  REASON")
        user_message = tracker.latest_message.get("text")
        sheet_name=tracker.get_slot("sheet_name")
        if value == "FALSE":
            dispatcher.utter_template("utter_not_accepted_reason_post_due", tracker)
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               flag=TIMEOUT_FLAG, delay_reason=decline_reason_disposition_id.get(intent),emi_flow="post_emi_0_7",sheet_name=sheet_name)
            return {"ask_delay_reason": value, "stop_conversation": "TRUE"}
        elif value == "decline_reason":
            dispatcher.utter_template("utter_not_accepted_reason_post_due", tracker)
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               flag=TIMEOUT_FLAG, delay_reason=decline_reason_disposition_id.get(intent),emi_flow="post_emi_0_7",sheet_name=sheet_name)
            return {"ask_delay_reason": value, "stop_conversation": "TRUE"}
        elif value == "+1":
            print("Entering into +1")
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
            dispatcher.utter_template("utter_pay_today_post_due8_15", tracker)
            # dispatcher.utter_template("utter_bye_common",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="agree to pay",
                                               flag=TIMEOUT_FLAG,emi_flow="post_emi_0_7",sheet_name=sheet_name)
            return {"ask_delay_reason": value, "stop_conversation": "TRUE"}

        if value == "disagree_to_proceed":
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo = get_emi_details(tracker,total_loans)
            user_details = get_user_details(tracker)
            dispatcher.utter_template("utter_not_available_to_talk", tracker,EMI_Amount = total_emi_amount)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="disagree to proceed",flag=TIMEOUT_FLAG,emi_flow="post_emi_0_7")
            return {"ask_delay_reason": value, "stop_conversation": "TRUE"}
        # return {"ask_delay_reason": None}

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[EventType]:
        return [FollowupAction("action_listen"), AllSlotsReset()]