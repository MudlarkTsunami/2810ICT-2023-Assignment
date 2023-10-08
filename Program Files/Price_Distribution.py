#!/usr/bin/env python
# coding: utf-8

# Library Imports

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# NOTE!!! CODE REQUIRED TO RECIEVE INPUT VARIABLES  s_date, e_date

# TEST
s_date = '2019-04-19'
e_date = '2019-05-19'

# Datetime allocation
s_date = datetime.strptime(s_date, "%Y-%m-%d") # INPUT MUST BE IN THIS FORMAT
e_date = datetime.strptime(e_date, "%Y-%m-%d")

# Load Data
calendar_df = pd.read_csv("Data/calendar_dec18.csv")

# Datframe Convertions

#date to datetime datatype
calendar_df['date'] = pd.to_datetime(calendar_df['date'])

#listing_id to id in calendar_df
calendar_df.rename(columns={'listing_id': 'id'}, inplace=True)

# Filtering by dates
def date_filtered_listings(calendar_df,s_date, e_date):
    fprice_df = calendar_df[((calendar_df['date'] > s_date) & (calendar_df['date'] < e_date))]
    return fprice_df
    # Outputs data frame containing filtered listings

# Execute functions
fprice_df = date_filtered_listings(calendar_df,s_date, e_date)
fprice_df

# Drop Unneed Attributes
fprice_df = fprice_df.drop('available', axis=1)
fprice_df = fprice_df.reset_index(drop=True)
fprice_df

# Remove rows where 'price' is NaN
fprice_df = fprice_df.dropna(subset=['price'])

# Convert price datatype to float
fprice_df['price'] = fprice_df['price'].replace('[\$,]', '', regex=True).astype(float)

#Getting Min, Max price values
min_price = fprice_df["price"].min()
max_price = fprice_df["price"].max()

# Loop unique id and plot
for u_id in fprice_df['id'].unique():
    subset = fprice_df[fprice_df['id'] == u_id]
    plt.plot(subset['date'], subset['price'], label=f'ID: {unique_id}')

# Titles and labels
plt.title(f'Property Price distribution, {s_date} - {e_date}')
plt.xlabel('Date')
plt.ylabel('Price')

# Formatting dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gcf().autofmt_xdate()

# Add a legend
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Layout Adjustment
plt.tight_layout()

# Show the plot
plt.show()




