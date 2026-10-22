from pymongo import MongoClient
import time

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "cti_platform"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

reports = db["cti_reports"]
embedded_reports = db["cti_reports_embedded"]


def create_embedded_design():

    embedded_reports.drop()

    documents = []

    for index, report in enumerate(
        reports.find({})
    ):

        source = db["cti_sources"].find_one(
            {"_id": report["source_id"]}
        )

        if source:

            documents.append({
                "title": report["title"],
                "summary": report["summary"],
                "category": report["category"],
                "tags": report["tags"],

                "sources": [
                    {
                        "name": source["name"],
                        "url": source["url"],
                        "type": source["type"],
                        "is_actual_threat": index % 2 == 0
                    }
                ]
            })

    if documents:
        embedded_reports.insert_many(documents)

    print("Embedded documents created:")
    print(embedded_reports.count_documents({}))


def referenced_query():

    print("\n====================================")
    print("REFERENCED DESIGN QUERY")
    print("====================================")

    start = time.perf_counter()

    result = []

    for report in reports.find({}):

        source = db["cti_sources"].find_one(
            {"_id": report["source_id"]}
        )

        if source:
            result.append({
                "title": report["title"],
                "source": source["name"]
            })

    end = time.perf_counter()

    print("Reports found:", len(result))
    print("Time:", round(end - start, 6), "seconds")


def embedded_query():

    print("\n====================================")
    print("EMBEDDED DESIGN QUERY")
    print("====================================")

    start = time.perf_counter()

    result = list(
        embedded_reports.find(
            {
                "sources.is_actual_threat": True
            },
            {
                "_id": 0,
                "title": 1,
                "sources": 1
            }
        )
    )

    end = time.perf_counter()

    print("Actual threat reports:", len(result))
    print("Time:", round(end - start, 6), "seconds")

    print("\nReports where source is an actual threat:")

    for report in result:
        print(report["title"])


def explain_redesign():

    print("\n====================================")
    print("ANALYSIS")
    print("====================================")

    print("\nQueries that become faster:")
    print("1. Finding reports where a source is an actual threat.")
    print("2. Reading report and source information together.")
    print("3. No separate lookup is required.")

    print("\nWhat becomes harder:")
    print("1. Source information may be duplicated.")
    print("2. Updating a source in many reports becomes harder.")
    print("3. Documents become larger.")
    print("4. Maintaining consistency becomes harder.")

    print("\nEmbedded query used:")
    print(
        'db.cti_reports_embedded.find('
        '{"sources.is_actual_threat": True})'
    )


def main():

    create_embedded_design()
    referenced_query()
    embedded_query()
    explain_redesign()

    client.close()


if __name__ == "__main__":
    main()