from config.connection import get_db, banner, print_json
from pymongo.errors import WriteError


def main():
    banner("Lab 3.1 - Try Yourself: Course Prerequisites")

    db = get_db()

    # Recreate the collection
    db["courses_prerequisites"].drop()
    courses = db["courses_prerequisites"]

    # Course documents with embedded prerequisites
    course_documents = [
        {
            "course_name": "Introduction to Machine Learning",
            "course_code": "AIML101",
            "instructor": "Dr. Priya Sharma",
            "credits": 4,
            "schedule": {
                "days": ["Monday", "Wednesday"],
                "time": "10:00-11:30",
                "room": "LH-201"
            },
            "enrolled_students": [
                {
                    "name": "Rahul Kumar",
                    "email": "rahul@example.com",
                    "grade": "A"
                },
                {
                    "name": "Anjali Nair",
                    "email": "anjali@example.com",
                    "grade": "B+"
                }
            ],
            "prerequisites": []
        },
        {
            "course_name": "Deep Learning with PyTorch",
            "course_code": "AIML301",
            "instructor": "Dr. Anil Gupta",
            "credits": 3,
            "schedule": {
                "days": ["Tuesday", "Thursday"],
                "time": "14:00-15:30",
                "room": "LH-305"
            },
            "enrolled_students": [
                {
                    "name": "Arjun Menon",
                    "email": "arjun@example.com",
                    "grade": "A"
                }
            ],
            "prerequisites": ["AIML101"]
        },
        {
            "course_name": "Natural Language Processing",
            "course_code": "AIML201",
            "instructor": "Dr. Meera Joshi",
            "credits": 3,
            "schedule": {
                "days": ["Monday", "Wednesday", "Friday"],
                "time": "09:00-10:00",
                "room": "LH-102"
            },
            "enrolled_students": [
                {
                    "name": "Meera Thomas",
                    "email": "meera@example.com",
                    "grade": "A"
                }
            ],
            "prerequisites": ["AIML101"]
        }
    ]

    # Insert courses
    courses.insert_many(course_documents)

    print("\nCourses with prerequisites:")
    for course in courses.find({}, {"_id": 0}):
        print_json(course)

    # Query courses that have AIML101 as a prerequisite
    print("\nCourses requiring AIML101:")
    for course in courses.find(
        {"prerequisites": "AIML101"},
        {"_id": 0, "course_name": 1, "course_code": 1, "prerequisites": 1}
    ):
        print_json(course)

    print("\nWhy embed prerequisites?")
    print("Prerequisites are a small, bounded list closely related to each course.")
    print("Embedding allows the prerequisites to be retrieved together with the course.")
    print("Therefore, embedding is suitable for this use case.")


if __name__ == "__main__":
    main()