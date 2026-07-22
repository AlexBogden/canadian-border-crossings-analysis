import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
    WITH cte_year_totals AS (
        SELECT survey_year, count(*) AS total_responses
        FROM border_survey
        GROUP BY survey_year
    )
    SELECT purpose, bs.survey_year, count(*) AS responses,
        ROUND((count(*) * 100.0 / cte.total_responses), 1) AS percentage
    FROM border_survey AS bs
    JOIN cte_year_totals AS cte
        ON bs.survey_year = cte.survey_year
    WHERE purpose IN ('Purchase Gas', 'Shopping', 'Family Visit', 'Recreation/Vacation')
    GROUP BY purpose, bs.survey_year, cte.total_responses
    ORDER BY bs.survey_year, percentage DESC;
"""

df = pd.read_sql(query, conn)
conn.close()

df_pivot = df.pivot(index='survey_year', columns='purpose', values='percentage')

print(df_pivot)

plt.style.use('dark_background')

purposes = ['Purchase Gas', 'Shopping', 'Family Visit', 'Recreation/Vacation']
colors = ['#4C9BE8', '#F5A623', '#50C878', '#E8524C']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), sharey=True)

x = np.arange(len(purposes))
width = 0.35

# Summer pair: 2018 vs 2025
summer_2018 = [df_pivot.loc[2018, p] for p in purposes]
summer_2025 = [df_pivot.loc[2025, p] for p in purposes]
ax1.bar(x - width/2, summer_2018, width, label='Summer 2018', color='#2E9E8F')
ax1.bar(x + width/2, summer_2025, width, label='Summer 2025', color='#E8A23D')
ax1.set_xticks(x)
ax1.set_xticklabels(purposes, rotation=20, ha='right')
ax1.set_title('Summer 2018 vs Summer 2025')
ax1.set_ylabel('Share of Crossings (%)')
ax1.legend(fontsize=10)

# Winter pair: 2019 vs 2026
winter_2019 = [df_pivot.loc[2019, p] for p in purposes]
winter_2026 = [df_pivot.loc[2026, p] for p in purposes]
ax2.bar(x - width/2, winter_2019, width, label='Winter 2019', color='#2E9E8F')
ax2.bar(x + width/2, winter_2026, width, label='Winter 2026', color='#E8A23D')
ax2.set_xticks(x)
ax2.set_xticklabels(purposes, rotation=20, ha='right')
ax2.set_title('Winter 2019 vs Winter 2026')
ax2.legend(fontsize=10)

fig.suptitle('Trip Purpose Among Canadian Border Crossers: Season-Matched Comparison', fontsize=14)

fig.text(0.5, 0.02, 'Source: Border Policy Research Institute (BPRI), Western Washington University, in partnership with the International Mobility & Trade Corridor Program',
         ha='center', fontsize=8, color='gray')
plt.subplots_adjust(bottom=0.18, top=0.88, wspace=0.08)
plt.savefig('post8_purpose_season_matched.png', dpi=200, bbox_inches='tight')
plt.show()