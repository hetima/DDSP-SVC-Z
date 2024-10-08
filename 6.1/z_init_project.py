# pip install inquirerpy

import os
import sys
import shutil
from InquirerPy import inquirer
# from InquirerPy.validator import NumberValidator
import subprocess
import argparse
from pathlib import Path

PRETRAIN_MODEL_PATH = "model_0.pt"
MODELS_PATH = "exp"
DATASETS_PATH = "datasets"
CONFIGS_PATH = "configs"
CONFIG_NAME = "reflow.yaml"
PYTHON_PATH = os.path.join(os.environ["VIRTUAL_ENV"], "Scripts/python.exe")


def init_project(project_name, pretrain_path):
    print(project_name)
    dataset_path = os.path.join(DATASETS_PATH, project_name)
    config_tmpl = os.path.join(CONFIGS_PATH, CONFIG_NAME)
    if not os.path.exists(config_tmpl):
        print("ERROR: " + config_tmpl + " does not exists")
        exit(0)
    if os.path.exists(dataset_path):
        print("ERROR: " + dataset_path + " exists")
        exit(0)
    model_path = os.path.join(MODELS_PATH, project_name)
    if os.path.exists(model_path):
        print("ERROR: " + model_path + " exists")
        exit(0)
    config_path = os.path.join(CONFIGS_PATH, project_name, CONFIG_NAME)
    if os.path.exists(config_path):
        print("ERROR: " + config_path + " exists")
        exit(0)

    # makedirs
    print("make dirs")
    os.makedirs(os.path.join(dataset_path, "train", "audio"), exist_ok=True)
    os.makedirs(os.path.join(dataset_path, "val", "audio"), exist_ok=True)
    os.makedirs(model_path, exist_ok=True)
    os.makedirs(os.path.join(CONFIGS_PATH, project_name), exist_ok=True)

    # config
    print("make config file")
    cnfg = Path(config_tmpl).read_text()
    cnfg = cnfg.replace("data/train", os.path.join(dataset_path, "train").replace("\\", "/"))
    cnfg = cnfg.replace("data/val", os.path.join(dataset_path, "val").replace("\\", "/"))
    cnfg = cnfg.replace("exp/reflow-test", model_path.replace("\\", "/"))
    Path(config_path).write_text(cnfg)

    # copy pre-trained model
    if os.path.exists(pretrain_path):
        print("copy pre-trained model")
        shutil.copyfile(pretrain_path, os.path.join(model_path, "model_0.pt"))
        
    print("done")

def do_main():
    parser = argparse.ArgumentParser(description="DDSP-SVC-Z z_main_diff")
    parser.add_argument("-m", "--model_name", type=str, default="", help="model_name")
    parser.add_argument("-p", "--pretrained_model", type=str, default="", help="pretrained_model path")
    args = parser.parse_args()

    if args.pretrained_model:
        pretrain_path = args.pretrained_model
    else:
        pretrain_path = PRETRAIN_MODEL_PATH
    if args.model_name:
        model_name = args.model_name
    else:
        model_name = inquirer.text(message="new model name:").execute()
    if not model_name:
        exit(0)
    init_project(model_name, pretrain_path)


if __name__ == "__main__":
    do_main()
