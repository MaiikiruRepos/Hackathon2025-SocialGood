import os
import pandas as pd
import random
from faker import Faker
import zipfile

def generate_dummy_bom_data(theme="ai", output_dir="generated_bom_data", seed=42, set_index=1):
    random.seed(seed)
    fake = Faker()
    Faker.seed(seed)

    THEME_COUNTRY_MULTIPLIERS = {
        "ai": {
            "US": 1.4,
            "CA": 1.3,
            "CN": 1.6,
            "IN": 1.7,
            "GB": 1.3
        },
        "lego": {
            "US": 1.1,
            "CA": 1.0,
            "CN": 1.15,
            "IN": 1.2,
            "GB": 0.95
        },
        "insurance": {
            "US": 1.0,
            "CA": 0.95,
            "CN": 1.05,
            "IN": 1.05,
            "GB": 0.90
        }
    }

    MIN_DECAY = 0.60
    DECAY_PER_SET = 0.10

    themes = {
        "ai": {
            "sku_names": [
                "GPU Cluster", "Training Dataset", "Inference Engine", "Model Weights", "Transformer Block",
                "Edge Device", "AutoML Tool", "Pretrained Model", "Neural Processor", "Data Labeling Tool"
            ],
            "process_names": [
                "Data Collection", "Model Training", "Hyperparameter Tuning", "Model Deployment",
                "Inference Testing", "Performance Monitoring"
            ],
            "plant_locations": ["San Francisco", "Toronto", "Bangalore", "Zurich"]
        },
        "lego": {
            "sku_names": [
                "2x4 Brick", "Minifigure Torso", "Wheel Hub", "Axle Peg", "Window Frame",
                "Technic Beam", "Base Plate", "Hinge Plate", "Slope Brick", "Gear Wheel"
            ],
            "process_names": [
                "Injection Molding", "Color Sorting", "Assembly", "Quality Check",
                "Packaging", "Distribution"
            ],
            "plant_locations": ["Billund", "Monterrey", "Kladno", "Jiaxing"]
        },
        "insurance": {
            "sku_names": [
                "Auto Liability", "Homeowners Policy", "Life Insurance", "Disability Coverage",
                "Commercial Property", "Health Plan", "Travel Coverage", "Pet Insurance",
                "Flood Insurance", "Cyber Liability"
            ],
            "process_names": [
                "Underwriting", "Claims Review", "Risk Assessment", "Policy Issuance",
                "Audit", "Customer Service"
            ],
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
        "country_code": [random.choice(list(THEME_COUNTRY_MULTIPLIERS[theme].keys())) for _ in range(num_plants)],
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

    # Generate Process table with energy logic
    process_rows = []
    for definition_id in range(1, num_processes + 1):
        proc_def = random.choice(list(process_definitions.itertuples(index=False)))
        plant_id = random.choice(plants["plant_id"])
        plant_country = plants.loc[plants["plant_id"] == plant_id, "country_code"].values[0]

        # Base values
        if theme == "insurance":
            gas = 0.0
            diesel = 0.0
            elec = random.uniform(20.0, 50.0)


        elif theme == "lego":
            if proc_def.process_name in ["Injection Molding", "Assembly", "Packaging"]:
                gas = round(random.uniform(4.0, 12.0), 2)
                diesel = round(random.uniform(3.0, 8.0), 2)
                elec = random.uniform(1.0, 2.5)

            else:
                gas = round(random.uniform(2.0, 6.0), 2)
                diesel = round(random.uniform(1.5, 5.0), 2)
                elec = round(random.uniform(0.8, 1.5), 2)

        elif theme == "ai":
            if proc_def.process_name in ["Model Training", "Hyperparameter Tuning", "Inference Testing"]:
                gas = round(random.uniform(10.0, 30.0), 2)
                diesel = round(random.uniform(20.0, 50.0), 2)
                elec = round(random.uniform(20.0, 50.0), 2)
            else:
                gas = round(random.uniform(6.0, 20.0), 2)
                diesel = round(random.uniform(10.0, 25.0), 2)
                elec = round(random.uniform(10.0, 30.0), 2)

        else:
            gas = round(random.uniform(0.0, 10.0), 2)
            diesel = round(random.uniform(0.0, 5.0), 2)
            elec = round(random.uniform(0.1, 1.0), 2)

        # Apply modifiers
        country_multiplier = THEME_COUNTRY_MULTIPLIERS[theme].get(plant_country, 1.0)
        decay_multiplier = max(1 - ((set_index - 1) * DECAY_PER_SET), MIN_DECAY)

        gas = round(gas * country_multiplier * decay_multiplier, 2)
        diesel = round(diesel * country_multiplier * decay_multiplier, 2)
        elec = round(elec * country_multiplier * decay_multiplier, 2)

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

    # SkuBOM table
    sku_bom = pd.DataFrame({
        "parent_sku_id": [random.choice(skus["sku_id"]) for _ in range(num_sku_bom_links)],
        "child_sku_id": [random.choice(skus["sku_id"]) for _ in range(num_sku_bom_links)],
        "quantity": [random.randint(1, 10) for _ in range(num_sku_bom_links)],
    }).drop_duplicates(subset=["parent_sku_id", "child_sku_id"])
    sku_bom.to_csv(f"{output_dir}/SkuBOM.csv", index=False)

    # SkuProcess table
    sku_process = pd.DataFrame({
        "sku_id": [random.choice(skus["sku_id"]) for _ in range(num_sku_process_links)],
        "process_id": [random.choice(process_definitions["process_id"]) for _ in range(num_sku_process_links)],
    }).drop_duplicates(subset=["sku_id", "process_id"])
    sku_process.to_csv(f"{output_dir}/SkuProcess.csv", index=False)

    # PlantSKUQuantity table
    plant_sku_quantity = pd.DataFrame({
        "plant_id": [random.choice(plants["plant_id"]) for _ in range(num_plant_sku_quantities)],
        "sku_id": [random.choice(skus["sku_id"]) for _ in range(num_plant_sku_quantities)],
        "quantity": [random.randint(100, 1000) for _ in range(num_plant_sku_quantities)],
    }).drop_duplicates(subset=["plant_id", "sku_id"])
    plant_sku_quantity.to_csv(f"{output_dir}/PlantSKUQuantity.csv", index=False)

    # Zip it up
    zip_path = f"{output_dir}_{theme}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for file in os.listdir(output_dir):
            zf.write(os.path.join(output_dir, file), arcname=file)

    print(f"[✓] Theme: {theme.capitalize()} — data generated and zipped at: {zip_path}")
