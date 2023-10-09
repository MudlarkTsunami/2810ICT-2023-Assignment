#!/usr/bin/env python
# coding: utf-8

# Library Imports

import pandas as pd


# Load datasets
reviews_df = pd.read_csv("Data/reviews_dec18.csv")
reviews_df.info()

# Dataframe Manipulation

reviews_df = reviews_df.drop_duplicates(subset='comments', keep='first')
reviews_df = reviews_df.drop('date', axis=1)
reviews_df = reviews_df.drop('reviewer_id', axis=1)
reviews_df = reviews_df.drop('reviewer_name', axis=1)
reviews_df['comments'] = reviews_df['comments'].astype(str)
reviews_df.info()

# Establish Positive and Negative Cleanliness keywords
pos_keywords = ['clean', 'tidy', 'immaculate', 'sanitary', 'spotless', 'neat'] # Reasoning: https://www.thesaurus.com/browse/clean
neg_keywords = ['dirty', 'dusty', 'filthy', 'messy', 'stained', 'unkempt'] # Reasoning: https://www.thesaurus.com/browse/dirty

# Designating functions

# Identifies keywords
def keyword_filtered_reviews(reviews_df):
    # Check Comment is String 
    reviews_df['comments'] = reviews_df['comments'].astype(str)
    
    # Check if keywords in text
    def keyword_in_text(keywords, text):
        for word in keywords:
            if word in text:
                return True
        return False
    
    # Create masks for positive and negative comments
    pos_mask = reviews_df['comments'].apply(lambda x: keyword_in_text(pos_keywords, x.lower()))
    neg_mask = reviews_df['comments'].apply(lambda x: keyword_in_text(neg_keywords, x.lower()))
    
    # Combine masks
    mask = pos_mask | neg_mask
    
    # Filter dataframe by mask
    return reviews_df[mask]

#Counts Keywords
def count_keywords_in_reviews(reviews_df):
    # Check Comment is String
    reviews_df['comments'] = reviews_df['comments'].astype(str)
    
    # Count keywords in text
    def keywords_count(keywords, text):
        count = 0
        for word in keywords:
            count += text.lower().count(word)
        return count
    
    #Count Both pos and neg keywords
    reviews_df['pos_keyword_count'] = reviews_df['comments'].apply(lambda x: keywords_count(pos_keywords, x))
    reviews_df['neg_keyword_count'] = reviews_df['comments'].apply(lambda x: keywords_count(neg_keywords, x))
    
    return reviews_df


def find_by_cleanliness(reviews_dataframe):
    reviews_dataframe = keyword_filtered_reviews(reviews_dataframe)

    reviews_dataframe = count_keywords_in_reviews(reviews_dataframe)

    # Group listing_id & keyword counts sum
    temporary_reviews_dataframe = reviews_dataframe.groupby('listing_id')[['pos_keyword_count', 'neg_keyword_count']].sum().reset_index()

    # Percentage generation

    # Make totals
    temporary_reviews_dataframe['total_keywords'] = temporary_reviews_dataframe['pos_keyword_count'] + temporary_reviews_dataframe['neg_keyword_count']

    # Make Percentage
    temporary_reviews_dataframe['pos_keyword_percentage'] = (temporary_reviews_dataframe['pos_keyword_count'] / temporary_reviews_dataframe['total_keywords']) * 100

    # table cleaning

    # Drop attribute
    temporary_reviews_dataframe = temporary_reviews_dataframe.drop('total_keywords', axis=1)

    # Order by decending 'pos_keyword_count'
    temporary_reviews_dataframe = temporary_reviews_dataframe.sort_values(by='pos_keyword_count', ascending=False)

    return temporary_reviews_dataframe


reviews_df = keyword_filtered_reviews(reviews_df)

reviews_df = count_keywords_in_reviews(reviews_df)

find_by_cleanliness(reviews_df)



# Group listing_id & keyword counts sum
k_sum_df = reviews_df.groupby('listing_id')[['pos_keyword_count', 'neg_keyword_count']].sum().reset_index()




#Percentage generation

# Make totals
k_sum_df['total_keywords'] = k_sum_df['pos_keyword_count'] + k_sum_df['neg_keyword_count']

# Make Percentage
k_sum_df['pos_keyword_percentage'] = (k_sum_df['pos_keyword_count'] / k_sum_df['total_keywords']) * 100

# table cleaning

#Drop attribute
k_sum_df = k_sum_df.drop('total_keywords', axis=1)

#Order by decending 'pos_keyword_count'
k_sum_df = k_sum_df.sort_values(by='pos_keyword_count', ascending=False)

# Export filtered data
k_sum_df.to_csv('fitered_Cleanliness_data.csv', index=False)

