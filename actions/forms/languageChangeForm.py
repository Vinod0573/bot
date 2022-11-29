import time

from actions.utils.common_imports import *
from actions.utils.helper import *

helper = Helper()


class LanguageChangeForm(FormAction):
    def name(self):  # type: () -> Text
        return "language_recheck_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        if stop_conversation == "TRUE":
            return []
        return ["language_confirm"]

    @staticmethod
    def _should_request_slot(tracker, slot_name):  # type: (Tracker, Text) -> bool
        """Check whether form action should request given slot"""
        return tracker.get_slot(slot_name) is None

    def slot_mappings(self):  # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        return {
            "language_confirm": [
                self.from_intent(intent="affirm", value="TRUE"),
                self.from_intent(intent="agree_to_proceed", value="TRUE"),
                self.from_intent(intent="agree_to_pay", value="TRUE"),
                self.from_intent(intent="deny", value="FALSE"),
                self.from_intent(intent="disagree_to_proceed", value="FALSE"),
                self.from_intent(intent="disagree_to_pay", value="FALSE"),
                self.from_intent(intent="inform_payment_delay_reason", value="FALSE"),
                self.from_intent(intent="pay_later", value="TRUE"),
                self.from_intent(intent="thankyou", value="TRUE"),
                self.from_intent(intent="bye", value="FALSE"),
                self.from_intent(intent="inform_pay_with_other_method", value="FALSE"),
                self.from_intent(intent="inform_dont_have_payment_link", value="TRUE"),
                self.from_intent(intent="inform_dont_have_sms", value="TRUE"),
                self.from_intent(intent="ask_payment_link", value="TRUE"),
                self.from_intent(intent="inform_issue_in_payment", value="TRUE"),
                self.from_intent(intent="inform_wrong_info", value="TRUE"),
                # self.from_intent(intent="inform_payment_done", value="inform_wrong_info"),
                self.from_intent(intent="inform_payment_going_on", value="TRUE"),
                self.from_intent(intent="how_to_pay", value="TRUE"),
                self.from_intent(intent="language_change", value="FALSE"),
            ],
        }

    def request_next_slot(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ):
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                if slot == "language_confirm":
                    dispatcher.utter_template("utter_language_check", tracker)
                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time())]

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[EventType]:
        language_confirm = tracker.get_slot("language_confirm")
        current_slot = tracker.get_slot("current_slot")
        main_flow = tracker.get_slot("main_flow")
        if language_confirm == "TRUE":
            return [FollowupAction(main_flow), SlotSet(current_slot, "TRUE")]
        else:
            dispatcher.utter_template("utter_first_case_inform_customer_care", tracker)
            helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher, disposition_id=language_issue)
            store_call_log(flow_name=main_flow, disposition_id=language_issue, tracker=tracker)
        return [FollowupAction("action_listen"), AllSlotsReset()]
