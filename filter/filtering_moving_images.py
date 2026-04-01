import os
import shutil
import pandas as pd
from pathlib import Path

# -------------------- CONFIG --------------------
csv_path = "trening.csv"  # putanja do CSV fajla
source_root = Path("/Users/katarinakrstin/Downloads/ALL IMAGES")  # folder gde se nalaze BEN, MEL folderi
folders = ["BEN", "BEN DARKEN", "MEL", "MEL DARKEN"]
dest_folder = Path("/Users/katarinakrstin/Downloads/ALL IMAGES/TRENING")  # gde premestamo slike
dest_folder.mkdir(exist_ok=True)
# ------------------------------------------------

# Učitavanje CSV-a
df = pd.read_csv(csv_path)
image_names = df["image_name"].tolist()

# Prolazak kroz sve foldere i slike
for folder_name in folders:
    folder_path = source_root / folder_name
    if not folder_path.exists():
        print(f"⚠️ Folder {folder_path} ne postoji, preskačem.")
        continue

    for image_file in folder_path.iterdir():
        if image_file.is_file():
            name_only = image_file.stem  # ime slike bez ekstenzije
            if name_only in image_names:
                dest_path = dest_folder / image_file.name
                print(f"Premestam {image_file} -> {dest_path}")
                shutil.move(str(image_file), str(dest_path))  # premesta fajl
