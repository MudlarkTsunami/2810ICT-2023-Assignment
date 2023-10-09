import pandas as pd
import pytest
import Cleanliness as cln

# Test data
t_data = pd.DataFrame({
    'listing_id': [1, 1, 2, 2],
    'comments': [
        'Very clean and tidy!',
        'Absolutely spotless!',
        'Quite dirty and messy...',
        'So neat yet a bit dusty in corners...'
    ]
})

# Test keyword_filtered_reviews: Check Pos and Neg KW Filtering
def t_keyword_filtering():
    res_df = cln.keyword_filtered_reviews(t_data)
    assert all(res_df['comments'].apply(lambda x: any(keyword in x.lower() for keyword in cln.pos_keywords + cln.neg_keywords)))

# Test count_keywords_in_reviews: Validate Keyword Count
def t_count_keywords():
    res_df = cln.count_keywords_in_reviews(t_data.copy())
    assert 'pos_keyword_count' in res_df.columns
    assert 'neg_keyword_count' in res_df.columns
    assert res_df['pos_keyword_count'].iloc[0] == 2  # 'clean' and 'tidy' 1st col
    assert res_df['neg_keyword_count'].iloc[2] == 2  # 'dirty' and 'messy' 3rd col

# Test find_by_cleanliness: Check Grouping, Summ, and % Calc
def t_find_by_cleanliness():
    res_df = cln.find_by_cleanliness(t_data)
    assert 'pos_keyword_count' in res_df.columns
    assert 'neg_keyword_count' in res_df.columns
    assert 'pos_keyword_percentage' in res_df.columns

    # Check dataframe grouped by 'listing_id' & keyword counts sum
    assert res_df.loc[res_df['listing_id'] == 1, 'pos_keyword_count'].iloc[0] == 3 # Sum of positive keywords for listing_id 1

    # Check % calc
    assert res_df.loc[res_df['listing_id'] == 1, 'pos_keyword_percentage'].iloc[0] == 100 # 100% positive keywords for listing_id 1

# Execute tests
t_res = {"Passed": [], "Failed": []}

for t_func in [t_keyword_filtering, t_count_keywords, t_find_by_cleanliness]:
    try:
        t_func()
        print(f"{t_func.__name__}: Passed")
        t_res["Passed"].append(t_func.__name__)
    except AssertionError as e:
        print(f"{t_func.__name__}: Failed - {str(e)}")
        t_res["Failed"].append(t_func.__name__)

t_res