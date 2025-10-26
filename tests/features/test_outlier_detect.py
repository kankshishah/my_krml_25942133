# test_detect_outliers_iqr.py
import pytest
import pandas as pd
from my_krml_25942133.features.outlier_detect import detect_outliers_iqr  # adjust import path

@pytest.fixture
def sample_df():
    data = {
        "price": [10, 12, 11, 14, 100, 13, 15, 12],  # 100 is an outlier
        "quantity": [1, 2, 2, 3, 1, 2, 3, 2]
    }
    return pd.DataFrame(data)

def test_detect_outliers_iqr_detects_outlier(sample_df):
    """Test that outliers are correctly detected."""
    df_result, outliers = detect_outliers_iqr(sample_df, column="price")
    
    # Check that the boolean series has True for outliers
    assert outliers.sum() == 1
    assert outliers.iloc[4] == True  # 100 should be flagged
    assert isinstance(df_result, pd.DataFrame)
    assert df_result.shape[0] == sample_df.shape[0]  # original df returned

def test_detect_outliers_iqr_removes_outlier(sample_df):
    """Test that outliers are removed when remove=True."""
    df_result, outliers = detect_outliers_iqr(sample_df, column="price", remove=True)
    
    # 100 should be removed
    assert 100 not in df_result["price"].values
    assert df_result.shape[0] == sample_df.shape[0] - outliers.sum()

def test_detect_outliers_iqr_no_column(sample_df):
    """Test behavior when column does not exist."""
    with pytest.raises(KeyError):
        detect_outliers_iqr(sample_df, column="nonexistent")

def test_detect_outliers_iqr_empty_df():
    """Test behavior with an empty DataFrame."""
    empty_df = pd.DataFrame(columns=["price"])
    df_result, outliers = detect_outliers_iqr(empty_df, column="price")
    
    assert df_result.empty
    assert outliers.empty
