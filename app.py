from flask import Flask, jsonify
from yahooquery import Ticker
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    try:
        # Initialize the Ticker object
        stock = Ticker(symbol)

        # Fetch key statistics
        key_stats = stock.key_stats.get(symbol, {})
        if not key_stats:
            return jsonify({'error': 'No data found for symbol.'}), 404

        # Extract relevant data
        current_price = key_stats.get('regularMarketPrice', 0)
        market_cap = key_stats.get('marketCap', 0)

        # Fetch historical data for the past month
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        historical = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        # Prepare historical data
        historical_data = [
            {
                'date': date.strftime('%Y-%m-%d'),
                'price': round(row['close'], 2)
            }
            for date, row in historical.iterrows()
        ]

        response = {
            'price': round(current_price, 2),
            'marketCap': round(market_cap / 1e9, 2),  # Convert to billions
            'historical': historical_data
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
