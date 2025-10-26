import pandas as pd

def detect_outliers_iqr(df: pd.DataFrame, column: str, remove: bool = False):
    """Identify and optionally remove outliers using the IQR method.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the data.
    column : str
        Name of the numeric column to check for outliers.
    remove : bool, optional
        If True, returns a DataFrame with outliers removed. Default is False.

    Returns
    -------
    pd.DataFrame
        Either the original DataFrame or a DataFrame with outliers removed.
    pd.Series
        Boolean series indicating which rows are outliers (True if outlier, False otherwise).
    """

    df_copy = df.copy()
    
    if column not in df_copy.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame.")
    
    Q1 = df_copy[column].quantile(0.25)
    Q3 = df_copy[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = (df_copy[column] < lower_bound) | (df_copy[column] > upper_bound)
    
    if remove:
        df_copy = df_copy.loc[~outliers].reset_index(drop=True)
    
    return df_copy, outliers
