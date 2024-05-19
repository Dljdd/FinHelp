import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
import streamlit as st
import plotly.graph_objects as go

# Example dataset
data = pd.DataFrame({
    'date': pd.date_range(start='2020-01-01', periods=100),
    'variable1': np.random.normal(0, 1, 100).cumsum(),
    'variable2': np.random.normal(0, 1, 100).cumsum()
})
data.set_index('date', inplace=True)
# Preprocess data (e.g., fill missing values)
def preprocess_data(data):
    return data.fillna(method='ffill')

# Fit VAR model
def fit_var_model(data, lags):
    model = VAR(data)
    model_fitted = model.fit(lags)
    return model_fitted

# Preprocess the data
data = preprocess_data(data)

# Streamlit UI
st.title('Hedging Stratergies')

# Assuming you want to manually specify these instead of using Streamlit widgets
lags = 5  # Example: Number of lags
steps = 5  # Example: Forecast steps

# Fit the model
model_fitted = fit_var_model(data, lags)



# Forecasting
forecast, stderr, conf_int = model_fitted.forecast_interval(data.values[-lags:], steps=steps)
forecast_df = pd.DataFrame(forecast, index=pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=steps, freq='D'), columns=data.columns)

# Plotting forecast
# Plotting past and forecasted values
fig = go.Figure()
# Plot historical data
for col in data.columns.drop("variable2"):
    fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=f'{col} - Historical'))

# Plot forecasted data
for col in forecast_df.columns.drop("variable2"):
    fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[col], mode='lines+markers', name=f'{col} - Forecast'))

# Add a vertical line for the current date
current_date = data.index[-1]
fig.add_vline(x=current_date, line_width=2, line_dash="dash", line_color="grey")

# Update layout
fig.update_layout(title="VAR Forecast with Historical Data",
                  xaxis_title="Date",
                  yaxis_title="Value",
                  legend_title="Variable")

# Show plot in Streamlit
st.plotly_chart(fig)

# Calculate the average of the forecasted values for each variable
forecast_avg = forecast_df.mean()

# Access the last value of each variable in the dataframe
last_values = data.iloc[-1]

# Recommendations based on the comparison
hedging_recommendations = ""
# Recommendations based on the comparison
hedging_recommendations = ""


if forecast_avg[col] < last_values[col]:
        # If the average forecast is less than the last historical value
        hedging_recommendations += f"""For {col}, Objective: Protect against potential declines in asset value.
Approach: Purchase put options to secure the right to sell the underlying asset at a predetermined strike price before the option expires. This strategy ensures that if the asset's market price falls below this strike price, you can still sell it at the higher, agreed-upon price, thereby limiting your losses.
Key Considerations:
Strike Price Selection: Choose a strike price that provides an acceptable level of protection versus the cost (premium) of the option.
Expiration Date: The expiration date should align with your forecast period or the timeframe over which you seek protection.
Premium Cost: Evaluate the cost of the option against the potential benefit of protection to ensure it's economically viable.\n"""
else:
        # Other hedging strategies
        hedging_recommendations += f"""For {col}, 
Objective: Mitigate risk and protect against volatility in a stable or upward-trending market.
Approach:
Diversification: Spread investments across various assets, sectors, or instruments to reduce the impact of any single market movement.
Futures Contracts: Use futures contracts to lock in future sale or purchase prices for assets. This can protect against unfavorable price movements by setting known prices for transactions ahead of time.
Key Considerations:
Portfolio Balance: Ensure diversification addresses all major sources of risk without diluting potential returns excessively.
Futures Strategy: Select contracts that align with your market outlook and hedging needs, considering the contract size, expiration, and underlying asset.\n"""

# Display the recommendations in Streamlit
st.write(hedging_recommendations)



