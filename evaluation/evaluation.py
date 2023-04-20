import os
from sandbox import Sandbox, get_meta

from os.path import normpath
from os.path import join as path_join

from tabulate import tabulate

from colorama import Fore
from colorama import Style

from tqdm import tqdm


TIME_LIMIT = 1000
MEMORY_LIMIT = 16


with open("res/untrusted_code.cpp") as f:
    unstrusted_source = f.read()

results = []

for i in tqdm(range(6)):
    with open(f"res/tests/in/{i + 1}") as f:
        test_input = f.read()

    sandbox = Sandbox()
    sandbox.init()
    sandbox.create_files([('main.cpp', unstrusted_source, ''), ('input.txt', test_input, 'box')])
    
    out, err = sandbox.run_cmd('g++ -o ' + path_join('.', 'box', 'main') + ' ' + 'main.cpp')
    if err != b'':
        print('Compilation Error:\n' + str(err))
        break

    test_output, err = sandbox.run_exec(
        "main",
        dirs=[('/box', 'box', 'rw')],
        meta_file=sandbox.get_box_dir('meta'),
        stdin_file='input.txt',
        time_limit=TIME_LIMIT,
        memory_limit=MEMORY_LIMIT,
    )
    test_output = test_output.decode()

    with open(f"res/tests/out/{i + 1}") as f:
        test_answer = f.read()
    
    verdict = "Unknown"
    meta = get_meta(sandbox, 'meta')

    if meta.get('exitcode') == '0':
        if test_answer == test_output:
            verdict = f"{Fore.GREEN}OK{Style.RESET_ALL}"
        else:
            verdict = f"{Fore.RED}Wrong answer{Style.RESET_ALL}"
    else:
        if meta.get('status') == 'TO':
            verdict = f"{Fore.BLUE}{meta['message']}{Style.RESET_ALL}"
        else:
            verdict = f"{Fore.RED}Runtime error{Style.RESET_ALL}"

    results.append((i + 1, verdict, float(meta['time'])))


print(tabulate(results, ["Test #", "Verdict", "Time (s)"], tablefmt="rounded_outline"))
