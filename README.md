# Data Orchestration

***Note:*** For a comprehensive installation guide of all the AEF repositories together, please look [here](https://github.com/oscarpulido55/aef-orchestration-framework/blob/main/AEF_DEPLOYMENT.md).

This repository automates the creation of [Google Cloud Workflows Definition](https://cloud.google.com/workflows/docs/reference/syntax) files or [Cloud Composer DAGs](https://cloud.google.com/composer/docs/how-to/using/writing-dags) from [data pipeline configuration files](https://github.com/oscarpulido55/aef-data-orchestration/blob/main/workflow-definitions/demo_pipeline_cloud_workflows.json). 
It's designed for seamless integration into your CI/CD pipeline, using ***LEVEL***, ***THREAD***, and ***STEP*** abstractions to define your batch data pipeline. 
You also have the flexibility to directly execute ***workflows_generator.py*** for manual workflow definition generation.

## Key Features
- ***Abstracted Pipeline Definition:*** Conveniently define your batch data pipelines using the intuitive concepts of LEVEL, THREAD, and STEP.
- ***Manual Execution:*** Option to directly run ***workflows_generator.py*** for on-demand creation.
- ***CI/CD Integration:***  Effortlessly streamline your Cloud Workflows or Cloud Composer DAGs generation within your CI/CD pipeline.

##  Concepts
Most batch data pipelines can be effectively defined using three simple concepts, simplifying  pipeline creation and scheduling for data analysts:
- ***LEVEL:*** The largest aggregation within your pipeline. Levels execute sequentially, and you can have as many as needed. Identify each LEVEL with a unique ID.
- ***STEP:*** The atomic unit of execution. A STEP represents a data transformation process (e.g., Dataflow job, BigQuery job, Dataproc job).
- ***THREAD:*** Allows for complex dependencies and parallel execution within your pipeline. A THREAD groups steps that execute sequentially.  A LEVEL can have multiple THREADs running in parallel.

![level-thread-step.png](level-thread-step.png)

Find sample Json configuration files [here](https://github.com/oscarpulido55/aef-data-orchestration/tree/main/workflow-definitions).

This approach enables data analysts to build intricate data pipelines and reliably orchestrate them without writing  code. Configuration is handled through simple JSON definition files containing levels, threads, and steps.

## Usage
### Manual Execution
This script processes a JSON-formatted data pipeline definition (specifying levels, threads, and steps) and generates deployment-ready code for your chosen orchestration platform.

**Note**: There is a dependency on the JSON formatted `tfvars` located at `config`. The workflow or DAGs will be rendered subject the value tied to the `deploy_cloud_workflows` and `deploy_composer_dags` variables contained within the `tfvars` file respectively. 

- ***Cloud Workflows***: Produces a [source file](https://cloud.google.com/workflows/docs/reference/syntax#file_structure) that incorporates robust error handling, retry mechanisms, and cyclical execution. It invokes step executors as Cloud Functions --pre-deployed in your project, typically using the [Orchestration framework repository](https://github.com/oscarpulido55/aef-orchestration-framework)--.
- ***Cloud Composer/Airflow***: Generates an Airflow DAG that leverages Google Cloud operators to execute the pipeline steps as defined in the JSON definition.
Both options rely on predefined [templates](https://github.com/oscarpulido55/aef-data-orchestration/tree/main/workflows-generator) to streamline the code generation process.
```bash
    python3 orchestration_generator.py \
        -w ../workflow-definitions/ \
        -c ../config/dev.tfvars.json
```
### Terraform
The provided Terraform code enables reading defined JSON data pipelines definitions and managing the deployment of the resulting Cloud Workflows or Composer DAGs. 

The Composer DAGs and/or the Cloud Workflows need to be rendered before executing any `terraform` commands.

Steps for local `terraform` execution are below:

1. Locate your JSON data pipeline definition files in the repository and navigate to that location in a terminal.
    ```
    ├── workflow-definitions
    │   ├── demo_pipeline.json
    │   └── ...
    ```
1. Define your terraform variables for the environment & render the templates by executing the following command:
    ```bash
        python3 orchestration_generator.py \
            -w ../workflow-definitions/ \
            -c ../config/[ENVIRONMENT].tfvars.json
    ```
    The `[ENVIRONMENT]` value above needs to be changed to the relevant environment's `tfvars` file.

1. Initialise, plan and apply terraform as needed:

    ```bash
        cd terraform
        terraform init
        terraform plan --var-file ../config/[ENVIRONMENT].tfvars.json -out [ENVIRONMENT].plan
        terraform apply [ENVIRONMENT].plan
    ```


**NOTE**: It is highly recommended if deploying to setup a backend for the terraform state files to allow for teams to work and adjust the configurations as required.

### Domain-Based vs. Central Orchestration

The [engine](https://github.com/oscarpulido55/aef-data-orchestration/blob/e7efd8ec7ad33a280290ba62573c7e7bf2734646/workflow-definitions/demo_pipeline_composer.json#L2) variable currently supports `cloud_workflows` or `composer`. 

*   `cloud_workflows`:  Deploy Cloud Workflows in the project specified by the `project` variable. This allows for both **Domain-Based Orchestration** (deploying to a domain team's project) and **Central Orchestration** (deploying to a centralized project).

*   `composer`: Creates/uses a Composer environment in the data domain team's project, following a **Domain-Based Orchestration** approach. This addresses [Airflow scalability complexity](https://cloud.google.com/blog/products/data-analytics/scale-your-composer-environment-together-your-business?e=48754805) and aligns with [tenancy strategies for Cloud Composer](https://cloud.google.com/blog/products/data-analytics/a-cloud-composer-tenancy-case-study?e=48754805).

**Domain-Based Orchestration**: Isolates orchestration by domain, potentially simplifying IAM and networking but increasing operational overhead. Preferred for multi-domain environments with distinct data needs. This repository demonstrates this with one Composer environment per data domain team.

**Central Orchestration**: Consolidates orchestration, centralizing Data Ops and potentially reducing management complexity. Simpler for single-domain environments or those with shared networks. May require IAM adjustments. Easily achieved with Cloud Workflows due to its serverless nature.

The optimal approach depends on your organization's needs and constraints, including the number of domains, data access patterns, and networking configurations.

## Integration with Analytics Engineering Framework
Data orchestration plays a vital role in enabling efficient data access and analysis, making it critical for data lakes and data warehouses.

While usable independently, this tool is optimized as a component within a comprehensive Analytics Engineering Framework comprising:

1. [Orchestration Framework](https://github.com/oscarpulido55/aef-orchestration-framework): Maintained by Analytics Engineers to provide seamless, extensible orchestration and execution infrastructure.
1. [Data Model](https://github.com/oscarpulido55/aef-data-model): Directly used by end data practitioners to manage data models, schemas, and Dataplex metadata.
1. **(This repository) Data Orchestration**: Directly used by end data practitioners to define and deploy data pipelines using levels, threads, and steps.
1. [Data Transformation](https://github.com/oscarpulido55/aef-data-transformation): Directly used by end data practitioners to define, store, and deploy data transformations.

![AEF_repositories_data_orchestration.png](AEF_repositories_data_orchestration.png)
