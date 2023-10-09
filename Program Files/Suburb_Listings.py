#!/usr/bin/env python
# coding: utf-8

# Library Imports

import pandas as pd

# Filtering by suburb
def suburb_filtered_listings(listings_df, sub):
    fsub_df = listings_df[listings_df['neighbourhood'].str.lower() == sub.lower()]
    return fsub_df
    # Outputs data frame containing filtered listings 

# Filtering by dates
def date_filtered_listings(calendar_df,s_date, e_date):
    fdate_df = calendar_df[((calendar_df['date'] > s_date) & (calendar_df['date'] < e_date))]
    return fdate_df
    # Outputs data frame containing filtered listings


def find_suburb_listings(listings_dataframe, calendar_dataframe, requested_suburb, start_date, end_date):
    """
    Fetches a dataframe of listings that contain the given suburb name within a given time period
    :param listings_dataframe: listings dataframe
    :param calendar_dataframe: calendar dataframe
    :param requested_suburb: requested suburb
    :param start_date: start date
    :param end_date: end date
    :return: dataframe of listings
    """
    # date to datetime datatype
    calendar_dataframe['date'] = pd.to_datetime(calendar_dataframe['date'])
    # listing_id to id in calendar_df
    calendar_dataframe.rename(columns={'listing_id': 'id'}, inplace=True)

    # Create a suburb dataframe from the requested suburb
    temporary_suburb_dataframe = listings_dataframe[listings_dataframe['neighbourhood'].str.lower() == requested_suburb.lower()]
    # Create a date dataframe from the requested dates
    temporary_date_dataframe = calendar_dataframe[((calendar_dataframe['date'] > start_date) &
                                                   (calendar_dataframe['date'] < end_date))]

    # Merging the two dataframes
    temporary_merged_dataframe = pd.merge(temporary_suburb_dataframe, temporary_date_dataframe, on='id')

    # Drop Unneeded Attributes
    temporary_merged_dataframe = temporary_merged_dataframe.drop('calculated_host_listings_count', axis=1)
    temporary_merged_dataframe = temporary_merged_dataframe.drop('price_y', axis=1)

    # changing price_x to price in f_df
    temporary_merged_dataframe.rename(columns={'price_x': 'price'}, inplace=True)

    # sort
    temporary_merged_dataframe = temporary_merged_dataframe.sort_values(by=['id'])

    # Drop Duplicates
    temporary_merged_dataframe = temporary_merged_dataframe.drop_duplicates(subset='id', keep='first')

    return temporary_merged_dataframe
