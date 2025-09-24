import pytest
import pandas as pd

from my_krml_25942133.data.sets import separate_columns


@pytest.fixture
def df_fixture():
    data = [
        [1, 25, "Junior"],
        [2, 33, "Confirmed"],
        [3, 42, "Manager"],
    ]
    return pd.DataFrame(data, columns=["employee_id", "age", "level"])


def test_separate_columns_basic(df_fixture):
    num_cols, cat_cols = separate_columns(df_fixture)

    assert num_cols == ["employee_id", "age"]
    assert cat_cols == ["level"]


def test_separate_columns_empty_df():
    df_empty = pd.DataFrame()
    num_cols, cat_cols = separate_columns(df_empty)

    assert num_cols == []
    assert cat_cols == []


def test_separate_columns_all_numeric():
    df_num = pd.DataFrame({"a": [1,2], "b":[3,4]})
    num_cols, cat_cols = separate_columns(df_num)

    assert num_cols == ["a", "b"]
    assert cat_cols == []


def test_separate_columns_all_categorical():
    df_cat = pd.DataFrame({"x": ["a","b"], "y":["c","d"]})
    num_cols, cat_cols = separate_columns(df_cat)

    assert num_cols == []
    assert cat_cols == ["x", "y"]


def test_separate_columns_none_df():
    with pytest.raises(AttributeError):
        separate_columns(None)
