#!/usr/bin/env python
# coding: utf-8

# Library Imports

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# NOTE!!! CODE REQUIRED TO RECIEVE INPUT VARIABLES  s_date, e_date

# WIP TEST VARIABLE COMMENT
s_date = '19/04/2019'
e_date = '19/05/2019'

# Datetime allocation
s_date = datetime.strptime(s_date, "%d/%m/%Y") # INPUT MUST BE IN THIS FORMAT
e_date = datetime.strptime(e_date, "%d/%m/%Y")

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

def generate_date_distribution(calendar_dataframe, start_date, end_date):

    # date to datetime datatype
    calendar_dataframe['date'] = pd.to_datetime(calendar_dataframe['date'])

    # listing_id to id in calendar_df
    calendar_dataframe.rename(columns={'listing_id': 'id'}, inplace=True)

    temporary_calendar_dataframe = date_filtered_listings(calendar_dataframe, start_date, end_date)
    # Drop Unneed Attributes
    temporary_calendar_dataframe = temporary_calendar_dataframe.drop('available', axis=1)
    temporary_calendar_dataframe = temporary_calendar_dataframe.reset_index(drop=True)

    # Remove rows where 'price' is NaN
    temporary_calendar_dataframe = temporary_calendar_dataframe.dropna(subset=['price'])

    # Convert price datatype to float
    temporary_calendar_dataframe['price'] = temporary_calendar_dataframe['price'].replace('[\$,]', '', regex=True).astype(float)

    # Drop duplicates of id and price and then sort by id and price
    temporary_calendar_dataframe = temporary_calendar_dataframe.drop_duplicates(subset=['id', 'price']).sort_values(by=['id', 'price'])

    # Dynamically make bins and labels

    min_price = temporary_calendar_dataframe["price"].min()
    max_price = temporary_calendar_dataframe["price"].max()
    b_width = 500
    b = list(range(int(np.floor(min_price)), int(np.ceil(max_price)) + b_width, b_width))
    l = [f'{i}-{j}' for i, j in zip(b[:-1], b[1:])]

    # Create price category column
    temporary_calendar_dataframe['price_category'] = pd.cut(temporary_calendar_dataframe['price'], bins=b, labels=l)

    # Group by date and price and, count unique id
    temporary_grouped_dataframe = temporary_calendar_dataframe.groupby(['date', 'price_category'])['id'].nunique().reset_index()

    # Make price categories become columns
    temporary_pivoted_dataframe = temporary_grouped_dataframe.pivot(index='date', columns='price_category', values='id')

    # Plot
    ax = temporary_pivoted_dataframe.plot(kind='bar', stacked=True, figsize=(15, 7), cmap='Oranges')
    plt.title('Distribution of Unique IDs Across Various Price Ranges')
    plt.xlabel('Date')
    plt.ylabel('Count of Unique IDs')
    plt.legend(title='Price Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    # display fewer x-axis labels
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    plt.savefig("img/price_distribution2.png", dpi=300, bbox_inches='tight')


# Execute functions
fprice_df = date_filtered_listings(calendar_df,s_date, e_date)


# Drop Unneed Attributes
fprice_df = fprice_df.drop('available', axis=1)
fprice_df = fprice_df.reset_index(drop=True)

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
plt.savefig("img/price_distribution.png", dpi=300, bbox_inches='tight')





