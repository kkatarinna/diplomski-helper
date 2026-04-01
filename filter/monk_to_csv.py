import os
import cv2
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from classification import (
    colorparallel,
    brightest_color,
    get_closest_monk_tone,
)

# ------------------ PUTANJE ------------------
csv_path = "data.csv"
images_root = Path("/Users/katarinakrstin/Downloads/ALL IMAGES")

image_folders = [
    "BEN",
    "BEN DARKEN",
    "MEL",
    "MEL DARKEN"
]

# ------------------ UČITAJ CSV ------------------
df = pd.read_csv(csv_path)

if "monk_skin_tone" not in df.columns:
    df["monk_skin_tone"] = pd.NA

# ------------------ OBRADA SLIKA ------------------
for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing images"):
    image_name = row["image_name"]
    image_path = None

    # tražimo sliku kroz sve foldere i ekstenzije
    for folder in image_folders:
        folder_path = images_root / folder
        matches = list(folder_path.glob(f"{image_name}.*"))
        if matches:
            image_path = matches[0]
            break

    if image_path is None:
        print(f"⚠️ Slika {image_name} nije pronađena, preskačem.")
        continue

    image_bgr = cv2.imread(str(image_path))
    if image_bgr is None:
        print(f"⚠️ Slika {image_name} nije mogla biti učitana, preskačem.")
        continue

    image_rgb = cv2.resize(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), (256, 256))

    dominant_color, top_5_colors, brightest_color_global, superpixel_mean_image = colorparallel(image_rgb)
    # lightest_color = brightest_color(*top_colors[:5])
    monk_index, _ = get_closest_monk_tone(brightest_color_global)

    df.at[idx, "monk_skin_tone"] = monk_index

# ------------------ SAČUVAJ CSV ------------------
df.to_csv(csv_path, index=False)

print("✅ Monk skin tone uspešno dodat u CSV")
