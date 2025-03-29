-- Create EnvTable first because others depend on it
CREATE TABLE IF NOT EXISTS EnvTable (
    countryCode VARCHAR(10) PRIMARY KEY,
    countryName VARCHAR(100),
    continent VARCHAR(50),
    gasCarbonLbPerGal DECIMAL(10,4),
    gasWaterGalPerGal DECIMAL(10,4),
    dieselCarbonLbPerGal DECIMAL(10,4),
    dieselWaterLbPerGal DECIMAL(10,4),
    elecCarbonLbPerKwh DECIMAL(10,4),
    elecWaterGalPerKwh DECIMAL(10,4),
    employeeCarbonLbPer DECIMAL(10,4),
    employeeWaterGalPer DECIMAL(10,4)
) ENGINE=InnoDB;

-- Create Item next
CREATE TABLE IF NOT EXISTS Item (
    sku_id INT PRIMARY KEY,
    sku_name VARCHAR(100) NOT NULL,
    parent_sku_id INT,
    process_id INT
) ENGINE=InnoDB;

-- Then Plant (depends on EnvTable and Item)
CREATE TABLE IF NOT EXISTS Plant (
    plant_id INT PRIMARY KEY,
    location VARCHAR(100),
    FOREIGN KEY (location) REFERENCES EnvTable(countryCode),
) ENGINE=InnoDB;

-- Now the Process table (note backticks because "Process" is a MySQL keyword)
CREATE TABLE IF NOT EXISTS Processes (
    process_id INT PRIMARY KEY,
    PlantID INT,
    processName VARCHAR(100) NOT NULL,
    employeeCount INT,
    electricCount DECIMAL(10,2),
    GasCount DECIMAL(10,2),
    DieselCount DECIMAL(10,2),
    FOREIGN KEY (PlantID) REFERENCES Plant(plant_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ItemProcess (
    itemID INT,
    processID INT,
    PRIMARY KEY (itemID, processID),
    FOREIGN KEY (itemID) REFERENCES Item(sku_id),
    FOREIGN KEY (processID) REFERENCES Processes(process_id)
) ENGINE=InnoDB;

-- Finally, PlantSKUQuantity (composite key, links Plant and Item)
CREATE TABLE IF NOT EXISTS PlantSKUQuantity (
    plant_id INT,
    sku_id INT,
    quantity INT NOT NULL,
    PRIMARY KEY (plant_id, sku_id),
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id),
    FOREIGN KEY (sku_id) REFERENCES Item(sku_id)
) ENGINE=InnoDB;

-- Create SkuScore table
CREATE TABLE IF NOT EXISTS SkuScore (
    sku_id INT,
    plant_id INT,
    carbonScore DECIMAL(10,2),
    waterScore DECIMAL(10,2),
    PRIMARY KEY (plant_id, sku_id),
    FOREIGN KEY (sku_id) REFERENCES Item(sku_id)
) ENGINE=InnoDB;

-- Create Overall table
CREATE TABLE IF NOT EXISTS OverallScore (
    carbonScore DECIMAL(10,2),
    waterScore DECIMAL(10,2)
) ENGINE=InnoDB;

-- Create PieChartData table
CREATE TABLE IF NOT EXISTS PieChartData (
    plant_id INT PRIMARY KEY,
    carbon_percent DECIMAL(5,2),
    water_percent DECIMAL(5,2),
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id)
) ENGINE=InnoDB;

