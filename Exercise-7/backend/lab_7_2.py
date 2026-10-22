from pymongo import MongoClient
import requests
import random
import time
import sys

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "cti_platform"
COLLECTION_NAME = "annual_security_reports"

REPO_README = (
    "https://raw.githubusercontent.com/"
    "jacobdjwilson/awesome-annual-security-reports/"
    "master/README.md"
)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def get_repository_reports():

    try:

        response = requests.get(
            REPO_README,
            timeout=20
        )

        text = response.text

        reports = []

        for line in text.splitlines():

            if "](" in line:

                start = line.find("[")

                middle = line.find("](")

                end = line.find(")", middle)

                if start != -1 and middle != -1 and end != -1:

                    title = line[start + 1:middle].strip()

                    url = line[middle + 2:end].strip()

                    if title and url:

                        reports.append({
                            "title": title[:150],
                            "source_url": url[:500]
                        })

        return reports

    except Exception as e:

        print("Could not read repository:", e)

        return []


def make_document(i, base_report):

    text = (
        "This is a working-set test document based on an annual "
        "cybersecurity report. The document represents security "
        "report metadata and text used for MongoDB cache analysis. "
        "The purpose is to create approximately 2 KB records for "
        "random-read workload testing. "
    )

    padding = (text * 20)[:1500]

    return {
        "report_id": i,
        "title": base_report["title"],
        "source_url": base_report["source_url"],
        "year": 2026,
        "category": "Annual Security Report",
        "content": padding,
        "tags": [
            "cybersecurity",
            "security-report",
            "threat-intelligence"
        ]
    }


def insert_100000_documents():

    collection.drop()

    base_reports = get_repository_reports()

    if not base_reports:

        base_reports = [
            {
                "title": "Annual Cybersecurity Report",
                "source_url": (
                    "https://github.com/"
                    "jacobdjwilson/"
                    "awesome-annual-security-reports"
                )
            }
        ]

    print("Source report records found:", len(base_reports))

    batch = []

    start = time.perf_counter()

    for i in range(100000):

        base_report = base_reports[
            i % len(base_reports)
        ]

        batch.append(
            make_document(i, base_report)
        )

        if len(batch) == 1000:

            collection.insert_many(
                batch,
                ordered=False
            )

            batch = []

            if (i + 1) % 10000 == 0:
                print(
                    "Inserted:",
                    i + 1
                )

    if batch:
        collection.insert_many(
            batch,
            ordered=False
        )

    end = time.perf_counter()

    print("\n====================================")
    print("INSERT COMPLETE")
    print("====================================")

    print(
        "Documents:",
        collection.count_documents({})
    )

    print(
        "Insertion time:",
        round(end - start, 2),
        "seconds"
    )


def check_document_size():

    result = list(
        collection.aggregate([
            {
                "$project": {
                    "size": {
                        "$bsonSize": "$$ROOT"
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "average_size": {
                        "$avg": "$size"
                    },
                    "minimum_size": {
                        "$min": "$size"
                    },
                    "maximum_size": {
                        "$max": "$size"
                    }
                }
            }
        ])
    )

    if result:

        print("\n====================================")
        print("DOCUMENT SIZE")
        print("====================================")

        print(
            "Average:",
            round(result[0]["average_size"], 2),
            "bytes"
        )

        print(
            "Minimum:",
            result[0]["minimum_size"],
            "bytes"
        )

        print(
            "Maximum:",
            result[0]["maximum_size"],
            "bytes"
        )


def get_cache_stats():

    status = db.command(
        "serverStatus"
    )

    wired = status.get(
        "wiredTiger",
        {}
    )

    cache = wired.get(
        "cache",
        {}
    )

    bytes_in_cache = cache.get(
        "bytes currently in the cache",
        0
    )

    pages_read = cache.get(
        "pages read into cache",
        0
    )

    pages_requested = cache.get(
        "pages requested from the cache",
        0
    )

    if pages_requested > 0:

        hit_ratio = (
            1 -
            (
                pages_read /
                pages_requested
            )
        ) * 100

    else:

        hit_ratio = 0

    return {
        "bytes_in_cache": bytes_in_cache,
        "pages_read": pages_read,
        "pages_requested": pages_requested,
        "hit_ratio": hit_ratio
    }


def random_reads():

    print("\n====================================")
    print("RANDOM READ TEST")
    print("====================================")

    ids = random.sample(
        range(100000),
        5000
    )

    start = time.perf_counter()

    for report_id in ids:

        collection.find_one(
            {
                "report_id": report_id
            }
        )

    end = time.perf_counter()

    print(
        "Random reads:",
        len(ids)
    )

    print(
        "Read time:",
        round(end - start, 2),
        "seconds"
    )

    stats = get_cache_stats()

    print(
        "Bytes currently in cache:",
        stats["bytes_in_cache"]
    )

    print(
        "Pages read into cache:",
        stats["pages_read"]
    )

    print(
        "Pages requested from cache:",
        stats["pages_requested"]
    )

    print(
        "Estimated cache hit ratio:",
        round(stats["hit_ratio"], 2),
        "%"
    )


def main():

    insert_100000_documents()

    check_document_size()

    print("\nInitial cache information:")

    stats = get_cache_stats()

    print(
        "Cache bytes:",
        stats["bytes_in_cache"]
    )

    print(
        "Cache hit ratio:",
        round(stats["hit_ratio"], 2),
        "%"
    )

    random_reads()

    client.close()


if __name__ == "__main__":
    main()