import sma_temp
import copy
import add_trigger

"""
This script is used to manually add new instrument of your choice to firebase db with desired model structure
"""

User = {
    "user_id": "",
    "instruments": []  # instrument
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
    "created": 0
}

Instrument_config = {
    "instrument": "",
    "rules": "",
    "value": 0,
    "test_period": "",
    "portfolio": 0,
    "active": False,
    "last_updated": 0,
    "created": 0
}

Instrument = {
    "instrument": "",
    "config": {},
    "transactions": [],
    "config_simulation_history": [],
    "config_history": []
}

new_instrument = ["BA"]


def main(dummy: bool = False):
    if dummy:
        set_dummy_data()
    else:
        return ""


def set_dummy_data():
    users = sma_temp.get_all_db_user()
    result_list = []
    for user in users:
        if user["user_id"] == "":
            temp_user = copy.deepcopy(user)
            for item in new_instrument:
                instrument = copy.deepcopy(Instrument)
                instrument["instrument"] = item
                instrument["config"] = copy.deepcopy(Instrument_config)
                instrument["config"]["instrument"] = item
                temp_user["instruments"].append(instrument)
            result_list.append(temp_user)
    sma_temp.update_users_table(new_user_list = result_list)
    result = add_trigger.main(new_list = new_instrument)
    print(result)


if __name__ == '__main__':
    main(dummy = True)
