import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

dossier_data = Path(__file__).parent.parent / "data"
df = pd.read_csv(dossier_data / "dvf_59_final.csv", parse_dates=["Date mutation"])

df.columns = (
    df.columns.str.lower()
    .str.replace(" ", "_")
    .str.replace("é", "e")
)

url = URL.create(
    "postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)
engine = create_engine(url)

df.to_sql("ventes", engine, if_exists="replace", index=False)
print(f"{len(df)} lignes chargées dans la table ventes")