#!/usr/bin/env python
# coding: utf-8

# Library Imports

import pandas as pd


# NOTE!!! CODE REQUIRED TO RECIEVE INPUT VARIABLES  sub, s_date, e_date

# WIP TEST VARIABLE COMMENT
sub = 'Mosman'
s_date = '19/01/2019'
e_date = '19/02/2019'


listings_df = pd.read_csv("Data/listings_dec18.csv")
calendar_df = pd.read_csv("Data/calendar_dec18.csv")

# Datframe Convertions

#date to datetime datatype
calendar_df['date'] = pd.to_datetime(calendar_df['date'])

#listing_id to id in calendar_df
calendar_df.rename(columns={'listing_id': 'id'}, inplace=True)

# Define Functions for Filtered Dataframe Creation

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


# Execute functions
fsub_df = suburb_filtered_listings(listings_df, sub)
fdate_df = date_filtered_listings(calendar_df,s_date, e_date)


## Merges both filtered dataframes based on listing id

f_df = pd.merge (fsub_df, fdate_df, on='id')

#Attribute Manipulation

# Drop Unneed Attributes
f_df = f_df.drop('calculated_host_listings_count', axis=1)
f_df = f_df.drop('price_y', axis=1)

# price_x to price in f_df
f_df.rename(columns={'price_x': 'price'}, inplace=True)

# sort
f_df = f_df.sort_values(by=['id'])

#Drop Duplicates
f_df = f_df.drop_duplicates(subset='id', keep='first')

# Export filtered data
f_df.to_csv('fitered_suburb_data.csv', index=False)

