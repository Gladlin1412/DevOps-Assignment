terraform {
  backend "s3" {
    bucket         = "gladlin-1412"
    key            = "dev/terraform.tfstate"
    region         = "ap-south-1"
    use_lockfile   = true
    encrypt        = true
  }
}