#Imports

import pytest
import pandas as pd
import Keyword ip

# Sample data for testing
s_cal_data = pd.DataFrame({
    'date': pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-03']),
    'listing_id': [1, 2, 3],
})

sample_listings_data = pd.DataFrame({
    'id': [1, 2, 3],
    'summary': ['Nice place', 'Another place', 'Yet another place'],
    'space': ['Small', 'Medium', 'Large'],
    'description': ['Cozy', 'Affordable', 'Luxurious'],
})


# Tests
def t_keyword_f_listings():
    f_data = ip.keyword_filtered_listings(
        sample_listings_data, 'Nice', ['summary', 'description'])

    # Assertions
    assert len(f_data) == 1, "Incorrect number of rows in the keyword filtered data"
    assert 'Nice place' in f_data['summary'].values, "Expected keyword not found in summary"


def t_date_f_listings():
    f_data = ip.date_filtered_listings(s_cal_data, '2022-01-01', '2022-01-03')

    # Assertions
    assert len(f_data) == 3, "Incorrect number of rows in the filtered data"
    assert f_data['date'].min() == pd.to_datetime('2022-01-01'), "Incorrect minimum date"
    assert f_data['date'].max() == pd.to_datetime('2022-01-03'), "Incorrect maximum date"


def t_find_keyword_listings():
    k_f_data = ip.find_keyword_listings(
        sample_listings_data, s_cal_data, 'Nice', '2022-01-01', '2022-01-03')

    # Assertions
    assert len(k_f_data) == 1, "Incorrect number of rows in the keyword filtered data"
    assert 'Nice place' in k_f_data['summary'].values, "Expected keyword not found in summary"
    assert k_f_data['id'].values[0] == 1, "Incorrect id for the keyword filtered data"

@pytest.mark.parametrize("test_func", [t_keyword_f_listings, t_date_f_listings, t_find_keyword_listings])
def t_run(t_func):
    t_func()

# Execute tests
t_res = {"Passed": [], "Failed": []}

for t_func in [t_keyword_f_listings, t_date_f_listings, t_find_keyword_listings]:
    try:
        t_run(t_func)
        t_res["Passed"].append(t_func.__name__)
    except AssertionError:
        t_res["Failed"].append(t_func.__name__)

t_res