from flask import Flask
from flask import jsonify
from flask import request

import requests

app = Flask(__name__)


@app.route(
    "/api/students/<int:id>/enroll",
    methods=["POST"]
)
def enroll(id):

    course_id = request.json.get(
        "course_id"
    )

    try:

        response = requests.get(
            f"http://localhost:5001/api/courses/{course_id}"
        )

        if response.status_code != 200:

            return jsonify(
                {"error": "Invalid course"}
            ), 404

        return jsonify(
            {
                "student_id": id,
                "course_id": course_id,
                "message": "Enrolled"
            }
        )

    except requests.exceptions.ConnectionError:

        return jsonify(
            {
                "error":
                "Course Service unavailable"
            }
        ), 503


if __name__ == "__main__":

    app.run(port=5002)