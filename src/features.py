import pandas as pd


def kpis(df: pd.DataFrame) -> dict:
    n = len(df)
    avg_dep = df["DEP_DELAY"].mean(skipna=True)
    avg_arr = df["ARR_DELAY"].mean(skipna=True)
    cancel_rate = (df["CANCELLED"].mean() * 100) if "CANCELLED" in df.columns else 0
    ontime_rate = df["ARR_DELAY"].lt(15).mean() * 100
    return {
        "total_flights": int(n),
        "avg_dep_delay_min": round(avg_dep, 2),
        "avg_arr_delay_min": round(avg_arr, 2),
        "cancel_rate_pct": round(cancel_rate, 2),
        "ontime_rate_pct": round(ontime_rate, 2),
    }


def group_delay(df: pd.DataFrame, by="OP_CARRIER", target="ARR_DELAY"):
    g = df.groupby(by)[target].mean(numeric_only=True).sort_values()
    return g.reset_index().rename(columns={target: "mean_delay"})
