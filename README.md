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

## Analytical Framework

This project works through a structured set of questions, moving from baseline trends to geographic breakdowns to event correlation and confounding factors. The questions cover year-over-year totals, measure type breakdowns, state and port-level geography, correlation with political events, exchange rate effects, and data quality. See `analysis.sql` for the full annotated query set.

## Key Findings

- Total Canadian land border crossings dropped 20% from 2024 to 2025 (69M to 55M)
- No early signal after the November 2024 election -- the decline began after tariffs were signed in February 2025
- The sharpest single-month drops occurred in July and August 2025, coinciding with the announcement and implementation of a 35% tariff
- Road travel accounted for nearly all of the decline; pedestrian and train passenger crossings actually increased year over year
- Vermont (-28.2%) and North Dakota (-26.6%) saw the steepest state-level percentage drops
- New York (-4.64M) and Washington (-3.93M) saw the largest raw declines
- Small, routine crossings like the Walpole-Algonac Ferry in Michigan (-42.4%) were hit harder on a percentage basis than high-volume tourist corridors like Niagara Falls

## LinkedIn Posts

This analysis is being shared progressively on LinkedIn as each section is completed.

- [Post 1: Year-over-year trends and measure type breakdown](https://www.linkedin.com/feed/update/urn:li:activity:7460829029156151296/)
- [Post 2: Sharpest monthly drops and travel mode analysis](https://www.linkedin.com/feed/update/urn:li:activity:7462951984451579904/)

## Status

Completed: Q1 through Q7 (baseline trends, measure type breakdown, state and port-level geography)
Upcoming: Event correlation, exchange rate analysis, and data quality review
