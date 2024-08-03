from flask import Flask, jsonify, request
import pandas as pd
import os


app = Flask(__name__)

data_path = 'cleaned_data'


def load_data(stock):
    file_path = os.path.join(data_path, f'cleaned_{stock}_TATA_data.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        return None
    

@app.route('/')
def home():
    return "Welcome to the stock Market Dashboard API!"


@app.route('/api/data/<stock>', methods=['GET'])
def get_stock_data(stock):
    df = load_data(stock)
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify({"error": "Data not found"}), 404
    

if __name__ == '__main__':
    app.run(debug=True)