from flask import Flask, jsonify
import yfinance as yf
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    try:
        # Get stock info
        stock = yf.Ticker(symbol)
        
        # Get current data
        current_data = stock.fast_info
        
        # Get historical data for the past month
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        historical = stock.history(start=start_date, end=end_date)
        
        response = {
            'price': round(current_data.get('regularMarketPrice', 0), 2),
            'change': round(current_data.get('regularMarketChangePercent', 0), 2),
            'marketCap': round(current_data.get('marketCap', 0) / 1000000000, 2),  # Convert to billions
            'historical': [
                {
                    'date': index.strftime('%Y-%m-%d'),
                    'price': round(row['Close'], 2)
                }
                for index, row in historical.iterrows()
            ]
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
