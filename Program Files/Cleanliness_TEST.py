
#Imports

import pandas as pd
import pytest
import Cleanliness as cln

# Sample data for testing
s_data = pd.DataFrame({
    'comments': [
        "The room was very clean and tidy",
        "The place was dirty and messy",
        "No comments",
        "Spotless and neat"
    ]
})

# Pos and Neg keywords
pos_keywords = ['clean', 'tidy', 'immaculate', 'sanitary', 'spotless', 'neat']
neg_keywords = ['dirty', 'dusty', 'filthy', 'messy', 'stained', 'unkempt']


def t_keyword_filtered_reviews():
    ft_df = cln.keyword_filtered_reviews(s_data, pos_keywords, neg_keywords)

    # Check returns DataFrame with expected rows
    assert len(ft_df) == 3


def t_count_keywords_in_reviews():
    ct_df = cln.count_keywords_in_reviews(s_data, pos_keywords, neg_keywords)

    # Check returns expected keyword counts
    assert ct_df['pos_keyword_count'].tolist() == [2, 0, 0, 2]
    assert ct_df['neg_keyword_count'].tolist() == [0, 2, 0, 0]

# Running tests
@pytest.mark.parametrize("test_func", [t_keyword_filtered_reviews, t_count_keywords_in_reviews])
def t_run(t_func):
    t_func()

# Execute tests
t_res = {"Passed": [], "Failed": []}

for t_func in [t_keyword_filtered_reviews, t_count_keywords_in_reviews]:
    try:
        t_run(t_func)
        t_res["Passed"].append(t_func.__name__)
    except AssertionError:
        t_res["Failed"].append(t_func.__name__)

t_res