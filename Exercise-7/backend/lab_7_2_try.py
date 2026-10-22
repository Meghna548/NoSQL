import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "cti_platform"
COLLECTION_NAME = "cti_reports"

CTI_URL = "https://ctidigest.com/"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
reports = db[COLLECTION_NAME]


def get_cache_stats():
    try:
        status = db.command("serverStatus")
        cache = status["wiredTiger"]["cache"]

        pages_read = cache.get("pages read into cache", 0)
        pages_requested = cache.get("pages requested from the cache", 0)

        if pages_requested > 0:
            hit_ratio = (
                1 - (pages_read / pages_requested)
            ) * 100
        else:
            hit_ratio = 100.0

        cache_bytes = cache.get("bytes currently in the cache", 0)

        return cache_bytes, hit_ratio

    except Exception as e:
        print("Cache statistics error:", e)
        return 0, 0


def get_db_urls():
    urls = set()

    for report in reports.find({}, {"source_url": 1, "url": 1, "_id": 0}):
        if report.get("source_url"):
            urls.add(report["source_url"])

        if report.get("url"):
            urls.add(report["url"])

    return urls


def browse_new_reports():
    try:
        response = requests.get(
            CTI_URL,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        db_urls = get_db_urls()

        new_reports = []

        for link in soup.find_all("a", href=True):

            href = link.get("href")

            title = link.get_text(" ", strip=True)

            if not title:
                continue

            if href.startswith("/"):
                href = "https://ctidigest.com" + href

            if href.startswith("http") and href not in db_urls:

                new_reports.append({
                    "title": title,
                    "url": href
                })

        unique_reports = {}

        for report in new_reports:
            unique_reports[report["url"]] = report

        return list(unique_reports.values())

    except Exception as e:
        print("Website browsing error:", e)
        return []


print("=" * 50)
print("LAB 7.2 TRY YOURSELF")
print("=" * 50)

print("\nMonitoring WiredTiger cache every 10 seconds...")
print("Browsing CTI Digest for newer reports...")
print("Press CTRL+C to stop.\n")


try:

    while True:

        cache_bytes, hit_ratio = get_cache_stats()

        new_reports = browse_new_reports()

        print("=" * 50)
        print("MONITORING UPDATE")
        print("=" * 50)

        print("Cache bytes currently in cache:", cache_bytes)
        print("Cache hit ratio: {:.2f}%".format(hit_ratio))

        print("\nNewer threat reports not available in DB:")

        if new_reports:

            for report in new_reports[:10]:

                print(
                    "-",
                    report["title"],
                    "|",
                    report["url"]
                )

            if len(new_reports) > 10:
                print(
                    "...and",
                    len(new_reports) - 10,
                    "more"
                )

        else:
            print("No new reports found.")

        print("\nNext check in 10 seconds...\n")

        time.sleep(10)


except KeyboardInterrupt:

    print("\nMonitoring stopped.")

finally:

    client.close()