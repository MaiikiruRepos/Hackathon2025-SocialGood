INSERT INTO SkuScore (sku_id, plant_id, carbon_score, water_score)
SELECT
    sp.sku_id,
    pq.plant_id,
    SUM(
        pr.gas_count * env.gas_cr +
        pr.elec_rate * env.elec_cr +
        pr.diesel_count * env.diesel_cr +
        pr.employee_count * env.employee_cr
    ) AS carbon_score,
    SUM(
        pr.gas_count * env.gas_wr +
        pr.elec_rate * env.elec_wr +
        pr.diesel_count * env.diesel_wr +
        pr.employee_count * env.employee_wr
    ) AS water_score
FROM SkuProcess sp
JOIN PlantSKUQuantity pq ON pq.sku_id = sp.sku_id
JOIN Process pr ON pr.plant_id = pq.plant_id AND pr.process_id = sp.process_id
JOIN Plant p ON pr.plant_id = p.plant_id
JOIN EnvTable env ON p.country_code = env.country_code
GROUP BY sp.sku_id, pq.plant_id;
