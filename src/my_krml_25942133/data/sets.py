import pandas as pd

def separate_columns(df):
    """
    Separate numeric and categorical columns from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.

    Returns
    -------
    num_cols : list
        List of numeric column names.
    cat_cols : list
        List of categorical column names.
    """

    df_copy = df.copy()
    num_cols = df_copy.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df_copy.select_dtypes(include=['object', 'category']).columns.tolist()

    return num_cols, cat_cols
