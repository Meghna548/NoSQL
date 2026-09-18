import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.connection import get_db, reset_collection, banner
from rich.table import Table
from rich.console import Console

console = Console()


def main():
    banner("Activity 1.2: Try It Yourself - E-Commerce")

    db = get_db("nosql_labs")
    col = reset_collection("nosql_labs", "activity_1_2_try")

    domains = [
        {
            "app": "E-Commerce",
            "domain": "customer_profiles",
            "description": "Customer information, preferences, addresses and account details",
            "read_write_pattern": "Read-heavy with occasional updates",
            "recommended_family": "Document",
            "recommended_db": "MongoDB",
            "rationale": "Customer information can have flexible and nested structures."
        },
        {
            "app": "E-Commerce",
            "domain": "product_catalog",
            "description": "Products, descriptions, categories, specifications and attributes",
            "read_write_pattern": "Read-heavy with frequent catalog updates",
            "recommended_family": "Document",
            "recommended_db": "MongoDB",
            "rationale": "Products can have different attributes and benefit from a flexible document structure."
        },
        {
            "app": "E-Commerce",
            "domain": "shopping_carts",
            "description": "Active shopping carts and their items",
            "read_write_pattern": "Frequent reads and writes with short-lived data",
            "recommended_family": "Key-Value",
            "recommended_db": "Redis",
            "rationale": "Fast key-based access and TTL support are useful for active shopping carts."
        },
        {
            "app": "E-Commerce",
            "domain": "orders",
            "description": "Orders, items, payment status, shipping status and timestamps",
            "read_write_pattern": "Write-heavy with queries by customer and date",
            "recommended_family": "Document",
            "recommended_db": "MongoDB",
            "rationale": "An order and its line items can be represented naturally as a document."
        },
        {
            "app": "E-Commerce",
            "domain": "recommendations",
            "description": "Relationships between customers, products and frequently purchased items",
            "read_write_pattern": "Relationship and traversal queries",
            "recommended_family": "Graph",
            "recommended_db": "Neo4j",
            "rationale": "Graph databases are suitable for analyzing relationships between customers and products."
        }
    ]

    col.insert_many(domains)

    print(f"[OK] Inserted {len(domains)} e-commerce domain mappings.\n")

    table = Table(title="E-Commerce - NoSQL Data Domain Mapping", show_lines=True)
    table.add_column("Domain", width=20)
    table.add_column("NoSQL Family", width=16)
    table.add_column("Recommended DB", width=20)
    table.add_column("Rationale", width=60)

    for d in col.find():
        table.add_row(
            d["domain"],
            d["recommended_family"],
            d["recommended_db"],
            d["rationale"]
        )

    console.print(table)

    print("\n--- Family Distribution ---")

    pipeline = [
        {
            "$group": {
                "_id": "$recommended_family",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    for g in col.aggregate(pipeline):
        print(f"  {g['_id']:20} : {g['count']} domain(s)")

    banner("Activity 1.2 Try It Yourself Complete")


if __name__ == "__main__":
    main()