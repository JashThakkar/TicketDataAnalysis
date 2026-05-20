from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

TABLE_LOAD_ORDER = [
    "locations",
    "departments",
    "support_teams",
    "systems",
    "sla_policies",
    "employees",
    "support_agents",
    "tickets",
    "ticket_updates",
]


def clear_tables():
    with engine.begin() as conn:
        conn.execute(text("""
            TRUNCATE TABLE
                ticket_updates,
                tickets,
                employees,
                support_agents,
                sla_policies,
                systems,
                support_teams,
                departments,
                locations
            RESTART IDENTITY CASCADE;
        """))
    print("Existing table data cleared.")


def load_table(table_name):
    file_path = RAW_DIR / f"{table_name}.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(df)} rows into {table_name}")


def main():
    clear_tables()

    for table in TABLE_LOAD_ORDER:
        load_table(table)

    print("\nAll CSV data loaded into PostgreSQL successfully.")


if __name__ == "__main__":
    main()