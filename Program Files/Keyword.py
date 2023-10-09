#!/usr/bin/env python
# coding: utf-8

# Library Imports

import pandas as pd
from datetime import datetime

# Filtering by Keyword check
def keyword_filtered_listings(listings_df, keyword, check_attributes):
    # Function to check if keyword is in any specified column of a row
    def contains_keyword(row):
        for at in check_attributes:
            if keyword.lower() in str(row[at]).lower():
                return True 
        return False
    
    # Applying the function to filter the DataFrame and return the result
    return listings_df[listings_df.apply(contains_keyword, axis=1)]

# Filtering by dates
def date_filtered_listings(calendar_df,s_date, e_date):
    fdate_df = calendar_df[((calendar_df['date'] > s_date) & (calendar_df['date'] < e_date))]
    return fdate_df
    # Outputs data frame containing filtered listings


def find_keyword_listings(listings_dataframe, calendar_dataframe, requested_keyword, start_date, end_date):
    """
    Fetches a dataframe of listings that contain the given keyword within a given time period
    :param listings_dataframe: listings dataframe
    :param calendar_dataframe: calendar dataframe
    :param requested_keyword: requested keyword
    :param start_date: start date
    :param end_date: end date
    :return: dataframe of listings
    """
    # function local version of unnecessary global variable, to allow for use of function in other files
    local_check_attributes = ['id', 'summary', 'space', 'description']
    listings_dataframe = listings_dataframe[local_check_attributes]

    # date to datetime datatype
    calendar_dataframe['date'] = pd.to_datetime(calendar_dataframe['date'])

    # listing_id to id in calendar_df
    calendar_dataframe.rename(columns={'listing_id': 'id'}, inplace=True)

    # calendar dataframe attribute drops
    # calendar_dataframe = calendar_dataframe.drop('available', axis=1)
    # calendar_dataframe = calendar_dataframe.drop('price', axis=1)

    #creating temporary lists
    temporary_listings_dataframe = keyword_filtered_listings(listings_dataframe, requested_keyword, local_check_attributes)
    temporary_date_dataframe = date_filtered_listings(calendar_dataframe, start_date, end_date)
    temporary_merged_dataframe = pd.merge(temporary_listings_dataframe, temporary_date_dataframe, on='id')

    # sort
    temporary_merged_dataframe = temporary_merged_dataframe.sort_values(by=['id'])

    # Drop Duplicates
    temporary_merged_dataframe = temporary_merged_dataframe.drop_duplicates(subset='id', keep='first')

    return temporary_merged_dataframe
