
-- PieChartData Calculation
-- Calculate what % of total carbon/water usage occurs at each plant

REPLACE INTO PieChartData (plant_id, carbon_percent, water_percent)
SELECT
    plant_id,
    ROUND(100 * SUM(carbon_score) / NULLIF((SELECT SUM(carbon_score) FROM SkuScore), 0), 2),
    ROUND(100 * SUM(water_score) / NULLIF((SELECT SUM(water_score) FROM SkuScore), 0), 2)
FROM SkuScore
GROUP BY plant_id;
