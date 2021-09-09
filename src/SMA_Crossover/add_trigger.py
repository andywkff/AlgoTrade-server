from datetime import datetime, timezone
import sma_temp
import boto3
import copy
import uuid
import time


dynamodb = boto3.resource("")
table = dynamodb.Table("")

"""
This script is used to manually add trigger to Amazon db which will trigger automatic checking/sim/update of some sort
"""
current_time_epoch = int(datetime.now(tz = timezone.utc).timestamp())

"""
"reason":
1-> manual trigger sma_plot for latest transactions
2-> manual trigger sma_test for best SMA
3-> manual trigger update csv
4-> new instrument added
"""

dummy = {
    "uuid": str(uuid.uuid4()),
    "user_id": "",
    "instrument": "",
    "reason": 4,
    "status": "PENDING",
    "last_updated": current_time_epoch,
    "created": current_time_epoch
}


# For server use only
def schedule_check():
    users_list = sma_temp.get_all_db_user()
    for user in users_list:
        for item in user["instruments"]:
            payload = copy.deepcopy(dummy)
            payload["user_id"] = user["user_id"]
            payload["uuid"] = str(uuid.uuid4())
            payload["instrument"] = item["instrument"]
            payload["last_updated"] = int(datetime.now(tz = timezone.utc).timestamp())
            payload["created"] = int(datetime.now(tz = timezone.utc).timestamp())
            if item["config"]["rules"] == "sma":
                payload["reason"] = 1
            elif item["config"]["rules"] == "macd":
                payload["reason"] = 5
            table.put_item(
                Item = payload
            )
    return "SUCCESS"


# For server use only
def find_best():
    users_list = sma_temp.get_all_db_user()
    for user in users_list:
        for item in user["instruments"]:
            payload = copy.deepcopy(dummy)
            payload["user_id"] = user["user_id"]
            payload["uuid"] = str(uuid.uuid4())
            payload["reason"] = 2
            payload["instrument"] = item["instrument"]
            payload["last_updated"] = int(datetime.now(tz = timezone.utc).timestamp())
            payload["created"] = int(datetime.now(tz = timezone.utc).timestamp())
            table.put_item(
                Item = payload
            )
    return "SUCCESS"
            

# Will pass in new_list if used together with add_new_instrument.py
def main(new_list: list = None) -> str:
    if new_list is None:
        listsss = ["NVDA"]
        for item in listsss:
            payload = copy.deepcopy(dummy)
            payload["uuid"] = str(uuid.uuid4())
            payload["instrument"] = item
            table.put_item(
                Item = payload
            )
            time.sleep(1)
        return "SUCCESS"
    else:
        for item in new_list:
            payload = copy.deepcopy(dummy)
            payload["uuid"] = str(uuid.uuid4())
            payload["instrument"] = item
            table.put_item(
                Item = payload
            )
            time.sleep(1)
        return "SUCCESS"


if __name__ == '__main__':
    main(new_list = ["NVDA"])
