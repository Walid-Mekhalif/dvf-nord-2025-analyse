from pathlib import Path
import pandas as pd

dossier = Path(__file__).parent
df = pd.read_csv(dossier / "dvf_59_propre.csv", parse_dates=["Date mutation"])

avant = len(df)

# Bornes de prix au m² et de surface
df = df[df["prix_m2"].between(500, 10000)]
df = df[df["Surface reelle bati"].between(9, 500)]

print(f"Lignes supprimées : {avant - len(df)} ({(avant - len(df)) / avant:.1%})")
print(df.shape)
print(df.groupby("Type local")["prix_m2"].describe())

df.to_csv(dossier / "dvf_59_final.csv", index=False)