
# Stock Price Alert System

This Python project tracks the stock prices of a specified company, calculates the percentage difference between the closing prices of two consecutive days, and sends popular news alerts about the company via SMS using Twilio if the price difference exceeds a specified threshold.

## Features

-   **Stock Price Monitoring**: Fetches daily stock prices using the Alpha Vantage API.
-   **Percentage Difference Calculation**: Computes the percentage difference between yesterday's and the day before yesterday's closing prices.
-   **News Alert**: Fetches the latest news related to the company using the NewsAPI and sends an SMS alert with the news headlines and brief descriptions if the stock price changes significantly.
-   **SMS Notification**: Uses Twilio API to send SMS alerts to a specified phone number.

## Requirements

-   Python 3.x
-   An Alpha Vantage API key
-   A NewsAPI key
-   A Twilio account with account SID and authentication token

## Customization

-   **Threshold**: You can adjust the threshold for the percentage difference in the script to trigger the SMS alerts.
-   **Notification Method**: The current implementation sends SMS alerts via Twilio. You can modify the script to send emails using SMTP or another method if preferred.


## Acknowledgments

-   [Alpha Vantage](https://www.alphavantage.co/) for the stock price data.
-   [NewsAPI](https://newsapi.org/) for the news articles.
-   [Twilio](https://www.twilio.com/) for the SMS sending service.
