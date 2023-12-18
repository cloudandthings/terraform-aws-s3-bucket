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
