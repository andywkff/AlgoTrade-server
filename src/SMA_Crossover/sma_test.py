from __future__ import print_function
from pyalgotrade.optimizer import local
from pyalgotrade.barfeed import yahoofeed
from datetime import datetime, timezone
import sma_crossover
import itertools
import sma_temp
import copy
import update

code_list = []


# Used in server only
def test_specific(user_id: str = "", inputs: str = None):
    users_list = sma_temp.get_all_db_user()
    new_list = []
    for user in users_list:
        if user["user_id"] == user_id:
            new_user = copy.deepcopy(user)
            instrument_list = []
            for item in user["instruments"]:
                if inputs is not None:
                    instrument = copy.deepcopy(item)
                    if item["instrument"] == inputs:
                        update.main(instrument = item["instrument"])
                        run(instrument = item["instrument"])
                        for config in sma_temp.singleton.get_stock_best():
                            if "config_simulation_history" not in instrument or len(instrument["config_simulation_history"]) < 1:
                                instrument["config_simulation_history"] = []
                            instrument["config_simulation_history"].append(config)
                            if config["test_period"] == "2yrs":
                                if instrument["config"]["value"] == 0:
                                    if "config_history" not in instrument or len(
                                            instrument["config_history"]) < 1:
                                        instrument["config_history"] = []
                                    instrument["config_history"].append(config)
                                    config["active"] = True
                                    instrument["config"] = config
                        sma_temp.singleton.clear_all_lists()
                        instrument_list.append(instrument)
                    else:
                        instrument_list.append(instrument)
                else:
                    update.main(instrument = item["instrument"])
                    instrument = copy.deepcopy(item)
                    run(instrument = item["instrument"])
                    for config in sma_temp.singleton.get_stock_best():
                        if "config_simulation_history" not in instrument or len(
                                instrument["config_simulation_history"]) < 1:
                            instrument["config_simulation_history"] = []
                        instrument["config_simulation_history"].append(config)
                        if config["test_period"] == "2yrs":
                            if instrument["config"]["value"] == 0:
                                if "config_history" not in instrument or len(
                                        instrument["config_history"]) < 1:
                                    instrument["config_history"] = []
                                instrument["config_history"].append(config)
                                config["active"] = True
                                instrument["config"] = config
                    sma_temp.singleton.clear_all_lists()
                    instrument_list.append(instrument)
            new_user["instruments"] = instrument_list
            new_list.append(new_user)
    sma_temp.update_users_table(new_user_list = new_list)


# Normal use in local environment
def main(old: bool = False):
    if not old:
        users_list = sma_temp.get_all_db_user()
        new_list = []
        for user in users_list:
            new_user = copy.deepcopy(user)
            instrument_list = []
            for item in user["instruments"]:
                update.main(instrument = item["instrument"])
                instrument = copy.deepcopy(item)
                run(instrument = item["instrument"])
                for config in sma_temp.singleton.get_stock_best():
                    if "config_simulation_history" not in instrument or len(
                            instrument["config_simulation_history"]) < 1:
                        instrument["config_simulation_history"] = []
                    instrument["config_simulation_history"].append(config)
                    if config["test_period"] == "2yrs":
                        if instrument["config"]["value"] == 0:
                            if "config_history" not in instrument or len(
                                    instrument["config_history"]) < 1:
                                instrument["config_history"] = []
                            instrument["config_history"].append(config)
                            config["active"] = True
                            instrument["config"] = config
                sma_temp.singleton.clear_all_lists()
                instrument_list.append(instrument)
            new_user["instruments"] = instrument_list
            new_list.append(new_user)
        sma_temp.update_users_table(new_user_list = new_list)
    else:
        for item in code_list:
            run(instrument = item)


# Hijack for manual local execution
def run(instrument: str = "AAPL"):
    yrs = ["2yrs", "1yr", "3yrs"]
    for yr in yrs:
        current_time_epoch = int(datetime.now(tz = timezone.utc).timestamp())
        # print("****" + yr + "****")
        path_string = "/tmp/" + instrument + "_" + yr + ".csv"
        feed = yahoofeed.Feed()
        try:
            feed.addBarsFromCSV(instrument, path_string)
        except Exception:
            return
        result = local.run(sma_crossover.SMACrossOver, feed, parameters_generator(instrument = instrument),
                           workerCount = 8)
        temp = copy.deepcopy(sma_temp.Instrument_config)
        temp["instrument"] = result.getParameters()[0]
        temp["rules"] = "sma"
        temp["value"] = result.getParameters()[1]
        temp["test_period"] = yr
        temp["last_updated"] = current_time_epoch
        temp["created"] = current_time_epoch
        temp["portfolio"] = result.getResult()
        sma_temp.singleton.add_stock_best(temp)


def parameters_generator(instrument: str = "AAPL"):
    instrument = [instrument]
    smaPeriod = range(1, 50)
    return itertools.product(instrument, smaPeriod)


if __name__ == '__main__':
    test_specific(user_id = "")
