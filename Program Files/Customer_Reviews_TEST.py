# NOT USED DUE TO REFORMATTING OF "Customer_Reviews.py" FILE
"""
#Import
import pandas as pd
import pytest
import Customer_Reviews as cr

# Test Sample data
s_data = pd.DataFrame({
    'reviewer_name': ['Alice', 'Bob', 'Alice', 'Charlie'],
    'comments': ['Great!', 'Not good!', 'Lovely!', 'Horrible!'],
})

# Test functions

def t_rev_by_name():
    # Test that the function returns the correct subset of the DataFrame
    a_reviews = reviews_by_name(s_data, 'Alice')
    assert a_reviews.shape == (2, 2), "Shape mismatch for 'Alice'"
    assert a_reviews['reviewer_name'].tolist() == ['Alice', 'Alice'], "Reviewer name mismatch for 'Alice'"
    assert a_reviews['comments'].tolist() == ['Great!', 'Lovely!'], "Comments mismatch for 'Alice'"

    # Test with a name that is not in the DataFrame
    no_reviews = reviews_by_name(s_data, 'NoName')
    assert no_reviews.shape == (0, 2), "Shape mismatch for 'NoName'"


# Running the test and capturing the results

@pytest.mark.parametrize("test_func", [t_rev_by_name])
def t_run(t_func):
    t_func()

# Execute tests
t_res = {"Passed": [], "Failed": []}

for t_func in [t_rev_by_name]:
    try:
        t_run(t_func)
        t_res["Passed"].append(t_func.__name__)
    except AssertionError:
        t_res["Failed"].append(t_func.__name__)

t_res

"""
