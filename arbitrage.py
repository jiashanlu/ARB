# Import the necessary libraries and modules
import requests
import time


# Define the list of tokens to monitor
tokens = ["BTC", "ETH", "XRP", "LTC", "BCH"]

# Set up the exchanges that we want to monitor
exchanges = [
    {
        "id": "kraken",
        "name": "Kraken",
        "endpoint": "https://api.kraken.com/0/public/Ticker",
        "params": {"pair": "XBTUSD"},
        "auth": False,
    },
    {
        "id": "bitoasis",
        "name": "Bitoasis",
        "endpoint": "https://api.bitoasis.net/api/v1/ticker",
        "params": {"symbol": "btcusd"},
        "auth": True,
        "key": "your-api-key",
        "secret": "your-api-secret",
    },
    {
        "id": "binance",
        "name": "Binance",
        "endpoint": "https://api.binance.com/api/v3/ticker/price",
        "params": {"symbol": "BTCUSDT"},
        "auth": True,
        "key": "your-api-key",
        "secret": "your-api-secret",
    },
]


# Set up a loop or schedule to collect market data at regular intervals
while True:
  try:
    # Collect the latest market data from each exchange
    data = {}
    for exchange in exchanges:
      headers = {}
      if exchange["auth"]:
        # Set the authentication headers for the request
        headers["API-KEY"] = exchange["key"]
        headers["API-SECRET"] = exchange["secret"]
        if exchange["id"] == "kraken":
          # Authenticate with the Kraken API
          response = requests.get("https://api.kraken.com/0/private/AddOrder", params={"nonce": int(time.time())}, headers=headers)
          headers["API-SIGN"] = response.headers["API-SIGN"]
    if exchange["id"] == "kraken":
        # Set up pagination for the Kraken API
        params = exchange["params"]
        results = []
        has_more = True
        while has_more:
          # Make the HTTP request and collect the results
          response = requests.get(exchange["endpoint"], params=params, headers=headers)
          results += response.json()["result"]
          # Check if there are more results to fetch
          if "next" in response.links:
            params["after"] = response.links["next"]["url"].split("after=")[1]
          else:
            has_more = False
        data[exchange["id"]] = results
      else:
        # Make the HTTP request and collect the results
      response = requests.get(exchange["endpoint"], params=exchange["params"], headers=headers)
      data[exchange["id"]] = response.json()

    # Analyze the market data to compare the prices of the tokens on each exchange
    for token in tokens:
      kraken_price = data["kraken"][f"XBT{token.upper()}"]["c"][0]
      bitoasis_price = data["bitoasis"][token.upper()]["last"]
      binance_price = data["binance"][f"{token.upper()}USDT"]["price"]
      print(f"{token} prices:")
      print(f"Kraken: {kraken_price}")
      print(f"Bitoasis: {bitoasis_price}")
      print(f"Binance: {binance_price}")

    # Wait for 5 minutes before collecting the next set of market data
    time.sleep(300)

  except Exception as e:
    print(f"An error occurred: {e}")