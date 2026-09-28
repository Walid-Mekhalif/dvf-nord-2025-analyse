from pathlib import Path
import pandas as pd

dossier = Path(__file__).parent
colonnes = [
    "Date mutation", "Nature mutation", "Valeur fonciere",
    "No voie", "Type de voie", "Voie",
    "Code postal", "Commune", "Code departement", "Code commune",
    "Type local", "Surface reelle bati", "Nombre pieces principales",
    "Surface terrain", "No disposition",
]

df = pd.read_csv(
    dossier / "ValeursFoncieres-2025.txt",
    sep="|", decimal=",", usecols=colonnes, low_memory=False,
    dtype={"Code departement": str},
)

# On garde uniquement le Nord
df = df[df["Code departement"] == "59"].copy()

print(df.shape)
print(df["Nature mutation"].value_counts())
print(df["Type local"].value_counts(dropna=False))
print(df.isna().sum().sort_values(ascending=False))

# Sauvegarde d'un fichier léger pour la suite
df.to_csv(dossier / "dvf_59_brut.csv", index=False)