import csv

test_cases = {}
FLOW_NAME = "Flow name"
INTENT = "Intent"
USER_INPUT = "User"
TEMPLATE = "Templates"
CUSTOM_CODE = "Custom code"
DISPOSITION_ID = "Disposition ID"


def store_call_bot_output(message=None, bot_response=None, sender_id=None):
    if message == "/start":
        if sender_id:
            test_cases[sender_id] = []
        return
    if message == "/remove":
        test_cases.pop(sender_id)
        return
    if message is None:
        test_case = {}
        if "nlu_data" in bot_response:
            if "intent" in bot_response["nlu_data"] and "name" in bot_response["nlu_data"]["intent"]:
                test_case[INTENT] = bot_response["nlu_data"]["intent"]["name"]
            if "text" in bot_response["nlu_data"]:
                test_case[USER_INPUT] = bot_response["nlu_data"]["text"]

        if "custom" in bot_response:
            if "status" in bot_response["custom"]:
                test_case[CUSTOM_CODE] = bot_response["custom"]["status"]
            if "disposition_id" in bot_response["custom"]:
                test_case[DISPOSITION_ID] = bot_response["custom"]["disposition_id"]

        bot_templates = []
        if "data" in bot_response and len(bot_response["data"]) > 0:
            for template in bot_response["data"]:
                if "template_name" in template:
                    bot_templates.append(template["template_name"])
        bot_templates = ".".join(bot_templates)
        test_case[TEMPLATE] = bot_templates

        for item in [INTENT, USER_INPUT, TEMPLATE, CUSTOM_CODE, DISPOSITION_ID]:
            if item not in test_case:
                test_case[item] = ""
        if "sender_id" in bot_response and bot_response["sender_id"] in test_cases:
            test_cases[bot_response["sender_id"]].append(test_case)
        else:
            test_cases[bot_response["sender_id"]] = []
            test_cases[bot_response["sender_id"]].append(test_case)
        return
    if message == "/store":
        formatted_test_cases = []
        for sample_test_case in test_cases:
            if sample_test_case != sender_id:
                continue
            import uuid
            _sender_id = str(uuid.uuid4())
            for item in test_cases[sample_test_case]:
                formatted_test_cases.append(
                    [_sender_id, item[INTENT], item[USER_INPUT], item[TEMPLATE], item[CUSTOM_CODE],
                     item[DISPOSITION_ID]])
            formatted_test_cases.append([])
        print("formatted test cases ::", formatted_test_cases)

        try:
            with open('test_cases_formatted.csv', 'r+', newline='') as file:
                data = csv.reader(file)
                writer = csv.writer(file)
                if len(list(data)) == 0:
                    writer.writerows([["Flow name", "Intent", "User", "Templates", "Custom code", "Disposition ID"]])
                    writer.writerows(formatted_test_cases)
                else:
                    writer.writerows(formatted_test_cases)
        except IOError:
            with open('test_cases_formatted.csv', 'w+', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([["Flow name", "Intent", "User", "Templates", "Custom code", "Disposition ID"]])
                writer.writerows(formatted_test_cases)
        test_cases.pop(sender_id)
