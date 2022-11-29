from email import message
from flask import Flask, jsonify,request
from handle_bulk_data import store_into_redis,fetch_data
app= Flask(__name__)
# import asyncio
# cust_details=[]

@app.route("/fetch_customer_data",methods=['POST'])
def fetch_customer_data():
    customer_details=request.get_json()
    print("customer_details",customer_details)
    store_into_redis(customer_details['data'])
    return jsonify(message="Success")

@app.route("/get_data",methods=['POST'])
def get_data():
    customer_details=request.get_json()
    print("customer_details",customer_details)
    result = fetch_data(customer_details["data"])
    return jsonify(message=result)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=7222)
