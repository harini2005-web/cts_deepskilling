from flask import Blueprint
from flask import jsonify
from flask import request

from models import db
from models import Course
from models import Student

courses_bp = Blueprint(
    'courses',
    __name__,
    url_prefix='/api/courses'
)


@courses_bp.route('/', methods=['GET'])
def get_courses():

    courses = Course.query.all()

    return jsonify(
        [c.to_dict() for c in courses]
    )


@courses_bp.route('/', methods=['POST'])
def create_course():

    data = request.get_json()

    course = Course(
        name=data['name'],
        code=data['code'],
        credits=data['credits']
    )

    db.session.add(course)
    db.session.commit()

    return jsonify(
        course.to_dict()
    ), 201


@courses_bp.route('/<int:id>/', methods=['PUT'])
def update_course(id):

    course = Course.query.get_or_404(id)

    data = request.get_json()

    course.name = data.get(
        'name',
        course.name
    )

    db.session.commit()

    return jsonify(
        course.to_dict()
    )


@courses_bp.route('/<int:id>/', methods=['DELETE'])
def delete_course(id):

    course = Course.query.get_or_404(id)

    db.session.delete(course)

    db.session.commit()

    return jsonify({
        "message": "deleted"
    })


@courses_bp.route(
    '/<int:id>/students/',
    methods=['GET']
)
def course_students(id):

    course = Course.query.get_or_404(id)

    students = [
        {
            "id": e.student.id,
            "name": e.student.first_name
        }
        for e in course.enrollments
    ]

    return jsonify(students)