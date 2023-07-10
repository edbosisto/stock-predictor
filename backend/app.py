from flask import Flask, g, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

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


# Route to fetch ASX stocks
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
