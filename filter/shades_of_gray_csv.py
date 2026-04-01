import csv

input_csv = "trening.csv"
output_csv = "trening_shades_of_gray.csv"

suffixes = ["_orig", "_aug1", "_aug2", "_aug3"]

with open(input_csv, newline="", encoding="utf-8") as f_in, \
     open(output_csv, "w", newline="", encoding="utf-8") as f_out:

    reader = csv.DictReader(f_in)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)

    writer.writeheader()

    for row in reader:
        base_name = row["image_name"]
        for suf in suffixes:
            new_row = row.copy()
            new_row["image_name"] = base_name + suf
            writer.writerow(new_row)
