import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from dotenv import load_dotenv

plt.style.use('dark_background')

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

query = """
    WITH cte_port_totals AS (
        SELECT port_name, state, port_code, RIGHT(date,2) AS YEAR, SUM(value) AS total_crossings
        FROM border_crossings
        WHERE measure != 'Trucks'
            AND border = 'US-Canada Border'
            AND (date LIKE '%-25' OR date LIKE '%-26')
            AND port_code IN ('212', '3023', '3424', '704', '3801', '104')
            AND LEFT(date, 3) IN ('Jan', 'Feb', 'Mar', 'Apr')
        GROUP BY port_name, state, port_code, year
    ),
    cte_state_totals AS (
        SELECT state, RIGHT(date, 2) AS YEAR, SUM(value) AS total_crossings
        FROM border_crossings
        WHERE measure != 'Trucks'
            AND border = 'US-Canada Border'
            AND (date LIKE '%-25' OR date LIKE '%-26')
            AND LEFT(date, 3) IN ('Jan', 'Feb', 'Mar', 'Apr')
        GROUP BY state, year
    )
    SELECT 
        p25.state, p25.port_name, p25.port_code,
        p25.total_crossings AS port_total_2025, p26.total_crossings AS port_total_2026,
        (p26.total_crossings - p25.total_crossings) AS port_diff,
        s25.total_crossings AS state_total_2025, s26.total_crossings AS state_total_2026,
        (s26.total_crossings - s25.total_crossings) AS state_diff
    FROM cte_port_totals AS p25
    JOIN cte_port_totals AS p26
        ON p25.port_code = p26.port_code AND p25.year = '25' AND p26.year = '26'
    JOIN cte_state_totals AS s25
        ON p25.state = s25.state AND s25.year = '25'
    JOIN cte_state_totals AS s26
        ON p25.state = s26.state AND s26.year = '26'
    ORDER BY port_diff DESC
"""

df = pd.read_sql(query, conn)
conn.close()

# Limit to the four larger recovering ports for chart clarity; Baudette and
# Jackman's port_diff values are small enough to be hard to read at this scale
df = df[df['port_name'].isin(['Detroit', 'Highgate Springs', 'Kenneth G Ward', 'Massena'])]
df['label'] = df['port_name'] + ', ' + df['state'].map({
    'Michigan': 'MI', 'Vermont': 'VT', 'Washington': 'WA', 'New York': 'NY'
})

x = np.arange(len(df))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

bars_port = ax.bar(x - width/2, df['port_diff'], width, label='Port change', color="#1D9E51")
bars_state = ax.bar(x + width/2, df['state_diff'], width, label='State change', color="#C3695B")

ax.axhline(0, color='#444441', linewidth=0.8)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, pos: f'{val/1000:,.0f}k'))

ax.set_ylabel('Change in crossings, Jan-Apr 2025 to 2026')
ax.set_xticks(x)
ax.set_xticklabels(df['label'])
ax.legend(frameon=False, loc='lower left')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

def label_bars(bars):
    for bar in bars:
        height = bar.get_height()
        va = 'bottom' if height >= 0 else 'top'
        offset = 3 if height >= 0 else -3
        ax.annotate(f'{height:+,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, offset),
                    textcoords="offset points",
                    ha='center', va=va, fontsize=8, color='#444441')

label_bars(bars_port)
label_bars(bars_state)

fig.text(0.5, 0.01, 'Source: Bureau of Transportation Statistics (BTS) Border Crossing Entry Data',
          ha='center', fontsize=7, color='gray')

plt.tight_layout()
plt.savefig('q11_port_vs_state_recovery.png', dpi=200, bbox_inches='tight')
plt.show()
print("Saved chart")
