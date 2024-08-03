# import os  
# import pandas as pd
# import requests
# import time
# from datetime import datetime, timedelta
# from io import StringIO







# def fetch_stock_data(key_job, ticker, start_date, end_date, output_size = 'compact'):
#     url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize={output_size}&apikey={key_job}&datatype=csv"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  
#         data = pd.read_csv(StringIO(response.text))
#         if data.empty:
#             print(f"No data returned for {ticker}.")
#             return None
        
#         data['timestamp'] = pd.to_datetime(data['timestamp'])
#         start_date = pd.to_datetime(start_date)
#         end_date = pd.to_datetime(end_date)



#         data = data[(data['timestamp'] >= start_date) & (data['timestamp'] <= end_date)]

#         if data.empty:
#             print(f"No data within the date range for {ticker}.")
#             return None


#         return data
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data for {ticker}: {e}")
#         return None




# def rate_limited_fetch(key_job, tickers, output_size='compact'):
#     request_counter = 0
#     max_requests_per_minute = 5
#     max_requests_per_day = 500
#     start_time = datetime.now()

#     end_date = datetime.now().date()
#     start_date = end_date - timedelta(days=60)


#     for ticker in tickers:
#         if request_counter >= max_requests_per_day:
#             print("Reached daily API request limit. Please try again tomorrow.")
#             break



#         data = fetch_stock_data(key_job, ticker, start_date, end_date, output_size)
#         if data is not None:
#             save_path = os.path.join('data', f'{ticker}_TATA_data.csv')
#             os.makedirs(os.path.dirname(save_path), exist_ok=True)  
#             data.to_csv(save_path, index=False)
#             print(f"Data for {ticker} fetched and saved to {save_path}")

                  



#         request_counter += 1
#         time.sleep(15)

#         if datetime.now().date() != start_time.date():
#             request_counter = 0
#             start_time = datetime.now()



# if __name__ == "__main__":
#     key_job = os.getenv('key_job')
#     if not key_job:
#         raise ValueError('Please set the key_job environment variable')
#     else:
#         print(f'API key is set : {key_job}')
    

#     tickers = ['TTM', 'TSLA', 'JNJ', 'WMT']
#     output_size = 'compact'


#     rate_limited_fetch(key_job, tickers, output_size)