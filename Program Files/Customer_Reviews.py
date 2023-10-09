#!/usr/bin/env python
# coding: utf-8


# Retrieve reviews by Name (reviewer_name)
def reviews_by_name(reviews_dataframe, reviewer_name):
    """
    Fetches a dataframe of listings that contain the given reviewer name
    :param reviews_dataframe: reviews dataframe
    :param reviewer_name: reviewer's name
    :return: dataframe of listings
    """
    return reviews_dataframe[reviews_dataframe['reviewer_name'] == reviewer_name]


