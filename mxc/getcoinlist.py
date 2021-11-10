import requests

# get close price of 1 coin with url, return with list
class coin:
    def __init__(self, name):
        url = "https://www.mexc.com/open/api/v2/market/kline?interval=1d&limit=270&symbol=" + name
        r = requests.get(url)
        self.coin_prices = []
        # 15 array
        if r.status_code != 200:
            return
        info = r.json()["data"]

        if (len(info) >= 15):
            for i in range(0, len(info)):
                self.coin_prices.append(float(info[i][2]))
        
    def getlist(self):
        return self.coin_prices

class coinlist:
    def __init__(self):
        r = requests.get("https://www.mexc.com/open/api/v2/market/symbols")
        self.coinlist = []

        if r.status_code != 200:
            return

        info = r.json()
        pairs = info["data"]

        for item in pairs:
            tempstr = item['symbol']
            if (tempstr.find("_USDT") != -1):
                # add to coin list
                self.coinlist.append(tempstr)
    
    # return coinlist
    def getcoinlist(self):
        return self.coinlist

# calculate rsi 14 of all days
def calrsi14(price_list):
    ag = 0
    al = 0

    # first 15 day
    for i in range(1, 15):
        if ((price_list[i] - price_list[i - 1]) > 0):
            ag += (price_list[i] - price_list[i - 1])
        elif ((price_list[i - 1] - price_list[i]) > 0):
            al += (price_list[i - 1] - price_list[i])
    
    ag /= 14
    al /= 14

    # use prior value to calculate remain ag and al
    for i in range(15, len(price_list)):
        if ((price_list[i] - price_list[i - 1]) > 0):
            ag = ((ag * 13) + (price_list[i] - price_list[i - 1])) / 14
            al = (al * 13) / 14
        elif ((price_list[i - 1] - price_list[i]) > 0):
            al = ((al * 13) + (price_list[i - 1] - price_list[i])) / 14
            ag = (ag * 13) / 14
        else:
            al = (al * 13) / 14
            ag = (ag * 13) / 14
    
    if (al == 0):
        return 100.0

    return 100 - 100/(1 + ag/al)

# calculate rsi 14 of only 14 last days
def calrsi14_ver2(price_list):
    ag = 0
    al = 0

    # first 15 day
    for i in range((len(price_list) - 14), len(price_list)):
        if ((price_list[i] - price_list[i - 1]) > 0):
            ag += (price_list[i] - price_list[i - 1])
        elif ((price_list[i - 1] - price_list[i]) > 0):
            al += (price_list[i - 1] - price_list[i])
    
    # ag /= 14
    # al /= 14
    
    if (al == 0):
        return 100.0

    return 100 - 100/(1 + ag/al)

fw = open("temp.txt", "w")

coins = coinlist()
lines = coins.getcoinlist()

for nline in lines:
    testlist = coin(nline)
    # store all coin to dictionary and sort by rsi
    if (len(testlist.getlist()) > 0):
        tempstr = (str(nline) + '\t' + str(calrsi14(testlist.getlist())) + 
        '\t' + str(calrsi14_ver2(testlist.getlist())) + 
        '\t' + str(len(testlist.getlist())) + '\n')
        tempstr = tempstr.replace('.', ',')
        print(tempstr)
        fw.write(tempstr)

fw.close()