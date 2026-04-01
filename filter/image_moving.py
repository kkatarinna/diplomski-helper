import csv
import os
import shutil

# ====== PODESAVANJA ======
CSV_PATH = "/Users/katarinakrstin/Downloads/ISIC_2020_Training_GroundTruth (1).csv"              # putanja do csv fajla
SOURCE_DIR = "/Users/katarinakrstin/Downloads/ISIC_2020_Training_JPEG (1)/train"          # folder gde su sve slike
DEST_DIR = "/Users/katarinakrstin/Downloads/ALL IMAGES/BEN"            # folder gde premeštaš MEL=1 slike
# =========================

os.makedirs(DEST_DIR, exist_ok=True)

moved = 0
missing = 0

with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        if row["target"] == "0":
            image_name = row["image_name"]
            image_name += ".jpg"
            src_path = os.path.join(SOURCE_DIR, image_name)
            dst_path = os.path.join(DEST_DIR, image_name)
            # print(src_path, "->", dst_path)

            if os.path.exists(src_path):
                shutil.move(src_path, dst_path)
                moved += 1
            else:
                missing += 1

print(f"✅ Premešteno slika: {moved}")
print(f"⚠️ Nedostaje slika: {missing}")
