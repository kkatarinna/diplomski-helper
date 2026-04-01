import pandas as pd
import numpy as np

# ------------------ PUTANJE ------------------
input_csv = "dataset_remaining.csv"
test_csv = "trening.csv"
output_csv = "dataset_remaining_2.csv"

# ------------------ UČITAJ CSV ------------------
df = pd.read_csv(input_csv)

# radimo samo sa validnim Monk klasama
df_valid = df[df["monk_skin_tone"].between(1, 10, inclusive="both")]

test_rows = []

np.random.seed(42)  # reproducibilnost

# ------------------ PO KLASAMA ------------------
for tone in range(1, 11):
    df_tone = df_valid[df_valid["monk_skin_tone"] == tone]

    df_t1 = df_tone[df_tone["target"] == 1]
    df_t0 = df_tone[df_tone["target"] == 0]

    n_t1 = len(df_t1)
    if n_t1 == 0:
        continue

    sample_t1 = df_t1.sample(n=n_t1, random_state=42)
    sample_t0 = df_t0.sample(n=min(n_t1, len(df_t0)), random_state=42)

    test_rows.append(sample_t1)
    test_rows.append(sample_t0)

# ------------------ FORMIRAJ TEST CSV ------------------
df_test = pd.concat(test_rows).drop_duplicates()

# ------------------ UKLONI IZ ORIGINALA ------------------
df_remaining = df.drop(index=df_test.index)

# ------------------ SAČUVAJ ------------------
df_test.to_csv(test_csv, index=False)
df_remaining.to_csv(output_csv, index=False)

print("✅ trening.csv napravljen")
print(f"➡️ trening.csv: {len(df_test)} redova")
print(f"➡️ preostalo u dataset_remaining_2.csv: {len(df_remaining)} redova")