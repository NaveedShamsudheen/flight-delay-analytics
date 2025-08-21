import pandas as pd
from src.features import kpis


def test_kpis_runs():
    df = pd.DataFrame(
        {"ARR_DELAY": [0, 10, 20], "DEP_DELAY": [0, 5, 10], "CANCELLED": [0, 1, 0]}
    )
    out = kpis(df)
    assert "avg_arr_delay_min" in out and isinstance(out["avg_arr_delay_min"], float)
