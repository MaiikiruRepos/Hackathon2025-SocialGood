import pandas as pd
import yaml
import argparse
import os

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def export_csv(df, name, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}.csv")
    df.to_csv(output_path, index=False)

def convert_bom(excel_path, config_path, output_dir):
    config = load_config(config_path)
    sheets = pd.read_excel(excel_path, sheet_name=None)

    # Item table
    item_conf = config["item"]
    item_df = sheets[item_conf["sheet"]][list(item_conf["columns"].values())].copy()
    item_df.columns = item_conf["columns"].keys()
    for col, val in item_conf["default"].items():
        item_df[col] = val
    export_csv(item_df, "item", output_dir)

    # Plant table
    plant_conf = config["plant"]
    plant_df = sheets[plant_conf["sheet"]][[plant_conf["columns"]["skuID"]]].copy()
    plant_df.columns = ["skuID"]
    plant_df["location"] = plant_conf["default"]["location"]
    export_csv(plant_df, "plant", output_dir)

    # Processes table
    proc_conf = config["processes"]
    proc_df = sheets[proc_conf["sheet"]][list(proc_conf["columns"].values())].copy()
    proc_df.columns = proc_conf["columns"].keys()
    export_csv(proc_df, "processes", output_dir)

    # PlantSKUQuantity table
    psq_conf = config["plant_sku_quantity"]
    psq_df = sheets[psq_conf["sheet"]][list(psq_conf["columns"].values())].copy()
    psq_df.columns = psq_conf["columns"].keys()
    psq_df["plant_id"] = psq_conf["default"]["plant_id"]
    export_csv(psq_df, "plant_sku_quantity", output_dir)

    # ItemProcess table
    item_proc_sheet = config["item_process"]["from_sheets"][0]
    item_proc_df = sheets[item_proc_sheet][
        [config["item"]["columns"]["sku_id"], config["processes"]["columns"]["processName"]]
    ].copy()
    item_proc_df.columns = ["itemID", "processName"]
    item_proc_df = item_proc_df.dropna().drop_duplicates()
    export_csv(item_proc_df, "item_process", output_dir)

if __name__ == "__main__":

    default_excel = os.path.join("../../../../bom_converter/input", "bom.xlsx")
    default_config = os.path.join("../../../../bom_converter/config.yaml")
    default_output = os.path.join("../../../../bom_converter/output")

    parser = argparse.ArgumentParser(description="Convert BOM Excel to SQL-ready CSVs")
    parser.add_argument("--excel", default=default_excel, help="Path to Excel BOM file")
    parser.add_argument("--config", default=default_config, help="Path to YAML config file")
    parser.add_argument("--output", default=default_output, help="Output directory for CSVs")
    args = parser.parse_args()

    convert_bom(args.excel, args.config, args.output)
