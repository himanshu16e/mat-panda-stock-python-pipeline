import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import os
import json
from dash.exceptions import PreventUpdate

with open('metrics.json', 'r') as f:
    processing_metrics = json.load(f)

app = Dash(__name__, external_stylesheets=['/assets/style.css'], suppress_callback_exceptions=True)

data_path = 'cleaned_data'
asset_path = 'assets'
input_path = 'data'
stock_files = {
    'JNJ': 'cleaned_JNJ_TATA_data.csv',
    'TSLA': 'cleaned_TSLA_TATA_data.csv',
    'TTM': 'cleaned_TTM_TATA_data.csv',
    'WMT': 'cleaned_WMT_TATA_data.csv',
}

dfs = {stock: pd.read_csv(os.path.join(data_path, file)) for stock, file in stock_files.items()}



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Img(src='/assets/company_logo.png', className='header-img'),
        html.H1("Stock Market Dashboard", className='header-title'),
        html.Div("User Profile", className='header-profile')
    ], className='header'),

    html.Div([
        dcc.Link('Data Ingestion', href='/data-ingestion', className='nav-link'),
        dcc.Link('Data Processing', href='/data-processing', className='nav-link'),
        dcc.Link('Data Visualization', href='/data-visualization', className='nav-link'),
        dcc.Link('Analysis', href='/analysis', className='nav-link')
    ], className='nav'),

    html.Div(id='content', className='content'),

    html.Div([
        html.P("Last Update: ", id='last-update'),
        html.P("Source of Data: Alpha Vantage API")
    ], className='footer')
])


@app.callback(Output('content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/data-ingestion':
        stock_list = ['JNJ', 'TSLA', 'TTM', 'WMT']
        content = []

        for stock in stock_list:
            if stock in dfs:
                df = dfs[stock]
                if df.empty:
                    continue

                data_range = f"{df['timestamp'].min()} to {df['timestamp'].max()}"
                data_volume = df.shape[0]
                data_preview = df.head().to_dict('records')

                missing_values = df.isnull().sum().sum()
                missing_percentage = (df.isnull().sum() / len(df)) * 100
                duplicates = df.duplicated().sum()
                data_quality = f"Missing Values: {missing_values}, Missing Percentage: {missing_percentage.sum(): .2f}%, Duplicates: {duplicates}"
                ingestion_status = "Completed"

                dist_chart = px.bar(df, x='timestamp', y='volume', title=f'{stock} Volume Distribution')

                trend_chart = px.line(df, x='timestamp', y='daily_pct_change', title=f'{stock} Daily Percentage Change')

                content.append(html.Div([
                    html.H3(f'Data Ingestion Content for {stock}'),
                    html.P(f'Data Source: Alpha Vantage API'),
                    html.P(f'Data Range: {data_range}'),
                    html.P(f'Data Volume: {data_volume} records ingestion'),
                    html.P(f'Data Quality: {data_quality}'),
                    html.P(f'Ingestion Status: {ingestion_status}'),
                    html.H4('Data Preview'),
                    html.Table([
                        html.Thead(
                            html.Tr([html.Th(col) for col in df.columns])
                        ),
                        html.Tbody([
                            html.Tr([
                                html.Td(data[col]) for col in data
                            ])for data in data_preview
                        ])
                    ]),
                    html.H4('Data Distribution'),
                    dcc.Graph(figure=dist_chart),
                    html.H4('Data Trends'),
                    dcc.Graph(figure=trend_chart)
                ]))
        return html.Div(content)
    

    elif pathname == '/data-processing':
       return html.Div([
           html.Div([
               dcc.Dropdown(
                   id='processing-stock-dropdown',
                   options=[{'label': stock, 'value': stock} for stock in stock_files.keys()],
                   value='JNJ'
               )
           ], style={'width': '50%', 'margin': '20px auto'}),
           html.Div(id='processing-content')
       ])
    elif pathname == '/analysis':
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='analysis-stock-dropdown',
                    options=[{'label': stock, 'value': stock} for stock in stock_files.keys()],
                    value='JNJ'
                )
            ],style={'width': '50%', 'margin': '20px auto'}),
            html.Div(id='analysis-content')
        ])
    elif pathname == '/data-visualization':
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='stock-dropdown',
                    options=[{'label': stock, 'value': stock} for stock in stock_files.keys()],
                    value='JNJ'
                )
            ], style={'width': '50%', 'margin': '20px auto'}),

            html.Div([
                html.H2("Stock Price Over Time"),
                dcc.Graph(id='price-chart')
            ], className='graph-container'),

            html.Div([
                html.H2("Trading Volume Over Time"),
                dcc.Graph(id='volume-chart')
            ], className='graph-container'),

            html.Div([
                html.H2("Moving Averages (20-day)"),
                dcc.Graph(id='moving-avg-chart')
            ], className='graph-container'),

            html.Div([
                html.H2("Daily Percentage Change"),
                dcc.Graph(id='daily-pct-chart')
            ], className='graph-container'),

            html.Div([
                html.H2("Cumulative Return"),
                dcc.Graph(id='cumulative-return-chart')
            ], className='graph-container'),

            html.Div([
                html.H2("Rolling Volatility (20-day)"),
                dcc.Graph(id='rolling-volatility-chart')
            ], className='graph-container'),

            html.Div([
                html.H2("Histogram of Returns"),
                dcc.Graph(id='returns-histogram')
            ], className='graph-container'),

            html.Div([
                html.H2("Volume Distribution"),
                dcc.Graph(id='volume-pie-chart')
            ], className='graph-container')
        ])
    else:
        return html.Div([html.H3('Welcome to the Stock Market Dashboard!')])
    
@app.callback(
        Output('processing-content', 'children'),
        Input('processing-stock-dropdown', 'value')
)
def update_processing_content(stock):
    if f'{stock}_TATA_data.csv' not in processing_metrics:
        return html.div([html.H3("Metrics data not available")])
    
    metrics = processing_metrics[f'{stock}_TATA_data.csv']

    data_distribution_before = px.histogram(pd.read_csv(os.path.join(input_path, f'{stock}_TATA_data.csv')), x='close', title=f'{stock} Close Price Distribution (Before Processing)')
    data_distribution_after = px.histogram(dfs[stock], x='close', title=f'{stock} Close Price Distribution (After Processing)')

    heatmap_data = pd.DataFrame({
        'Stage': ['Missing Values', 'Duplicates', 'New Features', 'Normalized Data'],
        'Value': [metrics['missing_before'], metrics['duplicates_before'], metrics['final_shape'][1] - metrics['initial_shape'][1], metrics['final_shape'][1]]
    })
    
    
    heatmap = px.bar(heatmap_data, x='Stage', y='Value', title='Data Quality Heatmap')
    return html.Div([
        html.H3('Data Processing Content'),
        html.P(f'Data Cleaning: Number of missing values removed: {metrics["missing_before"] - metrics["missing_after"]}, Number of duplicate records removed: {metrics["duplicates_before"] - metrics["duplicates_after"]}'),
        html.P('Data Normalization/Scaling techniques applied: StandardScaler, MinMaxScaler'),
        html.P('Data Transformation: Rolling calculations, moving averages, percentage changes'),
        html.P(f'Number of new features created: {metrics["final_shape"][1] - metrics["initial_shape"][1]}'),
        html.P('Data Quality Metrics: Accuracy, Completness, Consistency'),
        html.P(f'Data Processing Time: Data Cleaning: {metrics["cleaning_time"]:.2f} seconds, Data Transformation: {metrics["transformation_time"]:.2f} seconds, Total Processing Time: {metrics["total_processing_time"]:.2f} seconds'),
        html.P(f'Data Processing Status: {metrics["processing_status"]}, Error Messages: {metrics.get("error_message", "None")}'),
        html.H4('Data Flow Diagram'),
        html.P('Data Flow Diagram not available.'),
        html.H4('Data Distribution Plots'),
        dcc.Graph(figure=data_distribution_before),
        dcc.Graph(figure=data_distribution_after),
        html.H4('Data Quality Heatmap'),
        dcc.Graph(figure=heatmap)
    ])
@app.callback(
        Output('analysis-content', 'children'),
        Input('analysis-stock-dropdown', 'value')
)
def update_analysis_content(stock):
    df = dfs[stock]

    if df.empty:
        raise PreventUpdate
    
    if 'timestamp' not in df.columns or 'cumulative_return' not in df.columns:
        return html.Div([html.H3("Required columns are missing")])
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    numeric_df = df.select_dtypes(include=[float, int])
    if numeric_df.empty:
        return html.Div([html.H3("No numeric data available for correlation analysis")])
    
    correlation_matrix = numeric_df.corr()
    
    summary_stats = df.describe().T
    summary_stats['mean'] = summary_stats['mean'].apply(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)

    heatmap = px.imshow(correlation_matrix, title='Correlation Heatmap')

    line_chart = px.line(df, x='timestamp', y='close', title=f'{stock} Closing Price Over Time')
    scatter_plot = px.scatter(df, x='volume', y='close', title=f'{stock} Volume vs. Closing Price')
    top_performing_stock = df.loc[df['cumulative_return'].idxmax()]
    underperforming_stock = df.loc[df['cumulative_return'].idxmin()]

    content = [
        html.H3(f'Analysis Content for {stock}'),
        html.H4('Summary Statistics'),
        html.Table([
            html.Thead(html.Tr([html.Th(col) for col in df.describe().columns])),
            html.Tbody([
                html.Tr([html.Td(summary_stats.loc[col, 'mean']) for col in summary_stats.index])

            ])
        ]),
        html.P(f'Data Range: {df["timestamp"].min()} to {df["timestamp"].max()}'),
        html.P(f'Data Volume: {df.shape[0]} records'),
        html.H4('Correlation Heatmap'),
        dcc.Graph(figure=heatmap),
        html.H4('Closing Price Over Time'),
        dcc.Graph(figure=scatter_plot),
        html.H4('Top Performing Stock'),
        html.P(f"Top performing stock is {top_performing_stock['timestamp']} with cumulative return {top_performing_stock['cumulative_return']: .2f}"),
        html.H4('Underperforming stock'),
        html.P(f"Underperforming stock is {underperforming_stock['timestamp']} with cumulative return {underperforming_stock['cumulative_return']: .2f}")
    ]
    return html.Div(content)

@app.callback(
    [Output('price-chart', 'figure'),
     Output('volume-chart', 'figure'),
     Output('moving-avg-chart', 'figure'),
     Output('daily-pct-chart', 'figure'),
     Output('cumulative-return-chart', 'figure'),
     Output('rolling-volatility-chart', 'figure'),
     Output('returns-histogram', 'figure'),
     Output('volume-pie-chart', 'figure'),
     Output('last-update', 'children')],
    [Input('stock-dropdown', 'value')]
)
def update_charts(stock):
    df = dfs[stock]

    if df.empty:
        return[dcc.Graph(), dcc.Graph(), dcc.Graph(), dcc.Graph(), dcc.Graph(), dcc.Graph(), dcc.Graph(), dcc.Graph(), html.P("No Data Available")]

    price_chart = px.line(df, x='timestamp', y='close', title=f'{stock} Stock Price Over Time')
    volume_chart = px.bar(df, x='timestamp', y='volume', title=f'{stock} Trading Volume Over Time')
    moving_avg_chart = go.Figure()
    moving_avg_chart.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Close Price'))
    moving_avg_chart.add_trace(go.Scatter(x=df['timestamp'], y=df['20_day_moving_avg'], mode='lines', name='20-Day MA'))
    moving_avg_chart.update_layout(title=f'{stock} Moving Averages')
    daily_pct_chart = px.line(df, x='timestamp', y='daily_pct_change', title=f'{stock} Daily Percentage Change')
    cumulative_return_chart = px.line(df, x='timestamp', y='cumulative_return', title=f'{stock} Cumulative Return')
    rolling_volatility_chart = px.line(df, x='timestamp', y='rolling_volatility', title=f'{stock} Rolling Volatility')
    returns_histogram = px.histogram(df, x='daily_pct_change', title=f'{stock} Histogram of Returns')
    volume_pie_chart = px.pie(df, values='volume', names='timestamp', title=f'{stock} Volume Distribution')
    last_update = f"Last Update: {df['timestamp'].max()}"

    return (price_chart, volume_chart, moving_avg_chart, daily_pct_chart, cumulative_return_chart, rolling_volatility_chart, returns_histogram, volume_pie_chart, last_update)

if __name__ == '__main__':
    app.run_server(debug=True)

                      