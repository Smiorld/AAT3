from input_code import solution

def get_function_name():
    return "def solution(a, b):"

def get_test_cases():
    return {'positive': '10', 'negative': '-10'}

def get_expected_outputs():
    return {'positive': '100', 'negative': '-1'}

def test_code():
    test_cases = get_test_cases()
    expected = get_expected_outputs()
    test_cases_count = len(test_cases)
    passed_test_cases = 0
    failed_test_cases = []
    for label in test_cases.keys():
        # check that the input is a tuple
        if isinstance(test_cases[label], tuple):
            function_call = str("solution"+str(test_cases[label]))
        else:  # add brackets if not a tuple to ensure correct evaluation
            function_call = "solution(" + str(test_cases[label]) + ")"
        # all answers converted to string to ensure compatibility
        code_result = str(eval(function_call))
        if code_result == expected[label]:
            passed_test_cases += 1
        else:
            failed_test_cases.append(label)

    print("Passed", passed_test_cases, "out of", test_cases_count, "test cases.")

    if len(failed_test_cases) > 0:
        print("Test cases not passed:", ", ".join(failed_test_cases)+".")
    print(" Answer saved...")

if __name__ == "__main__":
    test_code()
