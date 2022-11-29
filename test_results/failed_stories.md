
## sample_flow > sender id: 3672408783_sample_flow 
* call_after_bounce: /call_after_bounce
    - Templates: 
        - utter_first_case_greet
        - utter_first_case_ask_availability
    - Custom code: 702.0
* affirm: yes
    - Templates: 
        - utter_first_case_inform_emi_amount
        - None  <!-- Bot output: utter_first_case_ask_pay_now -->
    - Custom code: 702.0
* affirm: yes
    - Templates: 
        - utter_first_case_inform_payment_link
    - Custom code: 720.0
* inform_payment_done: i have done my payment
    - Templates: 
        - utter_first_case_thank_you_1
    - Custom code: 701.0

## sample_flow_2 > sender id: 7617998332_sample_flow_2 
* call_after_bounce: /call_after_bounce
    - Templates: 
        - utter_first_case_greet
        - utter_first_case_ask_availability
    - Custom code: 702.0
* agree_to_proceed: yes, tell me
    - Templates: 
        - utter_first_case_inform_emi_amount
        - utter_first_case_ask_pay_now
        - utter_first_case_ask_pay_now  <!-- Bot output: None -->
    - Custom code: 702.0
* agree_to_pay: okay, i will pay
    - Templates: 
        - utter_first_case_inform_payment_link
    - Custom code: 720.0
* inform_payment_done: i have done my payment
    - Templates: 
        - utter_first_case_thank_you  <!-- Bot output: utter_first_case_thank_you_1 -->
    - Custom code: 701.0
