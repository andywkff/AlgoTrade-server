import simplejson as json
import singleton_module
import boto3


User = {
    "user_id": "",
    "instruments": []
}

Transaction = {
    "date": "",
    "share": 0,
    "price": 0,
    "direction": "",
    "instrument": "",
    "done": False,
    "final_price": 0,
    "final_share": 0,
    "last_updated": 0,
    "created": 0,
    "sma": 0,
    "macd": 0,
    "signalEMA": 0,
    "histogram": 0,
}

Instrument_config = {
    "instrument": "",
    "rules": "",
    "value": 0,
    "test_period": "",
    "portfolio": 0,
    "active": False,
    "last_updated": 0,
    "created": 0,
    "slowEMA": 0,
    "fastEMA": 0,
    "signalEMA": 0
}

Instrument = {
    "instrument": "",
    "config": {},
    "transactions": [],
    "config_simulation_history": [],
    "config_history": []
}

singleton = singleton_module.SingleTon()

client = boto3.client(service_name='', region_name='')


def get_all_db_user() -> list:
    response = client.invoke(
        FunctionName = '',
        InvocationType = '',
        Payload = json.dumps({
            "method": "GET",
            "data": []
        }, use_decimal = True)
    )
    result = json.load(response['Payload'], use_decimal = True)
    if result["status"] == "SUCCESS":
        return result["data"]
    else:
        return []


def update_users_table(new_user_list: list):
    """
    # call another function here, in order to remove firebase_admin dependency
    """
    response = client.invoke(
        FunctionName = '',
        InvocationType = '',
        Payload = json.dumps({
            "method": "UPDATE",
            "data": new_user_list
        }, use_decimal = True)
    )
    result = json.load(response['Payload'], use_decimal = True)
    if result["status"] == "SUCCESS":
        return "SUCCESS"
    else:
        return "FAILED"
