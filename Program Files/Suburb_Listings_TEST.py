#Import Libraries
import pandas as pd
import pytest
import Suburb_Listings as sl

# Sample data
s_l_data = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['Place 1', 'Place 2', 'Place 3', 'Place 4'],
    'suburb': ['SuburbA', 'SuburbB', 'SuburbA', 'SuburbC'],
    'price': ['$100', '$150', '$200', '$250']
})

s_s_data = ['SuburbA', 'SuburbB', 'SuburbC']

# Test convert_price_to_number
def t_convert_price_to_number():
    assert sl.convert_price_to_number('$100') == 100

# Test calculate_average_price
def t_calculate_average_price():
    assert sl.calculate_average_price(s_l_data['price']) == 175  # Assuming the function averages all prices

# Test filter_listings_by_suburb
def t_filter_listings_by_suburb():
    f_df = sl.filter_listings_by_suburb(s_l_data, 'SuburbA')
    assert all(f_df['suburb'] == 'SuburbA')

# Test get_suburb_listing
def t_get_suburb_listing():
    sub_data = sl.get_suburb_listing('SuburbA', s_l_data)

    # Assuming average price and suburb count
    assert sub_data['average_price'].iloc[0] == 150  # Placeholder for expected average price
    assert sub_data['count'].iloc[0] == 2  # Placeholder for expected count

# Test get_all_suburbs_average_price
def t_get_all_suburbs_average_price():
    all_subs_data = sl.get_all_suburbs_average_price(s_s_data, s_l_data)

    # Expected values for each suburb
    exp_values = {
        'SuburbA': {'average_price': 150, 'count': 2},
        'SuburbB': {'average_price': 150, 'count': 1},
        'SuburbC': {'average_price': 250, 'count': 1},
    }

    # Check all suburbs avg price and count
    for suburb, values in exp_values.items():
        sub_data = all_subs_data[all_subs_data['suburb'] == suburb]
        assert sub_data['average_price'].iloc[0] == values['average_price']
        assert sub_data['count'].iloc[0] == values['count']

# Execute tests
t_res = {"Passed": [], "Failed": []}

for t_func in [t_convert_price_to_number, t_calculate_average_price, t_filter_listings_by_suburb, t_get_suburb_listing, t_get_all_suburbs_average_price]:
    try:
        t_func()
        print(f"{t_func.__name__}: Passed")
        t_res["Passed"].append(t_func.__name__)
    except AssertionError as e:
        print(f"{t_func.__name__}: Failed - {str(e)}")
        t_res["Failed"].append(t_func.__name__)

t_res