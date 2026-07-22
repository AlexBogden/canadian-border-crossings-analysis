import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

query = """
    WITH cte_monthly_crossings AS (
        SELECT date, SUM(value) AS total_crossings
        FROM border_crossings
        WHERE measure != 'Trucks'
            AND border = 'US-Canada Border'
        GROUP BY date
    )
    SELECT TO_DATE(m.date, 'Mon-YY') AS period, m.total_crossings, er.cad_usd AS exchange_rate
        FROM cte_monthly_crossings AS m
        JOIN exchange_rates AS er
            ON TO_DATE(m.date, 'Mon-YY') = er.observation_date
        ORDER BY period
"""

df = pd.read_sql(query, conn)
df['period'] = pd.to_datetime(df['period'])

conn.close()

df = df[df['period'] >= pd.Timestamp('2024-01-01')]

fig, ax1 = plt.subplots(figsize=(14, 7))
ax2 = ax1.twinx()

ax1.plot(df['period'], df['total_crossings'], color='steelblue', linewidth=2, label='Monthly Crossings')
ax2.plot(df['period'], df['exchange_rate'], color='red', linewidth=2, label='CAD/USD Rate')

ax1.set_ylabel('Monthly Crossings', color='steelblue')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
ax2.set_ylabel('CAD per 1 USD', color='red')

ax1.set_title('Canadian Land Border Crossings vs CAD/USD Exchange Rate: 2024–2026', fontsize=13, fontweight='bold')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45, ha='right')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')



events = [
    ('2025-02-01', 'Feb 2025\n25% tariffs signed'),
    ('2025-08-01', '35% tariff\ntakes effect'),
    ('2025-10-01', 'Oct 2025\n+10% tariff'),
]

for date, label in events:
    ax1.axvline(pd.Timestamp(date), color='gray', linestyle='--', linewidth=1, alpha=0.7)
    ax1.text(pd.Timestamp(date), ax1.get_ylim()[1] * 0.85, label, fontsize=7, color='gray', ha='center')



fig.text(0.5, 0.01, 'Sources: Bureau of Transportation Statistics (BTS) Border Crossing Entry Data; Federal Reserve Bank of St. Louis (FRED) DEXCAUS', 
         ha='center', fontsize=7, color='gray')

plt.tight_layout()
plt.savefig('q10_exchange_rate_chart.png', dpi=150, bbox_inches='tight')
plt.show()