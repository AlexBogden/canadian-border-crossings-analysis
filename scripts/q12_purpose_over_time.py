import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
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
    SELECT purpose, bs.survey_year, count(*) AS response, 
		ROUND(( count(*) * 100.0 / cte.total_responses), 1) AS percentage
        FROM border_survey AS bs
        JOIN cte_year_totals AS cte 
	        ON bs.survey_year = cte.survey_year
        WHERE purpose IN ('Recreation/Vacation', 'Family Visit', 'Shopping', 'Mail/Package', 'Purchase Gas', 'Work Commute')
        GROUP BY purpose, bs.survey_year, cte.total_responses
        ORDER BY survey_year, percentage desc;
"""

df = pd.read_sql(query, conn)

df_pivot = df.pivot(index='survey_year', columns='purpose', values='percentage')

conn.close()

print(df_pivot)

plt.style.use('dark_background')

ax = df_pivot.T.plot(kind='bar', figsize=(14, 7), color=['#4C9BE8', '#F5A623', '#50C878', '#E8524C'])

ax.set_xlabel('')
ax.set_ylabel('Share of Crossings (%)')
ax.legend(title='', fontsize=13)

ax.set_title('Trip Purpose Among Canadian Border Crossers: 2018–2026')
ax.title.set_fontsize(14)
ax.xaxis.label.set_fontsize(12)
ax.yaxis.label.set_fontsize(12)
ax.tick_params(axis='both', labelsize=11, rotation=0)

plt.figtext(0.5, 0.01, 'Source: Border Policy Research Institute (BPRI), Western Washington University', ha='center', fontsize=9, color='gray')
plt.subplots_adjust(bottom=0.12)
plt.savefig('q12_purpose_over_time.png', dpi=200, bbox_inches='tight')
plt.show()