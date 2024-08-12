from dotenv import load_dotenv
from datetime import date, timedelta
from twilio.rest import Client
import smtplib
import os
import requests

load_dotenv(".env")
AlphaVantage_API = os.environ.get("AV_API")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
my_email = os.environ.get("MAIL_ADD")
mail_pw = os.environ.get("MAIL_PW")

# Select the company and stock you wish to follow
STOCK_NAME = "NVDA" #AAPL, TSLA, GOOG
COMPANY_NAME = "NVIDIA"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


# Use https://www.alphavantage.co/documentation/#daily
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": AlphaVantage_API
}
 
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()


# Get yesterday's closing stock price.
yesterday = str(date.today() - timedelta(days=1))
day_before = str(date.today() - timedelta(days=2))

y_close_price = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])

# Get the closing stock price from day before yesterday
db_close_price = float(stock_data["Time Series (Daily)"][day_before]["4. close"])

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
pos_diff = round(abs(y_close_price - db_close_price), 2)

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_diff = round((pos_diff / db_close_price) * 100, 3)


# Get the first 3 news pieces for the COMPANY_NAME. 
news_api = os.environ.get("NEWS_API")

news_params = {
    "q": COMPANY_NAME,
    "from": day_before,
    "sortBy": "relevancy",
    "apiKey": news_api,
    "language": "en",
}

news_response = requests.get("https://newsapi.org/v2/everything", params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
#print(news_data)

# Use the News API to get articles related to the COMPANY_NAME.

# Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
news_dictionary = {}

for n in range(3):
    news_headline = news_data["articles"][n]["title"]
    news_desc = news_data["articles"][n]["description"]
    news_dictionary[news_headline] = news_desc


# Option 1: Use twilio.com/docs/sms/quickstart/python to send a separate message with each article's title 
# and description to your phone number. 

# Option 2: Use SMTP to recieve news via email


# Create a new list of the first 3 article's headline and description using list comprehension.
# Send each article as a separate message via Twilio. 
if percentage_diff > 1:
    if y_close_price > db_close_price:
        trend = "⬆️"
    else:
        trend = "⬇️"

    # Option 1: Twilio
    for key, value in news_dictionary.items():
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(body=f"{STOCK_NAME}: {trend}{percentage_diff}%\nHeadline: {key}\nBrief: {value}", from_='+11111111', to='+99999999')
        print(message.status)

    ## from_ - Twilio number, to - Phone number you wish to recieve the notifications to
    
    # Option 2: Email
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=mail_pw)
