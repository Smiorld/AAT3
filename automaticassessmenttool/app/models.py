from email.policy import default
import json
from flask_login import UserMixin
from sqlalchemy import null
from app import db, login_manager
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

class test1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer,nullable=False)

class test2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer,nullable=False)
class Assessment(db.Model):
    """
    Authored by Julius (Qiye Zhou)
    Modified by Rob (added time_allotted)
    """

    __tablename__ = "assessment"

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(
        db.Integer, db.ForeignKey("module.id"), nullable=False
    )  # foreign key from module table
    assessment_name = db.Column(db.Text, nullable=False)
    hand_in_date = db.Column(db.DateTime, nullable=True)
    hand_out_date = db.Column(db.DateTime, nullable=True)
    is_summative = db.Column(db.Boolean, nullable=True)
    is_draft = db.Column(db.Boolean, nullable=False, default=True)
    total_marks = db.Column(db.Integer, nullable=True, default=0)
    time_allotted = db.Column(db.Integer, nullable = True, default=0)

    # relationship()
    published_student_assessment = db.relationship(
        "PublishedStudentAssessment", backref="assessment", lazy=True
    )
    assessment2question = db.relationship(
        "Assessment2Question", backref="assessment", lazy=True
    )


class PublishedStudentAssessment(db.Model):
    """
    Authored by Julius (Qiye Zhou)
    Modified by Rob (added time_taken)
    """

    __tablename__ = "published_student_assessment"  # needed for backref

    # Primary keys does not have to separately unique
    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessment.id"),
        primary_key=True,
        autoincrement=False,
    )  # foreign key from assessment table
    student_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, autoincrement=False
    )  # foreign key from user table
    no_of_attempts = db.Column(
        db.Integer, primary_key=True, autoincrement=False, default=0
    )
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    awarded_marks = db.Column(db.Integer, nullable=False, default=0)
    time_taken = db.Column(db.Integer, nullable=True)
    # relationship()
    student_answer = db.relationship(
        "StudentAnswer", backref="published_student_assessment", lazy=True
    )


class Question(db.Model):
    """
    Authored by Devajith
    Modified by henry. julius
    """

    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)  # the actual question
    question_description = db.Column(db.Text, nullable=True)  # further information # Should be nullable? 28/03 -Rob -Yes, Henry 06/04
    correct_answer = db.Column(db.Text, nullable=True)
    correct_answer_count = db.Column(db.Integer, nullable=True)
    correct_feedback = db.Column(db.Text, nullable=True)  # added by henry
    incorrect_feedback = db.Column(
        db.Text, nullable=True
    )  # splitting feedback will make it easy to deliver?
    max_marks = db.Column(db.Integer, nullable=True)
    arguments = db.Column(db.Text, nullable=True) # added by henry
    test_inputs = db.Column(db.Text, nullable=True)
    expected_outputs = db.Column(db.Text, nullable=True)
    is_multiple_choice = db.Column(db.Boolean, nullable=False)
    total_choices = db.Column(db.Integer, nullable=True)
    category = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Text, nullable=True)
    points = db.Column(db.Integer, nullable=True)
    choices = db.Column(db.Text, nullable=True)  # Save as comma separated values
    options = db.Column(db.Text, nullable=True)  # Save as json

    # relationship()
    student_answer = db.relationship("StudentAnswer", backref="question", lazy=True)
    question_contributors = db.relationship(
        "QuestionContributors", backref="question", lazy=True
    )
    assessment2question = db.relationship(
        "Assessment2Question", backref="question", lazy=True
    )

    def as_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }


class Assessment2Question(db.Model):
    __tablename__ = "assessment_2_question"
    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessment.id"),
        primary_key=True,
        autoincrement=False,
    )
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.id"), primary_key=True, autoincrement=False
    )


class QuestionContributors(db.Model):
    __tablename__ = "question_contributors"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Text, nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class StudentAnswer(db.Model):
    __tablename__ = "student_answer"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.id"), nullable=False
    )  # foreign key from question table
    student_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key from user table

    marks = db.Column(db.Integer, nullable=True)
    student_answer = db.Column(db.Text, nullable=True)
    student_feedback = db.Column(db.Text, nullable=True)
    no_of_attempts = db.Column(
        db.Integer,
        db.ForeignKey("published_student_assessment.no_of_attempts"),
        nullable=False,
    )  # foreign key from published_student_assessment table


# class MultipleChoice(Question):
#     """
#     Authored by Devajith
#     """

#     __tablename__ = "multiple_choice"

#     question_id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.Text, nullable=False)  # the actual question
#     question_description = db.Column(db.Text, nullable=False)  # further information
#     correct_answer = db.Column(db.Text, nullable=True)
#     person_id = db.Column(
#         db.Integer, db.ForeignKey("user.id"), nullable=False
#     ) # foreign key from user table
#     feedback = db.Column(db.Text, nullable=True)
#     max_marks = db.Column(db.Integer, nullable=True)  # added by henry

#     choices = db.Column(
#         db.Text, nullable=False
#     )  # Save as json


# class ShortWrittenAnswer(Question):
#     """
#     Authored by Henry
#     Modified by Julius
#     """

#     __tablename__ = "short_written_answer"


class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    hashed_password = db.Column(db.String(128))
    modules = db.Column(
        db.Text, nullable=True
    )  # nullable should be false, but for dev test I make it true.
    # module-student relationship is descriped in modulestudent table
    courses = db.Column(db.Text, nullable=True)
    # new attributes
    is_student = db.Column(db.Boolean, nullable=False)
    assessment_list = db.Column(db.Text, nullable=True)
    extra_time = db.Column(db.Boolean, nullable=False, default=False)

    # relationship()
    module_student = db.relationship("ModuleStudent", backref="user", lazy=True)
    student_answer = db.relationship("StudentAnswer", backref="user", lazy=True)
    # question = db.relationship("Question", backref="user", lazy=True)
    published_student_assessment = db.relationship(
        "PublishedStudentAssessment", backref="user", lazy=True
    )
    question_contributors = db.relationship(
        "QuestionContributors", backref="user", lazy=True
    )

    @property
    def password(self):
        raise AttributeError("Password is not readable.")

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Course(db.Model):
    """
    Authored by Julius (Qiye)
    """

    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.Text, nullable=False)

    # relationship()
    module = db.relationship("Module", backref="course", lazy=True)


class Module(db.Model):
    """
    Authored by Julius (Qiye)
    """

    __tablename__ = "module"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(
        db.Integer, db.ForeignKey("course.id"), nullable=False
    )  # foreign key from course table
    module_name = db.Column(db.Text, nullable=False)

    # relationship()
    assessment = db.relationship("Assessment", backref="module", lazy=True)


class ModuleStudent(db.Model):
    """
    Authored by Julius (Qiye)
    """

    __tablename__ = "module_student"
    module_id = db.Column(
        db.Integer, db.ForeignKey("module.id"), primary_key=True, autoincrement=False
    )  # foreign key from module table
    student_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, autoincrement=False
    )  # foreign key from user table


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
