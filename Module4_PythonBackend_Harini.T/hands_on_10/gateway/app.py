from flask import Flask
from flask import request
from flask import jsonify

import requests

app = Flask(__name__)


@app.route(
    "/api/courses/<path:path>"
)
def course_proxy(path):

    url = (
        f"http://localhost:5001/"
        f"api/courses/{path}"
    )

    response = requests.get(url)

    return jsonify(
        response.json()
    )


@app.route(
    "/api/students/<int:id>/enroll",
    methods=["POST"]
)
def student_proxy(id):

    url = (
        f"http://localhost:5002/"
        f"api/students/{id}/enroll"
    )

    response = requests.post(
        url,
        json=request.json
    )

    return jsonify(
        response.json()
    ), response.status_code


if __name__ == "__main__":

    app.run(port=5000)