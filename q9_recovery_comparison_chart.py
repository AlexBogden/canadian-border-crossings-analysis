import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    WITH cte_monthly_totals AS (
        SELECT date, SUM(value) AS crossings
        FROM border_crossings
        WHERE measure != 'Trucks'
            AND border = 'US-Canada Border'
            AND (date LIKE '%-24' OR date LIKE '%-25' OR date LIKE '%-26')
        GROUP BY date
    )
    SELECT LEFT(a.date, 3) AS month,
        a.crossings AS crossings_2024,
        b.crossings AS crossings_2025,
        c.crossings AS crossings_2026
    FROM cte_monthly_totals AS a
    JOIN cte_monthly_totals AS b
        ON LEFT(a.date, 3) = LEFT(b.date, 3) AND RIGHT(a.date, 2) = '24' AND RIGHT(b.date, 2) = '25'
    JOIN cte_monthly_totals AS c
        ON LEFT(a.date, 3) = LEFT(c.date, 3) AND RIGHT(a.date, 2) = '24' AND RIGHT(c.date, 2) = '26'
    ORDER BY TO_DATE(a.date, 'Mon-YY');
"""

df = pd.read_sql(query, conn)
conn.close()

months = df['month'].tolist()
crossings_2024 = df['crossings_2024'].tolist()
crossings_2025 = df['crossings_2025'].tolist()
crossings_2026 = df['crossings_2026'].tolist()

x = np.arange(len(months))
width = 0.25

fig, ax = plt.subplots(figsize=(14, 9))

bars_2024 = ax.bar(x - width, crossings_2024, width, label='2024', color='steelblue')
bars_2025 = ax.bar(x, crossings_2025, width, label='2025', color='orange')
bars_2026 = ax.bar(x + width, crossings_2026, width, label='2026', color='green')

for i in range(len(months)):
    pct_25 = (crossings_2025[i] - crossings_2024[i]) / crossings_2024[i] * 100
    pct_26 = (crossings_2026[i] - crossings_2025[i]) / crossings_2025[i] * 100

    color_25 = 'green' if pct_25 > 0 else 'red'
    color_26 = 'green' if pct_26 > 0 else 'red'

    ax.text(x[i], crossings_2025[i] + 30000, f'{pct_25:+.1f}%',
            ha='center', va='bottom', fontsize=9, fontweight='bold', color=color_25)
    ax.text(x[i] + width, crossings_2026[i] + 30000, f'{pct_26:+.1f}%',
            ha='center', va='bottom', fontsize=9, fontweight='bold', color=color_26)

ax.set_title('Canadian Land Border Crossings: Q1 2024 vs 2025 vs 2026', fontsize=14, fontweight='bold')
ax.set_ylabel('Monthly Crossings')
ax.set_xticks(x)
ax.set_xticklabels(months)
ax.set_ylim(0, max(crossings_2024) * 1.15)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
ax.legend()

fig.text(0.5, 0.055, '% labels show year-over-year change vs prior year',
         ha='center', fontsize=9, color='gray')
fig.text(0.5, 0.02, 'Source: Bureau of Transportation Statistics (BTS) Border Crossing Entry Data',
         ha='center', fontsize=7, color='gray')
plt.subplots_adjust(bottom=0.1)
plt.savefig('q9_recovery_comparison_chart.png', dpi=150, bbox_inches='tight')
plt.show()