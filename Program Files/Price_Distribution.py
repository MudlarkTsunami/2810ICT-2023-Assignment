#!/usr/bin/env python
# coding: utf-8

# Library Imports

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# NOTE!!! CODE REQUIRED TO RECIEVE INPUT VARIABLES  s_date, e_date

# WIP TEST VARIABLE COMMENT
# s_date = '2019-04-19'
# e_date = '2019-05-19'

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

# Drop duplicates of id and price and then sort by id and price
fprice_df = fprice_df.drop_duplicates(subset=['id', 'price']).sort_values(by=['id', 'price'])
fprice_df

# Dynamically make bins and labels

min_price = fprice_df["price"].min()
max_price = fprice_df["price"].max()
b_width = 500
b = list(range(int(np.floor(min_price)), int(np.ceil(max_price)) + b_width, b_width))
l = [f'{i}-{j}' for i, j in zip(b[:-1], b[1:])]

# Create price category column
fprice_df['price_category'] = pd.cut(fprice_df['price'], bins=b, labels=l)

# Group by date and price and, count unique id
fprice_df_grouped = fprice_df.groupby(['date', 'price_category'])['id'].nunique().reset_index()

# Make price categories become columns
fprice_df_pivot_grouped = fprice_df_grouped.pivot(index='date', columns='price_category', values='id')

# Plot
ax = fprice_df_pivot_grouped.plot(kind='bar', stacked=True, figsize=(15,7), cmap='Oranges')
plt.title('Distribution of Unique IDs Across Various Price Ranges')
plt.xlabel('Date')
plt.ylabel('Count of Unique IDs')
plt.legend(title='Price Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# display fewer x-axis labels
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plt.savefig("price_distribution.png", dpi=300, bbox_inches='tight')





