import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Sample data structure
data = [
    ["RELIANCE", 2470, 2474.5, 2405, 2409.8, 2458.95, 26348, 285664, "2021-12-13"],
    ["RELIANCE", 2431.1, 2474.9, 2425.45, 2455.85, 2417.4, 12285, 170477, "2021-12-09"],
    ["RELIANCE", 2384, 2405, 2374.35, 2397.7, 2369.8, 8800, 100293, "2021-12-28"]
]

# Create a DataFrame
df = pd.DataFrame(data, columns=['Ticker', 'Open_Price', 'High_Price', 'Low_Price', 'Close_Price', 'Previous_Close', 'Number_Of_Trades', 'Volume', 'Trade_Date'])
df['Trade_Date'] = pd.to_datetime(df['Trade_Date'])

# Streamlit app
st.title('Monte Carlo Simulation')

# User input for ticker symbol
#user_ticker = st.text_input('Enter Ticker Symbol', value='RELIANCE').upper()
col1, col2,col3 = st.columns(3)
default_days = 250
default_simulations = 1000
# Use text_input in each column with default values
user_ticker = col1.text_input('Enter Ticker Symbol', value='RELIANCE').upper()
days = col2.text_input("Days to Simulate", str(default_days))
simulations = col3.text_input("Number of Simulations", str(default_simulations))

# Filter DataFrame based on ticker symbol entered by the user
df_filtered = df[df['Ticker'] == user_ticker]

if not df_filtered.empty:
    # Calculate daily returns
    df_filtered['Returns'] = df_filtered['Close_Price'].pct_change()

    # Calculate the mean (mu) and standard deviation (sigma) of daily returns
    mu = df_filtered['Returns'].mean()
    sigma = df_filtered['Returns'].std()

    # Use the last available close price as initial price
    initial_price = df_filtered['Close_Price'].iloc[-1]

    

# Use st.text_input instead of number_input for flexibility
    
    days = int(days)
    simulations = int(simulations)
    # Monte Carlo simulation function
    def monte_carlo_simulation(start_price, mu, sigma, days, simulations):
        dt = 1
        results = np.zeros((days+1, simulations))
        results[0] = start_price
        
        for t in range(1, days + 1):
            shock = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt), size=simulations)
            results[t] = results[t - 1] * np.exp(shock)
        
        return results

    # Run simulation
    results = monte_carlo_simulation(initial_price, mu, sigma, days, simulations)

    # Visualization
    fig = go.Figure()
    for i in range(simulations):
        fig.add_trace(go.Scatter(x=np.arange(days + 1), y=results[:, i], mode='lines', opacity=0.5, showlegend=False))
    # Unreliable region (0 to 30 days)
    fig.add_vrect(x0=0, x1=30, fillcolor="red", opacity=0.3, layer="below", line_width=0, annotation_text="Unreliable", annotation_position="top left")

    # Transition phase region (30 to 210 days)
    fig.add_vrect(x0=30, x1=210, fillcolor="yellow", opacity=0.3, layer="below", line_width=0, annotation_text="Transition Phase", annotation_position="top left")

    # Reliable region (210+ days)
    fig.add_vrect(x0=210, x1=days, fillcolor="green", opacity=0.3, layer="below", line_width=0, annotation_text="Reliable", annotation_position="top left")

    # Update layout and regions as needed...
    fig.update_layout(title=f'Monte Carlo Simulation Results for {user_ticker}', xaxis_title='Days', yaxis_title='Simulated Price')
    st.plotly_chart(fig)
else:
    st.write("Ticker not found. Please enter a valid ticker.")

average_predicted_close = np.mean(results[-1])
st.write(f"Average predicted close price after {days} days: {average_predicted_close:.2f}")


user_selling_price_str = st.text_input('Enter Selling Price')

try:
    user_selling_price = float(user_selling_price_str)  # Convert input to float

    if average_predicted_close - user_selling_price < 0:
        st.write("Selling Immediately would be advisable")
    else:
        st.write("Holding now would be advisable")

except ValueError:
    pass