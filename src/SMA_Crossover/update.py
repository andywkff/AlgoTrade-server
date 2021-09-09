from datetime import datetime, timezone
import requests
import sma_temp

current_epoch = int(datetime.now(tz = timezone.utc).timestamp())
baseURL = ""
temp_parm = ""

codeList = []

query = {
    "period1": 0,
    "period2": 0,
    "code": ""
}


def main(instrument: str = None, user_id: str = None):
    if instrument is None:
        if user_id is None:
            for item in codeList:
                query["code"] = item
                update_one_year()
                update_two_year()
                update_three_year()
                update_max()
                update_five_year()
                update_six_month()
                update_four_year()
        else:
            db_list = sma_temp.get_all_db_user()
            for user in db_list:
                for item in user["instruments"]:
                    query["code"] = item["instrument"]
                    update_three_year()
                    update_one_year()
                    update_two_year()
                    update_max()
                    update_five_year()
                    update_six_month()
                    update_four_year()
    else:
        query["code"] = instrument
        query["code"] = instrument
        update_one_year()
        update_two_year()
        update_three_year()
        update_max()
        update_five_year()
        update_six_month()
        update_four_year()
    print("saved successfully")


def get_parms(value: int = 0) -> dict:
    if value == 0:
        temp = query.copy()
        temp["period1"] = 345427200
        temp["period2"] = current_epoch
        return temp
    elif value == 0.5:
        temp = query.copy()
        temp["period1"] = current_epoch - 15768000
        temp["period2"] = current_epoch
        return temp
    elif value == 1:
        temp = query.copy()
        temp["period1"] = current_epoch - 31536000
        temp["period2"] = current_epoch
        return temp
    elif value == 2:
        temp = query.copy()
        temp["period1"] = current_epoch - 31536000 - 31536000
        temp["period2"] = current_epoch
        return temp
    elif value == 5:
        temp = query.copy()
        temp["period1"] = current_epoch - 31536000 - 31536000 - 31536000 - 31536000 - 31536000
        temp["period2"] = current_epoch
        return temp
    elif value == 3:
        temp = query.copy()
        temp["period1"] = current_epoch - 31536000 - 31536000 - 31536000
        temp["period2"] = current_epoch
        return temp
    elif value == 4:
        temp = query.copy()
        temp["period1"] = current_epoch - 31536000 - 31536000 - 31536000 - 31536000
        temp["period2"] = current_epoch
        return temp


def update_one_year():
    temp = get_parms(value = 1)
    url = baseURL + temp["code"]
    payload = {'period1': temp["period1"],
                'period2': temp["period2"],
                "interval": "1d",
                "events": "history",
                "includeAdjustedClose": True}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3" }
    r = requests.get(url = url,headers = headers, params = payload)
    link = "/tmp/" + temp["code"] + "_1yr.csv"
    with open(link, 'wb') as f:
        f.write(r.content)
        f.close()


def update_three_year():
    temp = get_parms(value = 3)
    url = baseURL + temp["code"]
    payload = {'period1': temp["period1"],
                'period2': temp["period2"],
                "interval": "1d",
                "events": "history",
                "includeAdjustedClose": True}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3" }
    r = requests.get(url = url, headers = headers, params = payload)
    link = "/tmp/" + temp["code"] + "_3yrs.csv"
    with open(link, 'wb') as f:
        f.write(r.content)
        f.close()


def update_four_year():
    temp = get_parms(value = 4)
    url = baseURL + temp["code"]
    payload = {'period1': temp["period1"],
                'period2': temp["period2"],
                "interval": "1d",
                "events": "history",
                "includeAdjustedClose": True}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3" }
    r = requests.get(url = url, headers = headers, params = payload)
    link = "/tmp/" + temp["code"] + "_4yrs.csv"
    with open(link, 'wb') as f:
        f.write(r.content)
        f.close()


def update_max():
    temp = get_parms(value = 0)
    url = baseURL + temp["code"]
    payload = { 'period1': temp["period1"],
                'period2': temp["period2"],
                "interval": "1d",
                "events": "history",
                "includeAdjustedClose": True }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3" }
    r = requests.get(url = url, headers = headers, params = payload)
    link = "/tmp/" + temp["code"] + "_max.csv"
    with open(link, 'wb') as f:
        f.write(r.content)
        f.close()


def update_five_year():
    temp = get_parms(value = 5)
    url = baseURL + temp["code"]
    payload = { 'period1': temp["period1"],
                'period2': temp["period2"],
                "interval": "1d",
                "events": "history",
                "includeAdjustedClose": True }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3" }
    r = requests.get(url = url, headers = headers, params = payload)
    link = "/tmp/" + temp["code"] + "_5yrs.csv"
    with open(link, 'wb') as f:
        f.write(r.content)
        f.close()
        
        
def update_two_year():
    temp = get_parms(value = 2)
    url = baseURL + temp["code"]
    payload = { 'period1': temp["period1"],
                'period2': temp["period2"],
                "interval": "1d",
                "events": "history",
                "includeAdjustedClose": True }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3" }
    r = requests.get(url = url, headers = headers, params = payload)
    link = "/tmp/" + temp["code"] + "_2yrs.csv"
    with open(link, 'wb') as f:
        f.write(r.content)
        f.close()

    
def update_six_month():
    temp = get_parms(value = 0.5)
    url = baseURL + temp["code"]
    payload = { 'period1': temp["period1"],
                'period2': temp["period2"],
                "interval": "1d",
                "events": "history",
                "includeAdjustedClose": True}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3" }
    r = requests.get(url = url, headers = headers, params = payload)
    link = "/tmp/" + temp["code"] + "_6mths.csv"
    with open(link, 'wb') as f:
        f.write(r.content)
        f.close()


if __name__ == '__main__':
    main(instrument = "AAPL")
