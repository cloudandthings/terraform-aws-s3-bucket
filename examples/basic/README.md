<!-- BEGIN_TF_DOCS -->
----
## main.tf
```hcl
#--------------------------------------------------------------------------------------
# Supporting resources
#--------------------------------------------------------------------------------------
# Generate unique naming for resources
resource "random_integer" "naming" {
  min = 100000
  max = 999999
}

locals {
  naming_prefix = "s3-example-basic-${random_integer.naming.id}"
}

# Using a KMS key is optional.
resource "aws_kms_key" "key" {
  description             = local.naming_prefix
  deletion_window_in_days = 7
}

# Optional KMS key policy.
data "aws_caller_identity" "current" {}
resource "aws_kms_key_policy" "key" {
  key_id = aws_kms_key.key.id
  policy = jsonencode({
    Id = "example"
    Statement = [
      {
        Action = "kms:*"
        Effect = "Allow"
        Principal = {
          AWS = data.aws_caller_identity.current.account_id
        }
        Resource = "*"
        Sid      = "Enable IAM User Permissions"
      },
    ]
    Version = "2012-10-17"
  })
}

#--------------------------------------------------------------------------------------
# Example
#--------------------------------------------------------------------------------------

module "example" {
  # Uncomment and update as needed
  # source  = "<your_module_url>"
  # version = "~> 1.0"
  source = "../../"

  # Required module parameters:
  name = local.naming_prefix

  # Optional module parameters:
  naming_method = "BUCKET_PREFIX"
  kms_key_id    = aws_kms_key.key.arn

  tags = {}
}
```
----

## Documentation

----
### Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_profile"></a> [aws\_profile](#input\_aws\_profile) | AWS profile | `string` | `null` | no |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | AWS region | `string` | `null` | no |

----
### Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_example"></a> [example](#module\_example) | ../../ | n/a |

----
### Outputs

| Name | Description |
|------|-------------|
| <a name="output_kms_key_arn"></a> [kms\_key\_arn](#output\_kms\_key\_arn) | KMS key ARN |
| <a name="output_module_example"></a> [module\_example](#output\_module\_example) | module.example |

----
### Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | ~> 5.0 |
| <a name="provider_random"></a> [random](#provider\_random) | ~> 3.4 |

----
### Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.13.1 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |
| <a name="requirement_random"></a> [random](#requirement\_random) | ~> 3.4 |

----
### Resources

| Name | Type |
|------|------|
| [aws_kms_key.key](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_key) | resource |
| [aws_kms_key_policy.key](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_key_policy) | resource |
| [random_integer.naming](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/integer) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |

----
<!-- END_TF_DOCS -->
