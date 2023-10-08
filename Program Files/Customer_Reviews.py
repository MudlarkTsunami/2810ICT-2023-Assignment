#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Library Imports 

import pandas as pd 

# NOTE!!! CODE REQUIRED TO RECIEVE INPUT VARIABLE  rev_name

# TEST
rev_name = 'Ben'


# In[3]:


# Load datasets
id_reviews_df = pd.read_csv("Data/TESTreviews_dec18.csv")
id_reviews_df.info()


# In[7]:


#Function/s

# Retrieve reviews by Name (rev_name)
def reviews_by_name(id_reviews_df, rev_name):

    return id_reviews_df[id_reviews_df['reviewer_name'] == rev_name]

rev_name_df = reviews_by_name(id_reviews_df, rev_name)

rev_name_df



# In[8]:


# Dataframe Clean
rev_name_df = rev_name_df.drop_duplicates(subset='comments', keep='first')
rev_name_df = rev_name_df.sort_values(by='reviewer_id')
rev_name_df


# In[9]:


# Export filtered data
rev_name_df.to_csv('fitered_rev_name_data.csv', index=False)
print (reviews_by_name(id_reviews_df, rev_name))

