from evaluation.sandbox import Sandbox, get_meta

from os.path import join as path_join

from submission.models import Test, Submission


TIME_LIMIT = 1000
MEMORY_LIMIT = 256


def evaluate(submission_id):
    submission = Submission.objects.get(id=submission_id)
    submission.verdict = "Testing"
    submission.save()

    tests = Test.objects.filter(problem_id=submission.problem_id)

    verdict = "Accepted"

    for test in tests:
        
        code = submission.code
        test_input = test.input

        sandbox = Sandbox()
        sandbox.init()
        sandbox.create_files([('main.cpp', code, ''), ('input.txt', test_input, 'box')])
        
        out, err = sandbox.run_cmd('g++ -o ' + path_join('.', 'box', 'main') + ' ' + 'main.cpp')
        if err != b'':
            verdict = "Compilation Error"
            break

        code_output, err = sandbox.run_exec(
            "main",
            dirs=[('/box', 'box', 'rw')],
            meta_file=sandbox.get_box_dir('meta'),
            stdin_file='input.txt',
            time_limit=TIME_LIMIT,
            memory_limit=MEMORY_LIMIT,
        )
        code_output = code_output.decode()
        meta = get_meta(sandbox, 'meta')

        test_answer = test.output

        if meta.get('exitcode') == '0':
            if test_answer.strip() != code_output.strip():
                verdict = "Wrong answer"
                break
        else:
            if meta.get('status') == 'TO':
                verdict = f"{meta['message']}"
            else:
                verdict = "Runtime error"
            break
    
    submission.verdict = verdict
    submission.save()
