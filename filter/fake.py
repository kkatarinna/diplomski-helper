import pandas as pd
import numpy as np

# ------------------ PUTANJE ------------------
csv_path = "data_fake.csv"        # ulazni CSV
output_csv = "dataset_updated.csv"  # izlazni CSV

# ------------------ UČITAJ CSV ------------------
df = pd.read_csv(csv_path)

# ------------------ FILTRIRAJ monk_skin_tone == 2 ------------------
mask = df["monk_skin_tone"] == 2
indices = df[mask].index.tolist()

# nasumično izmešaj indekse (reproducibilno ako želiš)
np.random.seed(42)
np.random.shuffle(indices)

n = len(indices)

n_3 = int(0.30 * n)
n_4 = int(0.30 * n)
n_1 = int(0.10 * n)

idx_3 = indices[:n_3]
idx_4 = indices[n_3:n_3 + n_4]
idx_1 = indices[n_3 + n_4:n_3 + n_4 + n_1]

# ------------------ IZMENI VREDNOSTI ------------------
df.loc[idx_3, "monk_skin_tone"] = 3
df.loc[idx_4, "monk_skin_tone"] = 4
df.loc[idx_1, "monk_skin_tone"] = 1

# ------------------ SAČUVAJ CSV ------------------
df.to_csv(output_csv, index=False)

print("✅ CSV uspešno izmenjen")
print(f"Ukupno monk_skin_tone == 2: {n}")
print(f"→ 3: {len(idx_3)}")
print(f"→ 4: {len(idx_4)}")
print(f"→ 1: {len(idx_1)}")
print(f"→ ostalo 2: {n - len(idx_3) - len(idx_4) - len(idx_1)}")
