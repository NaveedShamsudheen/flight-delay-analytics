from pathlib import Path
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    print(f"Loading {path}...")
    df = pd.read_csv(path, low_memory=False, parse_dates=["FL_DATE"])

    # Ensure required columns exist
    expected = {"FL_DATE", "DEP_DELAY", "ARR_DELAY", "CANCELLED"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    return df


def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:
    # Extract year-month
    df["year_month"] = df["FL_DATE"].dt.to_period("M").astype(str)

    # Compute KPIs
    monthly = (
        df.groupby("year_month")
        .agg(
            total_flights=("FL_DATE", "count"),
            avg_dep_delay=("DEP_DELAY", "mean"),
            avg_arr_delay=("ARR_DELAY", "mean"),
            cancel_rate=("CANCELLED", "mean"),
        )
        .reset_index()
    )

    # On-time rate = % flights with ARR_DELAY < 15 mins
    df["ontime"] = df["ARR_DELAY"].lt(15).astype(int)
    ontime = df.groupby("year_month")["ontime"].mean().reset_index()
    monthly = monthly.merge(ontime, on="year_month")
    monthly.rename(columns={"ontime": "ontime_rate"}, inplace=True)

    return monthly


def save_processed(df: pd.DataFrame, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved processed data to {out_path}")


if __name__ == "__main__":
    raw_path = "data/raw.csv"  # your raw dataset
    out_path = "data/processed.csv"  # smaller monthly summary
    df = load_data(raw_path)
    monthly = aggregate_monthly(df)
    save_processed(monthly, out_path)
