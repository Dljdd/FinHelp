import streamlit as st
import plotly.express as px
import pandas as pd

# Load the CSV file
file_path = 'user_rebal.csv'  # Replace with the actual path to your CSV file
data = pd.read_csv(file_path)

total_investment_returns_by_user = data.groupby('User_Id').agg({
    'Investment_Amount': 'sum',
    'Instrument_Returns': 'sum'
}).reset_index()

# Creating a new column for new investment amount
total_investment_returns_by_user['New_Investment_Amount'] = total_investment_returns_by_user['Investment_Amount'] + total_investment_returns_by_user['Instrument_Returns']
#print(total_investment_returns_by_user.iloc[0]['New_Investment_Amount'])


# Step 1: Calculate total returns for each investment instrument
total_returns_by_instrument = data.groupby('Investment_Instrument')['Instrument_Returns'].sum()

# Assuming an equal base weightage for each instrument to ensure each gets some allocation
base_weightage = 1 / len(total_returns_by_instrument)

# Calculating proportional weightage based on returns, ensuring each instrument gets a minimum allocation
total_returns_sum = total_returns_by_instrument.sum()
proportional_weightages = total_returns_by_instrument.apply(lambda x: base_weightage + (x / total_returns_sum))

# Assuming we have a new total investment amount to be allocated (this would be calculated for each user)
# For demonstration, let's assume a single new investment amount
new_total_investment_amount = total_investment_returns_by_user.iloc[0]['New_Investment_Amount'] # Example total new investment amount

# Allocating the new investment amount based on weightages
new_investment_allocation = proportional_weightages * new_total_investment_amount
#print(new_investment_allocation)





# Map each instrument to its volatility and assign adjusted base weightages
instrument_volatility = data[['Investment_Instrument', 'Instrument_Volatility']].drop_duplicates().set_index('Investment_Instrument')['Instrument_Volatility']
base_weightages = {'Low': 0.4, 'Medium': 0.3, 'High': 0.3}
adjusted_base_weightages = instrument_volatility.map(base_weightages)
total_adjusted_base_weightage = adjusted_base_weightages.sum()

# Adjusted proportional weightages calculation
normalized_base_weightages = adjusted_base_weightages / total_adjusted_base_weightage
total_returns_sum = total_returns_by_instrument.sum()

adjusted_proportional_weightages = {}
for instrument, returns in total_returns_by_instrument.items():
    base_weightage = normalized_base_weightages[instrument]
    adjusted_weightage = base_weightage + (returns / total_returns_sum)
    adjusted_proportional_weightages[instrument] = adjusted_weightage

# Normalize the sum of adjusted weightages to 1 for allocation
total_weightage = sum(adjusted_proportional_weightages.values())
new_investment_allocation_adjusted = {instrument: weightage / total_weightage * new_total_investment_amount for instrument, weightage in adjusted_proportional_weightages.items()}

#print(new_investment_allocation_adjusted)


user_id_of_interest = total_investment_returns_by_user.iloc[0]['User_Id']

# Filter the original data for this specific user
data_for_user = data[data['User_Id'] == user_id_of_interest]

# Sum the investment amounts by Investment Instrument for this user
investment_by_instrument_for_user = data_for_user.groupby('Investment_Instrument')['Investment_Amount'].sum().reset_index()



col1, col2, col3 = st.columns([1,2,1])  # Three columns, with the middle one being twice as wide
with col2:
    st.header('Original Allocation')
    fig1 = px.pie(investment_by_instrument_for_user, names='Investment_Instrument', values='Investment_Amount')
    st.plotly_chart(fig1)

# Space between the next two pie charts
# Adjusting the layout for spacing without excessively specifying spacers
col_left, spacer, col_right = st.columns([1, .1, 1])  # Simpler spacing

with col_left:
    st.header('Return Based Rebalancing')
    allocation_df = pd.DataFrame(list(new_investment_allocation.items()), columns=['Instrument', 'Amount'])
    fig2 = px.pie(allocation_df, names='Instrument', values='Amount')
    st.plotly_chart(fig2)

with col_right:
    st.header('Risk Based Rebalancing')
    allocation_adjusted_df = pd.DataFrame(list(new_investment_allocation_adjusted.items()), columns=['Instrument', 'Amount'])
    fig3 = px.pie(allocation_adjusted_df, names='Instrument', values='Amount')
    st.plotly_chart(fig3)