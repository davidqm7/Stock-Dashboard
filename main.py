import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Define stock tickers
stocks = ['TSLA', 'AMZN']

# Download historical data for each stock
tesla_data = yf.Ticker('TSLA').history(period="5y")
amazon_data = yf.Ticker('AMZN').history(period="5y")

tesla_revenue = pd.DataFrame({
    "Date": pd.to_datetime(["2021-09-30", "2021-06-30", "2021-03-31", "2020-12-31"]),
    "Revenue": [13761, 11958, 10389, 10744]  # Values are in millions of USD
})

amazon_revenue = pd.DataFrame({
    "Date": pd.to_datetime(["2021-09-30", "2021-06-30", "2021-03-31", "2020-12-31"]),
    "Revenue": [110810, 113080, 108518, 125555]  # Values in millions of USD
})


# Calculate daily returns
tesla_data['Daily Return'] = tesla_data['Close'].pct_change()
amazon_data['Daily Return'] = amazon_data['Close'].pct_change()

# Calculate quarterly revenue growth
tesla_revenue['Revenue Growth'] = tesla_revenue['Revenue'].pct_change()
amazon_revenue['Revenue Growth'] = amazon_revenue['Revenue'].pct_change()


def plot_stock_price(data, stock_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{stock_name} Close Price'))
    fig.update_layout(title=f'{stock_name} Historical Share Prices', xaxis_title='Date', yaxis_title='Close Price (USD)')
    return fig

# Tesla and Amazon stock price trends
tesla_fig = plot_stock_price(tesla_data, 'Tesla')
amazon_fig = plot_stock_price(amazon_data, 'Amazon')


def plot_revenue(data, stock_name):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data['Date'], y=data['Revenue'], name=f'{stock_name} Revenue'))
    fig.update_layout(title=f'{stock_name} Quarterly Revenue', xaxis_title='Quarter', yaxis_title='Revenue (in millions USD)')
    return fig

# Tesla and Amazon revenue trends
tesla_revenue_fig = plot_revenue(tesla_revenue, 'Tesla')
amazon_revenue_fig = plot_revenue(amazon_revenue, 'Amazon')

# Initialize Dash app
app = Dash(__name__)

# Set up dashboard layout
app.layout = html.Div(children=[
    html.H1(children='Investment Dashboard'),

    # Stock Price Graphs
    html.H2("Tesla Stock Price"),
    dcc.Graph(figure=tesla_fig),

    html.H2("Amazon Stock Price"),
    dcc.Graph(figure=amazon_fig),

    # Revenue Graphs
    html.H2("Tesla Quarterly Revenue"),
    dcc.Graph(figure=tesla_revenue_fig),

    html.H2("Amazon Quarterly Revenue"),
    dcc.Graph(figure=amazon_revenue_fig)
])

# Run the dashboard
if __name__ == '__main__':
    app.run_server(debug=True)