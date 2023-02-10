#--------------------------------------------------------------------------------------
# Supporting resources
#--------------------------------------------------------------------------------------
# Generate unique naming for resources
resource "random_pet" "naming" {
}

locals {
  naming_prefix = "s3-bucket-example-basic-${random_pet.naming.id}"
}

# Using a KMS key is optional.
resource "aws_kms_key" "key" {
  description             = local.naming_prefix
  deletion_window_in_days = 7
}

#--------------------------------------------------------------------------------------
# Example
#--------------------------------------------------------------------------------------

module "example" {
  # Uncomment and update as needed
  # source  = "<your_module_url>"
  # version = "~> 1.0"
  source = "../../"

  # Module parameters:
  naming_prefix = local.naming_prefix

  # Using a KMS key is optional.
  kms_key_id = aws_kms_key.key.arn

  tags = {}
}
