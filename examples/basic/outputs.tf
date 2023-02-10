output "module_example" {
  description = "module.example"
  value       = module.example
}

output "kms_key_arn" {
  description = "KMS key ARN"
  value       = aws_kms_key.key.arn
}
