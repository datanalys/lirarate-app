import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import datetime

# Page Configuration
st.set_page_config(
     page_title="Lebanses Lira Rate",
     page_icon="💵",
     layout="wide",
     initial_sidebar_state="expanded",
)



# Layout
left_column, right_column = st.columns(2)

# Get and modify Data
lira_rate = pd.read_csv('https://raw.githubusercontent.com/datanalys/datasets/main/datasets/lebanon/lirarate.csv')

lira_rate['timestamp'] = lira_rate['date']
lira_rate['date'] = pd.to_datetime(lira_rate['timestamp']).dt.date
lira_rate['year'] = pd.to_datetime(lira_rate['timestamp']).dt.year
lira_rate['month'] = pd.to_datetime(lira_rate['timestamp']).dt.month
lira_rate['year/month'] = pd.to_datetime(lira_rate['timestamp']).dt.year.apply(str) + '-' + pd.to_datetime(lira_rate['timestamp']).dt.month.apply(str)
lira_rate['time'] = pd.to_datetime(lira_rate['timestamp']).dt.time
lira_rate['hour'] = pd.to_datetime(lira_rate['timestamp']).dt.hour


lira_rate_bytime = lira_rate.groupby('hour').sum()[['cumulative_buy']]


lira_rate_byyearmonth = lira_rate.groupby(['year', 'month']).max()[['buy', 'sell']]
lira_rate_byyearmonth = lira_rate_byyearmonth.reset_index()
lira_rate_byyearmonth = lira_rate_byyearmonth.sort_values(by=['year', 'month'])
lira_rate_byyearmonth['year/month'] = lira_rate_byyearmonth['year'].apply(str) + '-' + lira_rate_byyearmonth['month'].apply(str)  
lira_rate_byyearmonth = lira_rate_byyearmonth[['year/month', 'buy', 'sell']].set_index('year/month')



lira_rate_dates = lira_rate['date'].drop_duplicates().sort_values(ascending=False)

last_updated = 'last updated: ' + lira_rate['timestamp'].max()

start_date = datetime.date(2021,1,1)
end_date = datetime.date(2022,5,1)


# Set the Page Title
st.title('Lebanese Lira Black Market Rate')
st.subheader(last_updated)

option = st.sidebar.selectbox('Date Filter', lira_rate_dates)
#option = st.sidebar.multiselect('Select countries', lira_rate_dates)
#option = st.sidebar.date_input("Pick a date")





# expander = st.expander("FAQ")
# expander.write("Here you could put in some really, really long explanations...")

if(option != ""):
    lira_rate_filtered = lira_rate[lira_rate['date'] == option].sort_values(by='timestamp', ascending=False)

lira_rate_filtered
lira_rate_byyearmonth


def reset_filter():
    lira_rate_filtered = lira_rate


# Bar Chart by Time
st.bar_chart(lira_rate_bytime)
st.line_chart(lira_rate_byyearmonth)