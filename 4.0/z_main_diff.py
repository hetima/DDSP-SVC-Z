# pip install inquirerpy

import os
import sys
import glob
from InquirerPy import inquirer
# from InquirerPy.validator import NumberValidator
import subprocess
import argparse

MODELS_PATH = "exp"
DIFF_MODEL_DIR = ""
PYTHON_PATH = os.path.join(os.environ["VIRTUAL_ENV"], "Scripts/python.exe")

def exec_main_diff(diff_model, input_path, output_path):
    args = [PYTHON_PATH, "main_diff.py"]
    args.extend(["-i", input_path])
    args.extend(["-diff", diff_model])
    args.extend(["-o", output_path])
    # 追加の引数
    args.extend(["-kstep", "100"])
    subprocess.run(args)

def unique_ouput_path(file_path):
    if not os.path.exists(file_path):
        return file_path
    file_path_splitext = os.path.splitext(file_path)[0]
    for i in range(2000):
        candidate_path = file_path_splitext + "-" + str(i+1) + ".wav"
        if not os.path.exists(candidate_path):
            return candidate_path
    return None

def latest_checkpoint_path(dir_path, regex="model_*.pt"):
    f_list = glob.glob(os.path.join(dir_path, regex))
    f_list.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    if len(f_list) <= 0:
        return ""
    x = f_list[-1]
    return x

def select_project():
    dir_path = MODELS_PATH
    dirs = []
    for f in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, f)):
            if os.path.exists(os.path.join(dir_path, f, DIFF_MODEL_DIR)):
                dirs.append(f)
    slct = inquirer.select(message="Select model:", choices=dirs, multiselect=False).execute()
    return slct

def models_in_project(project_path):
    diff_path = os.path.join(project_path, DIFF_MODEL_DIR)
    return latest_checkpoint_path(diff_path)

def do_main():
    parser = argparse.ArgumentParser(description="DDSP-SVC-Z z_main_diff")
    parser.add_argument("-o", "--output_dir", type=str, default="", help="output dir")
    args = parser.parse_args()

    #model
    project = select_project()
    if project == "":
        print("model is empty")
        exit(0)
    project_path = os.path.join(MODELS_PATH, project)
    diff_path = models_in_project(project_path)
    if not diff_path:
        print("diff model not found")
        exit(0)
    print(diff_path)

    #input file
    input_path = inquirer.filepath(message="wav file path:").execute()
    if not input_path:
        exit(0)
    if input_path[0] == '"' or input_path[0] == "'":
        input_path = input_path[1:-1]
    if not os.path.exists(input_path):
        print("file not found")
        exit(0)
    #output file
    input_name = os.path.basename(input_path)
    output_name = project + "-" + input_name
    output_dir = os.path.dirname(input_path)
    if args.output_dir:
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_name)
    output_path = unique_ouput_path(output_path)
    if not output_path:
        print("output path confused")
        exit(0)

    print(output_path)
    exec_main_diff(diff_path, input_path, output_path)


if __name__ == "__main__":
    do_main()
