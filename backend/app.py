from flask import Flask, g, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect and configure MySQL DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'stock_app'
app.config['MYSQL_PASSWORD'] = 'StockApp123#'
app.config['MYSQL_DB'] = 'stockapp'


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
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
