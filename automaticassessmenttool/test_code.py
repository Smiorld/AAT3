from input_code import solution

def get_function_name():
    return "def solution(a, b):"

def get_test_cases():
    return {'test_1': [1, 3], 'test_2': [8, -4]}

def get_expected_outputs():
    return {'test_1': 6, 'test_2': 26}

def test_code_q():
    test_cases = get_test_cases()
    expected = get_expected_outputs()
    test_cases_count = len(test_cases)
    passed_test_cases = 0
    failed_test_cases = []

    for label in test_cases.keys():
        code_result = eval("solution"+(str(tuple(test_cases[label]))))
        if code_result == expected[label]:
            passed_test_cases += 1
        else:
            failed_test_cases.append(label)

    message = "Passed" + passed_test_cases + "out of" + test_cases_count + "test cases. "

    if len(failed_test_cases) > 0:
       message += "Test cases not passed: " + ', '.join(failed_test_cases)
    print(message, passed_test_cases)
#
if __name__ == "__main__":
    test_code_q()
