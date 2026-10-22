from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import json
import os

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "cti_platform"

CTI_URL = "https://ctidigest.com/"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

sources = db["cti_sources"]
reports = db["cti_reports"]
indicators = db["cti_indicators"]


def get_cti_articles():
    try:
        response = requests.get(
            CTI_URL,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        seen = set()

        for a in soup.find_all("a", href=True):
            title = a.get_text(" ", strip=True)
            url = a["href"]

            if url.startswith("/"):
                url = "https://ctidigest.com" + url

            if (
                title
                and len(title) > 10
                and url.startswith("http")
                and url not in seen
            ):
                seen.add(url)

                articles.append({
                    "title": title[:200],
                    "url": url
                })

        return articles[:20]

    except Exception as e:
        print("CTI Digest could not be read:", e)
        return []


def create_data():
    sources.drop()
    reports.drop()
    indicators.drop()

    articles = get_cti_articles()

    if not articles:
        articles = [
            {
                "title": "Cyber Threat Intelligence Report",
                "url": "https://ctidigest.com/"
            },
            {
                "title": "Security Threat Report",
                "url": "https://ctidigest.com/"
            },
            {
                "title": "Threat Intelligence News",
                "url": "https://ctidigest.com/"
            }
        ]

    source_documents = []

    for i, article in enumerate(articles[:10]):
        source_documents.append({
            "name": "CTI Digest",
            "url": article["url"],
            "type": "Threat Intelligence Source",
            "publisher": "OpenSource CTI Digest"
        })

    source_result = sources.insert_many(source_documents)
    source_ids = source_result.inserted_ids

    report_documents = []

    for i, article in enumerate(articles[:10]):
        report_documents.append({
            "title": article["title"],
            "summary": "Threat intelligence report collected from CTI Digest.",
            "category": "Cyber Threat Intelligence",
            "source_id": source_ids[i],
            "tags": [
                "threat-intelligence",
                "cybersecurity",
                "security"
            ],
            "created_year": 2026
        })

    report_result = reports.insert_many(report_documents)
    report_ids = report_result.inserted_ids

    indicator_documents = []

    for i, report_id in enumerate(report_ids):
        indicator_documents.append({
            "indicator": f"example-threat-{i}.com",
            "indicator_type": "domain",
            "report_id": report_id,
            "confidence": "medium"
        })

    indicators.insert_many(indicator_documents)

    print("====================================")
    print("LAB 7.1 DATA CREATED")
    print("====================================")
    print("Sources:", sources.count_documents({}))
    print("Reports:", reports.count_documents({}))
    print("Indicators:", indicators.count_documents({}))


def analyze_schema():
    print("\n====================================")
    print("EMBEDDING AND REFERENCING ANALYSIS")
    print("====================================")

    print("\nEmbedded fields:")
    print("- tags are embedded inside reports")
    print("- report summary is embedded inside reports")
    print("- indicator confidence/type are embedded inside indicators")

    print("\nReferenced relationships:")
    print("- reports -> sources using source_id")
    print("- indicators -> reports using report_id")

    print("\nWhy referencing is useful:")
    print("- A source can be associated with many reports.")
    print("- A report can contain many indicators.")
    print("- Referencing avoids duplicating the same source information.")
    print("- Source information can be updated in one place.")


def calculate_document_sizes():
    print("\n====================================")
    print("BSON DOCUMENT SIZE ANALYSIS")
    print("====================================")

    for collection_name in [
        "cti_sources",
        "cti_reports",
        "cti_indicators"
    ]:
        collection = db[collection_name]

        result = list(
            collection.aggregate([
                {
                    "$project": {
                        "_id": 1,
                        "size": {"$bsonSize": "$$ROOT"}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "average_size": {"$avg": "$size"},
                        "maximum_size": {"$max": "$size"}
                    }
                }
            ])
        )

        if result:
            average_size = result[0]["average_size"]
            maximum_size = result[0]["maximum_size"]

            print("\nCollection:", collection_name)
            print("Average document size:", round(average_size, 2), "bytes")
            print("Maximum document size:", maximum_size, "bytes")
            print("16 MB limit:", 16 * 1024 * 1024, "bytes")

            if maximum_size < 16 * 1024 * 1024:
                print("Status: Documents are safely below 16 MB.")
            else:
                print("Status: WARNING - document approaches/exceeds 16 MB.")


def export_reports():
    os.makedirs("../data", exist_ok=True)

    data = list(
        reports.find(
            {},
            {"_id": 0}
        )
    )

    with open(
        "../data/lab_7_1_dump.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            default=str
        )

    print("\n[OK] Saved:")
    print("../data/lab_7_1_dump.json")


def main():
    create_data()
    analyze_schema()
    calculate_document_sizes()
    export_reports()

    client.close()


if __name__ == "__main__":
    main()