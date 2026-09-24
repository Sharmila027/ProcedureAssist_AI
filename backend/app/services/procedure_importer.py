import asyncio
from pathlib import Path

import pandas as pd
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.procedure import Procedure


DATA_DIR = Path(__file__).resolve().parents[3] / "knowledge_base" / "documents"


def convert_can(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if value == "yes":
        return True

    if value == "no":
        return False

    return None


def clean_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value:
        return None

    return value


def read_csv_files():
    files = sorted(DATA_DIR.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {DATA_DIR}"
        )

    all_rows = []

    for file in files:
        print(f"Reading {file.name}")
        dataframe = pd.read_csv(file)

        for _, row in dataframe.iterrows():
            all_rows.append(row)

    return all_rows


async def import_procedures():
    rows = read_csv_files()

    async with AsyncSessionLocal() as db:

        existing_result = await db.execute(
            select(Procedure.code)
        )

        existing_codes = set(
            existing_result.scalars().all()
        )

        procedures = []

        for row in rows:

            code = clean_value(row["Code"])

            if not code:
                continue

            if code in existing_codes:
                continue

            procedure = Procedure(
                service_name=clean_value(
                    row["Service Name"]
                ),

                code=code,

                department=clean_value(
                    row["Dept"]
                ),

                sla_days=clean_value(
                    row["SLA (Days)"]
                ),

                can_required=convert_can(
                    row["CAN Required?"]
                ),

                validity=clean_value(
                    row["Validity"]
                ),

                file_rules=clean_value(
                    row["File Rules"]
                ),

                target_demographic=clean_value(
                    row["Target Demographic"]
                ),

                govt_fee=clean_value(
                    row["Govt Fee"]
                ),

                esevai_fee=clean_value(
                    row["e-Sevai Fee"]
                ),

                access_sources=clean_value(
                    row["Online & Offline Access Sources"]
                ),

                tracker_url=clean_value(
                    row["Tracker URL"]
                ),

                first_appellate_authority=clean_value(
                    row["First Appellate Authority"]
                ),

                workflow=clean_value(
                    row["Workflow"]
                )
            )

            procedures.append(procedure)
            existing_codes.add(code)

        if procedures:
            db.add_all(procedures)
            await db.commit()

        print(
            f"Imported {len(procedures)} new procedures."
        )


if __name__ == "__main__":
    asyncio.run(import_procedures())