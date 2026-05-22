/*
 * SETUP: Creates and populates the border_crossings table
 * 
 * Data source: Bureau of Transportation Statistics (BTS) Border Crossing Entry Data
 * 
 * URL: https://data.bts.gov/stories/s/Border-Crossing-Entry-Data/jswi-2e7b/
 *
 * Note: Update the file path in the COPY statement to match your local CSV location
 */


CREATE TABLE border_crossings (
	port_name VARCHAR(100), 
	state VARCHAR(50),
	port_code VARCHAR(50),
	border VARCHAR(50),
	date VARCHAR(10),
	measure VARCHAR(100),
	value NUMERIC,
	latitude NUMERIC(10, 6),
	longitude NUMERIC(10, 6),
	point TEXT
);

ALTER TABLE border_crossings 
ALTER COLUMN value TYPE NUMERIC;

COPY border_crossings
FROM 'YOUR_FILE_PATH_HERE/Border_Crossing_Entry_Data.csv'
DELIMITER ','
CSV HEADER;



/* 
 * Q1: Total Canadian land border crossings by year from 2024 to 2026, excluding commercial
 * trucks
 */
SELECT ''''||RIGHT(date,2) AS YEAR, SUM(value) AS total_crossings
	FROM border_crossings 
	WHERE measure != 'Trucks' 
		AND border = 'US-Canada Border'
		AND (date LIKE '%-26' OR date LIKE '%-25' OR date LIKE '%-24')
	GROUP BY RIGHT(date, 2);



/* 
 * Q2: Compares Nov/Dec 2023 vs Nov/Dec 2024 to check for an early decline signal following 
 * the 2024 US presidential election
 */
SELECT date, SUM(value)
    FROM border_crossings
    WHERE measure != 'Trucks'
        AND border = 'US-Canada Border'
        AND (date LIKE 'Nov-23' OR date LIKE 'Dec-23' OR date LIKE 'Nov-24' OR date LIKE 'Dec-24')
    GROUP BY date
    ORDER BY date;



/* 
 * Q3: Finds the sharpest single-month drop in Canadian land border crossings between 2024
 *  and 2025 using a CTE and self-join
 */
WITH CTE_monthly_totals AS (
	SELECT date, SUM(value) AS crossings
		FROM border_crossings
		WHERE measure != 'Trucks'
			AND border = 'US-Canada Border'
			AND (date LIKE '%-24' OR date LIKE '%-25')
		GROUP BY date
	)
SELECT LEFT(a.date, 3) AS "month", a.crossings AS "2024_crossings", b.crossings AS "2025_crossings", (a.crossings - b.crossings) AS DROP
	FROM CTE_monthly_totals AS a
	JOIN CTE_monthly_totals AS b
		ON LEFT(a.date, 3) = LEFT(b.date, 3) AND RIGHT(a.date, 2) = '24' AND right(b.date,2) = '25'
ORDER BY (a.crossings - b.crossings) DESC;



/* 
 * Q4: Finds the largest decline in Canadian land border crossings by measure type between 
 * 2024 and 2025 using a CTE and self-join
 */
 
WITH CTE_measure_totals AS (
	SELECT '20'||RIGHT(date,2) AS year, SUM(value) AS total_crossings, measure
		FROM border_crossings
		WHERE measure != 'Trucks' 
			AND border = 'US-Canada Border'
			AND (date LIKE '%-24' OR date LIKE '%-25')
		GROUP BY RIGHT(date,2), measure
		)
SELECT a.measure, a.total_crossings AS total_2024, b.total_crossings AS total_2025, (a.total_crossings - b.total_crossings) AS DROP
	FROM CTE_measure_totals AS a
	JOIN CTE_measure_totals AS b
		ON a.measure = b.measure 
		AND a.YEAR = '2024'
		AND b.YEAR = '2025'
	ORDER BY DROP desc;



/* 
 * Q5: Compares the percentage decline in Canadian land border crossings by measure type 
 * between 2024 and 2025 to determine whether all travel modes declined at the same rate
 */

WITH CTE_measure_totals AS (
	SELECT '20'||RIGHT(date,2) AS year, SUM(value) AS total_crossings, measure
		FROM border_crossings
		WHERE measure != 'Trucks' 
			AND border = 'US-Canada Border'
			AND (date LIKE '%-24' OR date LIKE '%-25')
		GROUP BY RIGHT(date,2), measure
		)
SELECT a.measure, a.total_crossings AS total_2024, b.total_crossings AS total_2025, (a.total_crossings - b.total_crossings) AS DROP, 
	ROUND((a.total_crossings - b.total_crossings) / a.total_crossings * -100, 1) AS pct_change 
	FROM CTE_measure_totals AS a
	JOIN CTE_measure_totals AS b
		ON a.measure = b.measure 
		AND a.YEAR = '2024'
		AND b.YEAR = '2025'
	ORDER BY DROP desc;



/* 
 * Q6: Identifies which US states saw the largest decline in Canadian land border 
 * crossings between 2024 and 2025, using a CTE and self-join
 */

WITH CTE_state_totals AS (
	SELECT '20'||RIGHT(date,2) AS year, state, SUM(value) AS total_crossings
		FROM border_crossings
		WHERE measure != 'Trucks'
			AND border = 'US-Canada Border'
			AND (date LIKE '%-24' OR date LIKE '%-25')
		GROUP BY state, RIGHT(date,2)
		)
SELECT a.state, a.total_crossings AS total_2024, b.total_crossings AS total_2025,
		(b.total_crossings - a.total_crossings) AS difference,
		ROUND((a.total_crossings - b.total_crossings) / a.total_crossings * -100, 1) AS pct_change
		FROM CTE_state_totals AS a
		JOIN CTE_state_totals AS b
			ON a.state = b.state
			AND a.year = '2024'
			AND b.year = '2025'
	ORDER BY difference;



/* 
 * Q7: Identifies which ports saw the largest decline in Canadian land border 
 * crossings between 2024 and 2025, using a CTE and self-join
 */

WITH CTE_port_totals AS (
		SELECT RIGHT(date, 2) AS YEAR, state, port_name, port_code, SUM(value) AS total_crossings
		FROM border_crossings 
		WHERE measure != 'Trucks'
			AND border = 'US-Canada Border'
			AND (date LIKE '%-24' OR date LIKE '%-25')
		GROUP BY YEAR, port_code, state, port_name
	)
SELECT a.state, a.port_name, a.port_code, a.total_crossings AS total_2024, b.total_crossings AS total_2025, 
	(b.total_crossings - a.total_crossings) AS difference,
	ROUND(((a.total_crossings - b.total_crossings) / a.total_crossings) * -100,2 ) AS pct_change
	FROM CTE_port_totals AS a
	JOIN CTE_port_totals AS b
		ON a.port_code = b.port_code 
		AND a.YEAR = '24'
		AND b.YEAR = '25'
	ORDER BY difference;


