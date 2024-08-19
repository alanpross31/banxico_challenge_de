variable "region" {
  description = "AWS Region"
  default     = "us-east-1"
}

variable "lambda_function_name" {
  description = "tipo_cambio_challenge"
  default     = "banxico-data-fetcher"
}

variable "s3_bucket_name" {
  description = "banxico-tipo-de-cambio-dollar-raw"
  default     = "banxico-data-output"
}

variable "lambda_role_name" {
  description = "banxico"
  default     = "banxico-lambda-role"
}
