import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
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
    SELECT TO_DATE(date, 'Mon-YY') AS date, SUM(value) AS crossings
    FROM border_crossings
    WHERE measure != 'Trucks'
        AND border = 'US-Canada Border'
        AND (date LIKE '%-24' OR date LIKE '%-25' OR date LIKE '%-26')
    GROUP BY date
    ORDER BY date;
"""

df = pd.read_sql(query, conn)
conn.close()

df['date'] = pd.to_datetime(df['date'])

fig, ax = plt.subplots(figsize=(14, 9))
ax.plot(df['date'], df['crossings'], color='steelblue', linewidth=2)
ax.margins(x=0.02)
ax.set_xlim(datetime(2024, 1, 1), datetime(2026, 4, 1))

events = [
    (datetime(2024, 11, 1), 'Nov 2024: 25% tariff threat announced'),
    (datetime(2025, 1, 1), 'Jan 2025: CAD hits 2025 low; Canada overtakes US on Henley Index'),
    (datetime(2025, 2, 1), 'Feb 2025: 25% tariffs signed; Trudeau urges travel boycott'),
    (datetime(2025, 3, 1), 'Mar 2025: 25% tariffs take effect'),
    (datetime(2025, 4, 1), 'Apr 2025: Carney wins federal election'),
    (datetime(2025, 7, 1), 'Jul 2025: 35% tariff threatened'),
    (datetime(2025, 8, 1), 'Aug 2025: 35% tariff takes effect'),
    (datetime(2025, 10, 1), 'Oct 2025: Additional 10% tariff announced'),
    (datetime(2026, 1, 1), 'Jan 2026: 50% tariff threat over China deal'),
]

for i, (date, label) in enumerate(events, start=1):
    ax.axvline(x=date, color='red', linestyle='--', linewidth=0.8, alpha=0.6)
    ax.text(date - pd.Timedelta(days=5), ax.get_ylim()[1] * 0.98, str(i), rotation=0,
        fontsize=10, fontweight='bold', color='red', ha='right', va='top')


ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45, ha='right')

ax.set_title('Canadian Land Border Crossings 2024-2026', fontsize=14, fontweight='bold')
ax.set_ylabel('Monthly Crossings')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))

legend_text = '\n'.join([f'{i+1}. {label}' for i, (_, label) in enumerate(events)])
fig.text(0.5, 0.06, legend_text, ha='center', fontsize=9,
         verticalalignment='bottom')
fig.text(0.5, 0.03, 'Source: Bureau of Transportation Statistics (BTS) Border Crossing Entry Data',
         ha='center', fontsize=7, color='gray', verticalalignment='bottom')
plt.subplots_adjust(bottom=0.35)
plt.savefig('q8_events_timeline_chart.png', dpi=150, bbox_inches='tight')
plt.show()