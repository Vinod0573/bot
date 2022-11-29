from actions.utils.common_imports import *
from actions.utils.helper import *


helper = Helper()


class ActionGreet(Action):

    def name(self):
        return 'action_greet'

    def run(self, dispatcher, tracker, domain):
        greet_count = tracker.get_slot("greet_count")
        if greet_count == 0 and tracker.active_form.get("name") is None:
            return [FollowupAction("pre_emi_form"), SlotSet("greet_count", greet_count + 1)]
        else:
            intent = tracker.latest_message.get("intent").get("name")
            if intent == "greet":
                requested_slot = tracker.get_slot(REQUESTED_SLOT)
                trail_count = tracker.get_slot("trail_count")
                greet_count = tracker.get_slot("greet_count")
                if greet_count > 3:
                    dispatcher.utter_template("utter_agent_will_connect", tracker)
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                       user_message="no_message",
                                                       disposition_id=customer_says_hello_only, flag=TIMEOUT_FLAG)
                    return [FollowupAction("action_listen"), AllSlotsReset()]
                return_values = []
                if greet_count > 0:
                    main_flow = tracker.active_form.get("name")
                    if main_flow != "user_confirmation_form":
                        return_values.append(SlotSet("main_flow", main_flow))
                    current_slot = tracker.get_slot(REQUESTED_SLOT)
                    return [FollowupAction("user_confirmation_form"), SlotSet(REQUESTED_SLOT, None),
                            SlotSet("current_slot", current_slot),
                            SlotSet("greet_count", greet_count + 1)] + return_values
                if tracker.active_form.get("name") is not None and requested_slot == "availability_status" and \
                        trail_count is None:
                    dispatcher.utter_template("utter_ask_capability", tracker)
                else:
                    dispatcher.utter_template('utter_greet_again', tracker)
                return get_return_values(tracker) + [SlotSet("greet_count", greet_count + 1)]
            else:
                dispatcher.utter_template('utter_default', tracker)
        return get_return_values(tracker)


class ActionWait(Action):

    def name(self):
        return "action_wait"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_customer_informed_wait", tracker)
        return get_return_values(tracker)


class ActionBye(Action):

    def name(self):
        return "action_bye"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_bye", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                           disposition_id=customer_informed_bye, flag=TIMEOUT_FLAG)
        return [FollowupAction("action_listen")]


class ActionThankYou(Action):

    def name(self):
        return "action_thank_you"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_user_said_thank_you", tracker)
        return get_return_values(tracker)


class ActionDefault(Action):

    def name(self):
        return 'action_default'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template('utter_default', tracker)
        return get_return_values(tracker)


class ActionCallLater(Action):
    def name(self):
        return 'action_call_later'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_call_later", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                           disposition_id=customer_informed_call_later, flag=TIMEOUT_FLAG)
        return [FollowupAction("action_listen")]


class ActionNoMessage(Action):
    def name(self):
        return "action_no_message"

    def run(self, dispatcher, tracker, domain):
        no_response_count = tracker.get_slot("no_response_count")
        latest_event = tracker.events

        previous_message_no_message = True
        user_message_flag = False
        for event in reversed(latest_event):
            if event["event"] == "user":
                if user_message_flag:
                    if event["text"] == "/no_message":
                        previous_message_no_message = False
                        break
                    else:
                        break
                if event["text"] == "/no_message":
                    user_message_flag = True
                    continue
                elif event["text"] == "/noise":
                    no_response_count = None
                    break

        if previous_message_no_message:
            no_response_count = None
        if no_response_count is None:
            if tracker.active_form.get("name") is not None:
                dispatcher.utter_template("utter_idle", tracker)
                return [
                    SlotSet(REQUESTED_SLOT, None),
                    SlotSet("trail_count", get_trail_count(tracker)),
                    FollowupAction(tracker.active_form.get("name")),
                    SlotSet("no_response_count", 1)
                ]
            dispatcher.utter_template("utter_idle", tracker)
            return [FollowupAction("action_listen"), SlotSet("no_response_count", 1)]
        else:
            if no_response_count >= 2:
                dispatcher.utter_template("utter_idle_bye", tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message="no_message",
                                                   disposition_id=customer_no_response, flag=TIMEOUT_FLAG)
                return [FollowupAction("action_listen"), AllSlotsReset()]
            else:
                if tracker.active_form.get("name") is not None:
                    dispatcher.utter_template("utter_idle", tracker)
                    return [
                        SlotSet(REQUESTED_SLOT, None),
                        SlotSet("trail_count", get_trail_count(tracker)),
                        FollowupAction(tracker.active_form.get("name")),
                        SlotSet("no_response_count", int(no_response_count) + 1)
                    ]
                dispatcher.utter_template("utter_idle", tracker)
                return [FollowupAction("action_listen"), SlotSet("no_response_count", int(no_response_count) + 1)]


class ActionHumiliate(Action):

    def name(self):
        return 'action_humiliate'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template('utter_apology', tracker)
        return get_return_values(tracker)


class ActionRepeat(Action):
    def name(self):
        return 'action_repeat'

    def run(self, dispatcher, tracker, domain):

        data = tracker.events  # all the events

        # store the timestamp of action_listen events in a list
        action_listens = []
        end_idx = 1
        start_idx = 2
        for idx in range(0, len(data)):
            if data[idx]["event"] == 'action' and data[idx]["name"] == 'action_listen':
                action_listens.append(data[idx]["timestamp"])

            # if data[idx]["event"] == 'action' and data[idx]["name"] == 'action_wait':
            #     print("YES")
            #     end_idx+=1
            #     start_idx+=1

        # print(action_listens)
        # print(len(action_listens), start_idx, end_idx)
        # defining timestamp range reproduce the utterances.
        timestamp_to_end = action_listens[len(action_listens) - end_idx]
        timestamp_to_begin = action_listens[len(action_listens) - start_idx]

        # store bot utterances within the timestamp range into a list
        bot_utter = []
        for idx in range(0, len(data)):
            if timestamp_to_begin <= data[idx]["timestamp"] <= timestamp_to_end:
                if data[idx]["event"] == 'bot':
                    bot_utter.append(data[idx])

        # dispatch the bot utterances stored in the 'bot_utter' list
        for idx in range(0, len(bot_utter)):
            if bot_utter[idx]["data"]["buttons"]:
                dispatcher.utter_button_message(bot_utter[idx]["text"], bot_utter[idx]["data"]["buttons"])
            elif bot_utter[idx]["data"]["elements"]:
                dispatcher.utter_custom_message(bot_utter[idx]["data"]["elements"])
            elif bot_utter[idx]["data"]["attachment"]:
                dispatcher.utter_attachment(bot_utter[idx]["data"]["attachment"])
            else:
                # text = bot_utter[idx]["text"]
                # if text != 'ठीक है | मैं होल्ड पर जा रही हूँ. कृपया, वापस आकर बताइए |':
                dispatcher.utter_message(bot_utter[idx]["text"])

        # creating a restart event
        restart = dict()
        restart['event'] = "restart"
        restart['timestamp'] = data[0]["timestamp"]

        # storing the restart event and then the bot utterances in an event list
        updated_events = []
        updated_events.append(restart)
        for idx in range(0, len(data)):
            if data[idx]["timestamp"] <= timestamp_to_end:
                updated_events.append(data[idx])

        # return the event list
        return [UserUtteranceReverted()]


class ActionCustomerCareGeneralIntents(Action):
    def name(self):
        return 'action_customer_care_general_intents'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_general_queries_customer_care", tracker)
        return get_return_values(tracker)


class ActionHumanHandOff(Action):
    def name(self):
        return 'action_human_handoff'

    def run(self, dispatcher, tracker, domain):
        human_handoff_count = tracker.get_slot("human_handoff_count")
        if human_handoff_count == 0:
            dispatcher.utter_template("utter_human_handoff", tracker)
            return get_return_values(tracker) + [SlotSet("human_handoff_count", human_handoff_count + 1)]
        if human_handoff_count != 0:
            dispatcher.utter_template("utter_agent_will_connect", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id=customer_asked_human_handoff, flag=TIMEOUT_FLAG)
            return [FollowupAction("action_listen"), AllSlotsReset()]
        return get_return_values(tracker)


class ActionAskDueDate(Action):
    def name(self):
        return 'action_ask_due_date'

    def run(self, dispatcher, tracker, domain):
        user_details = get_user_details(tracker)
        
        dispatcher.utter_template("utter_inform_reminder", tracker, monthly_emi=user_details.get("EMI Amount"),
                                  monthly_emi_date=user_details.get("Due date"))
        return get_return_values(tracker)

class ActionAskNextDueDate(Action):
    def name(self):
        return 'action_ask_next_due_date'

    def run(self, dispatcher, tracker, domain):
        user_details = get_user_details(tracker)
        dispatcher.utter_template("utter_general_queries_customer_care_common", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id=customer_asked_human_handoff, flag=TIMEOUT_FLAG)
        return[FollowupAction("action_listen")]




class ActionAskBalance(Action):
    def name(self):
        return 'action_ask_balance'

    def run(self, dispatcher, tracker, domain):
        user_details = get_user_details(tracker)
        dispatcher.utter_template("utter_inform_reminder", tracker, monthly_emi=user_details.get("EMI Amount"),
                                  monthly_emi_date=user_details.get("Due date"))
        return get_return_values(tracker) + [SlotSet("availability_status", "TRUE")]


class ActionAskCapability(Action):
    def name(self):
        return 'action_ask_capability'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_ask_capability", tracker)
        return get_return_values(tracker)