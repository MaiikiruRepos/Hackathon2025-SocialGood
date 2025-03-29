import os
import pandas as pd
import random
from faker import Faker
import zipfile

def generate_dummy_bom_data(theme="pcb", output_dir="generated_bom_data", seed=42):
    random.seed(seed)
    fake = Faker()
    Faker.seed(seed)

    themes = {
        "pcb": {
            "sku_names": ["PCB Board", "Microcontroller", "Resistor", "Capacitor", "Inductor", "Diode", "Ferrite Bead", "Crystal Oscillator", "Solder Paste", "Thermal Pad"],
            "process_names": ["Soldering", "Pick-and-Place", "Etching", "Inspection", "Reflow", "AOI Testing"],
            "plant_locations": ["Shenzhen", "Austin", "Munich", "Tokyo"]
        },
        "trucking": {
            "sku_names": ["Truck Tire", "Diesel Fuel", "Hydraulic Fluid", "Brake Pads", "Cargo Strap", "Oil Filter", "Transmission Fluid", "Coolant", "Headlights", "Axle Shaft"],
            "process_names": ["Loading", "Route Planning", "Fueling", "Maintenance", "Inspection", "Dispatch"],
            "plant_locations": ["Los Angeles", "Dallas", "Chicago", "Atlanta"]
        },
        "insurance": {
            "sku_names": ["Auto Liability", "Homeowners Policy", "Life Insurance", "Disability Coverage", "Commercial Property", "Health Plan", "Travel Coverage", "Pet Insurance", "Flood Insurance", "Cyber Liability"],
            "process_names": ["Underwriting", "Claims Review", "Risk Assessment", "Policy Issuance", "Audit", "Customer Service"],
            "plant_locations": ["Boston", "Denver", "Seattle", "Charlotte"]
        }
    }

    if theme not in themes:
        raise ValueError(f"Invalid theme '{theme}'. Choose from {list(themes.keys())}")

    config = themes[theme]
    os.makedirs(output_dir, exist_ok=True)

    # Settings
    num_plants = 5
    num_skus = 50
    num_process_definitions = len(config["process_names"])
    num_processes = 30
    num_sku_bom_links = 40
    num_sku_process_links = 60
    num_plant_sku_quantities = 40

    # Generate Plant table
    plants = pd.DataFrame({
        "plant_id": range(1, num_plants + 1),
        "country_code": [fake.country_code() for _ in range(num_plants)],
    })
    plants.to_csv(f"{output_dir}/Plant.csv", index=False)

    # Generate Sku table
    skus = pd.DataFrame({
        "sku_id": [str(fake.unique.random_int(min=1000000, max=9999999)) for _ in range(num_skus)],
        "sku_name": [random.choice(config["sku_names"]) for _ in range(num_skus)],
    })
    skus.to_csv(f"{output_dir}/Sku.csv", index=False)

    # Generate ProcessDefinition table
    process_definitions = pd.DataFrame({
        "process_id": list(range(1, num_process_definitions + 1)),
        "process_name": config["process_names"]
    })
    process_definitions.to_csv(f"{output_dir}/ProcessDefinition.csv", index=False)

    # Generate Process table with logic-aware energy usage
    process_rows = []
    for definition_id in range(1, num_processes + 1):
        proc_def = random.choice(list(process_definitions.itertuples(index=False)))
        plant_id = random.choice(plants["plant_id"])

        # Energy usage logic
        if theme == "insurance":
            # Office processes – electric only
            gas = 0.0
            diesel = 0.0
            elec = round(random.uniform(0.2, 0.8), 2)
        elif theme == "trucking":
            # Fueling/Maintenance use gas + diesel; others mostly electric
            if proc_def.process_name in ["Fueling", "Maintenance"]:
                gas = round(random.uniform(30.0, 90.0), 2)
                diesel = round(random.uniform(20.0, 80.0), 2)
                elec = round(random.uniform(0.1, 0.4), 2)
            else:
                gas = 0.0
                diesel = 0.0
                elec = round(random.uniform(0.2, 0.6), 2)
        elif theme == "pcb":
            # Soldering/Pick-and-Place mostly electric, others use some gas
            if proc_def.process_name in ["Soldering", "Pick-and-Place", "AOI Testing", "Inspection"]:
                gas = round(random.uniform(0.0, 5.0), 2)
                diesel = round(random.uniform(0.0, 5.0), 2)
                elec = round(random.uniform(0.6, 1.0), 2)
            else:
                gas = round(random.uniform(5.0, 30.0), 2)
                diesel = round(random.uniform(2.0, 10.0), 2)
                elec = round(random.uniform(0.4, 0.8), 2)
        else:
            # fallback defaults
            gas = round(random.uniform(0.0, 10.0), 2)
            diesel = round(random.uniform(0.0, 5.0), 2)
            elec = round(random.uniform(0.1, 1.0), 2)

        process_rows.append({
            "definition_id": definition_id,
            "plant_id": plant_id,
            "process_id": proc_def.process_id,
            "employee_count": random.randint(1, 50),
            "gas_count": gas,
            "elec_rate": elec,
            "diesel_count": diesel
        })

    processes = pd.DataFrame(process_rows)
    processes.to_csv(f"{output_dir}/Process.csv", index=False)

    # Generate SkuBOM table
    sku_bom = pd.DataFrame({
        "parent_sku_id": [random.choice(skus["sku_id"]) for _ in range(num_sku_bom_links)],
        "child_sku_id": [random.choice(skus["sku_id"]) for _ in range(num_sku_bom_links)],
        "quantity": [random.randint(1, 10) for _ in range(num_sku_bom_links)],
    }).drop_duplicates(subset=["parent_sku_id", "child_sku_id"])
    sku_bom.to_csv(f"{output_dir}/SkuBOM.csv", index=False)

    # Generate SkuProcess table
    sku_process = pd.DataFrame({
        "sku_id": [random.choice(skus["sku_id"]) for _ in range(num_sku_process_links)],
        "process_id": [random.choice(process_definitions["process_id"]) for _ in range(num_sku_process_links)],
    }).drop_duplicates(subset=["sku_id", "process_id"])
    sku_process.to_csv(f"{output_dir}/SkuProcess.csv", index=False)

    # Generate PlantSKUQuantity table
    plant_sku_quantity = pd.DataFrame({
        "plant_id": [random.choice(plants["plant_id"]) for _ in range(num_plant_sku_quantities)],
        "sku_id": [random.choice(skus["sku_id"]) for _ in range(num_plant_sku_quantities)],
        "quantity": [random.randint(100, 1000) for _ in range(num_plant_sku_quantities)],
    }).drop_duplicates(subset=["plant_id", "sku_id"])
    plant_sku_quantity.to_csv(f"{output_dir}/PlantSKUQuantity.csv", index=False)

    # Zip the directory
    zip_path = f"{output_dir}_{theme}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for file in os.listdir(output_dir):
            zf.write(os.path.join(output_dir, file), arcname=file)

    print(f"[✓] Theme: {theme.capitalize()} — data generated and zipped at: {zip_path}")

# Example usage:
# generate_dummy_bom_data("pcb")
# generate_dummy_bom_data("trucking")
# generate_dummy_bom_data("insurance")
