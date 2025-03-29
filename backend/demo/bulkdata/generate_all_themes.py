
import os

from backend.demo.bulkdata.generate_dummy_bom_data import generate_dummy_bom_data


def run_all_themes(base_dir="all_themes_output"):
    themes = ["pcb", "trucking", "insurance"]
    runs_per_theme = 4

    for theme in themes:
        for i in range(1, runs_per_theme + 1):
            folder_name = f"{theme}_set_{i}"
            output_path = os.path.join(base_dir, folder_name)
            print(f"Generating: {folder_name}")
            generate_dummy_bom_data(theme=theme, output_dir=output_path)

if __name__ == "__main__":
    run_all_themes()
