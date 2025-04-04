import pandas as pd
from project import normalized_df
from project import prepare_df_from_df
from project import merge_df

def test_prepare_df_from_df():
    raw_df = pd.DataFrame({
        "snapped_at": ["2023-01-01 UTC", "2023-01-02 UTC", "2023-01-03 UTC"],
        "price": [100, 110, 105],
        "volume": [12345, 23456, 34567] 
    })

    result = prepare_df_from_df(raw_df, "bitcoin")

    assert list(result.columns) == ["date", "bitcoin"]
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result["bitcoin"].tolist() == [100, 110, 105]
    assert len(result) == 3

def test_merge_df():
    df1 = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "bitcoin": [100, 110, 105]
    })

    df2 = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-02", "2023-01-03", "2023-01-04"]),
        "ethereum": [200, 210, 220]
    })

    df3 = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-03", "2023-01-04", "2023-01-05"]),
        "solana": [50, 55, 60]
    })

    merged = merge_df([df1, df2, df3])

    assert merged.shape[0] == 1
    assert list(merged.columns) == ["date", "bitcoin", "ethereum", "solana"]
    assert merged["date"].iloc[0] == pd.to_datetime("2023-01-03")
    assert merged["bitcoin"].iloc[0] == 105
    assert merged["ethereum"].iloc[0] == 210
    assert merged["solana"].iloc[0] == 50

def test_normalized_df():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "bitcoin": [100, 110, 120],
        "ethereum": [200, 180, 210]
    })

    norm = normalized_df(df)

    assert round(norm["bitcoin"].iloc[0], 2) == 100.00
    assert round(norm["bitcoin"].iloc[1], 2) == 110.00
    assert round(norm["bitcoin"].iloc[2], 2) == 120.00

    assert round(norm["ethereum"].iloc[0], 2) == 100.00
    assert round(norm["ethereum"].iloc[1], 2) == 90.00
    assert round(norm["ethereum"].iloc[2], 2) == 105.00

