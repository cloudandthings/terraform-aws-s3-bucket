# Terraform AWS Template

## Description

*...example content; edit as needed...*

Terraform module for...

Features:

 - Creates an...

[AWS documentation](https://docs.aws.amazon.com...)

----
## Prerequisites

*...example content; edit as needed...*

None.

----
## Usage

*...example content; edit as needed...*

See `examples` dropdown on Terraform Cloud, or [browse here](/examples/).

----
## Testing

*...example content; edit as needed...*

This module is tested during development using [`pytest`](https://docs.pytest.org/en/7.2.x/) and [`tftest`](https://pypi.org/project/tftest/). See the `tests` folder for further details, and in particular the [testing readme](./tests/README.md).

----
## Notes

*...example content; edit as needed...*

*This repo was created from [terraform-aws-template](https://github.com/cloudandthings/terraform-aws-template)*


----
## Known issues

*...example content; edit as needed...*

This project is currently unlicenced. Please contact the maintaining team to add a licence.

----
## Contributing

*...example content; edit as needed...*

Direct contributions are welcome.

See [`CONTRIBUTING.md`](./.github/CONTRIBUTING.md) for further information.

<!-- BEGIN_TF_DOCS -->
----
## Documentation

----
### Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_bucket_logging_target_bucket"></a> [bucket\_logging\_target\_bucket](#input\_bucket\_logging\_target\_bucket) | Target S3 bucket name for logging. | `string` | `""` | no |
| <a name="input_bucket_logging_target_prefix"></a> [bucket\_logging\_target\_prefix](#input\_bucket\_logging\_target\_prefix) | Target S3 bucket prefix for logging. | `string` | `""` | no |
| <a name="input_create_aws_s3_bucket_lifecycle_configuration"></a> [create\_aws\_s3\_bucket\_lifecycle\_configuration](#input\_create\_aws\_s3\_bucket\_lifecycle\_configuration) | Whether to enable the default aws\_s3\_bucket\_lifecycle\_configuration on the bucket. | `bool` | `true` | no |
| <a name="input_enable_attach_default_bucket_policy"></a> [enable\_attach\_default\_bucket\_policy](#input\_enable\_attach\_default\_bucket\_policy) | Whether to attach the default bucket policy or not (default=true). You may wish to attach the bucket policy document separately, in which case it is an output from this module. | `bool` | `true` | no |
| <a name="input_enable_versioning"></a> [enable\_versioning](#input\_enable\_versioning) | Whether to enable versioning on the bucket. | `bool` | `true` | no |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | **Caution** Whether to automatically delete all objects from the bucket when it is destroyed. These objects are NOT recoverable. | `bool` | `false` | no |
| <a name="input_general_read_only_aws_principals"></a> [general\_read\_only\_aws\_principals](#input\_general\_read\_only\_aws\_principals) | List of AWS principals to give read access to all bucket objects via bucket policy resource. | `list(string)` | `[]` | no |
| <a name="input_general_read_write_aws_principals"></a> [general\_read\_write\_aws\_principals](#input\_general\_read\_write\_aws\_principals) | List of AWS principals to give read and write access to all bucket objects via bucket policy resource. | `list(string)` | `[]` | no |
| <a name="input_kms_key_id"></a> [kms\_key\_id](#input\_kms\_key\_id) | KMS key ID to use for encrypting bucket objects. | `string` | `null` | no |
| <a name="input_naming_prefix"></a> [naming\_prefix](#input\_naming\_prefix) | Naming prefix for all created resources. | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | Map of additional tags to assign to created resources. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level. | `map(string)` | `{}` | no |

----
### Modules

No modules.

----
### Outputs

| Name | Description |
|------|-------------|
| <a name="output_bucket_arn"></a> [bucket\_arn](#output\_bucket\_arn) | The bucket ARN that is created. |
| <a name="output_bucket_name"></a> [bucket\_name](#output\_bucket\_name) | The bucket name that is created. |
| <a name="output_default_bucket_policy_document"></a> [default\_bucket\_policy\_document](#output\_default\_bucket\_policy\_document) | Default bucket policy document, attached to the bucket if `var.attach_default_bucket_policy=true`. |
| <a name="output_kms_key_id"></a> [kms\_key\_id](#output\_kms\_key\_id) | The KMS key ID used for encrypting bucket objects. |
| <a name="output_region"></a> [region](#output\_region) | The bucket region. |

----
### Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | ~> 4.9 |

----
### Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.13.1 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 4.9 |
| <a name="requirement_null"></a> [null](#requirement\_null) | ~> 3.1 |

----
### Resources

| Name | Type |
|------|------|
| [aws_s3_bucket.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket_lifecycle_configuration.abort_incomplete_multipart_upload](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_lifecycle_configuration) | resource |
| [aws_s3_bucket_logging.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_logging) | resource |
| [aws_s3_bucket_ownership_controls.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_ownership_controls) | resource |
| [aws_s3_bucket_policy.default_bucket_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_policy) | resource |
| [aws_s3_bucket_server_side_encryption_configuration.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration) | resource |
| [aws_s3_bucket_versioning.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_versioning) | resource |
| [aws_iam_policy_document.default_bucket_policy_document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.deny_unencrypted_policy_document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.general_read_only_policy_document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.general_read_write_policy_document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

----
<!-- END_TF_DOCS -->
