REPLACE INTO OverallScore (id, carbon_score, water_score)
SELECT
    1,
    ROUND(
        100 * (total.carbon - minmax.min_carbon) /
        NULLIF(minmax.max_carbon - minmax.min_carbon, 0), 2
    ) AS normalized_carbon_score,
    ROUND(
        100 * (total.water - minmax.min_water) /
        NULLIF(minmax.max_water - minmax.min_water, 0), 2
    ) AS normalized_water_score
FROM (
    SELECT
        SUM(carbon_score) AS carbon,
        SUM(water_score) AS water
    FROM SkuScore
) AS total,
(
    SELECT
        MIN(carbon_score) AS min_carbon,
        MAX(carbon_score) AS max_carbon,
        MIN(water_score) AS min_water,
        MAX(water_score) AS max_water
    FROM SkuScore
) AS minmax;
