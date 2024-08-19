provider "aws" {
  region = "us-east-1" 
}

#terraform {
#  backend "s3" {
#    bucket         = "devops-directive-tf-state-quantum" 
#    key            = "terraform/lambda/terraform.tfstate"
#    region         = "us-east-1"  
#    dynamodb_table = "terraform-locks"  
#    encrypt        = true
#  }
#}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "your-terraform-state-bucket"  # Replace with your bucket name
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}