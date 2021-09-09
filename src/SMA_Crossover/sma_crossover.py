from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from datetime import datetime, timezone
import sma_temp
import copy

"""
This is the SMACrossOver Strategy which is the core of the simulation
"""


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(SMACrossOver, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        try:
            self.setUseAdjustedValues(True)
        except Exception:
            self.setUseAdjustedValues(False)
        finally:
            self.__prices = feed[instrument].getPriceDataSeries()
            self.__sma = ma.SMA(self.__prices, smaPeriod)

    def getSMA(self):
        return self.__sma

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        transaction = copy.deepcopy(sma_temp.Transaction)
        current_time_epoch = int(datetime.now(tz = timezone.utc).timestamp())
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                shares = int(self.getBroker().getCash() * 0.85 / bars[self.__instrument].getPrice())
                # Enter a buy market order. The order is good till canceled.
                self.info("Placing buy market order for %s shares" % shares)
                self.__position = self.enterLong(self.__instrument, shares, True)
                transaction["instrument"] = self.__instrument
                transaction["direction"] = "buy"
                transaction["price"] = bars[self.__instrument].getPrice()
                transaction["share"] = shares
                transaction["date"] = str(self.getCurrentDateTime())
                transaction["done"] = False
                transaction["final_price"] = 0
                transaction["final_share"] = 0
                transaction["last_updated"] = current_time_epoch
                transaction["created"] = current_time_epoch
                transaction["sma"] = self.getSMA()[-1]
                transaction["macd"] = 0
                transaction["signalEMA"] = 0
                transaction["histogram"] = 0
                sma_temp.singleton.add_transactions_list(transaction)
        
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            shares = self.getBroker().getShares(self.__instrument)
            self.info("Placing sell market order for %s shares" % shares)
            self.__position.exitMarket()
            transaction["instrument"] = self.__instrument
            transaction["direction"] = "sell"
            transaction["price"] = bars[self.__instrument].getPrice()
            transaction["share"] = shares
            transaction["date"] = str(self.getCurrentDateTime())
            transaction["done"] = False
            transaction["final_price"] = 0
            transaction["final_share"] = 0
            transaction["last_updated"] = current_time_epoch
            transaction["created"] = current_time_epoch
            transaction["sma"] = self.getSMA()[-1]
            transaction["macd"] = 0
            transaction["signalEMA"] = 0
            transaction["histogram"] = 0
            sma_temp.singleton.add_transactions_list(transaction)
