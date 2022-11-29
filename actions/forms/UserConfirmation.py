import time

from actions.utils.common_imports import *
from actions.utils.helper import *

helper = Helper()


class UserConfirmationForm(FormAction):
    def name(self):  # type: () -> Text
        return "user_confirmation_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        if stop_conversation == "TRUE":
            return []
        return ["user_confirmation"]

    @staticmethod
    def _should_request_slot(tracker, slot_name):  # type: (Tracker, Text) -> bool
        """Check whether form action should request given slot"""
        return tracker.get_slot(slot_name) is None

    def get_delay_reason(self, value=None):
        return [
            self.from_intent(intent="business_loss", value=value),
            self.from_intent(intent="cycle_date_issue", value=value),
            self.from_intent(intent="insufficient_funds", value=value),
            self.from_intent(intent="job_loss", value=value),
            self.from_intent(intent="medical_issue", value=value),
            self.from_intent(intent="technical_issue", value=value),
            self.from_intent(intent="family_dispute", value=value),
            self.from_intent(intent="foreclosing_through_own_funds", value=value),
            self.from_intent(intent="branch_issue", value=value),
            self.from_intent(intent="account_not_working", value=value),
            self.from_intent(intent="change_account_for_deduction", value=value),
            self.from_intent(intent="transfer_to_another_hfc", value=value),
        ]

    def slot_mappings(self):  # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        return {
            "user_confirmation": [
                self.from_intent(intent="affirm", value="TRUE"),
                self.from_intent(intent="agree_to_proceed", value="TRUE"),
                self.from_intent(intent="deny", value="FALSE"),
                self.from_intent(intent="disagree_to_proceed", value="FALSE"),
                self.from_intent(intent="inform_wrong_info", value="TRUE"),
                self.from_intent(intent="agree_to_pay", value="TRUE"),
                self.from_intent(intent="disagree_to_pay", value="TRUE"),
            ] + self.get_delay_reason(value="TRUE"),
        }

    def request_next_slot(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ):
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                if slot == "user_confirmation":
                    dispatcher.utter_template("utter_audible_check_common", tracker)
                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time())]

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[EventType]:
        user_confirmation = tracker.get_slot("user_confirmation")
        current_slot = tracker.get_slot("current_slot")
        main_flow = tracker.get_slot("main_flow")
        if user_confirmation == "TRUE":
            # send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
            #                                    user_message="no_message",
            #                                    disposition_id="Hello only", flag=TIMEOUT_FLAG)
            return [FollowupAction(main_flow), SlotSet(current_slot, None),
                    SlotSet("trail_count", get_trail_count(tracker))]
        else:
            dispatcher.utter_template("utter_call_later_common", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                               user_message="no_message",
                                               disposition_id="Hello only", flag=TIMEOUT_FLAG)
            return [FollowupAction("action_listen"), AllSlotsReset()]
