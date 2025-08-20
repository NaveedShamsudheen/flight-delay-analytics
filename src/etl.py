from pathlib import Path
import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Standard column names (adjust to your CSV)
    # Expect: FL_DATE, OP_CARRIER, ORIGIN, DEST, CRS_DEP_TIME, DEP_DELAY, ARR_DELAY, CANCELLED
    # Coerce times
    df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
    for c in ['DEP_DELAY','ARR_DELAY']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    if 'CANCELLED' in df.columns:
        df['CANCELLED'] = df['CANCELLED'].astype(float)
    # Hour & weekday
    if 'CRS_DEP_TIME' in df.columns:
        df['DEP_HOUR'] = (pd.to_numeric(df['CRS_DEP_TIME'], errors='coerce')//100).astype('Int64')
    df['WEEKDAY'] = df['FL_DATE'].dt.day_name()
    return df

def save_processed(df: pd.DataFrame, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

if __name__ == "__main__":
    df = load_data("data/flights.csv")
    save_processed(df, "data/processed.csv")
