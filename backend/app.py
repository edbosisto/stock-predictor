from flask import Flask, g, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests
import os
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


# Stock Statistics
@app.route('/stock-statistics', methods=['GET'])
def get_stock_statistics():
    asx_stock = request.args.get('asx_stock')

    db = get_db()
    cursor = db.cursor()

    # Execute the SQL query to retrieve the relevant data
    query = f"""
        SELECT COUNT(*) / (SELECT COUNT(*) FROM Comparison_Result
                           WHERE us_indicator_closing_price > 0) * 100 AS percentage
        FROM Comparison_Result
        WHERE asx_stock = '{asx_stock}' AND us_indicator_closing_price > 0
    """
    cursor.execute(query)
    result = cursor.fetchone()
    percentage = result[0]

    # Format the response
    response = {
        'asx_stock': asx_stock,
        'percentage': percentage
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run()
