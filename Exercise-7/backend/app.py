from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import re

app = Flask(__name__)
CORS(app)

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "cti_platform"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

reports = db["cti_reports"]


def classify_threat(text):

    text = text.lower()

    high_keywords = [
        "ransomware",
        "malware",
        "trojan",
        "botnet",
        "exploit",
        "credential theft"
    ]

    medium_keywords = [
        "phishing",
        "suspicious",
        "vulnerability",
        "attack",
        "threat"
    ]

    for word in high_keywords:

        if word in text:
            return "High"

    for word in medium_keywords:

        if word in text:
            return "Medium"

    return "Low"


@app.route("/")
def home():

    return jsonify({
        "message":
        "Cyber Threat Intelligence Platform API",
        "status": "running"
    })


@app.route("/api/reports")
def get_reports():

    search = request.args.get(
        "search",
        ""
    ).strip()

    category = request.args.get(
        "category",
        ""
    ).strip()

    query = {}

    if search:

        query["$or"] = [
            {
                "title": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "summary": {
                    "$regex": search,
                    "$options": "i"
                }
            }
        ]

    if category:

        query["category"] = category

    data = list(
        reports.find(
            query
        ).limit(100)
    )

    result = []

    for report in data:

        text = (
            report.get("title", "")
            + " "
            + report.get("summary", "")
        )

        result.append({
            "id": str(report["_id"]),
            "title": report.get(
                "title",
                "Untitled"
            ),
            "summary": report.get(
                "summary",
                ""
            ),
            "category": report.get(
                "category",
                ""
            ),
            "threat_level":
                classify_threat(text)
        })

    return jsonify(result)


@app.route("/api/categories")
def get_categories():

    categories = reports.distinct(
        "category"
    )

    return jsonify(categories)


@app.route("/api/classify")
def classify():

    text = request.args.get(
        "text",
        ""
    )

    return jsonify({
        "text": text,
        "threat_level":
            classify_threat(text)
    })


@app.route("/api/stats")
def stats():

    return jsonify({
        "total_reports":
            reports.count_documents({}),
        "categories":
            len(reports.distinct("category"))
    })


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )