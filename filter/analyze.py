import os
import csv

# PROMENI OVU PUTANJU
BASE_PATH = r"/Users/katarinakrstin/Downloads/ALL IMAGES"

folders = {
    "BEN": 0,
    "BEN DARKEN": 0,
    "MEL": 1,
    "MEL DARKEN": 1
}

output_csv = "data.csv"

with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["image_name", "target"])

    for folder, target in folders.items():
        folder_path = os.path.join(BASE_PATH, folder)

        if not os.path.isdir(folder_path):
            print(f"Folder ne postoji: {folder_path}")
            continue

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path):
                image_name = os.path.splitext(filename)[0]
                writer.writerow([image_name, target])

print(f"CSV fajl '{output_csv}' je uspešno napravljen.")
