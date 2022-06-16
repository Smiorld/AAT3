from itertools import count
import os
import ast
import json
from queue import Empty
import random
from datetime import datetime, timedelta
from random import choice, choices
import requests
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    flash,
    escape,
    jsonify,
    make_response,
)
from app import app, db
from app.forms import MCQForm, QuestionForm, LoginForm, RegistrationForm, CreateAssessmentForm, AttemptSelectForm, \
    ModuleSortForm, GenerateFormativeAssessment, QuestionContributorForm, CodeQuestionForm
from app.models import (
    User,
    Question,
    Assessment,
    Module,
    PublishedStudentAssessment,
    ModuleStudent,
    QuestionContributors,
    Assessment2Question, 
    StudentAnswer,
)
from flask_login import logout_user, login_user, current_user, login_required
from subprocess import run


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html", title="home")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash(
                "You've successfully logged in," + " " + current_user.first_name + "!"
            )
            return redirect(url_for("home"))
        flash("Login Error!")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password.data,
                email=form.email.data,
                is_student=True,
            )  # consider how faculty/ students are dealt with
            db.session.add(user)
            db.session.commit()
            flash("Registration successful!")
            new_user = User.query.filter_by(
                email=form.email.data
            ).first()  # last_name=form.last_name.data,
            login_user(new_user)
            return redirect(url_for("home"))
        else:
            flash("Sorry, there is a problem with your registration.")
            return render_template("register.html", form=form)
    return render_template("register.html", title="Register", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've successfully logged out!")
    return redirect(url_for("home"))


@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    return render_template("add_question.html")

# Faculty edits an unpublished assessment
@app.route("/edit_question/<int:question_id>",methods=["GET","POST"])
def edit_question(question_id):
    question = Question.query.filter_by(id=question_id).first()  
    if question.is_multiple_choice:
        return redirect(f"/add_mcq?question_id={question_id}")
    else:
        return redirect(f"/add_coding_question?question_id={question_id}")


@app.route("/add_coding_question", methods=["GET", "POST"])
@login_required
def add_coding_question():
    form = CodeQuestionForm()
    dic_test_inputs = None
    dic_test_outputs = None
    list_test_name = None
    list_test_input = None
    list_test_output = None
    no_test_cases = 1
    if request.method == 'GET':
        args = request.args
        question_id = args.get("question_id")
        question = Question.query.get(question_id) # replace q_id
        try:
            dic_test_inputs = ast.literal_eval(question.test_inputs)
            dic_test_outputs = ast.literal_eval(question.expected_outputs)
            list_test_name = [x for x in dic_test_inputs.keys()]
            list_test_input = [x for x in dic_test_inputs.values()]
            list_test_output = [x for x in dic_test_outputs.values()]
            no_test_cases = len(list_test_name)
        except:
            pass

    difficulty_map = {
        '1': "Easy",
        '2': "Medium",
        '3': "Hard"
    }

    if request.method == "POST":
        if current_user.is_authenticated:
            person_id = current_user.id
            question_id = request.form["question_id"]
            question = request.form["question"]
            no_tests = int(request.form["no_tests"])
            print(no_tests)
            test_input_dictionary = {}
            test_output_dictionary = {}
            for num in range(0, no_tests):
                data = request.form.getlist(f'flist{num}[]')
                print(data)
                name, input, output = data[0], data[1], data[2]
                # make numbers from strings
                test_input_dictionary[name] = input
                test_output_dictionary[name] = output
            correct_feedback = request.form["correct_feedback"]
            arguments = request.form["arguments"]
            incorrect_feedback = request.form["incorrect_feedback"]
            max_marks = int(request.form["max_marks"]) * (no_tests)
            category = request.form["category"]
            difficulty = difficulty_map[request.form["difficulty"]]
            test_inputs = str(test_input_dictionary)
            expected_outputs = str(test_output_dictionary)
            is_multiple_choice = False
            no_test_in= len(test_input_dictionary.keys())

            if question_id:
                question_object = Question.query.get(question_id)
                question_object.question = question
                question_object.test_inputs=test_inputs
                question_object.expected_outputs=expected_outputs
                question_object.correct_feedback=correct_feedback
                question_object.incorrect_feedback=incorrect_feedback
                question_object.arguments = arguments
                question_object.max_marks= max_marks
                question_object.category=category
                question_object.difficulty=difficulty
                question_object.is_multiple_choice=is_multiple_choice
                db.session.commit()
            else:
                question_object = Question(
                    question=question,
                    test_inputs=test_inputs,
                    expected_outputs=expected_outputs,
                    correct_feedback=correct_feedback,
                    incorrect_feedback=incorrect_feedback,
                    arguments = arguments,
                    max_marks=max_marks,
                    category=category,
                    difficulty=difficulty,
                    is_multiple_choice=is_multiple_choice
                )
                db.session.add(question_object)
            question_contributor = QuestionContributors(
                user_id=person_id, question=question_object, role="Author"
            )
            db.session.add(question_contributor)
            db.session.commit()
            question = Question.query.filter_by(question=question, test_inputs=test_inputs, expected_outputs=expected_outputs).first()
            flash("Question saved sucessfully")
            return redirect(url_for("coding_question", question_id=question.id, list_test_name=list_test_name,
                           list_test_output=list_test_output, list_test_input=list_test_input,
                           no_test_cases = no_test_cases))
    return render_template("add_coding_question.html", form=form, list_test_name=list_test_name,
                           list_test_output=list_test_output, list_test_input=list_test_input,
                           no_test_cases = no_test_cases)

@login_required
@app.route("/add_mcq", methods=["GET", "POST"])
def add_mcq():
    form = MCQForm()
    if request.method == "POST":
        data = request.get_json(force=True)
        if current_user.is_authenticated:
            person_id = current_user.id

            choices = []
            correct_answer = []

            for option in data["options"]:
                choices.append(option["optionVal"])
                if option["correctness"]:
                    correct_answer.append(option["optionVal"])
            
            correct_feedback = data["correct_feedback"]
            if not correct_feedback:
                correct_feedback = "Congratulations, your answers are correct"

            incorrect_feedback = data["incorrect_feedback"]
            if not incorrect_feedback:
                incorrect_feedback = f"Correct answers are {','.join(correct_answer)}"

            
            if "question_id" in data:
                question_object = Question.query.get(data["question_id"])
                question_object.question = data["question"]
                question_object.question_description=data["description"]
                question_object.max_marks=data["max_marks"]
                question_object.category=data["category"]
                question_object.difficulty=data["difficulty"]
                question_object.is_multiple_choice = True
                question_object.options=json.dumps(data["options"])
                question_object.choices=",".join(choices)
                question_object.total_choices=len(choices)
                question_object.correct_answer=",".join(correct_answer)
                question_object.correct_answer_count=len(correct_answer)
                question_object.correct_feedback=correct_feedback
                question_object.incorrect_feedback=incorrect_feedback
                db.session.commit()
            else:
                question_object = Question(
                    question=data["question"],
                    question_description=data["description"],
                    max_marks=data["max_marks"],
                    category=data["category"],
                    difficulty=data["difficulty"],
                    is_multiple_choice = True,
                    options=json.dumps(data["options"]),
                    choices=",".join(choices),
                    total_choices=len(choices),
                    correct_answer=",".join(correct_answer),
                    correct_answer_count=len(correct_answer),
                    correct_feedback=correct_feedback,
                    incorrect_feedback=incorrect_feedback
                )
                db.session.add(question_object)
            question_contributor = QuestionContributors(
                user_id=person_id, question=question_object, role="Author"
            )
            db.session.add(question_contributor)
            db.session.commit()
            flash("Question added sucessfully")
            return redirect(url_for("add_question"))

    return render_template("add_mcq.html", form=form)

@app.route("/api/google_search", methods=["POST"])
def google_search():
    data = request.get_json(force=True)
    url = f'http://129.213.165.158:3000/google_search?search={data["query"]}'
    x = requests.get(url)
    result = json.loads(x.text)
    if result["featured_snippet"]["description"]=="N/A":
        del result["featured_snippet"]
    if result["knowledge_panel"]["description"]=="N/A":
        del result["knowledge_panel"]
    
    # del result["results"]
    # print(json.dumps(result, indent=4, sort_keys=True))
    return result

@app.route("/api/generate_feedback_mcq", methods=["POST"])
def generate_feedback_mcq():
    data = request.get_json(force=True)
    print(data)
    question = data["question"]
    choices = []
    correct_answer = []

    for option in data["options"]:
        choices.append(option["optionVal"])
        if option["correctness"]:
            correct_answer.append(option["optionVal"])
    
    correct_feedback = "Congratulations, your answers are correct.\n"
    incorrect_feedback = f"Correct answer(s) are {','.join(correct_answer)}.\n"

    url = f'http://129.213.165.158:3000/google_search?search={question}'
    x = requests.get(url)
    result = json.loads(x.text)
    if result["featured_snippet"]["description"]=="N/A":
        del result["featured_snippet"]
    else:
        correct_feedback+=result["featured_snippet"]["description"]+ "\n"
        incorrect_feedback+=result["featured_snippet"]["description"]+ "\n"

    if result["knowledge_panel"]["description"]=="N/A":
        del result["knowledge_panel"]
    else:
        incorrect_feedback += result["knowledge_panel"]["description"] + "\n"
    
    print(url)
    incorrect_feedback+=f"You can learn more about this at {result['results'][0]['url']}."
    # del result["results"]
    # print(json.dumps(result, indent=4, sort_keys=True))
    feedbacks = {
        "correct_feedback": correct_feedback,
        "incorrect_feedback": incorrect_feedback
    }
    return feedbacks

@app.route("/api/get_questions", methods=["POST"])
def get_questions():
    data = request.get_json(force=True)
    question = Question.query.filter_by(id=data["question_id"]).first()
    question_dict = question.as_dict()
    print(question_dict["options"])
    if question_dict["is_multiple_choice"] == True:
        question_dict["options"] = json.loads(question_dict["options"])

    return question_dict

@app.route("/view_questions", methods=["GET", "POST"])
def view_questions():
    user_id = current_user.id
    field = None
    search_value = None
    questions = Question.query.join(Question.question_contributors).filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        field = request.form["field"]
        search_value = request.form["search_value"]
        # filters based on question contributors and category/difficutly level
        if field == "difficulty" and search_value:
            questions = Question.query.filter(Question.difficulty.like("%"+search_value+"%")).join(Question.question_contributors).filter_by(user_id=current_user.id).all()
        elif field == "category" and search_value:
            questions = Question.query.filter(Question.category.like("%"+search_value+"%")).join(Question.question_contributors).filter_by(user_id=current_user.id).all()
        
    return render_template("faculty_questions.html", questions=questions, field=field, search_value=search_value)


@app.route("/share_question/<int:question_id>", methods=["GET", "POST"])
def share_question(question_id):
    field = None
    search_value = None
    form = QuestionContributorForm()
    questions = Question.query.join(Question.question_contributors).filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        email = request.form["user_email"]
        share_user = User.query.filter_by(email=email, is_student=False).first()
        if share_user:
            question_contributor = QuestionContributors(user_id=share_user.id, question_id=question_id, role="Contributor")
            db.session.add(question_contributor)
            db.session.commit()
            flash(f"Question shared with {email}!", "message")
            return render_template("faculty_questions.html", questions=questions, field=field, search_value=search_value)
        else:
            flash("no user with that email address!", "error")
            return render_template("share_question.html", form=form, question_id=question_id)
    return render_template("share_question.html", form=form, question_id=question_id)


@app.template_filter('question_contributor_number') #
def question_contributor_number(question_id):
    contributors = QuestionContributors.query.filter_by(question_id=question_id).all()
    contributors_num = 0
    for c in contributors:
        contributors_num += 1
    return contributors_num


# Faculty deletes an unpublished assessment
@app.route("/delete_question/<int:question_id>")
def delete_question(question_id):
    contributors = QuestionContributors.query.filter_by(question_id=question_id).all()
    contributors_num = 0
    for c in contributors:
        contributors_num += 1
    assessment_q = Assessment2Question.query.filter_by(question_id=question_id).first()
    if contributors_num > 1 or assessment_q != None:
        QuestionContributors.query.filter_by(question_id=question_id, user_id=current_user.id).delete()
    if contributors_num == 1:
        Question.query.filter_by(id=question_id).delete()
    db.session.commit()
    return redirect(url_for("view_questions"))

@app.route("/coding_question/<int:question_id>", methods=["GET", "POST"])
def coding_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    return render_template("coding_question.html", question=question, question_id=question.id)


@app.route("/test", methods=["POST"])
def test():
    CODE_FOLDER = "app/static/js/code/"

    if request.method == "POST":
        code = request.form["code"]
        question_id = request.form["question_id"]
        # only sent following adding q to database
        faculty_test = request.form["faculty_test"]
        if faculty_test != 1:
            assessment_id = request.form["assessment_id"] #robchange
        # sets up python file for running the students code
        question = Question.query.filter_by(id=question_id).first()
        with open(CODE_FOLDER + "tests.py", "r") as file:
            lines=file.readlines()
        lines[6] = "    return " + question.test_inputs +"\n"
        lines[9] = "    return " + question.expected_outputs +"\n"
        with open(CODE_FOLDER + "tests.py", 'w', encoding='utf-8') as file:
            file.writelines(lines)
        file.close()
        try:
            f = open(CODE_FOLDER + "input_code.py", "w")
            f.write(code)
            f.close()
            output = run(
                "python " + CODE_FOLDER + "tests.py", capture_output=True
            ).stdout  # may have bugs when used with other machines
            if len(output) == 0:
                output = "Syntax Error"
            # gets marks from output (7th index - very hacky and wont work for anything past > 9 marks)
            # if time, fix by making variable and pushing to front end.
            passed = output[7:8]
            try:
                print(int(passed))
                marks = int(passed)
            # 0 marks for syntax error
            except:
                marks = 0
            result = make_response(output, 200)
            if marks == question.max_marks:
                student_feedback = question.correct_feedback
            else:
                student_feedback = question.incorrect_feedback
            # query database/ submit student answer
            if not int(faculty_test):
                PSA = PublishedStudentAssessment.query.filter_by(assessment_id=assessment_id,student_id=current_user.id).all()[-1] #robchange

                existing_answer = StudentAnswer.query.filter_by(question_id=question_id,
                                                                student_id=current_user.id,
                                                                no_of_attempts=PSA.no_of_attempts).first()  # do we need assessment id as well?? #robchange
                if existing_answer:
                    existing_answer.marks = marks
                    existing_answer.student_answer = code
                    existing_answer.student_feedback = student_feedback  # no_of_attempts??
                    db.session.commit()
                    print("updated existing")
                else:
                    student_answer = StudentAnswer(question_id=question_id, student_id=current_user.id, marks=marks,
                                                   student_answer=code, student_feedback=student_feedback, no_of_attempts=PSA.no_of_attempts) ## need help regarding getting publishstudent assessment number of attempts #robchange
                    db.session.add(student_answer)
                    db.session.commit()
                    print("created new answer")
            return result

        except Exception as e:
            print(e)
            return str(e), 400


# Julius part

# This is the faculty assessment dashboard page, showing all assessments.
@app.route("/faculty_assessments", methods=["GET", "POST"])
def faculty_assessments():
    assessments = Assessment.query.all()
    field=None
    search_value=None
    if request.method == "POST":
        field = request.form["field"]
        search_value = request.form["search_value"]
        if field == "module_id" and search_value:
            assessments = Assessment.query.filter(Assessment.module_id.like("%"+search_value+"%")).all()
        elif field == "assessment_name" and search_value:
            assessments = Assessment.query.filter(Assessment.assessment_name.like("%"+search_value+"%")).all()
        elif field == "module_name" and search_value:
            module_id = Module.query.filter(Module.module_name.like("%"+search_value+"%")).first()
            if module_id :
                assessments = Assessment.query.filter_by(module_id=module_id.id).all()
            else:
                assessments =[]
    return render_template("faculty_assessments.html", assessments=assessments, field=field, search_value=search_value)

# Faculty view detail information about an assessment.
@app.route("/detail_assessment/<int:assessment_id>")
def detail_assessment(assessment_id):
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    added_questions = Assessment2Question.query.filter_by(assessment_id=assessment_id).all()
    return render_template("detail_assessment.html", assessment=assessment, added_questions=added_questions)

# Faculty publish an assessment. Create rows in PublishedAssessment table.
@app.route("/publish_assessment/<int:assessment_id>")
def publish_assessment(assessment_id):
    # if(current_user.is_student):
    #     flash("You're not authorized.","warning")
    #     return redirect(url_for('home'))
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    if assessment.is_draft:  # only unpublished assessment can be published
        assessment.is_draft = False
        db.session.commit()
        modulestudents = ModuleStudent.query.filter_by(
            module_id=assessment.module_id
        ).all()
        for modulestudent in modulestudents:
            publishtmp = PublishedStudentAssessment(
                assessment_id=assessment.id,
                student_id=modulestudent.student_id,
                no_of_attempts=1,
                is_complete=False,
            )
            db.session.add(publishtmp)
        db.session.commit()
        flash("Successfully published.")
        return redirect(url_for("faculty_assessments"))
    flash("Publish unsuccessful. Please refresh and try again.", "warning")
    return redirect(url_for("faculty_assessments"))

# Faculty edits an unpublished assessment
@app.route("/edit_assessment/<int:assessment_id>",methods=["GET","POST"])
def edit_assessment(assessment_id):
    form=CreateAssessmentForm()
    field=None
    search_value=None
    assessment = Assessment.query.filter_by(id=assessment_id).first()  
    if request.method=="POST":
        if request.form["is_summative"] == "True":
            assessment.is_summative = True
        else:
            assessment.is_summative = False
        assessment.module_id = request.form["module_id"]
        assessment.assessment_name = request.form["assessment_name"]
        assessment.hand_in_date = datetime.strptime(
                request.form["hand_in_date"], "%Y-%m-%dT%H:%M"
            )
        assessment.hand_out_date = datetime.strptime(
                request.form["hand_out_date"], "%Y-%m-%dT%H:%M"
            )
        db.session.commit()  
        flash("Successfully edited assessment .")
        return redirect(url_for("edit_assessment",assessment_id=assessment.id))
      
    added_questions = Assessment2Question.query.filter_by(assessment_id=assessment_id).all()
    questions_repository = Question.query.order_by(Question.id).all()
    return render_template("edit_assessment.html", form=form, assessment=assessment, added_questions=added_questions, questions_repository=questions_repository, field=field, search_value=search_value)

# Faculty searches for a question to add to an assessment.
@app.route("/search_question_for_assessment/<int:assessment_id>", methods=["GET", "POST"])
def search_question_for_assessment(assessment_id):
    form=CreateAssessmentForm()
    field=None
    search_value=None
    assessment = Assessment.query.filter_by(id=assessment_id).first()  
    added_questions = Assessment2Question.query.filter_by(assessment_id=assessment_id).all()
    questions_repository = Question.query.order_by(Question.id).all()
    if request.method == "POST":
        field = request.form["field"]
        search_value = request.form["search_value"]
        if field == "question" and search_value:
            questions_repository = Question.query.filter(Question.question.like("%"+search_value+"%")).all()
        elif field == "difficulty" and search_value:
            questions_repository = Question.query.filter(Question.difficulty.like("%"+search_value+"%")).all()
        elif field == "category" and search_value:
            questions_repository = Question.query.filter(Question.category.like("%"+search_value+"%")).all()
        elif field == "question_id" and search_value:
            questions_repository = Question.query.filter(Question.id.like("%"+search_value+"%")).all()
    return render_template("edit_assessment.html",form=form, assessment=assessment, added_questions=added_questions, questions_repository=questions_repository, field=field, search_value=search_value )

# Faculty deletes an unpublished assessment
@app.route("/delete_assessment/<int:assessment_id>")
def delete_assessment(assessment_id):
    # if(current_user.is_student):
    #     flash("You're not authorized.","warning")
    #     return redirect(url_for('home'))
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    if assessment.is_draft == False:
        flash("You can not delete published assessments.", "warning")
        return redirect(url_for("faculty_assessments"))
    Assessment.query.filter_by(id=assessment_id).delete()
    db.session.commit()
    flash("Successfully delete assessment.")
    return redirect(url_for("faculty_assessments"))

# Faculty add a question to this assessment. When adding a question, the total marks of the assessment will be updated.
@app.route("/add_assessment2question/<int:assessment_id>/<int:question_id>", methods=["GET", "POST"])
def add_assessment2question(assessment_id, question_id):
    #check duplicate question
    exist = Assessment2Question.query.filter_by(assessment_id=assessment_id, question_id=question_id).first()
    if exist:
        flash("The question has already been added to the assessment.", "warning")
        return redirect(url_for("edit_assessment", assessment_id=assessment_id))
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    assessment2question = Assessment2Question(assessment_id=assessment_id, question_id=question_id)
    added_questions= Assessment2Question.query.filter_by(assessment_id=assessment_id).all()
    tmp_marks=Question.query.filter_by(id=question_id).first().max_marks
    for question in added_questions:
        tmp_marks+=question.question.max_marks
    assessment.total_marks=tmp_marks
    db.session.add(assessment2question)
    db.session.commit()
    flash("Successfully added a question to the assessment.")
    return redirect(url_for("edit_assessment", assessment_id=assessment_id))

# Remove a question from an assessment. When removes a question, the total marks of the assessment will be reduced.
@app.route("/remove_assessment2question/<int:assessment_id>/<int:question_id>")
def remove_assessment2question(assessment_id, question_id):
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    assessment2question = Assessment2Question.query.filter_by(assessment_id=assessment_id, question_id=question_id).first()
    assessment.total_marks -= assessment2question.question.max_marks
    db.session.delete(assessment2question)
    db.session.commit()
    flash("Successfully removed question from assessment.")
    return redirect(url_for("edit_assessment", assessment_id=assessment_id))

# Create a new assessment from scratch
@app.route("/add_assessments", methods=["GET", "POST"])
def add_assessments():
    form = CreateAssessmentForm()
    if request.method == "POST":
        # if form.validate_on_submit(): # not yet implemented
        if request.form["is_summative"] == "True":
            is_summative = True
        else:
            is_summative = False

        new_assessment = Assessment(
            module_id=request.form["module_id"],
            assessment_name=request.form["assessment_name"],
            hand_in_date=datetime.strptime(
                request.form["hand_in_date"], "%Y-%m-%dT%H:%M"
            ),
            hand_out_date=datetime.strptime(
                request.form["hand_out_date"], "%Y-%m-%dT%H:%M"
            ),
            is_summative=is_summative
        )
        db.session.add(new_assessment)
        db.session.commit()
        flash("Successfully added an assessment.")
        return redirect(url_for("faculty_assessments"))
    return render_template("add_assessments.html", form=form)

# This is the student assessment dashboard page, showing their assessments.
@app.route("/student_assessments", methods=["GET", "POST"])
def student_assessments():
    modules = ModuleStudent.query.filter_by(student_id=current_user.id).all()
    module_list = [str(x.module_id) for x in modules]
    form = ModuleSortForm()
    form.module.choices = [("show all", "Show All")]+[(x, str(x)) for x in module_list]
    now = datetime.now()
    PSA = PublishedStudentAssessment.query.filter_by(student_id=current_user.id).all()
    if request.method == "POST":
        if form.module.data == "show all":
            PSA_reloaded = PSA
        else:
            module_assessments = Assessment.query.filter_by(module_id=form.module.data)
            assessment_id_list = [x.id for x in module_assessments]
            PSA_reloaded = PublishedStudentAssessment.query.filter(PublishedStudentAssessment.student_id==current_user.id,PublishedStudentAssessment.assessment_id.in_(assessment_id_list)).all()
        return render_template("student_assessments.html", PSA=PSA_reloaded, now=now, form=form)
    return render_template("student_assessments.html", PSA=PSA, now=now, form=form)

# Display only assessments for which the hand out date has passed
@app.route("/take_assessment/<int:assessment_id>", methods=["GET", "POST"])
def take_assessment(assessment_id):
    assessment_id = assessment_id
    questions = Assessment2Question.query.filter_by(assessment_id=assessment_id).all()
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    # Dictionary to help limit number of questions selected during assessment
    choices_dict = {}
    for q in questions:
        if q.question.is_multiple_choice:
            choices_dict[q.question.id] = q.question.total_choices
    if current_user.extra_time:
        t = assessment.time_allotted*1.5
    else:
        t = assessment.time_allotted
    return render_template("take_assessment.html", questions=questions, assessment=assessment, assessment_id = assessment_id, choices_dict=choices_dict, t=t)

def assessment_function(questions, current_assessment, answer_dict, time_taken):
    for q in questions:
        if q.question.is_multiple_choice:
            answers = q.question.correct_answer.split(",")
            answers = [q.strip() for q in answers]
            marks = 0
            for question in answer_dict.get(str(q.question.id)):
                if question in answers:
                    marks += 1
            if [q.question.correct_answer] == answer_dict.get(str(q.question.id)):
                answer = StudentAnswer(
                    question_id = q.question.id,
                    student_id = current_user.id,
                    marks = marks,
                    student_answer = ", ".join(answer_dict.get(str(q.question.id))),
                    student_feedback = q.question.correct_feedback,
                    no_of_attempts = current_assessment.no_of_attempts,
                )
            else:
                answer = StudentAnswer(
                    question_id = q.question.id,
                    student_id = current_user.id,
                    marks = marks,
                    student_answer = ", ".join(answer_dict.get(str(q.question.id))),
                    student_feedback = q.question.incorrect_feedback,
                    no_of_attempts = current_assessment.no_of_attempts,
                )
            db.session.add(answer)
            db.session.commit()
    if current_assessment.assessment.is_summative != True:
        new_PSA = PublishedStudentAssessment (
            assessment_id=current_assessment.assessment.id,
            student_id=current_user.id,
            no_of_attempts=current_assessment.no_of_attempts+1,
            is_complete=False,
            awarded_marks=0,
        )
        db.session.add(new_PSA)
        db.session.commit() 
    
    counted_marks=0
    current_questions = [x.question_id for x in questions]
    current_answers = StudentAnswer.query.filter(StudentAnswer.question_id.in_(current_questions),StudentAnswer.no_of_attempts==current_assessment.no_of_attempts)
    for a in current_answers:
        counted_marks += a.marks
    current_assessment.is_complete = True
    current_assessment.awarded_marks = counted_marks
    current_assessment.time_taken = time_taken
    db.session.commit()

@app.route("/auto_assess/<int:assessment_id>", methods=["GET","POST"])
def auto_assess(assessment_id):
    req = request.get_json()
    questions = Assessment2Question.query.filter_by(assessment_id=assessment_id).all()
    current_assessment = PublishedStudentAssessment.query.filter_by(assessment_id=assessment_id,student_id=current_user.id).all()[-1]
    assessment_function(questions, current_assessment, req[0], req[1])

    res = make_response(jsonify(req), 200)
    return res

@app.route("/auto_submit_assess/<int:assessment_id>", methods=["GET","POST"])
def auto_submit_assess(assessment_id):
    req = request.get_json()
    questions = Assessment2Question.query.filter_by(assessment_id=assessment_id).all()
    current_assessment = PublishedStudentAssessment.query.filter_by(assessment_id=assessment_id,student_id=current_user.id).all()[-1]
    for q in questions:
        if q.question.id not in req and q.question.is_multiple_choice:
            req[str(q.question.id)] = ["No answer given."]
        elif q.question.id not in req and not q.question.is_multiple_choice:
            student_answer = StudentAnswer(question_id=q.question.id, student_id=current_user.id, marks=0,
                                                   student_answer="No answer given.", student_feedback=q.question.incorrect_feedback, no_of_attempts=current_assessment.no_of_attempts)
            db.session.add(student_answer)
            db.session.commit()
    assessment_function(questions, current_assessment, req[0], req[1])
                    
    res = make_response(jsonify(req), 200)
    return res


# Implement dropdown menu to switch between attempts
@app.route("/assessment_feedback/<int:assessment_id>", methods=["GET","POST"])
def assessment_feedback(assessment_id):
    PSA = PublishedStudentAssessment.query.filter_by(assessment_id=assessment_id,student_id=current_user.id,is_complete=True).all()
    attemptLength = list(range(1,len(PSA)+1))
    form = AttemptSelectForm()
    form.attempt.choices = [(x, "Attempt " +str(x)) for x in attemptLength[::-1]]
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    questions = Assessment2Question.query.filter_by(assessment_id=assessment_id).all()
    id_list = []
    for q in questions:
        id_list.append(q.question_id)
    answers = StudentAnswer.query.filter(StudentAnswer.question_id.in_(id_list),StudentAnswer.student_id == current_user.id,StudentAnswer.no_of_attempts==len(PSA)).order_by(StudentAnswer.question_id)
    if request.method == "POST":
        answers_reload = StudentAnswer.query.filter_by(student_id=current_user.id, no_of_attempts=form.attempt.data)
        return render_template("assessment_feedback.html", questions=questions, answers=answers_reload, assessment=assessment, form=form, current_PSA=PSA[int(form.attempt.data)-1])

    
    return render_template("assessment_feedback.html", questions=questions, answers=answers, assessment=assessment, form=form, current_PSA=PSA[-1])

@app.route("/generate_formative", methods=["GET","POST"])
def generate_formative():
    form = GenerateFormativeAssessment()
    if request.method == "POST":
        q_type = form.question_type.data.split(",")
        categoryList = form.category.data.split(",")
        difficultyList = []
        if form.easy.data:
            difficultyList.append("easy")
        if form.medium.data:
            difficultyList.append("medium")
        if form.hard.data:
            difficultyList.append("hard")  
        if q_type == [' ']:
            questions = Question.query.filter(Question.category.in_(categoryList),Question.difficulty.in_(difficultyList)).all()
        else:
            questions = Question.query.filter(Question.is_multiple_choice == bool(q_type),Question.category.in_(categoryList),Question.difficulty.in_(difficultyList)).all()
        if len(questions) >= form.question_quant.data > 0:
            random_qs = random.sample(range(1, len(questions)), form.question_quant.data)
            generated_qs = []
            for id in random_qs:
                generated_qs.append(questions[id].id)
                t_marks = 0
            for q in random_qs:
                t_marks += questions[q].max_marks
            assessment = Assessment(
                module_id = 999,
                assessment_name = current_user.first_name+"'s randomly generated assessment",
                hand_out_date = datetime.now(),
                is_summative = False,
                is_draft = False,
                total_marks = t_marks, 
            )
            db.session.add(assessment)
            db.session.commit() 
            #Create appropriate ass_2_question
            for i in range(form.question_quant.data):
                a2q = Assessment2Question(
                    assessment_id = assessment.id,
                    question_id = generated_qs[i],
                )
                db.session.add(a2q)
                db.session.commit() 
            #Create publishedStudentAssessment
            new_PSA = PublishedStudentAssessment (
                assessment_id=assessment.id,
                student_id=current_user.id,
                no_of_attempts=1,
                is_complete=False,
                awarded_marks=0,
            )
            db.session.add(new_PSA)
            db.session.commit() 
            return redirect(url_for("take_assessment",assessment_id=assessment.id))
        elif form.question_quant.data == 0:
            flash(
                "You must select at least one question.","warning"
            )
        else:
            flash(
                "There aren't this many questions in the database.","warning"
            )
    return render_template("generate_formative.html", form=form)


#Review stats dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")
    
@app.route("/student_review", methods=["GET","POST"])
def student_review():
    PSA = PublishedStudentAssessment.query.filter_by(student_id=current_user.id).all()
    psa_not_finished = PublishedStudentAssessment.query.filter_by(student_id=current_user.id,is_complete=False).count()
    psa_total=len(PSA)
    psa_finished=psa_total-psa_not_finished
    #psa_not_finished=len(PSA)
    now = datetime.now()
    return render_template("student_review.html", PSA=PSA,now=now,psa_total=psa_total,psa_finished=psa_finished,psa_not_finished=psa_not_finished)