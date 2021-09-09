import copy
import boto3
import update
import sma_temp
import sma_test
import sma_plot

db = boto3.resource("")
table = db.Table("")


def trigger(event: str = None):
    if event is None:
        return "NOT INSERT"
    else:
        trigger_list = get_single_trigger(uuid = event)
        edited_user_list = []
        for item_readOnly in trigger_list:
            if item_readOnly["status"] == "PENDING":
                item = copy.deepcopy(item_readOnly)
                item["status"] = "IN PROGRESS"
                temp_update = []
                temp_update.append(item)
                update_trigger(users = temp_update)
                if item["reason"] == 4:
                    if item["instrument"] == "":
                        sma_test.test_specific(user_id = item["user_id"])
                        sma_plot.plot_specific(user_id = item["user_id"])
                    else:
                        existing_user_list = sma_temp.get_all_db_user()
                        for user in existing_user_list:
                            if item["user_id"] == user["user_id"]:
                                targeted_user = copy.deepcopy(user)
                                new_instrument = get_new_instrument_object(instrument = item["instrument"])
                                targeted_user["instruments"].append(new_instrument)
                                temp_user_list = []
                                temp_user_list.append(targeted_user)
                                result = sma_temp.update_users_table(new_user_list = temp_user_list)
                            else:
                                pass
                        sma_test.test_specific(user_id = item["user_id"], inputs = item["instrument"])
                        sma_plot.plot_specific(user_id = item["user_id"], item = item["instrument"])
            
                elif item["reason"] == 3:
                    if item["instrument"] == "":
                        update.main(user_id = item["user_id"])
                    else:
                        update.main(instrument = item["instrument"], user_id = item["user_id"])
            
                elif item["reason"] == 2:
                    if item["instrument"] == "":
                        sma_test.test_specific(user_id = item["user_id"])
                    else:
                        sma_test.test_specific(user_id = item["user_id"], inputs = item["instrument"])
            
                elif item["reason"] == 1:
                    if item["instrument"] == "":
                        sma_plot.plot_specific(user_id = item["user_id"])
                    else:
                        sma_plot.plot_specific(user_id = item["user_id"], item = item["instrument"])
                
                edited_user_list.append(item["uuid"])
            else:
                pass
        result = delete_trigger(users = edited_user_list)
        return result
    
    
def get_single_trigger(uuid: str) -> list:
    temp_list = []
    response = table.get_item(
        Key = {
            'uuid': uuid,
        }
    )
    if "Item" in response:
        temp_list.append(response["Item"])
    return temp_list


def get_all_trigger() -> list:
    response = table.scan()
    result = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey = response['LastEvaluatedKey'])
        result.extend(response['Items'])
    return result


def update_trigger(users: list):
    for item in users:
        table.put_item(
            Item = item
        )


def delete_trigger(users: list) -> str:
    for item in users:
        table.delete_item(Key = {
            'uuid': item
        })
    return "SUCCESS"


def get_new_instrument_object(instrument: str = "") -> dict:
    temp_instrument = copy.deepcopy(sma_temp.Instrument)
    temp_instrument["instrument"] = instrument
    temp_config = copy.deepcopy(sma_temp.Instrument_config)
    temp_config["instrument"] = instrument
    temp_instrument["config"] = temp_config
    temp_instrument["config_simulation_history"] = []
    temp_instrument["config_history"] = []
    temp_instrument["transactions"] = []
    print(temp_instrument)
    return temp_instrument


if __name__ == '__main__':
    trigger(event = "")
