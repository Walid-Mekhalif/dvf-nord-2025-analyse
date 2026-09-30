from pathlib import Path
import pandas as pd

dossier_data = Path(__file__).parent.parent / "data"
df = pd.read_csv(dossier_data / "dvf_59_brut.csv", low_memory=False)

# 1. Ventes classiques de maisons et appartements
df = df[df["Nature mutation"] == "Vente"]
df = df[df["Type local"].isin(["Maison", "Appartement"])]

# 2. Colonnes indispensables non vides
df = df.dropna(subset=["Valeur fonciere", "Surface reelle bati"])
df = df[df["Surface reelle bati"] > 0]

# 3. Dates au bon format (jour/mois/année)
df["Date mutation"] = pd.to_datetime(df["Date mutation"], format="%d/%m/%Y")

# 4. Ne garder que les ventes d'un seul bien (évite les ventes groupées)
cle = ["Date mutation", "Valeur fonciere", "Commune", "Voie", "No voie"]
df["nb_biens"] = df.groupby(cle, dropna=False)["Type local"].transform("size")
df = df[df["nb_biens"] == 1].drop(columns="nb_biens")

# 5. Prix au m²
df["prix_m2"] = df["Valeur fonciere"] / df["Surface reelle bati"]

print(df.shape)
print(df["Type local"].value_counts())
print(df["prix_m2"].describe())

df.to_csv(dossier_data / "dvf_59_propre.csv", index=False)