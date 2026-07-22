import pandas as pd
from pathlib import Path

script_dir = Path(__file__).parent

raw_path = script_dir.parent / 'data' / 'raw' / 'Border_Crossing_Entry_Data_20260707.csv'

processed_path = script_dir.parent / 'data' / 'processed' / 'bts_cleaned_20260707.csv' 

df = pd.read_csv(raw_path, dtype={'Port Code': str})

print(repr(df.loc[df['Port Name'] == 'Jackman', 'Date'].values))

df['Value'] = df['Value'].str.replace(',' , '') 

df['Value'] = df['Value'].astype(int)

df['Date'] = df['Date'].str.replace(r'^(\d{2})-(\w{3})$', r'\2-\1', regex=True)

df.to_csv(processed_path, index=False)