-- Create EnvTable first (referenced by Plant)
CREATE TABLE IF NOT EXISTS EnvTable (
    country_code VARCHAR(10) PRIMARY KEY,
    country_name VARCHAR(100),
    continent VARCHAR(50),
    gas_cr FLOAT,
    gas_wr FLOAT,
    diesel_cr FLOAT,
    diesel_wr FLOAT,
    elec_cr FLOAT,
    elec_wr FLOAT,
    employee_cr FLOAT,
    employee_wr FLOAT
);

-- Create Plant (references EnvTable)
CREATE TABLE IF NOT EXISTS Plant (
    plant_id INT PRIMARY KEY,
    country_code VARCHAR(10),
    FOREIGN KEY (country_code) REFERENCES EnvTable(country_code)
);

-- Create Sku (standalone)
CREATE TABLE IF NOT EXISTS Sku (
    sku_id INT PRIMARY KEY,
    sku_name VARCHAR(100)
);

-- Create ProcessDefinition (referenced by Process)
CREATE TABLE IF NOT EXISTS ProcessDefinition (
    process_id INT PRIMARY KEY,
    process_name VARCHAR(100)
);

-- Create Process (references Plant and ProcessDefinition)
CREATE TABLE IF NOT EXISTS Process (
    site_process_id INT PRIMARY KEY,
    plant_id INT,
    process_id INT,
    employee_count INT,
    gas_count FLOAT,
    elec_rate FLOAT,
    diesel_count FLOAT,
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id),
    FOREIGN KEY (process_id) REFERENCES ProcessDefinition(process_id)
);

-- Create SkuBOM (recursive reference to Sku)
CREATE TABLE IF NOT EXISTS SkuBOM (
    parent_sku_id INT,
    child_sku_id INT,
    quantity INT,
    PRIMARY KEY (parent_sku_id, child_sku_id),
    FOREIGN KEY (parent_sku_id) REFERENCES Sku(sku_id),
    FOREIGN KEY (child_sku_id) REFERENCES Sku(sku_id)
);

-- Create SkuProcess (bridge table between Sku and Process)
CREATE TABLE IF NOT EXISTS SkuProcess (
    sku_id INT,
    process_id INT,
    PRIMARY KEY (sku_id, process_id),
    FOREIGN KEY (sku_id) REFERENCES Sku(sku_id),
    FOREIGN KEY (process_id) REFERENCES Process(site_process_id)
);

-- Create PlantSKUQuantity (plant + sku production quantities)
CREATE TABLE IF NOT EXISTS PlantSKUQuantity (
    plant_id INT,
    sku_id INT,
    quantity INT,
    PRIMARY KEY (plant_id, sku_id),
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id),
    FOREIGN KEY (sku_id) REFERENCES Sku(sku_id)
);

-- Create SkuScore table
CREATE TABLE IF NOT EXISTS SkuScore (
    sku_id INT,
    plant_id INT,
    carbon_score FLOAT,
    water_score FLOAT,
    PRIMARY KEY (sku_id, plant_id),
    FOREIGN KEY (sku_id) REFERENCES Sku(sku_id),
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id)
);

CREATE TABLE IF NOT EXISTS OverallScore (
    id TINYINT PRIMARY KEY DEFAULT 1,  -- fixed singleton ID
    carbon_score FLOAT,
    water_score FLOAT
);

CREATE TABLE IF NOT EXISTS PieChartData (
    plant_id INT PRIMARY KEY,
    carbon_percent FLOAT,
    water_percent FLOAT,
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id)
);
