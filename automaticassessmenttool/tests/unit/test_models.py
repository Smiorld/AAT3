from app import db

from app.class_methods import ShortWrittenAnswerMethods
from app.models import (
    Question,
    Assessment,
    Module,
    Course,
    StudentAnswer,
    QuestionContributors,
)


class QuestionTests:
    question = Question(
        question="Provide three advantages of a distributed system",
        question_description="Separate the answer with a comma, full-stop  or new line.",
        correct_answer=[
            "easier data sharing",
            "faster",
            "reliability",
            "scalability",
            "failure handling",
            "efficiency",
        ],
        feedback="You got 3 marks, congratulations, for more information visit " "LINK",
        max_marks=3,
    )

    student_answer = StudentAnswer(
        question_id=1, student_id=1, marks=50, no_of_attempts=2
    )
    question_contributors = QuestionContributors(
        role="Author", question_id=1, user_id=1
    )

    written_answer1 = StudentAnswer(
        answer_id=1,
        question_id=1,
        question="Provide three advantages of a distributed system",
        question_description="Separate the answer with a comma, full-stop  or new line.",
        correct_answer=[
            "easier data sharing",
            "faster",
            "reliability",
            "scalability",
            "failure handling",
            "efficiency",
        ],
        student_answer=[
            "share data more easily",
            "reliable",
            "handles system failures more effectively",
        ],
        person_id=2,
        assessment_id=1,
        feedback="You got 3 marks, congratulations, for more information visit LINK",
        max_marks=3,
        marks=3,
    )
    written_answer2 = StudentAnswer(
        answer_id=2,
        question_id=2,
        question="What is a data structure?",
        question_description="",
        correct_answer="data organization, management, and storage format that "
        "enables efficient access and modification. collection of "
        "data values, the relationships among them, and the functions "
        "or operations that can be applied to the data",
        student_answer="A data structure is a way of organizing the data so that it "
        "can be used efficiently or we can say that it is a way of "
        "arranging data on a computer so that it can be accessed and "
        "updated.",
        person_id=2,
        assessment_id=1,
        feedback="You got 2 marks, you could have talked about 'storage', ",
        max_marks=3,
        marks=2,
    )

    @staticmethod
    def student_answer_db_test(written_answer1):
        db.session.add(written_answer1)
        db.session.commit()
        written_answer_query = StudentAnswer.query.filter_by(answer_id=1).first()
        assert (
            written_answer1 == written_answer_query
        )  # checks to make sure data was entered and retrieved correctly

    @staticmethod
    def short_written_answer_db_test(written_answer_empty):
        db.session.add(written_answer_empty)
        db.session.commit()
        written_answer_query = ShortWrittenAnswer.query.filter_by(question_id=1).first()
        assert (
            written_answer_empty == written_answer_query
        )  # make sure data was stored and retrieved correctly

    assert (
        ShortWrittenAnswerMethods.mark_answer(written_answer1.student_answer)
        == written_answer1.marks
    )
    assert (
        ShortWrittenAnswerMethods.mark_answer(written_answer2.student_answer)
        == written_answer2.marks
    )


# to test database
db.drop_all()
db.create_all()

course1 = Course(course_name="MSc. Computing")

db.session.add(course1)

module1 = Module(course_id=1, module_name="Software Engineering")

db.session.add(module1)

assessment1 = Assessment(
    module_id=1,
    assessment_name="AAT",
    hand_in_date="2022-03-01 05:00:00",
    hand_out_date="2022-03-02 09:00:00",
    is_summative=True,
    is_draft=True,
    total_marks=100,
    max_attempts=3,
)

db.session.add(assessment1)

db.session.commit()
