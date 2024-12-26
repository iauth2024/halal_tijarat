import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import datetime
from django.shortcuts import render

# Function to fetch data based on a given scan clause
def fetch_data(scan_clause):
    url = "https://chartink.com/backtest/process"
    condition = {"scan_clause": scan_clause}

    with requests.session() as session:
        # First request to get the csrf token
        response = session.get("https://chartink.com/screener/process")
        soup = bs(response.content, "lxml")
        csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]
        headers = {"x-csrf-token": csrf_token}

        # Fetch results using the scan_clause data
        response_data = session.post(url, headers=headers, data=condition).json()

        # Check if 'metaData' exists in the response
        if 'metaData' not in response_data:
            # Log or handle the absence of 'metaData'
            print("Error: 'metaData' not found in response data.")
            return []  # Return an empty list or handle the error as needed

        # If 'metaData' exists, process the data
        meta_data = response_data['metaData']
        trade_times = meta_data[0].get("tradeTimes", [])
        stock_list = response_data.get("aggregatedStockList", [])

        final_data = []
        for i in range(len(trade_times)):
            stock_items = []
            if stock_list[i]:
                for j in range(len(stock_list[i])):
                    if j % 3 == 0:
                        stock_items.append(stock_list[i][j])
                final_data.append({
                    "Date": datetime.datetime.fromtimestamp(trade_times[i] / 1000),
                    "Stock": stock_items
                })

        return final_data


def combined_results(request):
    # Define multiple scan clauses
    scan_clauses = {
        'BBB': "( {cash} ( monthly close > monthly upper bollinger band( 20 , 2 ) and "
            "weekly close > weekly upper bollinger band( 20 , 2 ) and "
            "latest close > latest sma( latest close , 20 ) and "
            "1 day ago close <= 1 day ago sma( latest close , 20 ) and "
            "latest close > 100 ) )",
    'HDT': "( {cash} ( ( {cash} ( latest macd line( 26 , 12 , 9 ) > latest macd signal( 26 , 12 , 9 ) and latest ema( latest close , 9 ) > latest ema( latest close , 21 ) and latest rsi( 14 ) > 50 and latest rsi( 14 ) > latest sma( latest close , 20 ) and latest volume > latest sma( latest volume , 20 ) * 1.5 and monthly close > monthly upper bollinger band( 20 , 2 ) and weekly close > weekly upper bollinger band( 20 , 2 ) and latest close > latest sma( latest close , 20 ) and latest close > latest vwap and latest close > 40 and latest adx( 14 ) > 20 ) ) ) ) ",
    'HP Swing': "( {cash} ( monthly close > monthly upper bollinger band( 20 , 2 ) and weekly close > weekly upper bollinger band( 20 , 2 ) and latest close > latest upper bollinger band( 20 , 2 ) and latest close > latest open * 1.04 and latest close > [0] 1 hour vwap and latest close > [0] 15 minute vwap and latest close > [0] 10 minute vwap and market cap >= 2000 ) ) ",
    'Hp Strong Momentum': "( {cash} ( ( {cash} ( [0] 15 minute macd line( 26 , 12 , 9 ) > [0] 15 minute macd signal( 26 , 12 , 9 ) and [ -1 ] 15 minute macd line( 26 , 12 , 9 ) <= [ -1 ] 15 minute macd signal( 26 , 12 , 9 ) and [-1] 15 minute macd line( 26 , 12 , 9 ) <= [-1] 15 minute macd signal( 26 , 12 , 9 ) and latest macd line( 26 , 12 , 9 ) > latest macd signal( 26 , 12 , 9 ) and [0] 15 minute ema( [0] 15 minute close , 5 ) > [0] 15 minute ema( [0] 15 minute close , 9 ) and latest ema( latest close , 9 ) > latest ema( latest close , 21 ) and latest rsi( 14 ) > 55 and [0] 15 minute rsi( 14 ) > 70 and latest volume > latest sma( latest volume , 20 ) * 1.5 and [0] 15 minute volume > [0] 15 minute sma( [0] 15 minute volume , 20 ) * 1.5 and monthly close > monthly upper bollinger band( 20 , 2 ) and weekly close > weekly upper bollinger band( 20 , 2 ) and latest close > latest sma( latest close , 20 ) and [0] 15 minute close > [0] 15 minute vwap and latest adx( 14 ) > 20 ) ) ) ) ",
    'HSabi monthly upper': "( {cash} ( ( {cash} ( latest macd line( 26 , 12 , 9 ) > latest macd signal( 26 , 12 , 9 ) and [0] 15 minute ema( [0] 15 minute close , 9 ) > [0] 15 minute ema( [0] 15 minute close , 21 ) and latest ema( latest close , 9 ) > latest ema( latest close , 21 ) and [0] 15 minute rsi( 14 ) > 50 and [-2] 15 minute rsi( 14 ) <= [-1] 15 minute rsi( 14 ) and [-1] 15 minute rsi( 14 ) <= [0] 15 minute rsi( 14 ) and [0] 15 minute volume > [0] 15 minute sma( [0] 15 minute volume , 20 ) * 1.5 and [0] 15 minute close > [0] 15 minute vwap and [0] 15 minute adx( 14 ) > 20 and weekly close > weekly upper bollinger band( 20 , 2.5 ) and [0] 15 minute rsi( 14 ) > [0] 15 minute sma( [0] 15 minute close , 20 ) ) ) ) ) ",
    'Hasbi Upper reversal': "( {cash} ( ( {cash} ( latest macd line( 26 , 12 , 9 ) > latest macd signal( 26 , 12 , 9 ) and latest ema( latest close , 9 ) > latest ema( latest close , 21 ) and latest rsi( 14 ) > 60 and [0] 15 minute rsi( 14 ) > 60 and [0] 15 minute volume > [0] 15 minute sma( [0] 15 minute volume , 20 ) * 1.5 and latest close > latest sma( latest close , 20 ) and [0] 15 minute close > [0] 15 minute sma( [0] 15 minute close , 20 ) and [0] 15 minute close > [0] 15 minute vwap and [0] 15 minute adx( 14 ) > 20 and monthly close > monthly upper bollinger band( 20 , 2 ) and weekly close > weekly upper bollinger band( 20 , 2 ) and [0] 15 minute close < 1 year ago high ) ) ) ) ",
    }

    # Collect combined results from all clauses
    combined_data = {}
    for screener, scan_clause in scan_clauses.items():
        screener_data = fetch_data(scan_clause)

        # Sort screener data by date in descending order
        screener_data_sorted = sorted(screener_data, key=lambda x: x['Date'], reverse=True)
        combined_data[screener] = screener_data_sorted

    return render(request, 'combined_results.html', {'combined_data': combined_data})  

##########################################################################################################################################

from .models import ScreenerHistory

def fetch_and_store_data(scan_clause, screener_name):
    data = fetch_data(scan_clause)
    # Save today's screener result
    ScreenerHistory.objects.update_or_create(
        screener_name=screener_name,
        date=datetime.date.today(),
        defaults={'stocks': data}
    )
    return data

########################################################################################################################################

from email.utils import localtime
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import datetime


from django.shortcuts import render
from django.http import JsonResponse
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from .models import Stock  # Ensure the `Stock` model is properly imported

def screener_results(request):
    screener_names = [
        "ALL", "BBB", "HDT", "Hasbi RSI Surge", "Hasbi Monthly Upper",
        "Hasbi Upper Reversal", "Hasbi Swing", "Hasbi Strong Momentum"
    ]

    # Screener conditions
    screeners = {
    "BBB": (
        "{cash} (monthly close > monthly upper bollinger band(20, 2) and "
        "weekly close > weekly upper bollinger band(20, 2) and "
        "latest close > latest sma(latest close, 20) and "
        "1 day ago close <= 1 day ago sma(latest close, 20) and "
        "latest close > 100)"
    ),
    "HDT": (
        "{cash} (latest macd line(26, 12, 9) > latest macd signal(26, 12, 9) and "
        "latest ema(latest close, 9) > latest ema(latest close, 21) and "
        "latest rsi(14) > 50 and latest rsi(14) > latest sma(latest close, 20) and "
        "latest volume > latest sma(latest volume, 20) * 1.5 and "
        "monthly close > monthly upper bollinger band(20, 2) and "
        "weekly close > weekly upper bollinger band(20, 2) and "
        "latest close > latest sma(latest close, 20) and "
        "latest close > latest vwap and latest close > 40 and "
        "latest adx(14) > 20)"
    ),
    "Hasbi RSI Surge": (
        "{cash} (monthly close > monthly upper bollinger band(20, 2) and "
        "weekly close > weekly upper bollinger band(20, 2) and "
        "latest close > latest sma(latest close, 20) and "
        "latest rsi(14) > latest sma(latest rsi(14), 20) and "
        "1 day ago rsi(14) <= 1 day ago sma(latest rsi(14), 20) and "
        "1 day ago rsi(14) < 1 day ago sma(1 day ago rsi(14), 20) and "
        "latest volume > latest sma(latest volume, 20) * 1.5 and "
        "latest close > 100 and latest macd line(26, 12, 9) > "
        "latest macd signal(26, 12, 9) and latest rsi(14) > 55)"
    ),
    "Hasbi Monthly Upper": (
        "{cash} (latest macd line(26, 12, 9) > latest macd signal(26, 12, 9) and "
        "[0] 15 minute ema([0] 15 minute close, 9) > [0] 15 minute ema([0] 15 minute close, 21) and "
        "latest ema(latest close, 9) > latest ema(latest close, 21) and "
        "[0] 15 minute rsi(14) > 50 and [-2] 15 minute rsi(14) <= [-1] 15 minute rsi(14) and "
        "[-1] 15 minute rsi(14) <= [0] 15 minute rsi(14) and "
        "[0] 15 minute volume > [0] 15 minute sma([0] 15 minute volume, 20) * 1.5 and "
        "[0] 15 minute close > [0] 15 minute vwap and [0] 15 minute adx(14) > 20 and "
        "weekly close > weekly upper bollinger band(20, 2.5) and "
        "[0] 15 minute rsi(14) > [0] 15 minute sma([0] 15 minute close, 20))"
    ),
    "Hasbi Upper Reversal": (
        "{cash} (latest macd line(26, 12, 9) > latest macd signal(26, 12, 9) and "
        "latest ema(latest close, 9) > latest ema(latest close, 21) and "
        "latest rsi(14) > 60 and [0] 15 minute rsi(14) > 60 and "
        "[0] 15 minute volume > [0] 15 minute sma([0] 15 minute volume, 20) * 1.5 and "
        "latest close > latest sma(latest close, 20) and "
        "[0] 15 minute close > [0] 15 minute sma([0] 15 minute close, 20) and "
        "[0] 15 minute close > [0] 15 minute vwap and [0] 15 minute adx(14) > 20 and "
        "monthly close > monthly upper bollinger band(20, 2) and "
        "weekly close > weekly upper bollinger band(20, 2) and "
        "[0] 15 minute close < 1 year ago high)"
    ),
    "Hasbi Swing": (
        "{cash} (monthly close > monthly upper bollinger band(20, 2) and "
        "weekly close > weekly upper bollinger band(20, 2) and "
        "latest close > latest upper bollinger band(20, 2) and "
        "latest close > latest open * 1.04 and "
        "latest close > [0] 1 hour vwap and "
        "latest close > [0] 15 minute vwap and "
        "latest close > [0] 10 minute vwap and "
        "market cap >= 2000)"
    ),
    "Hasbi Strong Momentum": (
        "{cash} ([0] 15 minute macd line(26, 12, 9) > [0] 15 minute macd signal(26, 12, 9) and "
        "[+-1] 15 minute macd line(26, 12, 9) <= [+-1] 15 minute macd signal(26, 12, 9) and "
        "[-1] 15 minute macd line(26, 12, 9) <= [-1] 15 minute macd signal(26, 12, 9) and "
        "latest macd line(26, 12, 9) > latest macd signal(26, 12, 9) and "
        "[0] 15 minute ema([0] 15 minute close, 5) > [0] 15 minute ema([0] 15 minute close, 9) and "
        "latest ema(latest close, 9) > latest ema(latest close, 21) and "
        "latest rsi(14) > 55 and [0] 15 minute rsi(14) > 70 and "
        "latest volume > latest sma(latest volume, 20) * 1.5 and "
        "[0] 15 minute volume > [0] 15 minute sma([0] 15 minute volume, 20) * 1.5 and "
        "monthly close > monthly upper bollinger band(20, 2) and "
        "weekly close > weekly upper bollinger band(20, 2) and "
        "latest close > latest sma(latest close, 20) and "
        "[0] 15 minute close > [0] 15 minute vwap and latest adx(14) > 20)"
    )
        # Add other screener conditions similarly...
    }

    

    screener_name = request.GET.get("screener", "ALL")
    print(f"Selected Screener: {screener_name}")  # Debugging line

    condition = {
        "scan_clause": screeners.get(screener_name, "") if screener_name != "ALL" else ""
    }

    try:
        data = []
        if screener_name == "ALL":
            for name, clause in screeners.items():
                condition["scan_clause"] = clause
                response = fetch_screener_data(condition, name)
                if response is not None:
                    data.extend(response)
        else:
            response = fetch_screener_data(condition, screener_name)
            if response is not None:
                data = response

        return render(
            request,
            "screener_results.html",
            {
                "stocks": data,
                "screener_name": screener_name,
                "screener_names": screener_names,
            },
        )

    except Exception as e:
        return render(
            request,
            "screener_results.html",
            {
                "error": str(e),
                "screener_name": screener_name,
                "screener_names": screener_names,
            },
        )


def fetch_screener_data(condition, screener_name):
    """
    Helper function to fetch screener data from the Chartink API and include the screener name.
    """
    from datetime import datetime  # Import needed for Performance model updates
    from .models import Performance  # Ensure the model is correctly imported

    try:
        with requests.session() as s:
            # Fetch CSRF token from the website
            r_data = s.get("https://chartink.com")
            soup = bs(r_data.content, "lxml")
            meta = soup.find("meta", {"name": "csrf-token"})["content"]

            # Make the POST request to fetch screener data
            headers = {
                "x-csrf-token": meta,
                "Content-Type": "application/x-www-form-urlencoded",
            }
            response = s.post(
                "https://chartink.com/screener/process", headers=headers, data=condition
            ).json()

            # Convert response to a DataFrame
            stock_list = pd.DataFrame(response.get("data", []))

            # Ensure the required columns exist
            required_columns = [
                "sr", "nsecode", "name", "bsecode", "per_chg", "close", "volume"
            ]
            for col in required_columns:
                if col not in stock_list.columns:
                    stock_list[col] = None

            # Add screener name to the data
            stock_list["screener_name"] = screener_name

            # Filter required columns
            stock_list = stock_list[required_columns + ["screener_name"]]

            # Update or create Performance entries
            for _, row in stock_list.iterrows():
                Performance.objects.get_or_create(
                    symbol=row["nsecode"],
                    screener_name=screener_name,
                    defaults={
                        "triggered_at": datetime.now(),
                        "initial_price": row["close"],
                    }
                )

            # Convert DataFrame to dictionary and return
            return stock_list.to_dict(orient="records")

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error fetching data for screener '{screener_name}': {e}")
        return None

###########################################################################################################

from django.shortcuts import redirect
from .models import Performance

def delete_selected_stocks(request):
    """
    Delete selected stocks from the Performance model.
    """
    if request.method == "POST":
        selected_stocks = request.POST.getlist('selected_stocks')  # Get IDs of selected stocks
        Performance.objects.filter(id__in=selected_stocks).delete()  # Delete selected stocks
    return redirect('performance_page')  # Redirect back to the performance page



###########################################################################################################
from django.shortcuts import render
from django.utils.timezone import now
import logging
from .models import Performance


def performance_page(request):
    # Fetch all performances ordered by 'triggered_at' (latest first)
    performances = Performance.objects.all().order_by('-triggered_at')

    for performance in performances:
        # Skip this performance if the alert is already sent
        if performance.alert_sent:
            logging.info(f"Skipping alert for {performance.symbol} (already sent).")
            continue

        # Prepare stock details for the alert
        stock_details = f"Close Price: ₹{performance.initial_price} | Triggered At: {performance.triggered_at}"

        try:
            # Send an alert via Telegram
            send_telegram_alert(performance.symbol, performance.screener_name, stock_details)

            # Mark the performance as alerted and set the alert timestamp
            performance.alert_sent = True
            performance.alert_sent_at = now()  # Use timezone-aware 'now'
            performance.save()

            logging.info(f"Alert sent for stock: {performance.symbol} under screener: {performance.screener_name}")
        except Exception as e:
            # Log any errors encountered while sending the alert
            logging.error(f"Failed to send alert for {performance.symbol}: {e}")

    # Render the page with performance data
    return render(request, "performance.html", {"performances": performances})


import logging
from telegram import Bot
from django.http import JsonResponse
from asgiref.sync import async_to_sync
import telegram

# Your bot token and chat ID
BOT_TOKEN = "7182564091:AAHHtu6Rbes8GCnXVyWO-PMWYtXteYRg2rg"
CHAT_ID = "5212928367"

# Initialize bot
bot = Bot(token=BOT_TOKEN)

# Setting up logger
logger = logging.getLogger(__name__)

async def send_telegram_alert_async(stock_name, screener_name, stock_details):
    message = f"Alert for {stock_name} from {screener_name}: {stock_details}"
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    except telegram.error.TelegramError as e:
        logger.error(f"Error sending message: {e}")
        return False
    return True

# Using async_to_sync to wrap the async function for the synchronous view
def send_telegram_alert(stock_name, screener_name, stock_details):
    try:
        # Call async function using async_to_sync
        result = async_to_sync(send_telegram_alert_async)(stock_name, screener_name, stock_details)
        if result:
            logger.info(f"Sent alert for {stock_name} and updated record.")
        else:
            logger.error(f"Failed to send alert for {stock_name}.")
    except Exception as e:
        logger.error(f"Error in sending alert for {stock_name}: {e}")

# Example Django view that uses the send_telegram_alert function
def example_view(request):
    stock_name = "BANARBEADS"
    screener_name = "Hasbi Pure"
    stock_details = "Stock has reached the target price."

    # Call the refactored alert sending function
    send_telegram_alert(stock_name, screener_name, stock_details)

    # Returning a JsonResponse as an example
    return JsonResponse({"status": "Alert sent"})
