from sqlalchemy import true
from datetime import datetime
from app import db
from app.models import (
    User,
    Assessment,
    PublishedStudentAssessment,
    Question,
    StudentAnswer,
    User,
    Course,
    Module,
    ModuleStudent,
    QuestionContributors,
    Assessment2Question
)

db.drop_all()
db.create_all()

user1 = User(
    last_name="Zhou",
    first_name="Qiye",
    email="zhouq13@cardiff.ac.uk",
    password="123",
    is_student=False,
)
db.session.add(user1)

user3 = User(
    last_name="faculty",
    first_name="1",
    email="faculty",
    password="123",
    is_student=False,
)
db.session.add(user3)

user2 = User(
    last_name="aa",
    first_name="aa",
    email="lala@lala.com",
    password="123",
    is_student=True,
    extra_time=True,
)
db.session.add(user2)

user3 = User(
    last_name="bb",
    first_name="bb",
    email="lalab@lalba.com",
    password="123",
    is_student=True,
)
db.session.add(user3)



coding_question1 = Question(
    question="Given two integers a and b, which can be positive or negative, find the sum of all the integers "
             "between and including them and return it. If the two numbers are equal return a or b.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="<p>A possible solution is:</p> <p>def solution(a,b):<br /> &nbsp; &nbsp;&nbsp;mini = min([a, b])<br />"
                        "&nbsp; &nbsp;&nbsp;maxi = max([a, b])<br />&nbsp; &nbsp;&nbsp;arr = []<br />"
                        "&nbsp; &nbsp; for i in range(min, max+1):<br />"
                        "&nbsp; &nbsp; &nbsp; &nbsp;&nbsp;arr.append(i)<br />"
                        "&nbsp; &nbsp;&nbsp;return sum(arr)</p>",
    max_marks=2,
    arguments="a, b",
    test_inputs="{'test_1': '1, 3', 'test_2': '8, -4'}",
    expected_outputs="{'test_1': '6', 'test_2': '26'}",
    is_multiple_choice=False,
    category="range",
    difficulty="Medium"
)

coding_question2 = Question(
    question="Given two sorted arrays that both only contain integers, merge the arrays and return a single array, "
             "remove any duplicated integers in the returned result.",
    correct_feedback="You got 2 marks, congratulations",
    incorrect_feedback ="<p>A possible solution is:</p><p>def merge_arrays(arr1, arr2):</p><p>&nbsp; &nbsp; return sorted(set(arr1+arr2))</p>",
    max_marks=2,
    arguments="arr1, arr2",
    test_inputs="{'test_1': '[1, 3, 5, 7, 9], [10, 8, 6, 4, 2]', 'test_2': '[1, 3, 5, 7, 9, 11, 12], [1, 2, 3, 4, 5, 10, 12]'}",
    expected_outputs="{'test_1': '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]', 'test_2': '[1, 2, 3, 4, 5, 7, 9, 10, 11, 12]'}",
    is_multiple_choice=False,
    category="arrays",
    difficulty="Medium"
)

coding_question3 = Question(
    question="Given an array, return the maximum value in the array",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': '[1, 3, 8, 9, 21]', 'test_2': '[8, -4, 8, 0, 2]'}",
    expected_outputs="{'test_1': '21', 'test_2': '8'}",
    is_multiple_choice=False,
    category="arrays",
    difficulty="Easy"
)
mcq1 = Question(
    question =  "choose a",
    question_description = "come on guy, you can do it",
    correct_answer = "a,b",
    correct_answer_count = 2,
    correct_feedback = "www.google.com",
    incorrect_feedback = "www.google.com",
    max_marks = 2,
    is_multiple_choice = True,
    total_choices = 2,
    category = "test",
    difficulty = "Easy",
    points = 1,
    choices = "a,b,c,d",
    options = '[{"correctness": true, "optionVal":"a"}, {"correctness": true, "optionVal":"b"}, {"correctness": false, "optionVal":"c"}, {"correctness": false, "optionVal":"d"}]'
)
mcq2 = Question(
    question =  "choose 2",
    question_description = "come on guy, you can do it",
    correct_answer = "2",
    correct_answer_count = 1,
    correct_feedback = "You did it!!",
    incorrect_feedback = "just wow",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "test",
    difficulty = "Hard",
    points = 1,
    choices = "1,2,3,4",
    options = '[{"correctness": false, "optionVal":"1"}, {"correctness": true, "optionVal":"2"}, {"correctness": false, "optionVal":"3"}, {"correctness": false, "optionVal":"4"}]'
)
mcq3 = Question(
    question =  "choose X",
    question_description = "come on guy, you can do it",
    correct_answer = "X",
    correct_answer_count = 1,
    correct_feedback = "www.google.com",
    incorrect_feedback = "www.google.com",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "test",
    difficulty = "Medium",
    points = 1,
    choices = "X,Y,Z",
    options = '[{"correctness": true, "optionVal":"X"}, {"correctness": false, "optionVal":"Y"}, {"correctness": false, "optionVal":"Z"}]'
)
db.session.add(mcq1)
db.session.add(mcq2)
db.session.add(mcq3)

db.session.add(coding_question1)
db.session.add(coding_question2)
db.session.add(coding_question3)

question_contributors1 = QuestionContributors(role="Author", question_id=1, user_id=1)
question_contributors2 = QuestionContributors(role="Author", question_id=2, user_id=1)
question_contributors3 = QuestionContributors(role="Author", question_id=3, user_id=1)
question_contributors4 = QuestionContributors(role="Author", question_id=4, user_id=1)
question_contributors5 = QuestionContributors(role="Author", question_id=5, user_id=1)
question_contributors6 = QuestionContributors(role="Author", question_id=6, user_id=1)
db.session.add(question_contributors1)
db.session.add(question_contributors2)
db.session.add(question_contributors3)
db.session.add(question_contributors4)
db.session.add(question_contributors5)
db.session.add(question_contributors6)

course1 = Course(course_name="MSc. Computing")

db.session.add(course1)

module1 = Module(course_id=1, module_name="Software Engineering")

db.session.add(module1)

module2 = Module(course_id=1, module_name="Fundementals of Programming")

db.session.add(module2)

assessment1 = Assessment(
    module_id=1,
    assessment_name="AAT",
    hand_in_date=datetime.strptime("2022-07-01 05:00:00", "%Y-%m-%d %H:%M:%S"),
    hand_out_date=datetime.strptime("2022-03-01 09:00:00", "%Y-%m-%d %H:%M:%S"),
    is_summative=False,
    is_draft=True,
    total_marks=100,
    time_allotted=0
)
db.session.add(assessment1)

assessment2 = Assessment(
    module_id=1,
    assessment_name="AAT2",
    hand_in_date=datetime.strptime("2022-07-01 05:00:00", "%Y-%m-%d %H:%M:%S"),
    hand_out_date=datetime.strptime("2022-03-01 09:00:00", "%Y-%m-%d %H:%M:%S"),
    is_summative=True,
    is_draft=True,
    total_marks=100,    
    time_allotted=5
)
db.session.add(assessment2)

assessment1 = Assessment(
    module_id=2,
    assessment_name="AAT",
    hand_in_date=datetime.strptime("2022-07-01 05:00:00", "%Y-%m-%d %H:%M:%S"),
    hand_out_date=datetime.strptime("2022-03-01 09:00:00", "%Y-%m-%d %H:%M:%S"),
    is_summative=False,
    is_draft=True,
    total_marks=100,
    time_allotted=5    
)
db.session.add(assessment1)

assessment2 = Assessment(
    module_id=2,
    assessment_name="AAT2",
    hand_in_date=datetime.strptime("2022-07-01 05:00:00", "%Y-%m-%d %H:%M:%S"),
    hand_out_date=datetime.strptime("2022-03-01 09:00:00", "%Y-%m-%d %H:%M:%S"),
    is_summative=True,
    is_draft=True,
    total_marks=100,
    time_allotted=5
)
db.session.add(assessment2)

# assessment2 = Assessment(
#     module_id=1,
#     assessment_name="test2",
#     hand_in_date=datetime.strptime("2022-03-01 05:00:00", "%Y-%m-%d %H:%M:%S"),
#     hand_out_date=datetime.strptime("2022-03-01 09:00:00", "%Y-%m-%d %H:%M:%S"),
#     is_summative=True,
#     is_draft=True,
#     total_marks=100,
# )
# db.session.add(assessment2)

# assessment3 = Assessment(
#     module_id=1,
#     assessment_name="test3",
#     hand_in_date=datetime.strptime("2022-03-01 05:00:00", "%Y-%m-%d %H:%M:%S"),
#     hand_out_date=datetime.strptime("2022-03-01 09:00:00", "%Y-%m-%d %H:%M:%S"),
#     is_summative=True,
#     is_draft=False,
#     total_marks=100,
# )
# db.session.add(assessment3)

modulestudent2 = ModuleStudent(module_id=1, student_id=3)

db.session.add(modulestudent2)

modulestudent3 = ModuleStudent(module_id=1, student_id=4)

db.session.add(modulestudent3)


assessment2question3_1 = Assessment2Question(assessment_id=1,question_id=3)
assessment2question4_1 = Assessment2Question(assessment_id=1,question_id=4)
assessment2question5_1 = Assessment2Question(assessment_id=1,question_id=5)
assessment2question6_1 = Assessment2Question(assessment_id=1,question_id=6)


db.session.add(assessment2question3_1)
db.session.add(assessment2question4_1)
db.session.add(assessment2question5_1)
db.session.add(assessment2question6_1)

assessment2question4_2 = Assessment2Question(assessment_id=2,question_id=4)
assessment2question1_2 = Assessment2Question(assessment_id=2,question_id=1)
assessment2question2_2 = Assessment2Question(assessment_id=2,question_id=2)
assessment2question3_2 = Assessment2Question(assessment_id=2,question_id=3)

db.session.add(assessment2question4_2)
db.session.add(assessment2question1_2)
db.session.add(assessment2question2_2)
db.session.add(assessment2question6_1)
db.session.commit()


AET1 = Question(
    question =  "AET1",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Arrays",
    difficulty = "Easy",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
AET2 = Question(
    question =  "AET2",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Arrays",
    difficulty = "Easy",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
AET3 = Question(
    question =  "AET3",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Arrays",
    difficulty = "Easy",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
AMT1 = Question(
    question =  "AMT1",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Arrays",
    difficulty = "Medium",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
AMT2 = Question(
    question =  "AMT2",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Arrays",
    difficulty = "Medium",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
AMT3 = Question(
    question =  "AMT3",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Arrays",
    difficulty = "Medium",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
AHT1 = Question(
    question =  "AHT1",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Arrays",
    difficulty = "Hard",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
AHT2 = Question(
    question =  "AHT2",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Arrays",
    difficulty = "Hard",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
AHT3 = Question(
    question =  "AHT3",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Arrays",
    difficulty = "Hard",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
LET1 = Question(
    question =  "LET1",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Loops",
    difficulty = "Easy",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
LMT1 = Question(
    question =  "LMT1",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Loops",
    difficulty = "Medium",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
LHT1 = Question(
    question =  "LHT1",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Loops",
    difficulty = "Hard",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
LET2 = Question(
    question =  "LET2",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Loops",
    difficulty = "Easy",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
LMT2 = Question(
    question =  "LMT2",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Loops",
    difficulty = "Medium",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
LHT2 = Question(
    question =  "LHT2",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Loops",
    difficulty = "Hard",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
LET3 = Question(
    question =  "LET3",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Loops",
    difficulty = "Easy",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
LMT3 = Question(
    question =  "LMT3",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Loops",
    difficulty = "Medium",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
LHT3 = Question(
    question =  "LHT3",
    question_description = "test",
    correct_answer = "test",
    correct_answer_count = 1,
    correct_feedback = "test",
    incorrect_feedback = "test",
    max_marks = 1,
    is_multiple_choice = True,
    total_choices = 1,
    category = "Loops",
    difficulty = "Hard",
    points = 1,
    choices = "test,test,test,test",
    options = '[{"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}, {"correctness": true, "optionVal":"test"}]'
)
AEF1 = Question(
    question="AEF1",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Arrays",
    difficulty="Easy"
)
AMF1 = Question(
    question="AMF1",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Arrays",
    difficulty="Medium"
)
AHF1 = Question(
    question="AHF1",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': '21', 'test_2': '8'}",
    is_multiple_choice=False,
    category="Arrays",
    difficulty="Hard"
)
AEF2 = Question(
    question="AEF2",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Arrays",
    difficulty="Easy"
)
AMF2 = Question(
    question="AMF2",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Arrays",
    difficulty="Medium"
)
AHF2 = Question(
    question="AHF2",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Arrays",
    difficulty="Hard"
)
AEF3 = Question(
    question="AEF3",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Arrays",
    difficulty="Easy"
)
AMF3 = Question(
    question="AMF3",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Arrays",
    difficulty="Medium"
)
AHF3 = Question(
    question="AHF3",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Arrays",
    difficulty="Hard"
)
LEF1 = Question(
    question="LEF1",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Loops",
    difficulty="Easy"
)
LMF1 = Question(
    question="LMF1",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Loops",
    difficulty="Medium"
)
LHF1 = Question(
    question="LHF1",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Loops",
    difficulty="Hard"
)
LEF2 = Question(
    question="LEF2",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Loops",
    difficulty="Easy"
)
LMF2 = Question(
    question="LMF2",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Loops",
    difficulty="Medium"
)
LHF2 = Question(
    question="LHF2",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Loops",
    difficulty="Hard"
)
LEF3 = Question(
    question="LEF3",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Loops",
    difficulty="Easy"
)
LMF3 = Question(
    question="LMF3",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Loops",
    difficulty="Medium"
)
LHF3 = Question(
    question="LHF3",
    question_description="For example, in the array [1, -3, 5], the maximum number is 5.",
    correct_feedback="You got 2 marks, congratulations!",
    incorrect_feedback ="A possible solution is: \n def solution(arr): \n\treturn max(arr)",
    max_marks=2,
    arguments="arr",
    test_inputs="{'test_1': ([1, 3, 8, 9, 21]), 'test_2': ([8, -4, 8, 0, 2])}",
    expected_outputs="{'test_1': 21, 'test_2': 8}",
    is_multiple_choice=False,
    category="Loops",
    difficulty="Hard"
)

db.session.add(LET1)
db.session.add(LET2)
db.session.add(LET3)
db.session.add(LMT1)
db.session.add(LMT2)
db.session.add(LMT3)
db.session.add(LHT1)
db.session.add(LHT2)
db.session.add(LHT3)
db.session.add(AET1)
db.session.add(AET2)
db.session.add(AET3)
db.session.add(AMT1)
db.session.add(AMT2)
db.session.add(AMT3)
db.session.add(AHT1)
db.session.add(AHT2)
db.session.add(AHT3)
db.session.add(LEF1)
db.session.add(LEF2)
db.session.add(LEF3)
db.session.add(LMF1)
db.session.add(LMF2)
db.session.add(LMF3)
db.session.add(LHF1)
db.session.add(LHF2)
db.session.add(LHF3)
db.session.add(AEF1)
db.session.add(AEF2)
db.session.add(AEF3)
db.session.add(AMF1)
db.session.add(AMF2)
db.session.add(AMF3)
db.session.add(AHF1)
db.session.add(AHF2)
db.session.add(AHF3)

db.session.commit()