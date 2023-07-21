from flask import Flask, g, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Allow cross-origin-resource-sharing
CORS(app)

# Connect and configure MySQL DB
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**db_config)
    return g.db


@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()


# Homepage
@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ASX_Stock')
    rows = cursor.fetchall()

    # Process the rows and return a response
    return "Hello World!"  # replace with desired response


# US Index - S&P 500 API data
@app.route("/api/sp500")
def get_sp500_data():
    url = "https://yahoo-finance127.p.rapidapi.com/price/%5EGSPC"
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST"),
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract the required data from the response
        previous_close = data["regularMarketPreviousClose"]["raw"]
        current_value = data["regularMarketPrice"]["raw"]
        percent_change = round(
            data["regularMarketChangePercent"]["raw"] * 100, 2)

        # Create a dictionary with the extracted data
        sp500_data = {
            "previous_close": previous_close,
            "current_value": current_value,
            "percent_change": percent_change,
        }

        return jsonify(sp500_data)

    except requests.exceptions.HTTPError as e:
        return jsonify({"error": str(e)}), 500


# Route to get ASX stock data from Yahoo finance API
@app.route("/api/asxstock/<symbol>", methods=["GET"])
def get_asx_stock_data(symbol):
    url = f"https://yahoo-finance127.p.rapidapi.com/price/{symbol}"
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST"),
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract the required data from the response
        previous_close = data["regularMarketPreviousClose"]["raw"]
        current_price = data["regularMarketPrice"]["raw"]
        percent_change = round(
            data["regularMarketChangePercent"]["raw"] * 100, 2)

        # Create a dictionary with the extracted data
        stock_data = {
            "symbol": symbol,
            "previous_close": previous_close,
            "current_price": current_price,
            "percent_change": percent_change,
        }

        return jsonify(stock_data)

    except requests.exceptions.HTTPError as e:
        return jsonify({"error": str(e)}), 500


# Route to fetch ASX stocks from database
@app.route('/api/asxstocks')
def get_asx_stocks():
    db = get_db()
    cursor = db.cursor()

    # Execute query to fetch ASX stocks
    cursor.execute('SELECT * FROM ASX_Stock')

    # Fetch all rows and build a list of stock objects
    stocks = []
    for row in cursor.fetchall():
        stock = {
            'id': row[0],
            'symbol': row[1],
            'name': row[2]
        }
        stocks.append(stock)

    # Convert the list of stocks to JSON response
    response = jsonify(stocks)

    # Set response headers to allow cross-origin requests (adjust as needed)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


# Route to compare S&P 500 and ASX stock
@app.route("/api/compare", methods=["GET"])
def compare_sp500_asx_stock():
    asx_stock_symbol = request.args.get("symbol")

    # Fetch historical data for the selected ASX stock from your database
    asx_historical_data = get_asx_historical_data(asx_stock_symbol)

    # Fetch historical data for the S&P 500 from your database
    sp500_historical_data = get_sp500_historical_data()

    # Perform data synchronization based on dates
    # We'll assume both datasets have dates in the same format (e.g., "YYYY-MM-DD")
    merged_data = pd.merge(
        asx_historical_data, sp500_historical_data, on="date", suffixes=("_asx", "_sp500"))

    # Calculate percentage change for both the ASX stock and the S&P 500
    merged_data["percent_change_asx"] = (
        merged_data["closing_price_asx"] / merged_data["closing_price_asx"].shift(1) - 1) * 100
    merged_data["percent_change_sp500"] = (
        merged_data["closing_price_sp500"] / merged_data["closing_price_sp500"].shift(1) - 1) * 100

    # Calculate the probability of ASX stock moving in the same direction as S&P 500
    positive_sp500 = merged_data["percent_change_sp500"] > 0
    positive_asx_stock = merged_data["percent_change_asx"] > 0
    probability_up = (positive_sp500 & positive_asx_stock).mean()
    probability_down = (~positive_sp500 & ~positive_asx_stock).mean()

    result = {
        "symbol": asx_stock_symbol,
        "probability_up": round(probability_up * 100, 2),
        "probability_down": round(probability_down * 100, 2),
    }

    return jsonify(result)


# Function to fetch historical data for a given ASX stock from your database
def get_asx_historical_data(symbol):
    db = get_db()
    cursor = db.cursor()

    # Execute query to fetch historical data for the selected ASX stock
    query = f"""
        SELECT date, closing_price
        FROM asx_stock_price
        WHERE asx_stock_id = (SELECT id FROM asx_stock WHERE symbol = '{symbol}')
    """
    cursor.execute(query)

    # Fetch all rows and build a DataFrame of historical data
    data = cursor.fetchall()
    columns = ["date", "closing_price_asx"]
    asx_historical_data = pd.DataFrame(data, columns=columns)

    return asx_historical_data


# Function to fetch historical data for the S&P 500 from your database
def get_sp500_historical_data():
    db = get_db()
    cursor = db.cursor()

    # Execute query to fetch historical data for the S&P 500
    cursor.execute('SELECT date, closing_price FROM sp500_index')

    # Fetch all rows and build a DataFrame of historical data
    data = cursor.fetchall()
    columns = ["date", "closing_price_sp500"]
    sp500_historical_data = pd.DataFrame(data, columns=columns)

    return sp500_historical_data


if __name__ == '__main__':
    app.run()
