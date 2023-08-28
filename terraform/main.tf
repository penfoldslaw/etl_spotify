provider "aws" {
  region = "us-west-2" # Specify the appropriate region
}

resource "aws_s3_bucket" "spotify_bucket" {
  bucket = "etl-spotify-bucket" # Specify your desired bucket name
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket_policy" "spotify_bucket_policy" {
  bucket = aws_s3_bucket.spotify_bucket.id

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "GrantFullControl",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:*",
        "Resource": "${aws_s3_bucket.spotify_bucket.arn}",
        "Condition": {
          "StringEquals": {
            "aws:SourceAccount": "${data.aws_caller_identity.current.account_id}"
          }
        }
      }
    ]
  })
}


# Output the bucket name for reference
#output "bucket_name" {
#  value = aws_s3_bucket.my_bucket.id
#}

output "bucket_name" {
  value = aws_s3_bucket.spotify_bucket.id
}
