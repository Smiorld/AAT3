import json

class QuestionMethods:
    @staticmethod
    def parse_array(text):
        return json.dumps(text)

    @staticmethod
    def add_question():
        # return question_id
        pass

    @staticmethod
    def edit_question(question_id):
        pass

    @staticmethod
    def remove_question(question_id):
        pass


class ShortWrittenAnswerMethods(QuestionMethods):
    """
    Authored by Henry
    """

    @staticmethod
    def preprocess_correct_answer(self):
        pass

    @staticmethod
    def preprocess_student_answer(self):
        pass

    @staticmethod
    def mark_answer(self):
        pass


class StudentMethods:
    @staticmethod
    def take_uncompleted_assessment(student_id, assessment_id):
        pass


class FacultyMethods:
    """
    edited by henry
    """

    @staticmethod
    def view_draft_assessments():
        pass

    @staticmethod
    def edit_draft_assessment():
        pass

    @staticmethod
    def edit_question():
        pass

    @staticmethod
    def test_assessment():
        pass


class AdminMethods:
    """
    edited by henry
    """

    @staticmethod
    def change_person_password(person_id, new_password):
        pass

    @staticmethod
    def add_person_to_course(person_id, course_id):
        pass

    @staticmethod
    def add_person_to_module(person_id, module_id):
        pass
