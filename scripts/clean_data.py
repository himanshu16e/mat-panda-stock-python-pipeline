import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error
import os 
import joblib 
import time
import json


input_path = 'data'
output_path = 'cleaned_data'
model_path = 'models'

csv_files = {
    'JNJ': 'JNJ_TATA_data.csv',
    'TSLA': 'TSLA_TATA_data.csv',
    'TTM': 'TTM_TATA_data.csv',
    'WMT': 'WMT_TATA_data.csv'
}

metrics ={}

def clean_and_process_data(file):
    start_time = time.time()

    df = pd.read_csv(os.path.join(input_path, file))

    initial_shape = df.shape

    missing_before = df.isnull().sum().sum()
    duplicates_before = df.duplicated().sum()

    df.ffill(inplace=True)
    df.bfill(inplace=True)

    df.drop_duplicates(inplace=True)

    missing_after = df.isnull().sum().sum()
    duplicates_after = df.duplicated().sum()

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    df.sort_values('timestamp', inplace=True)


    df['daily_pct_change'] = df['close'].pct_change()
    df['cumulative_return'] = (1 + df['daily_pct_change']).cumprod()
    df['20_day_moving_avg'] = df['close'].rolling(window=20).mean()
    df['rolling_volatility'] = df['close'].rolling(window=20).std()

    df['mean_price'] = df[['open', 'high', 'low', 'close']].mean(axis=1)
    df['median_price'] = df[['open', 'high', 'low', 'close']].median(axis=1)
    df['std_price'] = df[['open', 'high', 'low', 'close']].std(axis=1)
    df['var_price'] = df[['open', 'high', 'low', 'close']].var(axis=1)


    normalization_start_time = time.time()
    df['normalized_close'] = StandardScaler().fit_transform(df[['close']])
    df['scaled_volume'] = MinMaxScaler().fit_transform(df[['volume']])
    normalization_end_time = time.time()

    df.dropna(inplace=True)

    final_shape = df.shape

    output_file = os.path.join(output_path, f'cleaned_{file}')
    os.makedirs(output_path, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

    end_time = time.time()

    metrics[file] = {
        'initial_shape': initial_shape,
        'final_shape': final_shape,
        'missing_before':int(missing_before),
        'missing_after': int(missing_after),
        'duplicates_before': int(duplicates_before),
        'duplicates_after': int(duplicates_after),
        'cleaning_time': normalization_start_time - start_time,
        'transformation_time': normalization_end_time - normalization_start_time,
        'total_processing_time': end_time - start_time,
        'processing_status': 'Success'
    }
    return df


def train_predictive_model(df, stock_name):

    features = ['open', 'high', 'low', 'volume', '20_day_moving_avg', 'rolling_volatility']
    x = df[features]
    y = df['close']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


    model = LinearRegression()
    model.fit(x_train, y_train)
    
    save_model(model, stock_name)

   

    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse} ")
def save_model(model, stock_name):
    model_file = os.path.join(model_path, f'{stock_name}_stock_price_predictor.pkl')
    joblib.dump(model, model_file)
    print(f"Predictive model saved to {model_file}")

os.makedirs(model_path, exist_ok=True)


for stock_name, file in csv_files.items():
    try:
        df = clean_and_process_data(file)
        train_predictive_model(df, stock_name)
    except Exception as e:
        metrics[file] = {
            'processing_status': 'Failed',
            'error_message': str(e)
        }
with open('metrics.json', 'w') as f:
    json.dump(metrics, f)
print(metrics)

