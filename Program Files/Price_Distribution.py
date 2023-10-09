#!/usr/bin/env python
# coding: utf-8

# Library Imports

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Filtering by dates
def date_filtered_listings(calendar_df,s_date, e_date):
    fprice_df = calendar_df[((calendar_df['date'] > s_date) & (calendar_df['date'] < e_date))]
    return fprice_df
    # Outputs data frame containing filtered listings


def generate_date_distribution(calendar_dataframe, start_date, end_date):
    """
    Generates a chart image for given time period and then saves it
    :param calendar_dataframe: calendar dataframe
    :param start_date: start date
    :param end_date: end date
    :return: none
    """
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
    plt.savefig("_internal/price_distributionlive.png", dpi=300, bbox_inches='tight')
