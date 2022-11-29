import redis
REDIS_HOST = "20.122.155.51"
REDIS_PORT = 6379
REDIS_DB = 11
REDIS_PASSWORD = "sam@1234"
REDIS_DB_CONV = "0"
REDIS_DB_1 = 15
red_customers = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_1, password=REDIS_PASSWORD, decode_responses=True)
red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)
def store_into_redis(customer_data):
    print("")
    for row in customer_data:
        red_customers.hmset(row['phone_number'],row)
        fetch_data(row['phone_number'])
        print("storeed")
    return True
def fetch_data(phone_number):
    data=red_customers.hgetall(phone_number)
    print(data)
    return data

def detect_camapin(sender_id):
    data=red.hget("cz",sender_id)
    return data


