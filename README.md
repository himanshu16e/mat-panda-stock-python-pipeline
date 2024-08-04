# Stock Market Data Pipeline and Dashboard

## Project Overview

This project is a complete data pipeline and interactive dashboard for stock market analysis. It includes data fetching, cleaning, processing, and visualization. The dashboard provides insights into stock data, including price trends, trading volume, and predictive modeling.

### Features
- **Data Ingestion**: Fetch and store historical stock data.
- **Data Processing**: Clean and transform data, including normalization and feature engineering.
- **Predictive Modeling**: Train and save a linear regression model to predict stock prices.
- **Dashboard**: Interactive web-based dashboard with data visualization and analysis using Plotly Dash.

## Prerequisites

Ensure you have the following installed:
- Python 3.12.4
- Required Python libraries: `pandas`, `plotly`, `dash`, `scikit-learn`, `joblib`, `numpy`

You can install the required libraries using:
```bash
pip install pandas plotly dash scikit-learn joblib numpy


## Project Structure

- `data/`: Directory for raw stock data CSV files.
- `cleaned_data/`: Directory for cleaned and processed data files.
- `models/`: Directory for saving trained machine learning models.
- `assets/`: Directory for static assets like images and CSS files.
- `script/`: Directory for Python scripts, including data fetching, cleaning, and model training.
- `dashboard.py`: Main script to run the Dash dashboard.
- `fetch_stock_data.py`: Script for fetching stock data from Alpha Vantage API.
- `clean_data.py`: Script for cleaning and processing stock data.
- `metrics.json`: JSON file storing metrics related to data processing.
- `style.css`: CSS file for styling the Dash dashboard.


Usage

Fetch Stock Data: Run `fetch_stock_data.py` to fetch historical stock data and save it in the `data/` directory.

Clean and Process Data

Run `clean_data.py` to clean and process the data. This script will:

Handle missing values and duplicates.
Create new features and normalize data.
Save the cleaned data and metrics in the `cleaned_data/` directory and `metrics.json` file.
Train Predictive Model

The `clean_data.py` script also trains a linear regression model and saves it in the `models/` directory.

Run the Dashboard

Run `dashboard.py` to start the Dash web application.
Open your web browser and navigate to `http://127.0.0.1:8050/` to access the dashboard.

Dashboard Features

- Data Ingestion: View data ingestion metrics and visualizations, including volume distribution and daily percentage change.
- Data Processing: Review data quality metrics and visualizations before and after processing, including histograms and heatmaps.
- Data Visualization: Interactive charts for stock price trends, trading volume, moving averages, daily percentage change, cumulative returns, and rolling volatility.
- Analysis: Summary statistics, correlation heatmap, and top-performing and underperforming stocks based on cumulative return.

File Descriptions

- fetch_stock_data.py: Fetches stock data from the Alpha Vantage API and saves it to the `data/` directory.
- clean_data.py: Cleans, processes, and transforms the stock data. Saves the cleaned data and model metrics.
- dashboard.py: Creates a Dash web application to visualize and analyze stock data.
- metrics.json: Contains metrics on data processing, including data quality and processing times.
- style.css: Provides custom styling for the Dash dashboard.

Notes

- Ensure that your environment has access to the required APIs and data sources.
- Check file paths and ensure all directories and files are correctly set up.

Contributing
Feel free to fork this repository and submit pull requests. Contributions are welcome!

License
This project is licensed under the MIT License. See the LICENSE file for more details.

For any questions or issues, please contact [himanshu.fh15@gmail.com].
