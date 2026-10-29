# this is the testing for the cleaning pipeline, ensuring clean and accurate data upon work


import pandas as pd

from Functions.data_pipe import enforce_ranges


def test_enforce_ranges():
    df = pd.DataFrame({"weight": [49.0, 50.0, 500.0, 501.0]})
    schema = {"weight": {"min": 50.0, "max": 500.0}}
    
    result = enforce_ranges(df, schema)
    
    
    assert result["weight"].isna().tolist() == [True, False, False, True]