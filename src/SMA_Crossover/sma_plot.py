from __future__ import print_function
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade import plotter
from pyalgotrade.barfeed import yahoofeed
import sma_crossover
import sma_temp
import copy
import update


# Used in server only
def plot_specific(user_id: str = "", item: str = None):
    new_list = []
    users_list = sma_temp.get_all_db_user()
    for user in users_list:
        if user["user_id"] == user_id:
            temp_user = copy.deepcopy(user)
            temp_instruments_list = []
            for instrument in user["instruments"]:
                if item is not None:
                    temp_instrument = copy.deepcopy(instrument)
                    if instrument["instrument"] == item:
                        update.main(instrument = instrument["instrument"])
                        if instrument["config"]["value"] != 0:
                            result, temp_result = main(instrument = instrument["instrument"],
                                                       yr = instrument["config"]["test_period"],
                                                       period = instrument["config"]["value"])
                            if result == "SUCCESS":
                                if "transactions" not in instrument or len(instrument["transactions"]) < 1:
                                    temp_instrument["transactions"] = []
                                    length = len(temp_result)
                                    if length > 20:
                                        for i in range(length - 20, length):
                                            temp_instrument["transactions"].append(temp_result[i])
                                    else:
                                        for item in temp_result:
                                            temp_instrument["transactions"].append(item)
                                else:
                                    if instrument["transactions"][-1]["date"] != temp_result[-1]["date"]:
                                        temp_instrument["transactions"].append(temp_result[-1])
                        temp_instruments_list.append(temp_instrument)
                    else:
                        temp_instruments_list.append(temp_instrument)
                else:
                    update.main(instrument = instrument["instrument"])
                    temp_instrument = copy.deepcopy(instrument)
                    if instrument["config"]["value"] != 0:
                        result, temp_result = main(instrument = instrument["instrument"],
                                                   yr = instrument["config"]["test_period"],
                                                   period = instrument["config"]["value"])
                        if result == "SUCCESS":
                            if len(instrument["transactions"]) < 1:
                                temp_instrument["transactions"] = []
                                length = len(temp_result)
                                for i in range(length - 20, length):
                                    temp_instrument["transactions"].append(temp_result[i])
                            else:
                                if instrument["transactions"][-1]["date"] != temp_result[-1]["date"]:
                                    temp_instrument["transactions"].append(temp_result[-1])
                        temp_instruments_list.append(temp_instrument)
                    else:
                        temp_instruments_list.append(temp_instrument)
            temp_user["instruments"] = temp_instruments_list
            new_list.append(temp_user)
    sma_temp.update_users_table(new_user_list = new_list)
    

# Normal use in local environment
def initialize():
    new_list = []
    users_list = sma_temp.get_all_db_user()
    for user in users_list:
        temp_user = copy.deepcopy(user)
        temp_instruments_list = []
        for instrument in user["instruments"]:
            update.main(instrument = instrument["instrument"])
            temp_instrument = copy.deepcopy(instrument)
            if instrument["config"]["value"] != 0:
                result, temp_result = main(instrument = instrument["instrument"],
                                           yr = instrument["config"]["test_period"],
                                           period = instrument["config"]["value"])
                if result == "SUCCESS":
                    if len(instrument["transactions"]) < 1:
                        temp_instrument["transactions"] = []
                        length = len(temp_result)
                        for i in range(length - 20, length):
                            temp_instrument["transactions"].append(temp_result[i])
                    else:
                        if instrument["transactions"][-1]["date"] != temp_result[-1]["date"]:
                            temp_instrument["transactions"].append(temp_result[-1])
                temp_instruments_list.append(temp_instrument)
            else:
                temp_instruments_list.append(temp_instrument)
        temp_user["instruments"] = temp_instruments_list
        new_list.append(temp_user)
    sma_temp.update_users_table(new_user_list = new_list)


# Hijack for manual local execution
def main(instrument: str = "AAPL", yr: str = "2yrs", period: int = 20):
    # Load the bar feed from the CSV file
    feed = yahoofeed.Feed()
    path_string = "/tmp/" + instrument + "_" + yr + ".csv"
    try:
        feed.addBarsFromCSV(instrument, path_string)
    except Exception:
        return "FAILED", []
    else:
        # Evaluate the strategy with the feed's bars.
        myStrategy = sma_crossover.SMACrossOver(feed, instrument, period)  # 20, 28
        # Attach the plotter to the strategy.
        plt = plotter.StrategyPlotter(myStrategy)
        sharpeRatioAnalyzer = sharpe.SharpeRatio()
        myStrategy.attachAnalyzer(sharpeRatioAnalyzer)
        # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
        plt.getInstrumentSubplot(instrument).addDataSeries("SMA", myStrategy.getSMA())
        # Run the strategy.
        myStrategy.run()
        myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
        myStrategy.getBarsProcessedEvent()
        sim_result = sma_temp.singleton.get_transactions_list()
        # Plot the strategy.
        plt.plot()
        return "SUCCESS", sim_result


if __name__ == '__main__':
    plot_specific(user_id = "")
