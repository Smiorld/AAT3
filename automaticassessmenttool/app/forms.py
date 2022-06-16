from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import (
    DateTimeLocalField,
    SelectField,
    BooleanField,
    StringField,
    PasswordField,
    validators,
    IntegerField,
    SubmitField,
    HiddenField
)
from wtforms.fields import FieldList, FormField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError
from wtforms.widgets import TextArea

from app import db
from flask_ckeditor import CKEditorField
from app.models import User

class CodeForm(FlaskForm):
    name = StringField("name")
    inputs = StringField("inputs")
    outputs = StringField("outputs")

class QuestionForm(FlaskForm):
    question_id = HiddenField('Question ID')
    question = CKEditorField("Question")
    question_description = StringField("Further information")
    correct_answer = StringField("Answer")
    feedback = StringField("Feedback")
    correct_feedback = CKEditorField("Feedback for correct answers")
    incorrect_feedback = CKEditorField("Feedback for incorrect answers")
    arguments = StringField("Arguments")
    flist = FieldList(StringField("Fields"))
    test_inputs = StringField("Test case inputs")
    expected_outputs = StringField("Test case outputs")
    max_marks = IntegerField("Maximum marks")
    category = StringField("Category")
    difficulty = SelectField("Difficulty level", choices=([(0, ""),(1, "Easy"), (2, "Medium"), (3, "Hard")]))
    points = IntegerField("Maximum marks")
    choices = StringField("Multiple choices")
    submit = SubmitField("Add and Test Question")
    no_tests = IntegerField("Number of Test Cases")

class CodeQuestionForm(FlaskForm):
    question_id = HiddenField('Question ID')
    question = StringField("Question", widget=TextArea(), validators=[DataRequired()])
    correct_feedback = CKEditorField("Feedback for correct answers", validators=[DataRequired()])
    incorrect_feedback = CKEditorField("Feedback for incorrect answers", validators=[DataRequired()])
    arguments = StringField("Arguments")
    flist = FieldList(StringField("Fields"))
    test_inputs = StringField("Test case inputs")
    expected_outputs = StringField("Test case outputs", validators=[DataRequired()])
    max_marks = IntegerField("Maximum marks", validators=[DataRequired()])
    category = StringField("Category")
    difficulty = SelectField("Difficulty level", choices=([(0, ""),(1, "Easy"), (2, "Medium"), (3, "Hard")]))
    submit = SubmitField("Add and Test Question")
    no_tests = IntegerField("Number of Test Cases")

class MCQForm(FlaskForm):
    correct_feedback = CKEditorField("Feedback for correct answers")
    incorrect_feedback = CKEditorField("Feedback for incorrect answers")

class LoginForm(FlaskForm):
    email = StringField(
        "Email", render_kw={"placeholder": "Email"}, validators=[DataRequired()]
    )
    password = PasswordField(
        "Password", render_kw={"placeholder": "Password"}, validators=[DataRequired()]
    )
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    first_name = StringField(
        "Firstname", render_kw={"placeholder": "Firstname"}, validators=[DataRequired()]
    )
    last_name = StringField(
        "Lastname", render_kw={"placeholder": "Lastname"}, validators=[DataRequired()]
    )
    email = StringField(
        "Email",
        render_kw={"placeholder": "email"},
        validators=[DataRequired(), Email(message="Invalid email. Please Check.")],
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "password"},
        validators=[
            DataRequired(),
            Regexp(
                "^[0-9a-zA-Z]{6,20}$",
                message="Your password contains invalid characters.",
            ),
            EqualTo(
                "confirm_password", message="Passwords do not match. Please try again."
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        render_kw={"placeholder": "confirm password"},
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("Email already exists. Please login.")


class CreateAssessmentForm(FlaskForm):
    module_id = StringField("Module ID", validators=[DataRequired()])
    assessment_name = StringField("Assessment Name", validators=[DataRequired()])
    hand_in_date = DateTimeLocalField(
        "Hand in Date", format="%d%b%Y %H:%M", validators=[DataRequired()]
    )
    hand_out_date = DateTimeLocalField(
        "Hand out Date", format="%d%b%Y %H:%M", validators=[DataRequired()]
    )
    is_summative = SelectField(
        "is_summative",
        choices=[(True, "Summative"), (False, "Formative")],
        default=True,
    )
    time_allotted = StringField("Time Allotted", validators=[DataRequired()], default="0")
    submit = SubmitField("Create")


class AttemptSelectForm(FlaskForm):
    attempt = SelectField("Attempt", choices =[])


class ModuleSortForm(FlaskForm):
    module = SelectField("Module", choices =[])


class GenerateFormativeAssessment(FlaskForm):
    category = SelectField("category", choices =[("Arrays,Loops", "All"),("Arrays","Arrays"),("Loops","Loops")])
    easy = BooleanField("easy", default="checked")
    medium = BooleanField("medium", default="checked")
    hard = BooleanField("hard", default="checked")
    question_type = SelectField("question type", choices = [(" ", "All"),(0,"Coding"),(1,"Multiple Choice")])
    question_quant = IntegerField("number of questions", default=1)
    submit = SubmitField("Generate")


class QuestionContributorForm(FlaskForm):
    user_email = StringField("email", validators=[DataRequired()])
    submit = SubmitField("Share")