import pandas as pd
import pytest
import Keyword as kw

# Test data
t_data_listings = pd.DataFrame({
    'id': [1, 2, 3],
    'summary': ['Nice place', 'Another place', 'Yet another place'],
    'space': ['Small', 'Medium', 'Large'],
    'description': ['Cozy', 'Affordable', 'Luxurious'],
})

t_data_calendar = pd.DataFrame({
    'date': pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-03']),
    'listing_id': [1, 2, 3],
})

# Test keyword_filtered_listings: Check function filters  listings in keyword.
def t_keyword_filtered_listings():
    res_df = kw.keyword_filtered_listings(t_data_listings, 'Nice', ['summary', 'space', 'description'])
    assert all(res_df['summary'].apply(lambda x: 'Nice' in x))

# Test date_filtered_listings: function filters listings in  date range.
def t_date_filtered_listings():
    res_df = kw.date_filtered_listings(t_data_calendar, '2022-01-01', '2022-01-02')
    assert all((res_df['date'] > '2022-01-01') & (res_df['date'] < '2022-01-02'))

# Test find_keyword_listings: Check function merges filtered dataframes properly .
def t_find_keyword_listings():
    res_df = kw.find_keyword_listings(t_data_listings, t_data_calendar, 'Nice', '2022-01-01', '2022-01-03')
    assert all(res_df['summary'].apply(lambda x: 'Nice' in x))
    assert all((res_df['date'] > '2022-01-01') & (res_df['date'] < '2022-01-03'))

# Execute tests
t_res = {"Passed": [], "Failed": []}

for t_func in [t_keyword_filtered_listings, t_date_filtered_listings, t_find_keyword_listings]:
    try:
        t_func()
        print(f"{t_func.__name__}: Passed")
        t_res["Passed"].append(t_func.__name__)
    except AssertionError as e:
        print(f"{t_func.__name__}: Failed - {str(e)}")
        t_res["Failed"].append(t_func.__name__)

t_res