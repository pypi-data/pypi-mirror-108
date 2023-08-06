import requests

def get_data(stock):
    httpResponse = requests.get("https://www.styvio.com/api/" + stock)
    pythonData = httpResponse.json()
    return(pythonData)

def get_current_price(stock):
    return(get_data(stock)['currentPrice'])

def get_daily_chart(stock):
    return(get_data(stock)['dailyPrices'])
