#!/usr/bin/env python
# coding: utf-8

# Establish Positive and Negative Cleanliness keywords
pos_keywords = ['clean', 'tidy', 'immaculate', 'sanitary', 'spotless', 'neat'] # Reasoning: https://www.thesaurus.com/browse/clean
neg_keywords = ['dirty', 'dusty', 'filthy', 'messy', 'stained', 'unkempt'] # Reasoning: https://www.thesaurus.com/browse/dirty


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
    # WARNING - this line throws soft errors
    reviews_df['comments'] = reviews_df['comments'].astype(str)
    
    # Count keywords in text
    def keywords_count(keywords, text):
        count = 0
        for word in keywords:
            count += text.lower().count(word)
        return count

    # WARNING - these lines throws soft errors
    #Count Both pos and neg keywords
    reviews_df['pos_keyword_count'] = reviews_df['comments'].apply(lambda x: keywords_count(pos_keywords, x))
    reviews_df['neg_keyword_count'] = reviews_df['comments'].apply(lambda x: keywords_count(neg_keywords, x))
    
    return reviews_df


def find_by_cleanliness(reviews_dataframe):
    """
    Generates a dataframe of listings that contain designated positive and negative phrases
    :param reviews_dataframe: reviews dataframe
    :return: a dataframe of listings
    """
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
