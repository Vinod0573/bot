import json

flows_need_to_accept = ["pre_emi", "post_emi"]


def get_call_flow(phone_number):
    try:
        with open("../../call_flows_map.json", "r+") as f:
            data = json.load(f)
        phone_number_found = False
        for item in data:
            if "phone_number" in item and item["phone_number"] == phone_number and "flow_name" in item and \
                    item["flow_name"] in flows_need_to_accept:
                phone_number_found = True
                return "/" + item["flow_name"]

        if not phone_number_found:
            phone_number = 12345
            for item in data:
                if "phone_number" in item and item["phone_number"] == phone_number and "flow_name" in item and \
                        item["flow_name"] in flows_need_to_accept:
                    return "/" + item["flow_name"]
    except Exception as e:
        print("exception------", e)
        return "/pre_emi"
