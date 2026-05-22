# Canadian Border Crossings Analysis

**Author**: Alex Bogden | [LinkedIn](https://www.linkedin.com/in/alex-bogden/)

SQL analysis of Canadian land border crossing trends from 2024 to 2026, using publicly available data from the Bureau of Transportation Statistics (BTS).

## Project Background

Following the introduction of US tariffs on Canadian imports in early 2025 and the subsequent Canadian travel boycott, Canadian land border crossings into the US declined significantly. This project uses SQL to quantify that decline, identify when it started, which travel modes were most affected, and which states and ports of entry saw the largest drops.

## Data Source

- **Source**: Bureau of Transportation Statistics (BTS) Border Crossing Entry Data
- **URL**: https://data.bts.gov/stories/s/Border-Crossing-Entry-Data/jswi-2e7b/
- **Coverage**: Monthly inbound crossings at US ports of entry, 1996 to present
- **Note**: This dataset captures inbound crossings into the US only. Outbound data is not collected.

## Tools

- PostgreSQL
- DBeaver
- Python (psycopg2, pandas, matplotlib)

## Analytical Framework

This project works through a structured set of questions, moving from baseline trends to geographic breakdowns to event correlation and confounding factors. The questions cover year-over-year totals, measure type breakdowns, state and port-level geography, correlation with political events, exchange rate effects, port-level recovery patterns, and data quality. See `border_crossings_analysis.sql` for the full annotated query set.

## Key Findings

- Total Canadian land border crossings dropped 20% from 2024 to 2025 (69M to 55M)
- No early signal in late 2024 -- the decline began after tariffs were signed in February 2025
- The sharpest single-month drops occurred in July and August 2025, coinciding with the announcement and implementation of a 35% tariff
- Road travel accounted for nearly all of the decline; pedestrian and train passenger crossings actually increased year over year
- Vermont (-28.2%) and North Dakota (-26.6%) saw the steepest state-level percentage drops
- New York (-4.64M) and Washington (-3.93M) saw the largest raw declines
- Small, routine crossings like the Walpole-Algonac Ferry in Michigan (-42.4%) were hit harder on a percentage basis than high-volume tourist corridors like Niagara Falls
- Crossings dropped at each tariff escalation, with 2026 tracking below even the depressed 2025 levels -- 14 consecutive months of year-over-year decline confirmed through March 2026
- April 2026 turned positive year-over-year (+10.2% vs April 2025), breaking the streak -- though it remains 18.1% below April 2024 and below every pre-COVID April on record
- CAD/USD exchange rate movements appear to follow crossing declines rather than lead them, pointing toward policy events as the primary driver
- Of 32 qualifying ports, only 6 showed positive year-over-year change in January-April 2026 vs 2025 -- and none of those gains appear at the state level

## LinkedIn Posts

This analysis is being shared progressively on LinkedIn as each section is completed.

- [Post 1: Year-over-year totals](https://www.linkedin.com/feed/update/urn:li:activity:7460829029156151296/)
- [Post 2: Sharpest monthly drops and travel mode breakdown](https://www.linkedin.com/feed/update/urn:li:activity:7462951984451579904/)
- [Post 3: State and port-level geography](https://www.linkedin.com/feed/update/urn:li:activity:7463675567435935745/)
- [Post 4: Monthly trend correlation with political events](https://www.linkedin.com/feed/update/urn:li:activity:7465524856168595456/)
- [Post 5: First year-over-year gain and what it does and doesn't mean](https://www.linkedin.com/feed/update/urn:li:activity:7468767226439897088/)
- [Post 6: CAD/USD exchange rate as a competing explanation](https://www.linkedin.com/feed/update/urn:li:activity:7470533020140150785/)
- [Post 7: Port-level recovery -- how narrow, and why](https://www.linkedin.com/feed/update/urn:li:activity:7473396620609474560/)

## Status

Completed: Baseline trends, travel mode breakdown, state and port-level geography, event correlation, exchange rate analysis, and port-level recovery  

Upcoming: Data quality review, passenger vehicle survey data from the Border Policy Research Institute at Western Washington University, and air travel analysis