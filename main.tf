######################################################################
## Bucket
######################################################################
## Bucket
#tfsec:ignore:aws-s3-enable-bucket-logging
#tfsec:ignore:aws-s3-block-public-acls
#tfsec:ignore:aws-s3-block-public-policy
#tfsec:ignore:aws-s3-ignore-public-acls
#tfsec:ignore:aws-s3-no-public-buckets
#tfsec:ignore:aws-s3-specify-public-access-block
resource "aws_s3_bucket" "this" {
  bucket = var.naming_prefix

  force_destroy = var.force_destroy
  #checkov:skip=CKV2_AWS_6:S3 public access block is applied at an account level.
  #checkov:skip=CKV_AWS_144:S3 replication is intentionally disabled by default.

  tags = var.tags
}

## Bucket Ownership Controls
# This disables bucket ACLs
# https://aws.amazon.com/about-aws/whats-new/2021/11/amazon-s3-object-ownership-simplify-access-management-data-s3/
resource "aws_s3_bucket_ownership_controls" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}


## Bucket Server Side Encryption Configuration
resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.bucket

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = var.kms_key_id == null ? null : var.kms_key_id
      sse_algorithm     = var.kms_key_id == null ? "AES256" : "aws:kms"
    }
    bucket_key_enabled = var.kms_key_id == null ? null : true
  }
}

## Bucket Versioning
resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}

## Bucket Logging
resource "aws_s3_bucket_logging" "this" {
  count  = length(var.bucket_logging_target_bucket) > 0 ? 1 : 0
  bucket = aws_s3_bucket.this.id

  target_bucket = var.bucket_logging_target_bucket
  target_prefix = var.bucket_logging_target_prefix
}

/*
# Bucket public access block. This should be set at an account level.
resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
*/

## Bucket Lifecycle Configuration
resource "aws_s3_bucket_lifecycle_configuration" "abort_incomplete_multipart_upload" {
  bucket = aws_s3_bucket.this.bucket
  count  = var.create_aws_s3_bucket_lifecycle_configuration ? 1 : 0
  rule {
    id     = "CleanIncompleteMultipartUploads"
    status = "Enabled"
    filter {
      prefix = ""
    }
    abort_incomplete_multipart_upload {
      days_after_initiation = 5
    }
  }
}

## Bucket Policy
resource "aws_s3_bucket_policy" "default_bucket_policy" {
  count  = var.enable_attach_default_bucket_policy ? 1 : 0
  bucket = aws_s3_bucket.this.id
  policy = data.aws_iam_policy_document.default_bucket_policy_document.json
}
