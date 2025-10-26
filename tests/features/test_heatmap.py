# tests/features/test_heatmap.py
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

def test_plot_correlation_matrix_default(sample_df):
    corr_matrix, ax, fig = plot_correlation_matrix(sample_df)

    # Check correlation matrix type
    assert isinstance(corr_matrix, pd.DataFrame)

    # Check axes type
    import matplotlib.axes
    assert isinstance(ax, matplotlib.axes.Axes)

    # Check figure type
    import matplotlib.figure
    assert isinstance(fig, matplotlib.figure.Figure)

    # Correlation matrix shape should match number of numeric columns
    numeric_cols = sample_df.select_dtypes(include="number").columns.tolist()
    assert corr_matrix.shape == (len(numeric_cols), len(numeric_cols))

def test_plot_correlation_matrix_specific_cols(sample_df):
    selected_cols = ["open", "close"]
    corr_matrix, ax, fig = plot_correlation_matrix(sample_df, numeric_cols=selected_cols)

    assert corr_matrix.shape == (len(selected_cols), len(selected_cols))
    assert all(corr_matrix.columns == selected_cols)
    assert all(corr_matrix.index == selected_cols)

def test_plot_correlation_matrix_empty_df():
    empty_df = pd.DataFrame()
    corr_matrix, ax, fig = plot_correlation_matrix(empty_df)

    assert corr_matrix.empty
    import matplotlib.figure
    assert isinstance(fig, matplotlib.figure.Figure)
