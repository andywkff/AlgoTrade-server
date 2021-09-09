import copy

"""
This is a singleton object used to handle list/dict across difference python files at runtime.
"""


class SingleTon:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._id = id(self)
        self._stock_best: list = []
        self._transactions_list: list = []
        self._instruments_list: list = []
    
    def get_id(self):
        return self._id
    
    def get_stock_best(self):
        return self._stock_best
    
    def get_transactions_list(self):
        return self._transactions_list
    
    def get_instruments_list(self):
        return self._instruments_list

    def add_stock_best(self, item: dict):
        self._stock_best.append(item)

    def add_transactions_list(self, item: dict):
        self._transactions_list.append(item)

    def add_instruments_list(self, item: dict):
        self._instruments_list.append(item)

    def clear_stock_best(self):
        self._stock_best.clear()

    def clear_transactions_list(self):
        self._transactions_list.clear()

    def clear_instruments_list(self):
        self._instruments_list.clear()

    def clear_all_lists(self):
        self._stock_best.clear()
        self._instruments_list.clear()
        self._transactions_list.clear()
    
    def get_dummy_user(self):
        return {
            "user_id": "",
            "instruments": []
        }
    
    def get_dummy_transaction(self):
        return copy.deepcopy({
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
        })

    def get_dummy_transaction_config(self):
        return copy.deepcopy({
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
        })
    
    def get_dummy_instrument(self):
        return copy.deepcopy({
            "instrument": "",
            "config": {},
            "transactions": [],
            "config_simulation_history": [],
            "config_history": []
        })
