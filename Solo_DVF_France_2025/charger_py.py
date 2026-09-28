import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

dossier = Path(__file__).parent
df = pd.read_csv(dossier / "dvf_59_final.csv", parse_dates=["Date mutation"])

# Noms de colonnes plus simples pour SQL
df.columns = (
    df.columns.str.lower()
    .str.replace(" ", "_")
    .str.replace("é", "e")
)

url = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=5432,
    database="dvf",
)
engine = create_engine(url)

df.to_sql("ventes", engine, if_exists="replace", index=False)
print(f"{len(df)} lignes chargées dans la table ventes")