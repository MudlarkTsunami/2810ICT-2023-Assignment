import pandas as pd
import pytest
import Price_Distribution as pdist

# Sample Data
s_calendar_data = pd.DataFrame({
    'date': pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-03']),
    'listing_id': [1, 2, 3],
    'available': ['t', 'f', 't'],
    'price': ['$100', '$150', '$200']
})


# Tests

# Test function filters listings in date range
def t_date_range_filter():
    s_date = '2022-01-01'
    e_date = '2022-01-02'
    res_df = pdist.date_filtered_listings(s_calendar_data, s_date, e_date)
    assert all((res_df['date'] >= s_date) & (res_df['date'] <= e_date))

 # Test how function handles empty dataframe
def t_handle_empty_dataframe():
    s_date = '2022-01-01'
    e_date = '2022-01-02'
    empty_df = pd.DataFrame(columns=['date', 'listing_id', 'available', 'price'])
    res_df = pdist.date_filtered_listings(empty_df, s_date, e_date)
    assert res_df.empty

# Test check different  date format.
def t_different_date_format():
    s_date = '01-01-2022'
    e_date = '02-01-2022'
    res_df = pdist.date_filtered_listings(s_calendar_data, s_date, e_date)
    assert not res_df.empty


# Execute tests
t_res = {"Passed": [], "Failed": []}

for t_func in [t_date_range_filter, t_handle_empty_dataframe, t_different_date_format]:
    try:
        t_func()
        print(f"{t_func.__name__}: Passed")
        t_res["Passed"].append(t_func.__name__)
    except AssertionError as e:
        print(f"{t_func.__name__}: Failed - {str(e)}")
        t_res["Failed"].append(t_func.__name__)

t_res