// HANDS-ON 5

// Task 1

// Question 60

use("college_nosql");

// Question 61

db.createCollection("feedback");

// Question 62

db.feedback.insertMany([
{
    student_id: 1,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent teaching. Would recommend.",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: ISODate("2022-11-30T10:15:00Z"),
    attachments: [
        {
            filename: "notes.pdf",
            size_kb: 240
        }
    ]
},
{
    student_id: 2,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Good course content.",
    tags: ["challenging", "informative"],
    submitted_at: ISODate("2022-11-29T09:00:00Z"),
    attachments: [
        {
            filename: "feedback.pdf",
            size_kb: 180
        }
    ]
},
{
    student_id: 3,
    course_code: "CS101",
    semester: "2022-EVEN",
    rating: 5,
    comments: "Very well structured.",
    tags: ["well-structured", "good-examples"],
    submitted_at: ISODate("2022-12-01T08:00:00Z"),
    attachments: [
        {
            filename: "assignment.pdf",
            size_kb: 200
        }
    ]
},
{
    student_id: 4,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 3,
    comments: "Average experience.",
    tags: ["average"],
    submitted_at: ISODate("2022-11-25T12:00:00Z"),
    attachments: [
        {
            filename: "review.pdf",
            size_kb: 120
        }
    ]
},
{
    student_id: 5,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 2,
    comments: "Needs improvement.",
    tags: ["difficult"],
    submitted_at: ISODate("2022-11-20T11:00:00Z"),
    attachments: [
        {
            filename: "remarks.pdf",
            size_kb: 100
        }
    ]
},
{
    student_id: 6,
    course_code: "CS103",
    semester: "2022-ODD",
    rating: 4,
    comments: "Interesting topics.",
    tags: ["interesting", "good-examples"],
    submitted_at: ISODate("2022-11-18T10:00:00Z"),
    attachments: [
        {
            filename: "course_notes.pdf",
            size_kb: 210
        }
    ]
},
{
    student_id: 7,
    course_code: "EC101",
    semester: "2021-EVEN",
    rating: 1,
    comments: "Very difficult course.",
    tags: ["challenging", "hard"],
    submitted_at: ISODate("2021-12-01T09:00:00Z"),
    attachments: [
        {
            filename: "complaint.pdf",
            size_kb: 140
        }
    ]
},
{
    student_id: 8,
    course_code: "ME101",
    semester: "2022-EVEN",
    rating: 5,
    comments: "Excellent practical sessions.",
    tags: ["practical", "excellent"],
    submitted_at: ISODate("2022-12-02T15:00:00Z"),
    attachments: [
        {
            filename: "lab.pdf",
            size_kb: 250
        }
    ]
},
{
    student_id: 9,
    course_code: "CS103",
    semester: "2022-ODD",
    rating: 3,
    comments: "Good but lengthy.",
    tags: ["lengthy"],
    submitted_at: ISODate("2022-11-21T13:00:00Z"),
    attachments: [
        {
            filename: "summary.pdf",
            size_kb: 160
        }
    ]
},
{
    student_id: 10,
    course_code: "CS102",
    semester: "2022-EVEN",
    rating: 4,
    comments: "Useful database concepts.",
    tags: ["informative", "well-structured"],
    submitted_at: ISODate("2022-11-27T14:00:00Z")
}
]);

// Question 63

db.feedback.insertOne({
    student_id: 11,
    course_code: "CS102",
    semester: "2023-ODD",
    rating: 4,
    comments: "Good learning experience.",
    tags: ["informative", "useful"],
    submitted_at: ISODate("2023-01-15T10:00:00Z")
});

// Question 64

db.feedback.countDocuments();

// Task 2

// Question 65

db.feedback.find({
    rating: 5
});

// Question 66

db.feedback.find({
    course_code: "CS101",
    tags: "challenging"
});

// Question 67

db.feedback.find(
    {},
    {
        _id: 0,
        student_id: 1,
        course_code: 1,
        rating: 1
    }
);

// Question 68

db.feedback.updateMany(
{
    rating: { $lt: 3 }
},
{
    $set: { needs_review: true }
}
);

// Question 69

db.feedback.updateMany(
{
    needs_review: true
},
{
    $push: { tags: "reviewed" }
}
);

// Question 70

db.feedback.deleteMany({
    semester: "2021-EVEN"
});

// Task 3

// Question 71

db.feedback.aggregate([
{
    $match: {
        semester: "2022-ODD"
    }
},
{
    $group: {
        _id: "$course_code",
        avg_rating: { $avg: "$rating" },
        feedback_count: { $sum: 1 }
    }
},
{
    $sort: {
        avg_rating: -1
    }
}
]);

// Question 72

db.feedback.aggregate([
{
    $match: {
        semester: "2022-ODD"
    }
},
{
    $group: {
        _id: "$course_code",
        avg_rating: { $avg: "$rating" },
        feedback_count: { $sum: 1 }
    }
},
{
    $project: {
        _id: 0,
        course_code: "$_id",
        average_rating: {
            $round: ["$avg_rating", 1]
        },
        feedback_count: 1
    }
},
{
    $sort: {
        average_rating: -1
    }
}
]);

// Question 73

db.feedback.aggregate([
{
    $unwind: "$tags"
},
{
    $group: {
        _id: "$tags",
        tag_count: { $sum: 1 }
    }
},
{
    $sort: {
        tag_count: -1
    }
}
]);

// Question 74

db.feedback.createIndex({
    course_code: 1
});

db.feedback.find({
    course_code: "CS101"
}).explain("executionStats");