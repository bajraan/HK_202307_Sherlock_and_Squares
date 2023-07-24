import json
import subprocess
import os
import time
import psutil
import sys
import shutil

output_path = None

def copy_main_file():

    # Make path to the target localization
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '00_HackerRank_Export'))
    os.makedirs(target_dir, exist_ok=True)

    # Make filename with current date and time
    filename = f"main_{time.strftime('%Y-%m-%d_%H-%M-%S')}.cpp"

    print("SW Version:    ");
    print(filename);

    # Make full path to the target file
    target_file = os.path.join(target_dir, filename)

    # Copy file to the target path
    try:
        shutil.copy('../main.cpp', target_file)
    except shutil.Error as e:
        print(f"Error while copying file: {e}")
        return None

    print("C++ file copied successfully")
    # Return path
    return target_file

def compile_cpp_file(file_path):
    process = subprocess.Popen(['g++', file_path , '-o', 'a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print("Error while compiling the C++ file:")
        print(error.decode())
        return False
    else:
        print("C++ file compiled succesfully")
    return True

def load_tests_from_files(tests_folder):
    input_file = os.path.join(tests_folder, "stdin.txt")
    output_file = os.path.join(tests_folder, "stdout.txt")

    with open(input_file) as f_input, open(output_file) as f_output:
        input_data = f_input.read()
        expected_output = f_output.read()

    #
    test_cases = [{'input': input_data, 'expected_output': expected_output}]

    return test_cases

def run_tests(test_cases, executable):

    if '-deb' in sys.argv:
        debug = True
    else:
        debug = False


    for i, test_case in enumerate(test_cases):
        input_data = test_case['input']
        expected_output = test_case['expected_output']

        start_time = time.time()
        #process = psutil.Process(os.getpid())
        #start_memory = psutil.Process(process.pid).memory_info().rss

        process = subprocess.Popen([executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        result = process.communicate(input=input_data.encode())[0]

        #end_memory = psutil.Process(process.pid).memory_info().rss
        end_time = time.time()

        with open(output_path, 'r') as f:
            output = f.read().strip()
        if output == expected_output.strip():
            print(f"Test {i+1}: PASSED")
        else:
            print(f"Test {i+1}: FAILED")
        if(debug):
            print(f"Expected output: {expected_output.strip()}")
            print(f"Observed output: {output}")
            print("Debug output:")
            print(result.decode())
            print(f"Execution time: {end_time - start_time:.5f}s")
            #print(f"Memory used: {end_memory - start_memory} bytes")
            print("------------------------\n")


def main():
    global output_path

    # Export program
    copy_main_file()

    # Set the output path
    file_name = "output.txt"
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))
    os.environ['OUTPUT_PATH'] = output_path

    # Compile the C++ file
    cpp_file_path = '../main.cpp'
    if not compile_cpp_file(cpp_file_path):
        return

    # Load the test cases from the files in the '60_Tests_Unit_Level' folder
    tests_folder = os.path.join(os.path.dirname(__file__), '..', '60_Tests_Unit_Level')
    test_cases = load_tests_from_files(tests_folder)

    # Run the tests
    executable = './a.out'
    run_tests(test_cases, executable)

    # Clean up
    os.remove("a.out")

if __name__ == '__main__':
    main()
