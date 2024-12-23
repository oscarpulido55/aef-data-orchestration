# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import argparse
from pathlib import Path
import shutil

from commons import write_result
from ComposerDagGenerator import ComposerDagGenerator
from WorkflowsGenerator import WorkflowsGenerator

ENCODING = "utf-8"

CURRENT_FILE_DIR = Path(__file__).resolve()
CURRENT_WORKNG_DIR = Path.cwd()


def workflows_generator(
    workflow_file: str,
    exec_config: dict,
    workflows_output_dir: str,
    composer_output_dir: str,
    generate_for_pipeline: bool,
):
    """
    Main function for workflows generator

    :param workflow_file: Json definition file in the form of THREADS and STEPS
    :param exec_config: Json parameters
    :param workflows_output_dir: Cloud Workflows output directory
    :params composer_output_dir: Composer output directory
    :param generate_for_pipeline: Boolean to identify if the run is part of a CICD pipeline
    :return: NA
    """
    workflow_file_path = Path(workflow_file)

    with open(workflow_file, encoding=ENCODING) as json_file:
        workflow_config = json.load(json_file)

    json_file_name = Path(workflow_file).stem

    generator = None
    workflow_definition = workflow_config.get("definition")
    output_file = workflow_file_path.name

    if (
        exec_config.get("deploy_cloud_workflows")
        and workflow_config.get("engine") == "cloud_workflows"
    ):
        generator = WorkflowsGenerator(
            workflow_definition, exec_config, generate_for_pipeline
        )
        output_file = f"{workflows_output_dir}/{output_file}"
    elif (
        exec_config.get("deploy_composer_dags")
        and workflow_config.get("engine") == "composer"
    ):
        generator = ComposerDagGenerator(
            workflow_definition,
            exec_config,
            generate_for_pipeline,
            json_file_name,
        )
        output_file = output_file.replace(".json", ".py")
        output_file = f"{composer_output_dir}/{output_file}"

    if generator:
        generator.load_templates()
        workflow_body = generator.generate_workflows_body()
        write_result(output_file, workflow_body)


def run():
    """
    Entrypoint function to parse arguments as needed
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--workflow_dir",
        help="Path of the workflow file",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-c", "--config_file", help="Path of the config file", required=True, type=str
    )
    parser.add_argument(
        "-o",
        "--workflows_output_dir",
        help="Path of the workflows output directory",
        required=False,
        type=str,
        default="../cloud-workflows",
    )
    parser.add_argument(
        "-d",
        "--composer_output_dir",
        help="Path of the composer dags output directory",
        required=False,
        type=str,
        default="../composer-dags",
    )
    parser.add_argument(
        "-g",
        "--generate_for_pipeline",
        help="Flag for whether to generate the execution config",
        action="store_true",
    )

    args = parser.parse_args()

    exec_config_path = (
        f"{CURRENT_FILE_DIR}/{args.config_file}"
        if args.generate_for_pipeline
        else f"{CURRENT_WORKNG_DIR}/{args.config_file}"
    )
    with open(exec_config_path, encoding=ENCODING) as fp:
        exec_config = json.load(fp)

    # Clean up output directories
    shutil.rmtree(args.workflows_output_dir, ignore_errors=True)
    shutil.rmtree(args.composer_output_dir, ignore_errors=True)

    for filename in Path(args.workflow_dir).glob("**/*"):
        if filename.is_file():
            workflows_generator(
                filename,
                exec_config,
                args.workflows_output_dir,
                args.composer_output_dir,
                args.generate_for_pipeline,
            )


if __name__ == "__main__":
    run()
