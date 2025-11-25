import argparse
import pandas as pd
from utils.ats_model import train_ats_model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to training CSV file")
    args = parser.parse_args()

    csv_path = args.csv
    print(f"[INFO] Loading CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"[INFO] Loaded {len(df)} rows")

    print("[INFO] Training ATS model...")
    train_ats_model(df=df)
    print("[SUCCESS] Training complete!")

if __name__ == "__main__":
    main()
