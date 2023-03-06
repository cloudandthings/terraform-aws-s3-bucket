######################################################################
## Required
######################################################################

######################################################################
## Optional
######################################################################
variable "enable_attach_default_bucket_policy" {
  description = "Whether to attach the default bucket policy or not (default=true). You may wish to attach the bucket policy document separately, in which case it is an output from this module."
  type        = bool
  default     = true
}

variable "enable_versioning" {
  description = "Whether to enable versioning on the bucket."
  type        = bool
  default     = true
}

variable "enable_public_access_block" {
  description = "Whether to enable public_access_block on the bucket."
  type        = bool
  default     = true
}

variable "create_aws_s3_bucket_lifecycle_configuration" {
  description = "Whether to enable the default aws_s3_bucket_lifecycle_configuration on the bucket."
  type        = bool
  default     = true
}

variable "name" {
  type        = string
  description = "Name for S3 bucket. Also see `naming_method`"
  default     = null
}

variable "naming_method" {
  type        = string
  description = "Whether to use `bucket`, `bucket_prefix` or neither when creating the `aws_s3_bucket` resource."
  default     = "BUCKET"
  validation {
    condition     = contains(["BUCKET", "BUCKET_PREFIX", "NONE"], var.naming_method)
    error_message = "Must be one of: \"BUCKET\", \"BUCKET_PREFIX\" or \"NONE\"."
  }
}

variable "tags" {
  description = "Map of additional tags to assign to created resources. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level."
  type        = map(string)
  default     = {}
}

## KMS
variable "kms_key_id" {
  type        = string
  description = "KMS key ID to use for encrypting bucket objects."
  default     = null
}

## Access
variable "general_read_only_aws_principals" {
  description = "List of AWS principals to give read access to all bucket objects via bucket policy resource."
  type        = list(string)
  default     = []
}

variable "general_read_write_aws_principals" {
  description = "List of AWS principals to give read and write access to all bucket objects via bucket policy resource."
  type        = list(string)
  default     = []
}

# Logging
variable "bucket_logging_target_bucket" {
  description = "Target S3 bucket name for logging."
  type        = string
  default     = ""
}

variable "bucket_logging_target_prefix" {
  description = "Target S3 bucket prefix for logging."
  type        = string
  default     = ""
}

variable "force_destroy" {
  description = "**Caution** Whether to automatically delete all objects from the bucket when it is destroyed. These objects are NOT recoverable."
  type        = bool
  default     = false
}
