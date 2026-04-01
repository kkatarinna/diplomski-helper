import pandas as pd

# ------------------ PUTANJE ------------------
csv_path = "trening.csv"  # promeni ako treba

# ------------------ UČITAJ CSV ------------------
df = pd.read_csv(csv_path)

# Ako je monk_skin_tone float, normalizuj (1.0 -> 1)
df_valid = df[df["monk_skin_tone"].between(1, 10, inclusive="both")]

# ------------------ PREBROJAVANJE ------------------
counts = (
    df
    .groupby(["monk_skin_tone", "target"])
    .size()
    .unstack(fill_value=0)
    .reindex(range(1, 11), fill_value=0)  # klase 1–10
)

# ------------------ ISPIS ------------------
print("Broj slika po Monk skin tone klasama:\n")
print("monk_skin_tone | target=0 | target=1")
print("-" * 35)

for tone in range(1, 11):
    t0 = counts.loc[tone].get(0, 0)
    t1 = counts.loc[tone].get(1, 0)
    print(f"{tone:^14} | {t0:^8} | {t1:^8}")
