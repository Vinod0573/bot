
from actions.utils.common_imports import *
from actions.utils.helper import *


import time
import handle_bulk_data

helper = Helper()


class ActionGreet(Action):

    def name(self):
        return 'action_greet'

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message.get("intent").get("name")
        greet_count = tracker.get_slot("greet_count")
        user_message=tracker.latest_message.get("text")
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        if intent == "greet":
            requested_slot = tracker.get_slot(REQUESTED_SLOT)
            if greet_count > 2:
                dispatcher.utter_template("utter_agent_will_connect_common", tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                   user_message=user_message,flag=TIMEOUT_FLAG,disposition_id="MULTIPLE HELLO",sheet_name=sheet_name,emi_flow=emi_flow)
                return [FollowupAction("action_listen"), AllSlotsReset()]
            return_values = []
            if greet_count > 0:
                print("inside greet_count == 0")
                main_flow = tracker.active_form.get("name")
                print("main_flow",main_flow)
                if main_flow != "user_confirmation_form":
                    return_values.append(SlotSet("main_flow", main_flow))
                current_slot = tracker.get_slot(REQUESTED_SLOT)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="greet",sheet_name=sheet_name,emi_flow=emi_flow)
                return [FollowupAction("user_confirmation_form"), SlotSet(REQUESTED_SLOT, None),
                        SlotSet("current_slot", current_slot),
                        SlotSet("greet_count", greet_count + 1)] + return_values
            trail_count = tracker.get_slot("trail_count")
            if tracker.active_form.get("name") is not None and requested_slot == "availability_status" and \
                    trail_count is None:
                print("tracker.active_form.get() is not None")
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="greet",sheet_name=sheet_name,emi_flow=emi_flow)
                dispatcher.utter_template("utter_ask_capability_common", tracker)
            else:
                print("tracker.active_form.get() is not None -2")
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="greet",sheet_name=sheet_name,emi_flow=emi_flow)
                dispatcher.utter_template('utter_ask_capability_common', tracker)
            print("tracker.active_form.get() is not None -3")
            return get_return_values(tracker) + [SlotSet("greet_count", greet_count + 1)]
        else:
            dispatcher.utter_template('utter_default_common', tracker)
            send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Not understood",sheet_name=sheet_name,emi_flow=emi_flow)
        return get_return_values(tracker)


class ActionWait(Action):

    def name(self):
        return "action_wait"

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        wait_count=tracker.get_slot("wait_count")
        time_diff=0
        if wait_count <2:
            dispatcher.utter_template("utter_customer_informed_wait", tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Wait",flag=WAIT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
            return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                FollowupAction(tracker.active_form.get("name")),
                SlotSet("wait_count",wait_count+1)
            ]
        else:
            dispatcher.utter_template('utter_agent_will_connect_common', tracker)
            user_message=tracker.latest_message.get("text")
            # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Human Handoff",sheet_name=sheet_name,emi_flow=emi_flow)
            return [FollowupAction("action_listen"), AllSlotsReset()]


class ActionBye(Action):

    def name(self):
        return "action_bye"

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_bye_common", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,disposition_id="bye",sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"), AllSlotsReset()]


class ActionCallLater(Action):
    def name(self):
        return 'action_call_later'

    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y")
        print("due_date...in later",due_date)
        ptp_date = due_date.strftime("%d %B %Y")
        print("ptp_date...in later",ptp_date)
        if emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_not_available_to_talk_2_reminder", tracker,EMI_Amount = total_emi_amount,monthly_emi_date = ptp_date)
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_not_available_to_talk", tracker,EMI_Amount = total_emi_amount)
        else:
            dispatcher.utter_template("utter_not_avail_talk", tracker,monthly_emi = total_emi_amount,monthly_emi_date = ptp_date)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                           disposition_id="Callback", flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen")]


class ActionThankYou(Action):

    def name(self):
        return "action_thank_you"

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_user_said_thank_you_common", tracker)
        send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Thank",sheet_name=sheet_name,emi_flow=emi_flow)
        return get_return_values(tracker)


class ActionChangeLanguage(Action):
    def name(self):
        return "action_change_language"

    def run(self, dispatcher, tracker, domain):
        change_language_count = tracker.get_slot("change_language_count")
        # Language_order = [hindi,tamil,kannada,telugu,malayalam,bengali,punjabi,marathi,english,gujarati]
        supported_languages=[
                            "हिंदी","तमिल","कन्नड़","कनाडा","तेलुगू","तेलुगु","मलयालम","बंगाली","मराठी","इंग्लिश","बांगला","बांग्ला","तेलगू","बंगला",
                            "ஹிந்தி","தமிழ்","கன்னடம்","தெலுங்கு","மலையாளம்","பெங்காலி","மராத்தி","பஞ்சாபி","இங்கிலீஷ்","கன்னடா","பங்கிலா","கன்னட","குஜராத்தி",
                            "ಹಿಂದಿ","ತಮಿಳು","ಕನ್ನಡ","ತೆಲುಗು","ಮಲಯಾಳಂ", "ತಮಿಳು","बेनाली","ತಮಿಳ್","ಬಾಂಗ್ಲಾ","ಮರಾಠಿ","ಪಂಜಾಬಿ","ಬೆಂಗಾಲಿ","ಇಂಗ್ಲಿಷ್",
                            "బెంగాలీ","మరాఠీ","పంజాబీ","హిందీ","తమిళం","కన్నడ","తెలుగు","ఇంగ్లీష్","బంగ్లా","తమిళ్","కనడ",
                            "తెలుగు","మలయాళం","ഹിന്ദി","തമിഴ്","കന്നഡ","തെലുങ്ക്","മലയാളം","പഞ്ചാബി","ഇംഗ്ലീഷ്","തെലുങ്കു","ബംഗ്ലാ","മറാത്ത","মালায়লাম",
                            "তামিল","তেলেগু","হিন্দি","কন্নড়","মালয়ালম","পাঞ্জাবি","মারাঠি","বাঙালি","ইংলিশ","ಮಲ್ಯಾಳಮ್","बेंगोली",
                            "ਤਾਮਿਲ","ਤੇਲੁਗੂ","ਹਿੰਦੀ","ਕੰਨੜ","ਮਲਿਆਲਮ","ਪੰਜਾਬੀ","ਮਰਾਠੀ","ਬੰਗਾਲੀ","અંગ્રેજી","ਅੰਗਰੇਜ਼ੀ","मलियालम","मल्यालम",
                            "तामिळ","तेलुगु","कन्नड","मल्याळम","बंगाली","કન્નડ","તેલુગુ","તમિલ","મલયાલમ","પંજાબી","મરાઠી","બંગાળી","पंजाबी",
                            "tamil","telugu","kannada","malayalam","hindi","bengali","marathi","punjabi","bangla","english","Punjabi",
                            "గుజరాతీ","ಗುಜರಾತಿ","ഗുജറാത്തി","गुजराती","গুজরাটি","ਗੁਜਰਾਤੀ","હિન્દી","બંગાલી","ਬੰਗਲਾ","মালায়ালাম"]
        if change_language_count <2:
            change_specific_language_count=tracker.get_slot("change_specific_language_count")
            text = tracker.latest_message.get("text")
            if text:
                text = text.lower()
            print("text:::::::::::::::", text)
            existed = 0
            for lan in supported_languages:
                if lan in text:
                    print("lan",lan)
                    existed += 1
            print("existed",existed)
            if existed >1 :
                print("existed",existed)
                dispatcher.utter_custom_json({"language_change": True})
                print("Coming here")
                send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Language change")
                dispatcher.utter_template("utter_language_preference_common",tracker)
                return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE"),SlotSet("change_language_count",change_language_count+1)]
            elif existed==1:
                if "தமிழ்" not in text and "ಕನ್ನಡ" not in text and "తెలుగు" not in text and "മലയാളം" not in text and "বাংলা" not in text and "ਪੰਜਾਬੀ" not in text and "ગુજરાતી" not in text:
                    if change_specific_language_count<1:
                        send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Language change")
                        dispatcher.utter_template("utter_confirm_language_support_common", tracker)
                        return [FollowupAction(tracker.active_form.get("name")),SlotSet("availability_status",None),SlotSet("payment_confirmation",None),SlotSet("default",None),SlotSet("ask_delay_reason",None),
                                SlotSet("trail_count",None),SlotSet("user_confirmation",None), SlotSet(REQUESTED_SLOT, None),SlotSet("change_specific_language_count",change_specific_language_count+1),SlotSet("change_language_count",change_language_count+2)]
                    else:
                        dispatcher.utter_template("utter_bye_common",tracker)
                        send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change")
                        return [FollowupAction("action_listen"),AllSlotsReset()]
                print("Coming Thereeeeeee")
                dispatcher.utter_template("utter_language_preference_common",tracker)
                return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE"),SlotSet("change_language_count",change_language_count+1)]
            else:
                dispatcher.utter_template("utter_language_preference_common", tracker)
                send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Language change")
                return [FollowupAction("action_listen"),AllSlotsReset()]
        else:
            dispatcher.utter_template("utter_bye_common",tracker)
            send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change")
            return [FollowupAction("action_listen"),AllSlotsReset()]

        # if "english" in text and "hindi" in text:
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE")]
        # if "हिंदी" in text and ("अंग्रेज़ी" in text or "इंग्लिश" in text):
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE")]
        # if "hindi" in text:
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen")]
        # if "english" in text or "हिंदी" in text:
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE")]
        # if "अंग्रेजी" in text or "इंग्लिश" in text:
        #     'क्या आप अंग्रेजी में बदल सकते हैं'
        #     print("this is working-----------------")
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen")]
        # other_languages = ["telugu", "tamil"]
        # for item in other_languages:
        #     if item in text.lower():
        dispatcher.utter_template("utter_apology_call_back_common", tracker, language=item)
        # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher, disposition_id="Language change")
        send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",sheet_name=sheet_name, emi_flow=emi_flow)
        return [FollowupAction("action_listen")]


# class ActionChangeLanguageFromEnglishToHindi(Action):
#     def name(self):
#         return "action_change_language_from_english_to_hindi"

#     def run(self, dispatcher, tracker, domain):
#         emi_flow=tracker.get_slot("emi_flow")
#         sheet_name=tracker.get_slot("sheet_name")
#         language_recheck = tracker.get_slot("language_recheck")
#         print("Language Recheck:",language_recheck)
#         if language_recheck:
#             main_flow = tracker.active_form.get("name")
#             current_slot = tracker.get_slot(REQUESTED_SLOT)
#             send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="English to Hindi",sheet_name=sheet_name,emi_flow=emi_flow)
#             return [FollowupAction("language_recheck_form"), SlotSet(REQUESTED_SLOT, None),
#                     SlotSet("main_flow", main_flow), SlotSet("current_slot", current_slot)]
#         send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Language change",sheet_name=sheet_name,emi_flow=emi_flow)
#         dispatcher.utter_template("utter_confirm_language_support_common", tracker)
#         return [FollowupAction("action_repeat")]


# class ActionChangeLanguageFromHindiToEnglish(Action):
#     def name(self):
#         return "action_change_language_from_hindi_to_english"

#     def run(self, dispatcher, tracker, domain):
#         sheet_name=tracker.get_slot("sheet_name")
#         emi_flow=tracker.get_slot("emi_flow")
#         language_recheck = tracker.get_slot("language_recheck")
#         print("**** Language Recheck:",language_recheck)
#         if language_recheck:
#             main_flow = tracker.active_form.get("name")
#             current_slot = tracker.get_slot(REQUESTED_SLOT)
#             send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Hindi to English",sheet_name=sheet_name,emi_flow=emi_flow)
#             return [FollowupAction("language_recheck_form"), SlotSet(REQUESTED_SLOT, None),
#                     SlotSet("main_flow", main_flow), SlotSet("current_slot", current_slot)]
#         send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Language change",sheet_name=sheet_name,emi_flow=emi_flow)
#         dispatcher.utter_template("utter_confirm_language_support_common", tracker)
#         return [FollowupAction("action_repeat")]


# class ActionLanguageChange(Action):
#     def name(self):
#         return "action_language_change"

#     def run(self, dispatcher, tracker, domain):
#         emi_flow=tracker.get_slot("emi_flow")
#         sheet_name=tracker.get_slot("sheet_name")
#         text = tracker.latest_message.get("text")
#         print("Language Text:",text)
#         if "hindi" in text:
#             dispatcher.utter_custom_json({"language_change": True})
#             send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",sheet_name=sheet_name,emi_flow=emi_flow)
#             return [FollowupAction("action_listen")]
#             pass
#         if "अंग्रेज़ी" in text or "इंग्लिश" in text:
#             pass
#         dispatcher.utter_message("Yes, i can change speak in")
#         send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",sheet_name=sheet_name,emi_flow=emi_flow)
#         return get_return_values(tracker)


# class ActionNoise(Action):
#     def name(self):
#         return "action_noise"

#     def run(self, dispatcher, tracker, domain):
#         timestamp = tracker.get_slot("timestamp")
#         if timestamp is None:
#             return [FollowupAction("action_listen")]
#         noise_count = tracker.get_slot("noise_count")
#         current_timestamp = time.time()
#         difference = current_timestamp - timestamp
#         print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", difference)
#         updated_time_limit = 60 - difference
#         send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Noise")
#         if int(updated_time_limit) > 0:
#             helper.send_conversation_flag(WAIT_FLAG, dispatcher, time_limit=int(updated_time_limit))
#             if int(noise_count) > 6:
#                 dispatcher.utter_template("utter_report_noise", tracker)
#                 return [FollowupAction("action_listen"), SlotSet("noise_count", 0)]
#             else:
#                 return [FollowupAction("action_listen"), SlotSet("noise_count", int(noise_count) + 1)]
#         else:
#             return [FollowupAction("action_no_message")]


class ActionDefault(Action):

    def name(self):
        return 'action_default'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        default_count=tracker.get_slot("default_count")
        print(default_count,"default_count-1")
        if default_count<2:
            dispatcher.utter_template('utter_default_common', tracker)
            send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Not understood",sheet_name=sheet_name,emi_flow=emi_flow)
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("default_count",default_count+1)
            ]
        else:
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
            send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Human handoff",sheet_name=sheet_name,emi_flow=emi_flow)
            return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionHumanHandOff(Action):
    def name(self):
        return 'action_human_handoff'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        dispatcher.utter_template('utter_general_queries_customer_care_common', tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        user_message=tracker.latest_message.get("text")
        # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Human Handoff",user_message=user_message,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"), AllSlotsReset()]


class ActionAskCapability(Action):

    def name(self):
        return 'action_ask_capability'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        dispatcher.utter_template("utter_ask_capability_common", tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="bot capability",sheet_name=sheet_name,emi_flow=emi_flow)
        return get_return_values(tracker)


class ActionNoMessage(Action):
    def name(self):
        return "action_no_message"

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
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
        print("No Response count:",no_response_count)
        if no_response_count is None:
            if tracker.active_form.get("name") is not None:
                dispatcher.utter_template("utter_idle_common", tracker)
                return [
                    SlotSet(REQUESTED_SLOT, None),
                    SlotSet("trail_count", get_trail_count(tracker)),
                    FollowupAction(tracker.active_form.get("name")),
                    SlotSet("no_response_count", 1)
                ]
            dispatcher.utter_template("utter_idle_common", tracker)
            return [FollowupAction("action_listen"), SlotSet("no_response_count", 1)]
        else:
            if no_response_count >= 2:
                dispatcher.utter_template("utter_idle_bye_common", tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message="no_message", flag=TIMEOUT_FLAG,disposition_id="No Response",sheet_name=sheet_name,emi_flow=emi_flow)
                return [FollowupAction("action_listen"), AllSlotsReset()]
            else:
                if tracker.active_form.get("name") is not None:
                    dispatcher.utter_template("utter_idle_common", tracker)
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="No Response",sheet_name=sheet_name,emi_flow=emi_flow)
                    return [
                        SlotSet(REQUESTED_SLOT, None),
                        SlotSet("trail_count", get_trail_count(tracker)),
                        FollowupAction(tracker.active_form.get("name")),
                        SlotSet("no_response_count", int(no_response_count) + 1)
                    ]
                dispatcher.utter_template("utter_idle_common", tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="No Response",sheet_name=sheet_name,emi_flow=emi_flow)
                return [FollowupAction("action_listen"), SlotSet("no_response_count", int(no_response_count) + 1)]


class ActionHumiliate(Action):

    def name(self):
        return 'action_humiliate'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template('utter_apology_common', tracker)
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="apology",sheet_name=sheet_name,emi_flow=emi_flow)
        return get_return_values(tracker)


class ActionCustomerCareGeneralIntents(Action):
    def name(self):
        return 'action_general_queries_customer_care'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        dispatcher.utter_template("utter_general_queries_customer_care_common", tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="general query",sheet_name=sheet_name,emi_flow=emi_flow)
        return get_return_values(tracker)


class ActionRepeat(Action):
    def name(self):
        return 'action_repeat'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        repeat_count=tracker.get_slot("repeat_count")
        if repeat_count<2:
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
                if data[idx]["timestamp"] >= timestamp_to_begin and data[idx]["timestamp"] <= timestamp_to_end:
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
                    print("Bot utter:",bot_utter)
                    template_name = {}
                    if 'template_name' in bot_utter[idx]['data']:
                        if bot_utter[idx]['data']["template_name"]!="utter_default_common" and bot_utter[idx]['data']["template_name"]!="utter_idle_common":
                            template_name = {"template_name": bot_utter[idx]['data']['template_name']}
                            dispatcher.utter_message(bot_utter[idx]["text"], **template_name)
                    # else:
                    #     dispatcher.utter_message(bot_utter[idx]["text"], **template_name)

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
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="repeat",sheet_name=sheet_name,emi_flow=emi_flow)
            # return the event list
            return [UserUtteranceReverted(),SlotSet("repeat_count",repeat_count+1)]
        main_flow = tracker.active_form.get("name")
        current_slot = tracker.get_slot(REQUESTED_SLOT)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="repeat",sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("user_confirmation_form"), SlotSet(REQUESTED_SLOT, None),SlotSet("current_slot", current_slot), SlotSet("main_flow",main_flow)]


class ActionLateFees(Action):

    def name(self):
        return 'action_late_fees'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask late fees", flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionWillPayLateFees(Action):
    
    def name(self):
        return 'action_will_pay_late_fee'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="will pay late fees", flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionAskInterestRate(Action):

    def name(self):
        return 'action_ask_interest_rate'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        # details = person_details[tracker.user_id if tracker.user_id in person_details else 'default']
        # monthly_emi_date, emi_interest, monthly_emi = details['monthly_emi_date'], details['emi_interest'], details[
        #     'monthly_emi']
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask interest rate", flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionTransferToAnotherHfc(Action):
    def name(self):
        return "action_transfer_to_another_hfc"
    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Transfer Account",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPrincipalAmountLeft(Action):

    def name(self):
        return 'action_principal_amount_left'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask principal amount left",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionTenureLeft(Action):

    def name(self):
        return 'action_tenure_left'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask tenure left",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionForeclosing(Action):
    
    def name(self):
        return 'action_foreclosing_through_own_funds'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="foreclosing through own funds",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionChangeAccount(Action):
    
    def name(self):
        return 'action_change_account_for_deduction'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="change account for deduction",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionVehicleSeized(Action):
    def name(self):
        return 'action_vehicle_seized'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="vehicle seized",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class MoratoriumPeriod(Action):

    def name(self):
        return 'action_moratorium_period'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask moratorium period",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ChangeEmiDate(Action):

    def name(self):
        return 'action_change_emi_due_date'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="change emi due date",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ReduceEmi(Action):
    def name(self):
        return 'action_reduce_emi'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask reduce emi",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionAskNextDueDate(Action):
    def name(self):
        return 'action_next_due_date'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask next due date",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionAskBalanceOrPaymentTillNow(Action):
    def name(self):
        return 'action_balance_payment'

    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        emi_flow=tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask balance payment",flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionInformPaymentDone(Action):
    def name(self):
        return 'action_inform_payment_done'
        
    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        dispatcher.utter_template("utter_bye_common", tracker)
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="Paid", flag=TIMEOUT_FLAG, sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"), AllSlotsReset()]


class ActionAskEmiAmount(Action):
    def name(self):
        return 'action_ask_emi_amount'
    def run(self, dispatcher, tracker, domain):
        sheet_name=tracker.get_slot("sheet_name")
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        # try:
        #     due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        # except:
        #     due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%y")
        # ptp_date = due_date.strftime("%d %B %Y")
        total_loans = tracker.get_slot("total_loans")
        if len(total_loans)>1:
            dispatcher.utter_template("utter_inform_outstanding_ml_common",tracker,total_amount=total_emi_amount,EMI_Amount=total_emi_amount,no_of_loans=str(len(total_loans)))
        else:
            # due_date=datetime.datetime.strptime(due_date[0],"%d/%m/%Y")
            # due_date=due_date.strftime("%d %b %Y")
            dispatcher.utter_template("utter_inform_outstanding_common",tracker,EMI_Amount=total_emi_amount,total_amount=total_emi_amount)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask emi amount",flag=DEFAULT_FLAG, sheet_name=sheet_name,emi_flow=emi_flow)
        return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                FollowupAction(tracker.active_form.get("name")),
            ]


class ActionAskDueDate(Action):
    def name(self):
        return 'action_ask_emi_due_date'

    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        due_date=due_date.strftime("%d %B %Y")
        dispatcher.utter_template("utter_inform_past_payment_date_common",tracker,EMI_Date=due_date)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask due date",flag=DEFAULT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return get_return_values(tracker)
class ActionInformHaveBalance(Action):
    def name(self):
        return "action_inform_have_balance"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_agree_to_pay",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="Inform have balance")
        return [FollowupAction("action_listen"),AllSlotsReset()]
class ActionMedicalIssue(Action):
    def name(self):
        return "action_medical_issue"
    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_medical_reson_post_due",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_medical_reason_reminder",tracker)
        else:
            dispatcher.utter_template("utter_disagree_to_pay_reason_medical",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="medical issue",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]
class ActionFamilyIssue(Action):
    def name(self):
        return "action_family_dispute_issue"
    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_not_accepted_reason_post_due",tracker)
        else:
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="family dispute",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPropertyDispute(Action):
    def name(self):
        return "action_property_dispute"
    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        if emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_reason_accepted_reminder",tracker)
        else:
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="property dispute",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionAskNextDueDate(Action):
    def name(self):
        return 'action_ask_next_due_date'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_general_queries_customer_care_common", tracker)
        dispatcher.utter_template("utter_bye_common",tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="next due date", flag=TIMEOUT_FLAG)
        return [FollowupAction("action_listen")]

class ActionThirdPartyContact(Action):
    def name(self):
        return 'action_third_party_contact'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_agent_will_connect_common", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="third party contact", flag=TIMEOUT_FLAG)
        return[FollowupAction("action_listen")]

class ActionPayViaAgent(Action):
    def name(self):
        return "action_pay_via_agent"
    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")   
        print("The total emi amount",total_emi_amount)                  
        if emi_flow =="post_due_0_7":
            dispatcher.utter_template("utter_accepted_ptp_post_due",tracker,monthly_emi=total_emi_amount)
        elif emi_flow =="PTP-Reminder":
            dispatcher.utter_template("utter_general_queries_customer_care_common",tracker,monthly_emi=total_emi_amount)
        else:
            dispatcher.utter_template("utter_agree_to_pay",tracker)

        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="pay via agent",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPayViaStore(Action):
    def name(self):
        return "action_pay_via_store"
    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")   
        print("The total emi amount",total_emi_amount)                  
        if emi_flow =="post_due_0_7":
            dispatcher.utter_template("utter_idle_common",tracker)
        elif emi_flow =="PTP-Reminder":
            dispatcher.utter_template("utter_general_queries_customer_care_common",tracker,monthly_emi=total_emi_amount)    
        else:
            dispatcher.utter_template("utter_agree_to_pay",tracker)

        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="pay via store",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPayBranch(Action):
    def name(self):
        return "action_pay_via_branch"
    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")                 
        if emi_flow =="post_due_0_7":
            dispatcher.utter_template("utter_accepted_ptp_post_due",tracker,monthly_emi=total_emi_amount)
        elif emi_flow =="PTP-Reminder":
            dispatcher.utter_template("utter_general_queries_customer_care_common",tracker,monthly_emi=total_emi_amount)
        else:
            dispatcher.utter_template("utter_agree_to_pay",tracker)

        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="pay via branch",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPayViaOnline(Action):
    def name(self):
        return "action_pay_via_online"
    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")                    
        if emi_flow =="post_due_0_7":
            dispatcher.utter_template("utter_accepted_ptp_post_due",tracker,monthly_emi=total_emi_amount)
        elif emi_flow =="PTP-Reminder":
            dispatcher.utter_template("utter_general_queries_customer_care_common",tracker,monthly_emi=total_emi_amount)    
        else:
            dispatcher.utter_template("utter_agree_to_pay",tracker)

        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="pay via online",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionAskPaymentLink(Action):
    def name(self):
        return "action_ask_payment_link"
    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        total_emi_amount=tracker.get_slot("total_emi_amount")                   
        if emi_flow =="post_due_0_7":
            dispatcher.utter_template("utter_accepted_ptp_post_due",tracker,monthly_emi=total_emi_amount)
        elif emi_flow =="PTP-Reminder":
            dispatcher.utter_template("utter_agree_to_pay_2_reminder",tracker,monthly_emi=total_emi_amount)
        else:
            dispatcher.utter_template("utter_agree_to_pay",tracker,monthly_emi=total_emi_amount)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="ask payment link",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionSalaryIssue(Action):
    def name(self):
        return "action_salary_issue"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        sheet_name=tracker.get_slot("sheet_name")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_not_accepted_reason_post_due",tracker)
        # elif emi_flow == "PTP-Reminder":
        #     dispatcher.utter_template("utter_reason_unaccepted_reminder",tracker)   
        else:
            dispatcher.utter_template("utter_reason_unaccepted_reminder",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="salary issue",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionTechnicalIssue(Action):
    def name(self):
        return "action_technical_issue"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        print("The emi flow in technical issue is ",emi_flow)
        sheet_name=tracker.get_slot("sheet_name")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "pre_emi":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="human handoff",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionCycleDateIssue(Action):
    def name(self):
        return "action_cycle_date_issue"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        sheet_name=tracker.get_slot("sheet_name")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="cycle date issue",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionDeathInFamily(Action):
    def name(self):
        return "action_death_in_family"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        print("The emi flow in technical issue is ",emi_flow)
        sheet_name=tracker.get_slot("sheet_name")
        if emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_reason_unaccepted_reminder",tracker)
        else:
            dispatcher.utter_template("utter_disagree_to_pay_reason_medical",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="death in family",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionCheckBounce(Action):
    def name(self):
        return "action_check_bounce"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        print("The emi flow in technical issue is ",emi_flow)
        sheet_name=tracker.get_slot("sheet_name")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "pre_emi":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        else:
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="human handoff",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionBranchIssue(Action):
    def name(self):
        return "action_branch_issue"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        print("The emi flow in technical issue is ",emi_flow)
        sheet_name=tracker.get_slot("sheet_name")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "pre_emi":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        else:
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="human handoff",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionAccountProblem(Action):
    def name(self):
        return "action_account_problem"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        print("The emi flow in technical issue is ",emi_flow)
        sheet_name=tracker.get_slot("sheet_name")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "pre_emi":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        else:
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="human handoff",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionAppNotWorking(Action):
    def name(self):
        return "action_app_not_working"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        print("The emi flow in technical issue is ",emi_flow)
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "pre_emi":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        else:
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="human handoff",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionInsufficientFunds(Action):
    def name(self):
        return "action_insufficient_funds"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        print("The emi flow in technical issue is ",emi_flow)
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "pre_emi":
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_reason_unaccepted_reminder",tracker)
        else:
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="human handoff",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionJobLosslIssue(Action):
    def name(self):
        return "action_job_loss"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_not_accepted_reason_post_due",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_reason_unaccepted_reminder",tracker)
        else:
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="job loss",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPersonalIssue(Action):
    def name(self):
        return "action_personal_issue"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_not_accepted_reason_post_due",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_reason_unaccepted_reminder",tracker)
        else:
            dispatcher.utter_template("utter_reason_unaccepted_reminder",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="personal issue",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionBusinessIssue(Action):
    def name(self):
        return "action_business_loss_issue"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        if emi_flow == "post_due_0_7":
            dispatcher.utter_template("utter_not_accepted_reason_post_due",tracker)
        elif emi_flow == "PTP-Reminder":
            dispatcher.utter_template("utter_reason_unaccepted_reminder",tracker)
        else:
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="business issue",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionInformWrongInfo(Action):
    def name(self):
        return "action_inform_wrong_info"
    def run(self, dispatcher, tracker, domain):
        due_date=tracker.get_slot("due_date")
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        total_emi_amount=tracker.get_slot("total_emi_amount")
        due_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
        ptp_date = due_date.strftime("%d %B %Y")
        dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="wrong info",emi_flow=emi_flow,sheet_name=sheet_name)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionInitialMessage(Action):
    def name(self):
        return "action_initial_message"
    def run(self,dispatcher,tracker,domain):
        # total_loans=get_total_loan(tracker)
        # total_emi_amount,due_date,sheet_name,emi_flow,URNNO,ReferenceNo=get_emi_details(tracker,total_loans)
        # print("The flow type",emi_flow)

        # if emi_flow =="pre_emi":
        #     return [FollowupAction("sriram_pre_emi_form")]
            
        # if emi_flow =="post_due_0_7":
        #     return [FollowupAction('post_emi_7_form')]
        
        # if emi_flow == "PTP-Reminder":
        #     return [FollowupAction('ptp_reminder_form')]
            
        # return [FollowupAction("sriram_pre_emi_form")]
        # if emi_flow == "post_due_0_7":
        #     return [FollowupAction('post_emi_7_form')]
        # if emi_flow == "post_due_7_15":
        #     return [FollowupAction('post_emi_20_form')]
        # if emi_flow == "post_due_15_20":
        #     return [FollowupAction('post_emi_20+_form')]
        # return [FollowupAction('post_emi_7_form')]
        # if emi_flow == "post_due_0_7":
        #     return [FollowupAction('post_emi_7_form')]
        sender_id = tracker.sender_id
        data = handle_bulk_data.detect_camapin(sender_id)
        
        print("sender_id >>>",sender_id)
        print("entering here and data is",data)
        
        if data == "yes" or data == None:
            print("Inside the sheet reading function:",data)
            total_loans=get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,URNNO,loan_id,employee_name,language,last_unpaid_emi_date,count_of_days=get_emi_details(tracker,total_loans)
            print("due_date>>>>>>>",due_date)
            print("total_emi_amount,due_date,sheet_name,emi_flow,URNNO,loan_id,employee_name,language,last_unpaid_emi_date,count_of_days",total_emi_amount,due_date,sheet_name,emi_flow,URNNO,loan_id,employee_name,language,last_unpaid_emi_date,count_of_days)
            total_loans = len(total_loans)
        else:
            user_details=get_user_details_redis(tracker)
            total_emi_amount = user_details.get("total_emi")
            due_date = user_details.get("due_date")
            sheet_name = user_details.get("sheet_name")
            emi_flow=user_details.get("emi_flow")
            URNNO=user_details.get("URNNO")
            loan_id=user_details.get("loan_id")
            employee_name=user_details.get("employee_name")
            language=user_details.get("language")
            # account_no=user_details.get("account_no")
            last_unpaid_emi_date=user_details.get("last_unpaid_emi_date")
            count_of_days=user_details.get("count_of_days")
            total_loans=user_details.get("total_loans")
        print("the emi flow is ***********************",emi_flow)
        if emi_flow =="pre_emi":
            return [FollowupAction("sriram_pre_emi_updated_form"),SlotSet("total_emi_amount",str(total_emi_amount)),SlotSet("URNNO",str(URNNO)),SlotSet("loan_id",str(loan_id)),SlotSet("due_date",str(due_date)),SlotSet("sheet_name",str(sheet_name)),SlotSet("emi_flow",str(emi_flow)),SlotSet("language",str(language)),SlotSet("employee_name",str(employee_name)),SlotSet("last_unpaid_emi_date",str(last_unpaid_emi_date)),SlotSet("count_of_days",str(count_of_days)),SlotSet("total_loans",str(total_loans))]
            
        if emi_flow =="post_due_0_7":
            return [FollowupAction('post_emi_7_updated_form'),SlotSet("total_emi_amount",str(total_emi_amount)),SlotSet("URNNO",str(URNNO)),SlotSet("loan_id",str(loan_id)),SlotSet("due_date",str(due_date)),SlotSet("sheet_name",str(sheet_name)),SlotSet("emi_flow",str(emi_flow)),SlotSet("language",str(language)),SlotSet("employee_name",str(employee_name)),SlotSet("last_unpaid_emi_date",str(last_unpaid_emi_date)),SlotSet("count_of_days",str(count_of_days)),SlotSet("total_loans",str(total_loans))]
        
        if emi_flow == "PTP-Reminder":
            return [FollowupAction('ptp_reminder_updated_form'),SlotSet("total_emi_amount",str(total_emi_amount)),SlotSet("URNNO",str(URNNO)),SlotSet("loan_id",str(loan_id)),SlotSet("due_date",str(due_date)),SlotSet("sheet_name",str(sheet_name)),SlotSet("emi_flow",str(emi_flow)),SlotSet("language",str(language)),SlotSet("employee_name",str(employee_name)),SlotSet("last_unpaid_emi_date",str(last_unpaid_emi_date)),SlotSet("count_of_days",str(count_of_days)),SlotSet("total_loans",str(total_loans))]
        
        # if emi_flow == "post_due_20":
        #     return [FollowupAction('post_emi_20_updated_form'),SlotSet("total_emi_amount",str(total_emi_amount)),SlotSet("URNNO",str(URNNO)),SlotSet("loan_id",str(loan_id)),SlotSet("due_date",str(due_date)),SlotSet("sheet_name",str(sheet_name)),SlotSet("emi_flow",str(emi_flow)),SlotSet("language",str(language)),SlotSet("employee_name",str(employee_name)),SlotSet("last_unpaid_emi_date",str(last_unpaid_emi_date)),SlotSet("count_of_days",str(count_of_days)),SlotSet("total_loans",str(total_loans))]

        # if emi_flow == "post_emi":
        #     return [FollowupAction('post_emi_updated_form'),SlotSet("total_emi_amount",str(total_emi_amount)),SlotSet("URNNO",str(URNNO)),SlotSet("loan_id",str(loan_id)),SlotSet("due_date",str(due_date)),SlotSet("sheet_name",str(sheet_name)),SlotSet("emi_flow",str(emi_flow)),SlotSet("language",str(language)),SlotSet("employee_name",str(employee_name)),SlotSet("last_unpaid_emi_date",str(last_unpaid_emi_date)),SlotSet("count_of_days",str(count_of_days)),SlotSet("total_loans",str(total_loans))]
        return [FollowupAction("sriram_pre_emi_updated_form")]
        