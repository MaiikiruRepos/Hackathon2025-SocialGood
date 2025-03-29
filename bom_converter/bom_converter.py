
import pandas as pd
import os

def process_bom_csv(input_file='input/test.csv', output_dir='output'):
    # Ensure the input file exists
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return

    # Load the CSV
    df = pd.read_csv(input_file)
    df.columns = df.columns.str.strip()

    # Drop rows missing critical data
    df = df.dropna(subset=["Part Number", "Description", "Parent Item", "Part Qty"])

    # Create Sku.csv with ID and name
    sku_df = df[["Part Number", "Description"]].drop_duplicates().rename(columns={
        "Part Number": "sku_id",
        "Description": "sku_name"
    })

    # Create SkuBOM.csv
    bom_df = df[["Parent Item", "Part Number", "Part Qty"]].rename(columns={
        "Parent Item": "parent_sku_id",
        "Part Number": "child_sku_id",
        "Part Qty": "quantity"
    })

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Save files
    sku_df.to_csv(os.path.join(output_dir, "Sku.csv"), index=False)
    bom_df.to_csv(os.path.join(output_dir, "SkuBOM.csv"), index=False)

    print(f"✅ Sku.csv and SkuBOM.csv saved to '{output_dir}'.")

if __name__ == "__main__":
    process_bom_csv()
