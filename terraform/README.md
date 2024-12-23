<!-- BEGIN_TF_DOCS -->
Copyright 2024 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.10.2 |
| <a name="requirement_github"></a> [github](#requirement\_github) | ~> 6.0 |
| <a name="requirement_google"></a> [google](#requirement\_google) | >= 6.13.0, < 7.0.0 |
| <a name="requirement_google-beta"></a> [google-beta](#requirement\_google-beta) | >= 6.13.0, < 7.0.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | 6.14.1 |
| <a name="provider_google-beta"></a> [google-beta](#provider\_google-beta) | 6.14.1 |
| <a name="provider_local"></a> [local](#provider\_local) | 2.5.2 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_composer-service-account"></a> [composer-service-account](#module\_composer-service-account) | github.com/GoogleCloudPlatform/cloud-foundation-fabric/modules/iam-service-account | n/a |
| <a name="module_dataproc-service-account"></a> [dataproc-service-account](#module\_dataproc-service-account) | github.com/GoogleCloudPlatform/cloud-foundation-fabric/modules/iam-service-account | n/a |

## Resources

| Name | Type |
|------|------|
| [google-beta_google_composer_environment.aef_composer_environment](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_composer_environment) | resource |
| [google-beta_google_service_account_iam_member.custom_service_account](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_service_account_iam_member) | resource |
| [google_project_service.gcp_services](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/project_service) | resource |
| [google_storage_bucket_object.uploaded_artifacts_composer](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket_object) | resource |
| [google_workflows_workflow.workflows](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/workflows_workflow) | resource |
| [google_project.project](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/project) | data source |
| [local_file.workflow](https://registry.terraform.io/providers/hashicorp/local/latest/docs/data-sources/file) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_composer_bucket_name"></a> [composer\_bucket\_name](#input\_composer\_bucket\_name) | If Composer environment is not created and deploy\_composer\_dags is set to true, then this will be used to upload DAGs to. | `string` | `null` | no |
| <a name="input_composer_config"></a> [composer\_config](#input\_composer\_config) | Cloud Composer config. | <pre>object({<br/>    vpc                     = optional(string)<br/>    subnet                  = optional(string)<br/>    connection_subnetwork   = optional(string)<br/>    cloud_sql               = optional(string)<br/>    gke_master              = optional(string)<br/>    service_encryption_keys = optional(string)<br/><br/>    environment_size = optional(string)<br/>    software_config = optional(object({<br/>      airflow_config_overrides       = optional(map(string), {})<br/>      pypi_packages                  = optional(map(string), {})<br/>      env_variables                  = optional(map(string), {})<br/>      image_version                  = optional(string)<br/>      cloud_data_lineage_integration = optional(bool, true)<br/>    }), {})<br/>    web_server_access_control = optional(map(string), {})<br/>    workloads_config = optional(object({<br/>      scheduler = optional(object({<br/>        cpu        = optional(number)<br/>        memory_gb  = optional(number)<br/>        storage_gb = optional(number)<br/>        count      = optional(number)<br/>        }<br/>      ), {})<br/>      web_server = optional(object({<br/>        cpu        = optional(number)<br/>        memory_gb  = optional(number)<br/>        storage_gb = optional(number)<br/>      }), {})<br/>      triggerer = optional(object({<br/>        cpu       = optional(number)<br/>        memory_gb = optional(number)<br/>        count     = optional(number)<br/>      }), {})<br/>      worker = optional(object({<br/>        cpu        = optional(number)<br/>        memory_gb  = optional(number)<br/>        storage_gb = optional(number)<br/>        min_count  = optional(number)<br/>        max_count  = optional(number)<br/>        }<br/>      ), {})<br/>    }), {})<br/>  })</pre> | `{}` | no |
| <a name="input_create_composer_environment"></a> [create\_composer\_environment](#input\_create\_composer\_environment) | Controls whether a composer environment will be created, If false and deploy\_composer\_dags set to true, then composer\_bucket\_name needs to be set. | `bool` | `false` | no |
| <a name="input_data_transformation_project"></a> [data\_transformation\_project](#input\_data\_transformation\_project) | Project where the data transformation jobs definitions reside (will be used to infer bucket storing job parameter json files). | `string` | n/a | yes |
| <a name="input_deploy_cloud_workflows"></a> [deploy\_cloud\_workflows](#input\_deploy\_cloud\_workflows) | Controls whether cloud workflows are generated and deployed alongside Terraform resources. If false cloud workflows could be deployed as a next step in a CICD pipeline. | `bool` | `true` | no |
| <a name="input_deploy_composer_dags"></a> [deploy\_composer\_dags](#input\_deploy\_composer\_dags) | Controls whether Airflow DAGs are generated and deployed alongside Terraform resources. If false DAGs could be deployed as a next step in a CICD pipeline. | `bool` | `false` | no |
| <a name="input_enable_services"></a> [enable\_services](#input\_enable\_services) | List of the services to enable. NOTE: Recommend this be done via the primary orchestration repository so leave blank where possible | `list(string)` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | AEF environment. Will be used to create the parameters file for Cloud Workflows: platform-parameters-<<environment>>.json | `string` | n/a | yes |
| <a name="input_jobs_definition_bucket_suffix"></a> [jobs\_definition\_bucket\_suffix](#input\_jobs\_definition\_bucket\_suffix) | Suffix for the bucket that will hold the data transformation configurations | `string` | n/a | yes |
| <a name="input_project"></a> [project](#input\_project) | Project where the cloud workflows or Composer DAGs will be created. | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | Region where the Cloud Workflows will be created. | `string` | n/a | yes |
| <a name="input_workflows_deletion_protection"></a> [workflows\_deletion\_protection](#input\_workflows\_deletion\_protection) | Flag for whether to protect against deletion of workflows | `bool` | n/a | yes |
| <a name="input_workflows_log_level"></a> [workflows\_log\_level](#input\_workflows\_log\_level) | Describes the level of platform logging to apply to calls and call responses during executions of cloud workflows | `string` | `"LOG_ERRORS_ONLY"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_cloud_workflows_file_names"></a> [cloud\_workflows\_file\_names](#output\_cloud\_workflows\_file\_names) | n/a |
| <a name="output_composer_file_names"></a> [composer\_file\_names](#output\_composer\_file\_names) | n/a |
<!-- END_TF_DOCS -->