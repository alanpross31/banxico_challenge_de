resource "aws_lambda_function" "banxico_fetcher" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "banxico_tipo_cambio_lambda.lambda_handler"
  runtime       = "python3.10"

  filename      = "my_deployment_package.zip" 
  source_code_hash = filebase64sha256("my_deployment_package.zip")

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.lambda_output_bucket.bucket
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tipo_cambio_challenge.function_name
  principal     = "events.amazonaws.com"
}