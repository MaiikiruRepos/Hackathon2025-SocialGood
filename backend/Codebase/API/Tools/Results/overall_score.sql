REPLACE INTO OverallScore (id, carbon_score, water_score)
WITH WeightedScores AS (
    SELECT
        ss.plant_id,
        ss.sku_id,
        ss.carbon_score * psq.quantity AS weighted_carbon,
        ss.water_score * psq.quantity AS weighted_water,
        psq.quantity
    FROM SkuScore ss
    JOIN PlantSKUQuantity psq ON ss.plant_id = psq.plant_id AND ss.sku_id = psq.sku_id
),
ScoreTotals AS (
    SELECT
        SUM(weighted_carbon) AS total_carbon,
        SUM(weighted_water) AS total_water,
        SUM(quantity) AS total_quantity
    FROM WeightedScores
),
AveragedScore AS (
    SELECT
        total_carbon / NULLIF(total_quantity, 0) AS avg_carbon,
        total_water / NULLIF(total_quantity, 0) AS avg_water
    FROM ScoreTotals
),
MinMax AS (
    SELECT
        MIN(carbon_score) AS min_carbon,
        MAX(carbon_score) AS max_carbon,
        MIN(water_score) AS min_water,
        MAX(water_score) AS max_water
    FROM SkuScore
)
SELECT
    1,
    ROUND(1000 * (avg_carbon - min_carbon) / NULLIF(max_carbon - min_carbon, 0), 2),
    ROUND(1000 * (avg_water - min_water) / NULLIF(max_water - min_water, 0), 2)
FROM AveragedScore, MinMax;
