import pytest
import pandas as pd

from scripts.utils import trim_dataframe_at_string


# write test cases for trim_dataframe_at_string function
# dataframes with 'Total' in different columns and rows
@pytest.fixture
def sample_dataframes():
    return {
        "case_1": pd.DataFrame({
            "A": [1, 2, 3, "Total", 5],
            "B": [6, 7, 8, 9, 10]
        }),
        "case_2": pd.DataFrame({
            "A": [1, 2, "Total", 4, 5],
            "B": [6, 7, 8, 9, 10]
        }),
        "case_3": pd.DataFrame({
            "A": [1, 2, 3, 4, "Total"],
            "B": [6, 7, 8, 9, 10]
        }),
        "case_4": pd.DataFrame({
            "A": ["Total", 2, 3, 4, 5],
            "B": [6, 7, 8, 9, 10]
        }),
        "case_5": pd.DataFrame({
            "A": [1, 2, 3],
            "B": [None, None, None]
        })
    }
@pytest.fixture
def expected_results():
    return {
        "case_1": (3,2),
        "case_2": (2,2),
        "case_3": (4,2),
        "case_4": (0,2),
        "case_5": (3,2),
    }
@pytest.mark.parametrize("case", ["case_1", "case_2", "case_3", "case_4", "case_5"])
def test_trim_dataframe_at_string(sample_dataframes, expected_results, case):
    df = sample_dataframes[case]
    expected_df = expected_results[case]
    
    # Call the function to test
    trimmed_df = trim_dataframe_at_string(df)
    print(trimmed_df)

    assert trimmed_df.shape == expected_results[case]
