# test_plot_correlation_matrix.py
import pytest
import pandas as pd
from my_krml_25942133.features.heatmap import plot_correlation_matrix  # adjust import path

@pytest.fixture
def sample_df():
    data = {
        "open": [10, 20, 30, 40],
        "high": [12, 22, 32, 42],
        "low": [9, 19, 29, 39],
        "close": [11, 21, 31, 41],
        "volume": [100, 200, 300, 400],
        "category": ["A", "B", "C", "D"]  # non-numeric column
    }
    return pd.DataFrame(data)

def test_plot_correlation_matrix_returns_df_and_ax(sample_df):
    """Test that function returns correlation matrix and Axes object."""
    corr_matrix, ax = plot_correlation_matrix(sample_df)
    
    # Check type of correlation matrix
    assert isinstance(corr_matrix, pd.DataFrame)
    
    # Check that returned Axes is a matplotlib AxesSubplot
    import matplotlib.axes
    assert isinstance(ax, matplotlib.axes.Axes)
    
    # Check that correlation matrix has correct shape
    numeric_cols = sample_df.select_dtypes(include="number").columns.tolist()
    assert corr_matrix.shape == (len(numeric_cols), len(numeric_cols))

def test_plot_correlation_matrix_specific_cols(sample_df):
    """Test selecting specific numeric columns."""
    selected_cols = ["open", "close"]
    corr_matrix, ax = plot_correlation_matrix(sample_df, numeric_cols=selected_cols)
    
    # Check correlation matrix shape matches selected columns
    assert corr_matrix.shape == (len(selected_cols), len(selected_cols))
    assert all(corr_matrix.columns == selected_cols)
    assert all(corr_matrix.index == selected_cols)

def test_plot_correlation_matrix_empty_df():
    """Test behavior when DataFrame is empty."""
    empty_df = pd.DataFrame()
    corr_matrix, ax = plot_correlation_matrix(empty_df)
    
    # Should return empty DataFrame
    assert corr_matrix.empty
