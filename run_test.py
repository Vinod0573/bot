import itertools
import json
from collections import OrderedDict
import random
import os
import argparse
import time

import pandas as pd
import requests

FLOW_NAME = "Flow name"
INTENT = "Intent"
USER_INPUT = "User"
TEMPLATE = "Templates"
CUSTOM_CODE = "Custom code"
DISPOSITION_ID = "Disposition ID"

URL = "http://localhost:8000/navi/testcases"
columns_available_for_testing = None


def get_null_columns(test_data):
    remove_columns = []
    for item in test_data:
        is_not_contain_none_values = True
        for _item in test_data[item]:
            if not str(_item) == "nan" and _item is not None:
                is_not_contain_none_values = False
                break
        if is_not_contain_none_values:
            remove_columns.append(item)
    return remove_columns


def check_null_rows(test_input):
    is_null_row = True
    for item in test_input:
        if str(item) != "nan":
            is_null_row = False
    return is_null_row


def compare_two_list(list1, list2):
    for item1, item2 in itertools.zip_longest(list1, list2):
        if item1 != item2:
            return False
    return True


def preprocess_testing_data(data):
    null_rows = get_null_columns(data)

    # Remove null rows
    data.drop(null_rows, axis=1, inplace=True)
    global columns_available_for_testing
    columns_available_for_testing = data.columns.values.tolist()
    # print(columns_available_for_testing)

    x = data.iloc[:, :].values
    final_data = []
    for item in x:
        flow = OrderedDict()
        # Remove null rows
        if check_null_rows(item):
            continue
        for index in range(len(item)):
            flow[columns_available_for_testing[index]] = item[index]
        final_data.append(flow)

    final_testing_data = OrderedDict()
    flow_name = None

    for idx, item in enumerate(final_data):
        test_case = OrderedDict()
        for name, value in item.items():
            if name == FLOW_NAME and str(value) != "nan" and value is not None:
                flow_name = str(random.randint(1000000, 10000000000)) + "_" + str(value)
                continue
            elif name == "Flow name":
                continue
            if name == INTENT and str(value) == "eot":
                flow_name = None
                break
            if name == TEMPLATE:
                templates = "nan"
                if not str(value) == "nan" and value is not None:
                    templates = value.replace("\n", "").replace(" ", "").split(",")
                    if str() in templates:
                        templates.remove(str())
                value = templates
            test_case[name] = value
        if test_case:
            if not flow_name or flow_name is None:
                flow_name = str(random.randint(1000000, 10000000000)) + "_" + str("default")
            if flow_name in final_testing_data:
                final_testing_data.get(flow_name).append(test_case)
            else:
                final_testing_data[flow_name] = [test_case]
    print(json.dumps(final_testing_data, indent=2))
    return final_testing_data


def get_failed_test_case_template(item_name, test_value, bot_value):
    test_case = OrderedDict()
    test_case["item_name"] = item_name
    test_case["test_input"] = test_value
    test_case["bot_output"] = bot_value
    return test_case


def store_failed_test_cases(failed_test_cases: list, file_name="failed_stories.md"):
    if not os.path.isdir("test_results"):
        os.makedirs("test_results")
    with open("test_results/{}".format(file_name), "w+") as f:
        if len(failed_test_cases) == 0:
            f.write("<!-- All stories passed -->")
        else:
            formatted_failed_test_cases = convert_json_to_md_format(failed_test_cases)
            f.writelines(formatted_failed_test_cases)


def convert_json_to_md_format(failed_test_cases: list):
    final_test_format = []
    for item in failed_test_cases:
        for flow_name, test_case in item.items():
            final_test_format.append("\n## {} {} \n".format(flow_name.split("_", 1)[1],
                                                            "> sender id: {}".format(flow_name)))
            for case in test_case:
                if INTENT in case and case[INTENT] != "nan":
                    if "status" in case and case["status"] == "failed" and "reason" in case and \
                            INTENT in case["reason"]:
                        failed_reason = "<!-- Bot output: {} -->".format(case["reason"][INTENT]["bot_output"])
                        final_test_format.append("* {}: {}  {}\n".format(case[INTENT], case[USER_INPUT], failed_reason))
                    else:
                        final_test_format.append("* {}: {}\n".format(case[INTENT], case[USER_INPUT]))

                if TEMPLATE in case and case[TEMPLATE] != "nan":
                    if "status" in case and case["status"] == "failed" and "reason" in case and \
                            TEMPLATE in case["reason"]:
                        if type(case[TEMPLATE]) is list:
                            final_test_format.append("    - {}\n".format("Templates: "))
                            for bot_template, test_template in itertools.zip_longest(
                                    case["reason"][TEMPLATE]["bot_output"],
                                    case["reason"][TEMPLATE]["test_input"]):
                                if bot_template != test_template:
                                    failed_reason = "<!-- Bot output: {} -->".format(bot_template)
                                    final_test_format.append("        - {}  {}\n".format(test_template, failed_reason))
                                else:
                                    final_test_format.append("        - {}\n".format(test_template))

                    else:
                        if type(case[TEMPLATE]) is list:
                            final_test_format.append("    - {}\n".format("Templates: "))
                            for template in case[TEMPLATE]:
                                final_test_format.append("        - {}\n".format(template))

                if CUSTOM_CODE in case and case[CUSTOM_CODE] != "nan":
                    if "status" in case and case["status"] == "failed" and "reason" in case and \
                            CUSTOM_CODE in case["reason"]:
                        failed_reason = "<!-- Bot output: {} -->".format(case["reason"][CUSTOM_CODE]["bot_output"])
                        final_test_format.append("    - {}: {}  {}\n".format(CUSTOM_CODE, case[CUSTOM_CODE],
                                                                             failed_reason))
                    else:
                        final_test_format.append("    - {}: {}\n".format(CUSTOM_CODE, case[CUSTOM_CODE]))

                if DISPOSITION_ID in case and str(case[DISPOSITION_ID]) != "nan":
                    if "status" in case and case["status"] == "failed" and "reason" in case and \
                            DISPOSITION_ID in case["reason"]:
                        failed_reason = "<!-- Bot output: {} -->".format(case["reason"][DISPOSITION_ID]["bot_output"])
                        final_test_format.append("    - {}: {}  {}\n".format(DISPOSITION_ID, case[DISPOSITION_ID],
                                                                             failed_reason))
                    else:
                        final_test_format.append("    - {}: {}\n".format(DISPOSITION_ID, case[DISPOSITION_ID]))

    print(final_test_format)
    return final_test_format


def validate_intent(bot_response, test_input):
    bot_intent = bot_response["nlu_data"]["intent"]["name"]
    if bot_intent != test_input[INTENT]:
        reason = get_failed_test_case_template(item_name=INTENT, test_value=test_input[INTENT],
                                               bot_value=bot_intent)
        print("Intent failed")
        test_input["status"] = "failed"
        test_input["reason"][INTENT] = reason
    return test_input


def validate_templates(bot_response, test_input):
    templates = [str(item["template_name"]) for item in bot_response.get("data")]
    print(templates, test_input[TEMPLATE])
    if not compare_two_list(templates, test_input[TEMPLATE]):
        print("Templates failed")
        reason = get_failed_test_case_template(item_name=TEMPLATE, test_value=test_input[TEMPLATE],
                                               bot_value=templates)
        test_input["status"] = "failed"
        test_input["reason"][TEMPLATE] = reason
    return test_input


def validate_custom_code(bot_response, test_input):
    bot_custom_code = bot_response.get("custom", None)
    if bot_custom_code and str(test_input[CUSTOM_CODE]) != "nan":
        status_code = bot_custom_code.get("status")
        if not status_code == test_input[CUSTOM_CODE]:
            print("Custom code")
            reason = get_failed_test_case_template(item_name=CUSTOM_CODE, test_value=test_input[CUSTOM_CODE],
                                                   bot_value=status_code)
            test_input["status"] = "failed"
            test_input["reason"][CUSTOM_CODE] = reason
    return test_input


def validate_disposition_id(bot_response, test_input):
    bot_custom_code = bot_response.get("custom", None)
    if bot_custom_code and "disposition_id" in bot_custom_code:
        status_code = bot_custom_code.get("disposition_id")
        if not status_code == test_input[DISPOSITION_ID]:
            print("Disposition id failed")
            reason = get_failed_test_case_template(item_name=TEMPLATE, test_value=test_input[TEMPLATE],
                                                   bot_value=status_code)
            test_input["status"] = "failed"
            test_input["reason"][DISPOSITION_ID] = reason
    return test_input


def validate_test_cases(final_testing_data, stop_on_fail=True, raise_exception=False):
    headers = {
        'Content-Type': 'application/json',
    }

    data = {"user_id": "9702045e066", "request_id": "request111124784", "sender": "", "message": ""}

    url = 'http://0.0.0.0:8025/webhooks/rest/webhook'
    test_case_status = True
    failed_test_case = []
    for flow_name, test_case in final_testing_data.items():
        test_case_status = True
        test_case_result = []
        data["sender"] = flow_name
        for test_input in test_case:
            test_input["status"] = "success"
            test_input["reason"] = {}
            if USER_INPUT in test_input:
                data["message"] = str(test_input[USER_INPUT])
            else:
                data["message"] = ""

            # time.sleep(10)
            bot_response = requests.post(url, headers=headers, data=json.dumps(data)).json()
            # time.sleep(2)
            print(json.dumps(bot_response, indent=2))

            if columns_available_for_testing:
                for item in columns_available_for_testing:
                    if item == INTENT:
                        test_input = validate_intent(bot_response, test_input)
                    if item == TEMPLATE:
                        test_input = validate_templates(bot_response, test_input)
                    if item == CUSTOM_CODE:
                        test_input = validate_custom_code(bot_response, test_input)
                    if item == DISPOSITION_ID:
                        test_input = validate_disposition_id(bot_response, test_input)
                    if test_input["status"] == "failed":
                        test_case_status = False
                        if stop_on_fail:
                            break

            test_case_result.append(test_input)
            if test_input["status"] == "failed":
                test_case_status = False
                if stop_on_fail:
                    break
        if not test_case_status:
            failed_test_case.append({flow_name: test_case_result})

    store_failed_test_cases(failed_test_case)

    if raise_exception and len(failed_test_case) != 0:
        raise Exception("Stories are failed: " + json.dumps(failed_test_case, indent=2))

    print(json.dumps(failed_test_case, indent=2))


def convert_json_to_dataframe(json_data):
    if json_data:
        preprocessed_data = []
        for test_case in json_data:
            data = {}
            for key, value in test_case.items():
                if value or value == 0:
                    data[key] = value
            preprocessed_data.append(data)
        final_data = pd.json_normalize(preprocessed_data)
        return final_data


def run_test_cases(stop_on_fail=True, raise_exception=False):
    response_data = requests.get(URL)
    if response_data.status_code == 200:
        data = response_data.json()["response"]
        test_data = convert_json_to_dataframe(data)
        test_data = preprocess_testing_data(test_data)
        print(columns_available_for_testing)
        validate_test_cases(test_data, stop_on_fail=stop_on_fail,
                            raise_exception=raise_exception)


def create_argument_parser():
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Enter arguments that will help to run test case')

    # Add the arguments
    # my_parser.add_argument('--file_name',
    #                        metavar='file_name',
    #                        type=str,
    #                        default="",
    #                        required=False,
    #                        help='Provide the excel file name in which Test cases available')
    # my_parser.add_argument('--sheet_name',
    #                        metavar='sheet_name',
    #                        type=str,
    #                        default="Sheet1",
    #                        help='Provide the excel sheet name')
    my_parser.add_argument('--stop_on_fail',
                           action="store_true",
                           help='Flag used to stop the test case on failed')

    my_parser.add_argument('--raise_exception',
                           action="store_true",
                           help='Throws exception on test cases failed ')
    return my_parser


if __name__ == "__main__":
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()
    print(cmdline_args)
    run_test_cases(stop_on_fail=cmdline_args.stop_on_fail, raise_exception=cmdline_args.raise_exception)
    # testing_data = preprocess_testing_data(filename=cmdline_args.file_name, sheet_name=cmdline_args.sheet_name)
    # print(columns_available_for_testing)
    # validate_test_cases(testing_data, stop_on_fail=cmdline_args.stop_on_fail,
    # raise_exception=cmdline_args.raise_exception)
