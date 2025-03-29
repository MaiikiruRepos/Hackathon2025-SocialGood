-- Create EnvTable first because others depend on it
CREATE TABLE IF NOT EXISTS EnvTable (
    Location VARCHAR(100) PRIMARY KEY,
    gasCarbonLbPerGal DECIMAL(10,4),
    gasWaterGalPerGal DECIMAL(10,4),
    elecCarbonLbPerKwh DECIMAL(10,4),
    elecWaterLbPerKwh DECIMAL(10,4),
    employeeCarbonLbPer DECIMAL(10,4),
    employeeWaterGalPer DECIMAL(10,4),
    dieselCarbonLbPerGal DECIMAL(10,4),
    dieselWaterLbPerGal DECIMAL(10,4)
) ENGINE=InnoDB;

-- Create Item next
CREATE TABLE IF NOT EXISTS Item (
    sku_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    subSKUID INT,
    processID INT
) ENGINE=InnoDB;

-- Then Plant (depends on EnvTable and Item)
CREATE TABLE IF NOT EXISTS Plant (
    plant_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100),
    skuID INT,
    FOREIGN KEY (location) REFERENCES EnvTable(Location),
    FOREIGN KEY (skuID) REFERENCES Item(sku_id)
) ENGINE=InnoDB;

-- Now the Process table (note backticks because "Process" is a MySQL keyword)
CREATE TABLE IF NOT EXISTS Processes (
    process_id INT AUTO_INCREMENT PRIMARY KEY,
    PlantID INT,
    processName VARCHAR(100) NOT NULL,
    employeeCount INT,
    electricCount DECIMAL(10,2),
    GasCount DECIMAL(10,2),
    FOREIGN KEY (PlantID) REFERENCES Plant(plant_id)
) ENGINE=InnoDB;

-- Create ItemProcess (many-to-many between Item and Process)
CREATE TABLE IF NOT EXISTS ItemProcess (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    itemID INT,
    processID INT,
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