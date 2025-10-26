import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation_matrix(df, numeric_cols=None, figsize=(10, 8), cmap="coolwarm"):
    """Plot a correlation matrix for numeric variables in a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the data.
    numeric_cols : list of str, optional
        List of numeric columns to include in the correlation matrix.
        If None, all numeric columns in df will be used.
    figsize : tuple, optional
        Figure size for the plot. Default is (10, 8).
    cmap : str, optional
        Color map for the heatmap. Default is "coolwarm".

    Returns
    -------
    pd.DataFrame
        Correlation matrix of the selected numeric variables.
    matplotlib.axes._subplots.AxesSubplot
        Axes object of the heatmap.
    matplotlib.figure.Figure
        Matplotlib figure object (useful for testing or saving).
    """

    df_copy = df.copy()

    # If numeric_cols is None, select all numeric columns
    if numeric_cols is None:
        numeric_cols = df_copy.select_dtypes(include="number").columns.tolist()

    corr_matrix = df_copy[numeric_cols].corr()

    # Create figure and axes even if empty
    fig, ax = plt.subplots(figsize=figsize)

    if not corr_matrix.empty:
        sns.heatmap(corr_matrix, annot=True, cmap=cmap, fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Correlation Matrix")
    else:
        ax.set_title("Empty Correlation Matrix")
        ax.axis("off")  # hide axes for empty plot

    return corr_matrix, ax, fig
