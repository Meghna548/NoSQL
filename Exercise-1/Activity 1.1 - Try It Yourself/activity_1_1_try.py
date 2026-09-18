import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.connection import get_db, reset_collection, banner
from rich.table import Table
from rich.console import Console

console = Console()


def main():
    banner("Activity 1.1: Try It Yourself")

    db = get_db("nosql_labs")
    col = reset_collection("nosql_labs", "activity_1_1_try")

    product = {
        "name": "ArangoDB",
        "family": "Multi-Model",
        "data_model": "Document / Graph / Key-Value",
        "vendor": "ArangoDB Inc.",
        "use_case": "Applications requiring flexible document data and graph relationships",
        "open_source": True,
        "classification_reason": "ArangoDB supports multiple data models in one database, including document and graph models."
    }

    col.insert_one(product)

    print("[OK] Inserted ArangoDB classification.\n")

    table = Table(title="Try It Yourself - Database Product")
    table.add_column("Product")
    table.add_column("Family")
    table.add_column("Data Model")
    table.add_column("Vendor")
    table.add_column("Reason")

    p = col.find_one()

    table.add_row(
        p["name"],
        p["family"],
        p["data_model"],
        p["vendor"],
        p["classification_reason"]
    )

    console.print(table)

    banner("Activity 1.1 Try It Yourself Complete")


if __name__ == "__main__":
    main()