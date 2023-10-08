#!/usr/bin/env python
# coding: utf-8

# Library Imports

import pandas as pd
from datetime import datetime

# NOTE!!! CODE REQUIRED TO RECIEVE INPUT VARIABLES  keyword, s_date, e_date

# WIP TEST VARIABLE COMMENT
keyword = 'pool'
s_date = '17/10/2023'
e_date = '27/10/2023'

listings_df = pd.read_csv("Data/listings_dec18.csv")
calendar_df = pd.read_csv("Data/calendar_dec18.csv")

# Description dataframe extraction 
check_attributes = ['id','summary','space','description']
listings_df = listings_df[check_attributes]

# Datframe Convertions

# date to datetime datatype
calendar_df['date'] = pd.to_datetime(calendar_df['date'])

# listing_id to id in calendar_df
calendar_df.rename(columns={'listing_id': 'id'}, inplace=True)

# calendar dataframe attribute drops
calendar_df = calendar_df.drop('available', axis=1)
calendar_df = calendar_df.drop('price', axis=1)

# Define Functions for Filtered Dataframe Creation

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
    # function local version of unnecessary global variable, to allow for use of function in other files
    local_check_attributes = ['id', 'summary', 'space', 'description']
    listings_dataframe = listings_dataframe[local_check_attributes]

    # date to datetime datatype
    calendar_dataframe['date'] = pd.to_datetime(calendar_dataframe['date'])

    # listing_id to id in calendar_df
    calendar_dataframe.rename(columns={'listing_id': 'id'}, inplace=True)

    # calendar dataframe attribute drops
    #calendar_dataframe = calendar_dataframe.drop('available', axis=1)
    #calendar_dataframe = calendar_dataframe.drop('price', axis=1)

    #creating temporary lists
    temporary_listings_dataframe = keyword_filtered_listings(listings_dataframe, requested_keyword, check_attributes)
    temporary_date_dataframe = date_filtered_listings(calendar_dataframe, start_date, end_date)
    temporary_merged_dataframe = pd.merge(temporary_listings_dataframe, temporary_date_dataframe, on='id')

    # sort
    temporary_merged_dataframe = temporary_merged_dataframe.sort_values(by=['id'])

    # Drop Duplicates
    temporary_merged_dataframe = temporary_merged_dataframe.drop_duplicates(subset='id', keep='first')


    return temporary_merged_dataframe

# Execute function
flist_df = keyword_filtered_listings(listings_df, keyword, check_attributes) 
fdate_df = date_filtered_listings(calendar_df,s_date, e_date)
print(find_keyword_listings(listings_df,calendar_df,keyword,s_date,e_date))

# Merges both filtered dataframes based on listing id
f_df = pd.merge (flist_df, fdate_df, on='id')

# sort 
f_df = f_df.sort_values(by=['id'])

#Drop Duplicates
f_df = f_df.drop_duplicates(subset='id', keep='first')

# Export filtered data
f_df.to_csv('fitered_keyword_data.csv', index=False)

